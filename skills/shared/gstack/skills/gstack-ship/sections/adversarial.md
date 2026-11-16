<!-- AUTO-GENERATED from adversarial.md.tmpl — do not edit directly -->
<!-- Regenerate: bun run gen:skill-docs -->
**Step 9's last full-pass plan governs this step:** run the native pass only on
`DISPATCH: adversarial-native` and the outside voice only on
`DISPATCH: outside-voice`. Without the native line (light depth at runtime 0;
above 0 the plan lists it beside the batched specialist), print `ADVERSARIAL: skipped (review plan)`;
with neither line, take decision 3 of Finish the adversarial phase. The native pass takes its line's
`checklists=` and `classes=` as render flags and runs on its `model=` (`lane`: yours). On `DISPATCH: targeted`, also run the targeted reader
(`gstack-review-dispatch render --role targeted --classes <TARGETED classes> --base <base> --diff-base <merge base>`, the merge base on every pass, never RANGE_BASE) like the voices; `verify --targeted-out .gstack/tmp/targeted.json` feeds the receipt's `--review-targeted`. Under a token cap,
reserve the planned voices as one batch (`gstack-ship-budget check --next dispatch:<roles>`)
and add `--reservation <id>` to the `--start adversarial-review` call below.
After `NEXT: voices` (gate class: Step 11 before any stop), Finish the adversarial phase takes neither
decision 2 nor 3: rerun Step 9's repeat decision with `--adversarial-ran` (a queued blocking finding as
`--blocking-open`); its `NEXT:` stands: only `stop` (Step 9.4's decision 2)
or a granted fix-check (item 3.5, then Step 11.5) follows voices.



## Capture Learnings

If you discovered a non-obvious pattern, pitfall, or architectural insight during
this session, log it for future sessions:

```bash
[ -d "${GSTACK_ROOT:-/-}/bin" ]&&[ -d "$GSTACK_ROOT/lib" ]||{ GSTACK_ROOT="/home/ubuntu/.gstack/repos/gstack";[ -d "$GSTACK_ROOT/bin" ]||{ echo "gstack: no install found (tried $GSTACK_ROOT). Fix: ./setup --host openclaw from your gstack checkout; ./setup --status shows it.">&2;exit 1;};}
GSTACK_BIN=$GSTACK_ROOT/bin
$GSTACK_BIN/gstack-learnings-log '{"skill":"ship","type":"TYPE","key":"SHORT_KEY","insight":"DESCRIPTION","confidence":N,"source":"SOURCE","files":["path/to/relevant/file"]}'
```

**Types:** `pattern` (reusable approach), `pitfall` (what NOT to do), `preference`
(user stated), `architecture` (structural decision), `tool` (library/framework insight),
`operational` (project environment/CLI/workflow knowledge).

**Sources:** `observed` (you found this in the code), `user-stated` (user told you),
`inferred` (AI deduction), `cross-model` (both Claude and Codex agree).

**Confidence:** 1-10. Be honest. An observed pattern you verified in the code is 8-9.
An inference you're not sure about is 4-5. A user preference they explicitly stated is 10.

**files:** Include the specific file paths this learning references. This enables
staleness detection: if those files are later deleted, the learning can be flagged.

**Only log genuine discoveries.** Don't log obvious things. Don't log things the user
already knows. A good test: would this insight save time in a future session? If yes, log it.



### Refresh learnings for the headline feature on this branch

Step 8 used broad release terms. Before VERSION/CHANGELOG, search for versioning
or changelog pitfalls tied to this branch's headline feature.

Use ONE alphanumeric-or-hyphen noun naming the skill, module, feature or changed
binary: `token-or-search`, not `feat: token-or search`.

```bash
{ _LE=$(/home/ubuntu/.gstack/repos/gstack/bin/gstack-learnings-search --query "<your-keyword>" --limit 5 2>&1 >&3 3>&-); _LR=$?; } 3>&1
[ "$_LR" = 0 ] || { _LE=${_LE%%$'\n'*}; echo "LEARNINGS: unavailable (${_LE:-exit $_LR})"; }
```

Name an applicable learning and its effect on the bump or CHANGELOG in
one sentence, or continue without one.
