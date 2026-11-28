---
name: pt-claude-tmux
description: purple tmux 소켓을 통해 pt/purplemux가 실행한 Claude Code 세션에 attach하고 제어합니다. 사용자가 기존 pt Claude 세션을 inspect, reset, 입력 전송(send input), capture, 또는 continue하려 할 때 사용합니다.
---

# pt Claude tmux

**목차**

- [세션 찾기](#세션-찾기)
- [동작하기 전에 inspect](#동작하기-전에-inspect)
- [reset 후 간단한 프롬프트 전송](#reset-후-간단한-프롬프트-전송)
- [임의 텍스트 전송](#임의-텍스트-전송)
- [수동으로 attach](#수동으로-attach)
- [안전 수칙](#안전-수칙)

사용자가 `pt` / purplemux 안에서 실행 중인 Claude 세션에 대해 물어볼 때 사용합니다.

## 세션 찾기

`pt`는 기본 tmux 소켓이 아니라 `purple` tmux 소켓을 사용합니다.

```bash
tmux -L purple list-sessions
tmux -L purple list-panes -a -F '#{session_name}:#{window_index}.#{pane_index} #{pane_id} #{pane_tty} #{pane_current_command} #{pane_title}'
```

Claude pane은 보통 `pane_current_command`가 `claude`로 표시됩니다. tmux 안에 있지 않은 직접 SSH `pts/*` Claude 프로세스는 tmux로 안전하게 재연결(reattach)할 수 없습니다.

## 동작하기 전에 inspect

키를 보내기 전에 항상 pane을 capture합니다.

```bash
tmux -L purple capture-pane -t 'SESSION:0.0' -p -S -80
```

현재 프롬프트에 이미 텍스트가 있는지 확인합니다. 오래된 지시가 들어 있다면, 새 내용을 보내기 전에 `C-c`로 지웁니다.

## reset 후 간단한 프롬프트 전송

```bash
tmux -L purple send-keys -t 'SESSION:0.0' C-c
tmux -L purple send-keys -t 'SESSION:0.0' -l -- '/clear'
tmux -L purple send-keys -t 'SESSION:0.0' Enter
sleep 2
tmux -L purple send-keys -t 'SESSION:0.0' -l -- '안녕'
tmux -L purple send-keys -t 'SESSION:0.0' Enter
```

몇 초 뒤에 다시 capture합니다:

```bash
tmux -L purple capture-pane -t 'SESSION:0.0' -p -S -80 | tail -80
```

## 임의 텍스트 전송

literal send 모드를 사용하고 `Enter`는 따로 보냅니다.

```bash
tmux -L purple send-keys -t 'SESSION:0.0' -l -- 'message text'
tmux -L purple send-keys -t 'SESSION:0.0' Enter
```

여러 줄 프롬프트의 경우, 간결한 한 단락이나 짧은 heredoc 형태의 지시를 붙여넣는 것을 선호합니다. 큰 파일을 interactive pane에 그대로 쏟아붓지 않습니다.

## 수동으로 attach

사용자가 직접 세션에 들어가려는 경우:

```bash
tmux -L purple attach-session -t SESSION
```

tmux에서 빠져나오려면 `Ctrl-b d`를 누릅니다.

## 안전 수칙

- 무엇이 큐에 쌓여 있는지 파악하기 전에는 기존 프롬프트에서 `Enter`를 누르지 않습니다.
- 명시적인 사용자 승인 없이 Claude 프롬프트에서 파괴적이거나, 외부로 나가거나, credential, 배포(deployment), 공개 전송(public-send) 동작을 승인하지 않습니다.
- 무슨 일이 있었는지 보고할 만큼의 맥락은 capture하되, 비밀 정보나 긴 로그를 사용자에게 다시 붙여넣지 않습니다.
