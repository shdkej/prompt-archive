#!/bin/bash
# Agent-First Heartbeat 알림 스크립트
# Usage: ./notify.sh "메시지 내용"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../config/telegram.env"

if [ -f "$ENV_FILE" ]; then
  source "$ENV_FILE"
fi

if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ]; then
  echo "[notify] TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set" >&2
  exit 1
fi

MESSAGE="${1:-No message}"

curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${TELEGRAM_CHAT_ID}" \
  -d "text=${MESSAGE}" \
  -d "parse_mode=Markdown" \
  > /dev/null 2>&1

echo "[notify] sent"
