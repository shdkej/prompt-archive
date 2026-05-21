# [marketing-01] Approved Deploy Report

- timestamp: 2026-05-21T10:17Z
- status_before: waiting
- status_after: completed
- approval: user-approved via Telegram direct message ("인피니티 승인")
- executor: SAM direct execution after local Claude Code stalled before making changes

## Summary

사용자 승인 후 `marketing-01-add-flow-telemetry` 브랜치를 `master`에 fast-forward 머지하고 GitHub에 push했다. Oracle SSH alias는 현재 DNS 해석이 되지 않았지만, 실제 Virtue 운영 표면은 Kubernetes `deployment/virtue-rebirth`이며 pod 시작 시 GitHub `master`를 clone/build하는 구조다. 따라서 승인 범위의 배포 반영은 deployment rollout restart로 수행했다.

## Actions

- `/home/ubuntu/dev/virtue-rebirth-app`
  - `master` fast-forward: `99bf53b` → `b28d01f`
  - pushed: `origin/master` → `b28d01f719db344f4e76c5c7d32934617a2d0f28`
- Kubernetes
  - command: `kubectl rollout restart deployment/virtue-rebirth`
  - rollout: success
  - new pod: `virtue-rebirth-6b6656cd8b-6w6gn`

## Verification

- GitHub remote: `refs/heads/master = b28d01f719db344f4e76c5c7d32934617a2d0f28`
- Deployment pod: `/app` HEAD = `b28d01f719db344f4e76c5c7d32934617a2d0f28`
- Live URL: `https://virtue.oracle.shdkej.com`
  - HTTP: 200
  - ETag: `"60azsylmbqcvu"`
  - demo markers: `641` not found, `MOCK` not found
  - empty state copy found: `아직 비어있어요`, `아직 기록이 없어요`

## Notes

- Local Claude Code was invoked first per Infinity local-execution preference, but it produced no output and made no repo changes before stalling. SAM stopped that path and completed the already-approved gate directly.
- The current deployment is Kubernetes-based, not PM2-based. The older PM2 wording in the gate came from historical deployment notes and should not be used as the current execution assumption.
- Old terminating pod logs briefly showed Next.js "Failed to find Server Action" messages, consistent with in-flight requests crossing deployments. The new pod became ready and live HTTP verification passed.

## Next Actions

- 7일 후 PostHog 424014에서 `add_flow_started` 대비 `add_flow_abandoned` / `deed_saved` 비율을 확인한다.
