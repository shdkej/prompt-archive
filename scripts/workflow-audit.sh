#!/usr/bin/env bash
# workflow-audit.sh — workflow 로그 위생 스캔 (세션 시작 시 SessionStart hook이 호출)
# 출력: ①빈 로그 ②봉인(END/STATUS) 없는 로그 ③진짜 INCOMPLETE(후속 종결 제외) ④미회수 PENDING
# 판정은 사람이 한다 — 이 스크립트는 "닫아야 할 목록"만 만든다. 후보 0건이면 침묵.

set -u
LOGS_DIR="${HOME}/.claude/logs"
cd "$LOGS_DIR" 2>/dev/null || exit 0
shopt -s nullglob

empty=() unsealed=() incomplete=() closed_by=()
pending_lines=()

for f in workflow_*.log; do
  if [[ ! -s "$f" ]]; then empty+=("$f"); continue; fi

  # 마지막 END/STATUS 라인으로 봉인 상태 판정 (INCOMPLETE가 COMPLETE를 부분문자열로 포함하므로 순서 주의)
  endline=$(grep -E '\[(WORKFLOW:)?END\]|\[STATUS\]|^\[END\]' "$f" | tail -1)
  if [[ -z "$endline" ]]; then
    unsealed+=("$f")
  elif echo "$endline" | grep -q 'WAITING:USER\|DISCARDED\|EXPIRED'; then
    : # 의도적으로 닫힘
  elif echo "$endline" | grep -q 'INCOMPLETE'; then
    # 다른 로그가 CONTINUES_FROM으로 이 로그를 종결했는지 (forward-link)
    stem="${f%.log}"
    successor=$(grep -l "CONTINUES_FROM.*${stem##workflow_}" workflow_*.log 2>/dev/null | grep -v "^$f$" | head -1)
    if [[ -n "$successor" ]]; then
      closed_by+=("$f -> $successor")
    else
      incomplete+=("$f")
    fi
  fi

  # 미회수 PENDING: OUTPUT id가 같은 파일(레거시) 또는 전체 로그(전역 id)의 FATE에 없으면 미회수
  while IFS= read -r id; do
    [[ -z "$id" ]] && continue
    if [[ "$id" == *-* ]]; then
      grep -q "WORKFLOW:FATE.*id=${id}[^0-9a-zA-Z-]*" workflow_*.log 2>/dev/null || \
      grep -q "WORKFLOW:FATE.*${id}" workflow_*.log 2>/dev/null || pending_lines+=("$f: id=$id")
    else
      grep -q "WORKFLOW:FATE.*\b${id}\b" "$f" 2>/dev/null || pending_lines+=("$f: id=$id")
    fi
  done < <(grep -oE '\[WORKFLOW:OUTPUT\][^"]*status=PENDING' "$f" | grep -oE 'id=[^ ]+' | sed 's/^id=//')
done

total=$(( ${#empty[@]} + ${#unsealed[@]} + ${#incomplete[@]} + ${#closed_by[@]} + ${#pending_lines[@]} ))
[[ $total -eq 0 ]] && exit 0

echo "=== workflow-audit: 닫을 후보 ${total}건 ==="
[[ ${#empty[@]} -gt 0 ]]      && printf '⚪ 빈 로그 (DISCARDED 봉인 권장): %s\n' "${empty[@]}"
[[ ${#unsealed[@]} -gt 0 ]]   && printf '🟡 END/STATUS 봉인 없음: %s\n' "${unsealed[@]}"
[[ ${#closed_by[@]} -gt 0 ]]  && printf '🟢 후속 로그가 종결 — CLOSED_BY 봉인만 필요: %s\n' "${closed_by[@]}"
[[ ${#incomplete[@]} -gt 0 ]] && printf '🔴 진짜 INCOMPLETE (이어할지 확인): %s\n' "${incomplete[@]}"
if [[ ${#pending_lines[@]} -gt 0 ]]; then
  echo "🟠 미회수 PENDING ${#pending_lines[@]}건 (운명 확정 필요, 최근 10건만 표시):"
  printf '   %s\n' "${pending_lines[@]}" | tail -10
fi
exit 0
