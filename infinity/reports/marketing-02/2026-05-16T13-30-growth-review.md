# marketing-02 growth review - 2026-05-16T13:30Z

## Signal

- PostHog project 424014, last 24 hours: $pageview 9, $autocapture 7, $web_vitals 3, $pageleave 1.
- Last 24 hours paths: / 5, /dex 2, /add 1, /me 1, all from 1 user.
- Last 7 days: 40 pageviews / 3 users, /add 7 pageviews / 2 users, deed_judged 1, deed_saved 0, $exception 4.
- Live HTML check no longer exposes 641 or MOCK; only expected product text such as 덕 쌓기 and 환생 was found.

## Diagnosis

The previously approved marketing-01 deployment appears to have removed the demo-state blocker. The remaining growth issue is activation proof: users are visiting /add, but no post-deployment judgement or save events are visible yet.

The $exception events are from 2026-05-14 and include React hydration error #418 details inside the exception list, but top-level message/type remain null for those older events. No new 24h exceptions appeared in this review.

## Action Candidate

Create marketing-02 as an Inbox candidate for a bounded /add activation friction audit. The task should produce a UX/telemetry recommendation only; production edits and deployment remain outside scope.

## Measurement

- Watch deed_judge_attempted / /add pageview.
- Watch deed_saved / deed_judged.
- Treat the first clean deed_saved event as the activation proof needed before any public growth push.

## Routing

Routed to Inbox as infinity/intents/inbox/marketing-02.md.
