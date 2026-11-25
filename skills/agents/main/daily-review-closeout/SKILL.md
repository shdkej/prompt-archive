---
name: daily-review-closeout
description: >-
  필수 자동 트리거: 사용자가 Slack·채팅에 `오늘의 잡상`, `데일리 잡상`, `오늘 회고`, `데일리 회고`를 보내거나 날짜가 붙은 하루 경험·생각을 남기면 즉시 이 스킬을 읽고 같은 턴에서 회고 마감을 시작한다. “회고해줘”라는 별도 요청을 기다리거나 해석만 답하지 않는다. 4단 회고, 기록, 카드, 회고 캘린더, Threads 후보, 원 스레드 전달까지 마친다.
---

# Daily Review Closeout

Use this skill whenever the user sends a daily reflection, daily thoughts, daily review, or a message that clearly describes that day's experiences and asks for 회고. Do not stop after writing the four-section message.

## Trigger and Slack delivery guard (2026-11-25)

- **Start on the first input.** A message headed `오늘의 잡상`, `데일리 잡상`, or otherwise containing the day's reflections is already the trigger. Begin this workflow in that same turn; do not first send only an acknowledgement, ask whether the skill is running, or wait for the user to request it again.
- **Keep visual QA out of Slack delivery.** In this Slack path, an image block emitted from `functions.exec` with `image(...)` or `generatedImage(...)` becomes its own visible file post. Never use those helpers to inspect the card: that is not an internal preview. Inspect through a non-posting local visual tool (for example, the available desktop screenshot/viewer) and do not forward its image result. If no private visual inspection path is available, mark visual QA blocked; do not create a second Slack image as a workaround.
- **Send the card once.** In Slack, send the final review text as a text-only message in the original thread, then use exactly one `message(action="upload-file")` call for the validated PNG in that thread. Do not put the PNG in text-message attachments, emit a screenshot/image block, or retry an upload whose receipt is uncertain; inspect the original thread first. The explicit upload is the only permitted Slack media post for this closeout.
- **Verify one visible image.** Read the original thread after delivery and confirm the review text and exactly one final PNG are present. Count the thread's actual file attachments, not just tool receipts. If a duplicate file-only post appears, delete only the confirmed redundant post by its message timestamp, re-read the thread, and confirm one final PNG remains before reporting completion.

## Required sequence

**One closeout run means prepare → verify → deliver.** The review body being written or sent is not completion. Do not send the four-section review as an early standalone reply and then leave card/calendar work for a later turn. Prepare every deliverable before the final user-facing closeout.

1. Read `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/docs/LOCAL_REVIEW_AUTOMATION.md` and `/home/ubuntu/workspace/prompt-archive/DAILY_ARCHIVE_CARD_PROMPT.md`. For travel days, confirm current place and next movement with `hj`; do not invent them.
2. Determine the review's local date and source evidence. Draft exactly `Keep`, `Problem`, `Action Item`, and `Tomorrow Expectation`; separate user facts from SAM's operational work and keep `Action Item` to one experiment.
3. Save the full review to `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/daily-reviews/YYYY-MM-DD-review.md`. Add only genuinely reusable rules to `data/spaced_repetition_items.json`; otherwise record that none was added.
4. Create one private daily archive card using the current book-page editorial layout in `DAILY_ARCHIVE_CARD_PROMPT.md`: warm ivory paper, top/bottom dotted frame, centered medium-weight serif title with generous separation from the body, bold numbered Keep/Problem/Action Item/Tomorrow Expectation headings, same-size indented body text, generous margins, and the date at bottom right instead of a page number. Do not add illustration or photo by default. Validate PNG and HTML and inspect the actual render; file existence is not validation.
5. Read existing events, then write or update the same-day 5-minute headline and next-day sourced quote in the `회고` calendar only through `gog`. The next-day quote event runs 21:00–23:59 Asia/Seoul, not all day. Select a new quote for each day; check the previous 30 days of quote events in `회고` and do not reuse any quote from that period. Never create or update daily-review entries in the default/general calendar. Verify the quote's author and exact wording against a reliable text, include its source in the event description, avoid duplicates, and re-read `회고` to verify. If quote sourcing or calendar access fails, record the exact failure and leave the closeout incomplete; do not fall back to a guessed quote or a task event.
6. Record one Threads demand-validation candidate internally; run its gate and never publish it without separate approval.
7. Before delivery, re-read the review file and verify the four sections, card render check, the `회고` calendar re-query, Spaced decision, Threads candidate/gate, and delivery asset. Confirm the default/general calendar was not modified. Correct any mismatch now. If an event date is already past, record that it was added retrospectively rather than silently moving it.
8. Only after preparation and checks, send the complete four-section review plus a concise `운영 처리` block in the original Slack thread. Attach the validated final daily archive PNG (1080×1350) in that same thread; if the channel tool requires separate text and media calls, send them consecutively as one closeout and verify both receipts before reporting completion. Never substitute the source illustration, HTML, or a path for the final PNG.
9. If a required step fails after reasonable recovery, send one closeout that clearly says `미완료`, identifies the exact failed step and next action, and does not imply success. Do not report `완료` until the user-facing review and final PNG attachment receipts are both confirmed.

## Output boundary

After the four sections, append only a concise `운영 처리` block listing the saved file, Spaced result, card validation, calendar result, and Threads candidate. Never expose credentials, raw logs, or unverified travel details.
