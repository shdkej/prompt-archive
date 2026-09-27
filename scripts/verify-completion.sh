#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
사용법: scripts/verify-completion.sh [저장소 경로] [원격 ref]

검사 항목:
  - 대상 경로가 Git 저장소인지
  - origin 원격과 현재 브랜치 확인
  - 작업 트리가 깨끗한지
  - 로컬 HEAD와 origin ref의 SHA가 같은지
USAGE
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

repo=${1:-.}
repo=$(cd "$repo" && pwd)
ref=${2:-}

git -C "$repo" rev-parse --show-toplevel >/dev/null
remote=$(git -C "$repo" remote get-url origin)
branch=$(git -C "$repo" branch --show-current)
if [[ -z "$branch" ]]; then
  echo "FAIL: detached HEAD: $repo" >&2
  exit 1
fi

if [[ -z "$ref" ]]; then
  ref="refs/heads/$branch"
elif [[ "$ref" != refs/* ]]; then
  ref="refs/heads/$ref"
fi

if [[ -n "$(git -C "$repo" status --porcelain)" ]]; then
  echo "FAIL: 작업 트리가 깨끗하지 않습니다: $repo" >&2
  git -C "$repo" status --short >&2
  exit 1
fi

local_sha=$(git -C "$repo" rev-parse HEAD)
remote_sha=$(git -C "$repo" ls-remote origin "$ref" | awk 'NR == 1 { print $1 }')
if [[ -z "$remote_sha" ]]; then
  echo "FAIL: 원격 ref를 찾지 못했습니다: $remote $ref" >&2
  exit 1
fi
if [[ "$local_sha" != "$remote_sha" ]]; then
  echo "FAIL: 로컬/원격 SHA 불일치: local=$local_sha remote=$remote_sha" >&2
  exit 1
fi

echo "PASS: repository=$repo"
echo "PASS: remote=$remote"
echo "PASS: branch=$branch ref=$ref"
echo "PASS: sha=$local_sha"
