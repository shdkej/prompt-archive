# marketing-02 - Virtue /add activation gap follow-up

## Status

Inbox

## Source

- Created by marketing agent daily growth review at 2026-05-16T13:30Z.
- Evidence: PostHog project 424014, live page fetch, virtue-rebirth-app instrumentation, archived marketing-01 expectation.

## Signal

- Last 24 hours: 9 pageviews from 1 user, including /add 1 pageview, but no activation events beyond default analytics.
- Last 7 days: 40 pageviews / 3 users, /add 7 pageviews / 2 users, deed_judged 1, deed_saved 0, $exception 4.
- Since the 2026-05-16 deployment, the old demo markers (641, MOCK) are no longer visible in fetched HTML.
- $exception events are pre-deployment and still show null top-level message/type, but their exception list contains React hydration error #418.

## Diagnosis

The demo-state issue appears resolved, but activation is still not proven. A user can reach /add, yet no deed_judge_attempted, deed_judged, or deed_saved event appears in the last 24 hours.

This could be normal low-volume behavior, but it is now the highest-leverage next measurement gap: determine whether /add visitors are bouncing before attempting judgement, or whether the judgement/save path is hard to complete on a real phone.

## Action Candidate

Prepare a bounded activation friction audit:

1. Inspect the current /add mobile flow against the latest deployed build without changing production code.
2. Identify the first obvious user action where a visitor might stop before deed_judge_attempted.
3. Draft one small UX or telemetry improvement candidate for Infinity execution.
4. Keep any production code change or deployment out of scope until separately approved.

## Measurement

- Primary: deed_judge_attempted / /add pageview and deed_saved / deed_judged over the next 7 days.
- Secondary: presence of post-deployment $exception events with usable exception detail.
- Guardrail: do not scale acquisition or public posting until at least one clean save event is observed.

## Routing

Inbox. This is internal L0/L1 research/preparation. Any code change, deployment, public post, ad spend, email, or privacy/tracking config change must move to Waiting for user approval.
