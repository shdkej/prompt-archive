#!/usr/bin/env bash
# diary-sync.sh — 30분마다 세션/시청 raw 데이터를 Claude로 정제해
# agent-wiki/content/docs/diary/YYYY-MM-DD.mdx 에 merge하고 push. 7일 경과 파일 삭제.
set -euo pipefail

export PATH="/Users/seongho-noh/.asdf/installs/nodejs/24.3.0/bin:/opt/homebrew/bin:/usr/bin:/bin:$PATH"
export HOME="${HOME:-/Users/seongho-noh}"

REPO="$HOME/workspace/agent-wiki"
DIARY_DIR="$REPO/content/docs/diary"
SESSIONS_SCRIPT="$HOME/workspace/prompt-archive/scripts/daily-sessions.py"
PROMPT_TEMPLATE="$HOME/workspace/prompt-archive/diary-sync/diary-sync.prompt.md"
TODAY=$(date +%F)
TARGET="$DIARY_DIR/$TODAY.mdx"
LOG_DIR="$HOME/.claude/logs"
mkdir -p "$DIARY_DIR" "$LOG_DIR"

log() { printf '[%s] %s\n' "$(date +'%F %T')" "$*"; }

retry() {
  local n=0 max=3 delay=5
  until "$@"; do
    n=$((n+1))
    [[ $n -ge $max ]] && return 1
    sleep $delay
    delay=$((delay*2))
  done
}

cd "$REPO"
if ! retry git pull --rebase --quiet origin main; then
  log "error: git pull failed after retries, skipping run to avoid divergence"
  exit 0
fi

RAW_SESSIONS=$(python3 "$SESSIONS_SCRIPT" 2>/dev/null || true)

TMP_DB="/tmp/chrome-history-$$.db"
RAW_MEDIA=""
if cp "$HOME/Library/Application Support/Google/Chrome/Profile 1/History" "$TMP_DB" 2>/dev/null; then
  RAW_MEDIA=$(sqlite3 "$TMP_DB" "SELECT CASE WHEN url LIKE '%youtube.com/watch%' THEN 'YouTube' WHEN url LIKE '%netflix.com/watch%' THEN 'Netflix' END AS platform, title, datetime(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime') AS visit_time FROM urls WHERE (url LIKE '%youtube.com/watch%' OR url LIKE '%netflix.com/watch%') AND date(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime') = date('now', 'localtime') ORDER BY last_visit_time DESC;" 2>/dev/null || true)
  rm -f "$TMP_DB"
fi

EXISTING="(빈 파일)"
if [[ -f "$TARGET" ]]; then
  EXISTING=$(python3 - "$TARGET" <<'PYEOF'
import sys, re
t = open(sys.argv[1], encoding='utf-8').read()
m = re.match(r'^---\n.*?\n---\n', t, re.DOTALL)  # frontmatter 제거, 본문만 LLM에 전달
body = (t[m.end():] if m else t).strip()
sys.stdout.write(body or "(빈 파일)")
PYEOF
)
fi

NOW_ISO=$(date -Iseconds)
PROMPT_FILE="/tmp/diary-prompt-$$.txt"

if [[ ! -f "$PROMPT_TEMPLATE" ]]; then
  log "error: prompt template not found: $PROMPT_TEMPLATE"
  exit 1
fi

export TODAY NOW_ISO EXISTING RAW_SESSIONS RAW_MEDIA

python3 - "$PROMPT_TEMPLATE" "$PROMPT_FILE" <<PYEOF
import os, sys
src, dst = sys.argv[1], sys.argv[2]
with open(src, 'r', encoding='utf-8') as f:
    tpl = f.read()
out = (tpl
    .replace('{{TODAY}}', os.environ['TODAY'])
    .replace('{{NOW_ISO}}', os.environ['NOW_ISO'])
    .replace('{{EXISTING}}', os.environ['EXISTING'])
    .replace('{{RAW_SESSIONS}}', os.environ['RAW_SESSIONS'])
    .replace('{{RAW_MEDIA}}', os.environ['RAW_MEDIA']))
with open(dst, 'w', encoding='utf-8') as f:
    f.write(out)
PYEOF

OUT=$(claude -p --dangerously-skip-permissions < "$PROMPT_FILE" 2>>"$LOG_DIR/diary-sync.err" || true)
rm -f "$PROMPT_FILE"
if [[ -n "$OUT" ]]; then
  # frontmatter는 LLM에 맡기지 않고 셸이 결정적으로 생성·주입한다.
  # (fumadocs pageSchema가 title 필수라 LLM이 누락하면 빌드가 깨짐)
  # heredoc이 stdin을 점유하므로 LLM 출력은 파이프가 아닌 임시파일로 전달한다.
  RAW_OUT="/tmp/diary-out-$$.md"
  printf '%s' "$OUT" > "$RAW_OUT"
  TODAY="$TODAY" NOW_ISO="$NOW_ISO" python3 - "$RAW_OUT" "$TARGET" <<'PYEOF'
import sys, os, re
body = open(sys.argv[1], encoding='utf-8').read()
body = re.sub(r'^\s*```[a-zA-Z]*\n', '', body)          # 선행 코드펜스 제거
body = re.sub(r'\n```\s*$', '', body)                   # 후행 코드펜스 제거
body = re.sub(r'^\s*---\n.*?\n---\n', '', body, count=1, flags=re.DOTALL)  # LLM이 낸 frontmatter 제거
body = body.strip()
today = os.environ['TODAY']
if not body.startswith('#'):
    body = f"# {today}\n\n{body}"
fm = (f'---\ntitle: "{today}"\ndate: {today}\n'
      f'type: diary\nlast_sync: {os.environ["NOW_ISO"]}\n---\n\n')
open(sys.argv[2], 'w', encoding='utf-8').write(fm + body + "\n")
PYEOF
  rm -f "$RAW_OUT"
  log "merged $TARGET ($(wc -l <"$TARGET") lines)"
else
  log "warn: claude output empty, keeping existing $TARGET"
fi

CUTOFF=$(date -v-7d +%F)
for f in "$DIARY_DIR"/*.mdx; do
  [[ -f "$f" ]] || continue
  fname=$(basename "$f" .mdx)
  if [[ "$fname" < "$CUTOFF" ]]; then
    git rm -q "$f" 2>/dev/null || rm -f "$f"
    log "pruned $fname (older than $CUTOFF)"
  fi
done

git add -A
if ! git diff --cached --quiet; then
  git commit -m "diary: auto-sync $(date +'%Y-%m-%d %H:%M')" >/dev/null
  push_once() {
    git pull --rebase --quiet origin main 2>/dev/null && git push --quiet origin main 2>/dev/null
  }
  if retry push_once; then
    log "pushed"
  else
    log "error: push failed after retries, will retry next run"
  fi
else
  log "no changes"
fi

exit 0
