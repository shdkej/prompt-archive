---
name: infinity-intake-publish
description: Register an Infinity intent only after its scoped files are committed, pushed, and proven identical to origin/main. Use for nontrivial Infinity research, planning, generation, comparison, or implementation intake.
---

# Infinity intake publish gate

Use this skill before returning an Infinity intent ID or saying that an Infinity task has been accepted.

## Required gate

1. Before reading or writing an Intent, fetch the canonical Infinity checkout at `/home/ubuntu/workspace/infinity` from `origin main`. If it is clean and can fast-forward, run `git pull --ff-only origin main`; otherwise preserve it and use step 3. Confirm the prepared checkout's `HEAD` equals fetched `origin/main`.
2. Search `origin/main:INTENTS.yaml` across `lanes.backlog`, `lanes.inbox`, `lanes.active`, `lanes.waiting`, and Archive for the same objective. Reuse an existing open Intent; if an equivalent Intent is already archived, report or link its result and create a new follow-up only when the scope materially differs. Never create duplicate open and archived entries for one objective.
3. If the canonical checkout is dirty or cannot fast-forward, preserve unrelated work: do not stash, discard, merge, or rebase it. Reuse only an already-existing, task-specific checkout if it can be safely fast-forwarded to `origin/main`; do not create a new temporary worktree. Otherwise report the precise blocker and do not register from a stale/diverged checkout.
4. Build and read the Infinity Context Pack. Before the Intent is registered, run `python3 scripts/record_intent_trace.py intake` to create `data/traces/{intent-id}.json` with the raw request, normalized query, Context Pack path, `INTENTS.yaml` evidence, and next decision; then run `python3 scripts/validate_intent_trace.py data/traces/{intent-id}.json`. A missing or invalid Context Map trace blocks registration.
5. Write the canonical `INTENTS.yaml` Inbox/Active registry block. An individual `intents/{lane}/{intent-id}.md` file is optional, but it never replaces the registry block because the dashboard and dispatcher consume `INTENTS.yaml`.
6. Before commit, verify the intent ID appears exactly once in the canonical `INTENTS.yaml` open lane and run the repository's intent consistency/parser check when available. A missing registry entry or parser failure blocks acceptance; unrelated pre-existing warnings must be reported separately.
   - The canonical `lanes.inbox`/`lanes.active` entry in `INTENTS.yaml` must parse with its `status` matching the lane.
   - Capture `python3 scripts/prepare_dispatch_cycle.py --repo . --intents INTENTS.yaml --json` output in a shell variable and confirm the new intent appears in `counts` and in the expected `promote_candidates`/`handoff_candidates` output. Do not leave a generated dispatch-check file in the worktree. A GitHub-visible commit that the dispatcher cannot parse is not an accepted intake.
7. Create only the scoped intake files: the Context Pack, `data/traces/{intent-id}.json`, canonical `INTENTS.yaml` entry, optional `intents/inbox/{intent-id}.md` entry, and any required task-plan artifacts.
8. Inspect the scoped diff and stage those paths explicitly. Do not stage unrelated worktree changes.
9. Commit the scoped intake change in the prepared checkout at `/home/ubuntu/workspace/infinity` (or the already-existing task-specific checkout reused in step 3).
10. Push the commit to `origin main` with `git push origin main`.
11. Run exactly:

   ```
   /home/ubuntu/workspace/knowledge-lab/source/openclaw-system/scripts/verify_git_publish.sh <prepared-checkout> main -- <all scoped intake paths>
   ```

12. Return the intent ID only after the script exits `0`. Preserve its local and remote SHA in the intent or intake record.

## Failure handling

- A nonzero result means the intake is not registered. Do not claim acceptance, Active, Waiting, or dispatch readiness.
- Report the specific failing boundary: local changes, Context Map trace, commit/push failure, fetch failure, or SHA mismatch.
- Do not bypass the gate by leaving an untracked Context Pack, Context Map trace, or `INTENTS.yaml` change.
- Once the gate passes, later research artifacts and terminal/archive changes each require their own scoped commit/push/verification.

## Boundaries

- This gate proves remote persistence only; it does not authorize public sends, payments, permission changes, deployments, secrets, or destructive actions.
- Keep existing unrelated changes untouched.
