#!/usr/bin/env bash
# diary-sync.sh — 30분마다 세션/시청 raw 데이터를 Claude로 정제해
# agent-wiki/diary/YYYY-MM-DD.md 에 merge하고 push. 7일 경과 파일 삭제.
set -euo pipefail

export PATH="/Users/seongho-noh/.asdf/installs/nodejs/24.3.0/bin:/opt/homebrew/bin:/usr/bin:/bin:$PATH"
export HOME="${HOME:-/Users/seongho-noh}"

REPO="$HOME/workspace/agent-wiki"
DIARY_DIR="$REPO/diary"
SESSIONS_SCRIPT="$HOME/workspace/prompt-archive/scripts/daily-sessions.py"
TODAY=$(date +%F)
TARGET="$DIARY_DIR/$TODAY.md"
LOG_DIR="$HOME/.claude/logs"
mkdir -p "$DIARY_DIR" "$LOG_DIR"

log() { printf '[%s] %s\n' "$(date +'%F %T')" "$*"; }

cd "$REPO"
git pull --rebase --quiet origin main || log "warn: git pull skipped"

RAW_SESSIONS=$(python3 "$SESSIONS_SCRIPT" 2>/dev/null || true)

TMP_DB="/tmp/chrome-history-$$.db"
RAW_MEDIA=""
if cp "$HOME/Library/Application Support/Google/Chrome/Profile 1/History" "$TMP_DB" 2>/dev/null; then
  RAW_MEDIA=$(sqlite3 "$TMP_DB" "SELECT CASE WHEN url LIKE '%youtube.com/watch%' THEN 'YouTube' WHEN url LIKE '%netflix.com/watch%' THEN 'Netflix' END AS platform, title, datetime(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime') AS visit_time FROM urls WHERE (url LIKE '%youtube.com/watch%' OR url LIKE '%netflix.com/watch%') AND date(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime') = date('now', 'localtime') ORDER BY last_visit_time DESC;" 2>/dev/null || true)
  rm -f "$TMP_DB"
fi

EXISTING="(빈 파일)"
[[ -f "$TARGET" ]] && EXISTING=$(cat "$TARGET")

PROMPT_FILE="/tmp/diary-prompt-$$.txt"
NOW_ISO=$(date -Iseconds)
cat > "$PROMPT_FILE" <<EOF
너는 일일 활동 로그 유지자. 기존 diary 파일과 오늘 raw 데이터를 받아 중복을 제거하고 시간순으로 정제된 최종 마크다운만 출력한다. 설명 문구/코드펜스 금지, 본문만.

요구 구조:
---
date: $TODAY
type: diary
last_sync: $NOW_ISO
---

# $TODAY

## Sessions

### 업무
테이블 헤더: # / 프로젝트 / 시간 / 주요 작업

### 개인
동일 테이블 형식

### 기타
불릿 "- HH:MM — 요약"

## Media
"- HH:MM [플랫폼] 제목" 형식, 플랫폼은 YouTube/Netflix

## Notes
raw에 없으면 섹션 생략

규칙:
- 시간 HH:MM, 주요 작업은 한 줄 한국어 요약
- 기존 항목 유지, 신규만 병합
- 같은 프로젝트/시간 중복이면 더 구체적인 쪽 유지
- 빈 섹션은 본문 생략 가능

=== 기존 파일 ===
$EXISTING

=== 신규 Session raw ===
$RAW_SESSIONS

=== 신규 Media raw ===
$RAW_MEDIA
EOF

OUT=$(claude -p --dangerously-skip-permissions < "$PROMPT_FILE" 2>>"$LOG_DIR/diary-sync.err" || true)
rm -f "$PROMPT_FILE"
if [[ -n "$OUT" ]]; then
  printf '%s\n' "$OUT" > "$TARGET"
  log "merged $TARGET ($(wc -l <"$TARGET") lines)"
else
  log "warn: claude output empty, keeping existing $TARGET"
fi

CUTOFF=$(date -v-7d +%F)
for f in "$DIARY_DIR"/*.md; do
  [[ -f "$f" ]] || continue
  fname=$(basename "$f" .md)
  if [[ "$fname" < "$CUTOFF" ]]; then
    git rm -q "$f" 2>/dev/null || rm -f "$f"
    log "pruned $fname (older than $CUTOFF)"
  fi
done

git add -A
if ! git diff --cached --quiet; then
  git commit -m "diary: auto-sync $(date +'%Y-%m-%d %H:%M')" >/dev/null
  if git push --quiet origin main 2>/dev/null; then
    log "pushed"
  else
    log "warn: push rejected, attempting rebase+push"
    if git pull --rebase --quiet origin main 2>/dev/null && git push --quiet origin main 2>/dev/null; then
      log "pushed (after rebase)"
    else
      log "error: push failed, will retry next run"
    fi
  fi
else
  log "no changes"
fi

exit 0
