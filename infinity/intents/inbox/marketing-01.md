# marketing-01 - Virtue activation and demo-state audit

## Status

Inbox

## Source

- Created by marketing agent daily growth review at 2026-05-15T13:32Z.
- Evidence: PostHog project 424014, live page fetch, Virtue repo instrumentation, Knowledge Lab product-growth notes.

## Signal

- Last 7 days and 24 hours currently show the same small traffic set: 31 pageviews, 3 users, all direct.
- Activation event path is thin: 1 `deed_judged`, 0 `deed_saved`, 0 `deed_scored`, 0 `deed_score_failed`.
- Live first page HTML still exposes seeded demo-like state (`641덕`, sample recent deeds anchored around 2026-05-13), while current store code says production should start empty unless `NEXT_PUBLIC_SHOW_DEMO=1`.
- PostHog captured 4 `$exception` events, but exception message/type are null, so the current signal is not debuggable enough.

## Diagnosis

The product has enough instrumentation to see a first activation gap, but not enough volume or diagnostic detail to separate three possibilities:

- users reach `/add` but do not save,
- scoring/UX friction prevents save,
- production is still presenting demo state and making the user journey feel pre-filled rather than personal.

Knowledge Lab's product notes frame AARRR as a diagnostic board for finding where users stop. The immediate stop appears to be activation, not acquisition scaling.

## Action Candidate

Run a bounded Virtue activation audit:

1. Verify why production HTML still shows demo seeded state despite the current `SHOW_DEMO` guard.
2. Reproduce one clean incognito/mobile add-flow from landing -> add -> judge -> save.
3. Inspect why `$exception` events lack message/type and propose the smallest telemetry improvement.
4. Produce a small fix plan, but do not modify production code or deploy without SAM/user approval.

## Measurement

- Primary: `deed_saved / deed_judged` over the next 7 days.
- Secondary: clean first-load state, add-flow completion on mobile, and `$exception` events with usable message/type or a clearer replacement event.

## Routing

Inbox. Promote to Active only when a slot is open. Keep public launch/growth pushes in Waiting until activation is trustworthy.
