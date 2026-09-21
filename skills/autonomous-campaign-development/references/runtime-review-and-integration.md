# Runtime Testing, Independent Review, Integration, Campaign End

## Runtime testing contract

Unit and integration tests are optional supplemental signals and NEVER proof that a
feature works. Mandatory runtime testing:

- Invokes the actual application/CLI/API/UI through the production path.
- Checks observable user outcomes, not internal call counts.
- Records build/source identity (exact commit/tree/build) and the commands, actions, and
  results of every scenario.
- A UI feature requires actual rendered interaction in the real UI - an endpoint response
  alone does not verify a UI.
- Mocks are allowed ONLY for external dependencies, must be declared with their limits,
  and the feature under test is never mocked. Mock-only or unexecuted real integration is
  never labeled "verified"; a missing runtime capability BLOCKS the task instead.
- Timing: run after the executor declares the feature ready and after each completed fix
  batch - not after each line or intermediate edit.
- An independent runtime test executor (separate from the coding agent) is allowed and
  useful; assign one per task. Its report is evidence, never the independent review.
- Concurrency/retry/durability features need actual runtime reproductions with real
  persistence boundaries and controlled overlap/fault injection when feasible - a
  sequential mock cannot prove atomicity. If scheduling is probabilistic, say so. An
  executor reproduces the pre-fix failure (the fix must make a previously failing
  scenario pass); a regression that also passes on broken behavior proves nothing.
- A failing acceptance run stays unresolved until explained: record failure and load
  conditions, seek a reproducible explanation, assess runtime risk. One passing rerun
  never reclassifies a failure as "harmless flaky".
- Scenario versioning: bind each result to the scenario version; a scenario change
  invalidates prior results just like a code change does.

## Independent review contract

The coordinator MUST commission its own independent review for every frozen candidate -
even if the author ran a self-review or spawned a reviewer subagent itself. Self-review
is optional preparation, never a completion gate substitute.

Review packet (assembled by the coordinator, unbiased): task acceptance criteria, source
contracts, exact diff base/tip, runtime evidence, and known findings - the raw material,
never the author's reassuring summary, and never a "already PASS, please confirm"
framing. The reviewer independently inspects every acceptance point.

Reviewer rules:

- Independent: an inquisitor-style profile/agent when actually available, else a
  separately spawned read-only session; never the implementing session, and never a
  session that authored the change under review.
- Verdict: an explicit, complete `PASS` or `FAIL` plus actionable findings classified as
  acceptance / API / correctness / security. Shell rc=0, a terminated review process, or
  an empty response is NOT a verdict - re-commission until a complete verdict for the
  expected snapshot exists.
- No edits, commits, merges, pushes, or automatic fixes - not even a temporary edit of
  the reviewed tree. The reviewer may PROPOSE source-mutating probes (negative controls,
  mutation-sensitive checks); the EXECUTOR runs them in a disposable isolated copy,
  archives the evidence, and the reviewer assesses that evidence.
- Re-review after a fix checks: the corrected finding, sibling paths of the same defect
  class (for example claim/release/rebind together; duplicate IDs within one request AND
  across requests; replay/cancel/concurrent-execution variants; permission boundary
  variants), and regressions introduced by the fix.
- Scope stays fixed: out-of-scope systemic findings are reported to the coordinator for
  scheduling as follow-up work; the reviewer does not roam, fix, or expand the task.
- Exactly one active review per candidate; dispatch it exactly once (dedupe by commit).
- Freeze the writer before review: the verdict binds to the exact commit/tree/build; any
  new commit invalidates it and requires a fresh review.
- The coordinator validates evidence and verdict metadata (bindings, coverage of
  acceptance points), not the code itself - substantive code review belongs to the
  reviewer.

Evidence chain: preserve the initial FAIL, the executor fix handoff, the runtime retest,
and the new PASS in campaign evidence BEFORE removing the worktree. Exact SHA binding
prevents stale or self-declared PASS reuse.

A commit arriving is not "feature done": done = executor's explicit ready handoff +
final runtime evidence + clean frozen candidate + independent verdict.

## Git topology

- Worktrees below are created by the EXECUTION session after a validated START - never
  by the planning session (see [handoff-and-start.md](handoff-and-start.md)).
- Capture the original NAMED target branch and its full starting SHA at campaign start.
  Do not assume main/master; do not reinterpret HEAD later. Detached HEAD start: the user
  must name the target branch.
- Campaign integration: a dedicated Orca-managed worktree `{prefix}-campaign` on its own
  branch created from the pinned start. Task worktrees branch from the appropriate
  CURRENT campaign tip. Record the branch names Orca actually returned.
- Task branches NEVER merge to the original target. Only the campaign branch does, once,
  at the end.
- Serialize ALL integration writes: one merge at a time under integration ownership.

## Task squash integration

Task -> campaign is a squash-merge, ALWAYS. For each integration record a receipt:
task source tip SHA, pre-squash campaign SHA, resulting squash SHA and tree, plus
evidence pointers.

- A squash source tip is NOT an ancestor of the squash commit: never use an ancestor
  check as the only idempotency test - match receipts (see crash recovery in
  [state-and-recovery.md](state-and-recovery.md)).
- Integrate only the reviewed snapshot: pin both source and destination SHAs; if either
  ref moved, the candidate's approval is invalidated - re-test/re-review the new
  prospective candidate first.
- Integration conflicts and fixes are delegated to an OMP agent (coordinator never edits
  source), followed by runtime retest and independent review of the integrated candidate.
- After the squash: run a post-merge runtime smoke on the ACTUAL campaign tree before
  releasing dependent tasks. A failed smoke blocks all dependent work; fix through an OMP
  agent, then repeat testing/review. Never silently reset published or durable history.

## End of campaign

1. Every task TODO done; every required runtime scenario exercised.
2. Full campaign acceptance plus seams runtime test at the EXACT campaign tip, then
   independent final review at that same tip.
3. If the original target moved since the start: integrate the latest target into the
   campaign through the same fix/test/review rules and re-run final runtime verification.
   Never clobber the target or assume old acceptance still applies.
4. Verify expected refs immediately before merging (under integration ownership,
   coordinator only). Default final merge is `--no-ff` to retain task squash commits and
   mark the campaign boundary - this choice was recorded in the plan approval.
5. Post-final-merge runtime smoke ON the target.
6. Archive receipts and evidence outside every disposable worktree; stop scoped test
   resources; remove the campaign worktree only after the smoke passes.
7. Write `{prefix}_REPORT.md`. The campaign is done only when ALL stage TODOs are done.
8. Push/publication/deployment remain disabled unless separately approved. Merge is not
   user delivery: if packaged/installable delivery was requested, runtime acceptance
   includes it.

## Cleanup

- Final evidence lives OUTSIDE every disposable worktree, INCLUDING the campaign
  integration worktree. Canonical artifacts stay in the original repo's plans/ path (or a
  durable user-approved path). Plans and evidence are never deleted as "test artifacts".
- Remove only inventoried disposable items: test fixtures, ports/processes belonging to
  the task, sessions, worktrees - and prove each removal (process gone, port free,
  worktree absent from `worktree ps` / `worktree list`).
- Squash trap: after a squash-merge, git may report the task branch as "unmerged". NEVER
  auto force-delete based on that status text. Prove the recorded receipt (squash SHA,
  tree, post-merge smoke) and archive a recovery ref or bundle if needed, then delete
  with precisely scoped, approved commands.
- Dirty or untracked work in a worktree slated for removal: rescue it into the campaign
  evidence/plans area or PAUSE cleanup - never destroy it.
- The mandatory cleanup checkbox is checked only after the actual verified removal, not
  as a promise. Resource reuse waits for cleanup completion.
- Teardown order per worktree: close terminals and verify processes stopped -> archive
  evidence -> safety checks -> `worktree rm` (selector form). See
  [hermes-orca-omp.md](hermes-orca-omp.md#teardown).
