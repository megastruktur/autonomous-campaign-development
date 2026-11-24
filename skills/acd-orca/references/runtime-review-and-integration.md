# Runtime testing, review and integration

This current portable procedure owns topology, execution ordering, integration and
source-preserving completion under the actual owner/project mandate, current
[skill entrypoint](../SKILL.md) and [common fleet contract](../../../fleet/skills/fleet-campaign/references/common-contract.md).
Read [roles](roles.md) for ownership. Coordinators supervise and validate receipts;
they neither implement nor resolve source conflicts nor perform substantive code review.

## Authority and admission

Apply the actual mandate and [handoff admission](handoff.md#execution-admission), not
historical approval or fresh-session START ceremonies. An available command, successful
worker report or provider-readiness receipt creates no delivery authority. Before every
affected dispatch, integration or acceptance-gate completion, check actual UTC against
the persisted original attempt deadline and any non-null campaign cutoff, current revision,
pause state, ownership and permitted operations. The campaign cutoff is null when the actual
mandate has none; never inherit a historical campaign cutoff. Null does not waive finite
15-minute source attempts, 10-minute checkpoints or 10-minute reviews; stricter mandates win.
No new affected work after expiry; retries, wakes and fixes cannot reset the original clock.
A late native wake cannot prove an in-flight process exited. Use
[state and recovery](state-and-recovery.md#native-continuation-and-original-clocks)
for native continuation and guarded settlement, never an external watcher or poller.

Default substantive code review is roborev under the current skill/common contract, not an
author's amendment. [Code review](code-review.md) owns the qualified interface and fail-closed
provider contract. Preserve independence, complete coverage, source/scenario binding, runtime
testing and source retention. Readiness requires actual scoped environment, configuration and
source evidence; reuse valid same-scope receipts only, never inherited PASS. Historical success
is not this user's qualification, and missing evidence does not authorize automatic paid probes.
Readiness receipts never accept a product candidate.

The historical [owner amendment](../../../fleet/execution/fullauto/AMENDMENT_01_ROBOREV.md) and
[execution charter](../../../fleet/execution/fullauto/CHARTER.md) retain provenance only.
They supply no new-user permissions, inherited no-commit prohibition, timer/budget/delivery
constraints or private readiness prerequisites. Historical wording in linked references does
not override this current runtime policy, the current skill/common contract or actual mandate.
Commit and integration operations require actual authority; do not create a commit merely for
review. Default MERGE only to the explicitly bound branch when the mandate grants it; without
a merge grant, do not merge. That changes the integration operation, not the review/smoke gate.
Keep actual identities, host paths and model routes in private project records.

## Git topology

1. Capture the original **named target branch and full starting SHA**, repository
   identity and intended destination before work. Never assume main/master, reinterpret
   a later HEAD as the original target or infer a target name from detached HEAD. An
   absent or ambiguous target requires owner reconciliation before affected mutation.
2. For a new campaign, use one Orca-managed campaign integration worktree on its own
   branch, conventionally `{prefix}-campaign`, cut from the named target branch at
   the admitted starting point. Create task worktrees as Orca children of that root,
   based on the recorded campaign **branch at its current accepted tip**. Branch bases,
   not raw SHA/HEAD selectors, preserve intended lineage; a pinned SHA is the comparison
   identity, not a substitute for the branch base.
3. Use installed version-matched native worktree/worker discovery through
   [Orca runtime](orca-runtime.md). Do not copy old terminal recipes or use bare Git
   worktree creation. Record actual returned worktree, parent, branch and HEAD, since
   generated branch names may differ. Compare returned HEAD with the expected branch
   tip before dispatch; a mismatch blocks work until reconciled.
4. Reuse an existing feature worktree only when the mandate permits it and its named
   branch/base, parentage, idle state, dirty/untracked baseline and sole-writer custody
   are verified. An owner-specified pinned-base pilot must retain that explicit base
   contract and receipt; do not silently substitute the current campaign tip. If the
   installed native interface cannot express the authorized topology, report the gap
   instead of detaching, inventing flags or creating a duplicate workspace.
5. Task branches never merge directly into the original target. Serialize all writes
   to the campaign integration destination under one integration owner. A target branch
   is updated only through the authorized final campaign operation, not per-task merges.

`{prefix}` is the sole placeholder in this reference: the campaign's unique short slug,
resolved privately. Native launch acceptance is not proof work began; keep the actual
session and output discoverable and bind them to the assignment. Unknown launch or
ownership outcomes block duplicate starts under the recovery contract.

## Concurrency and resource exclusions

The global campaign ceiling is **three occupied resource slots**, normally one writer plus
one reviewer across candidate-separated scopes, with **one source writer per worktree**.
Count reviewers, runtime executors, fixes, remediation, conflict workers and any permitted
nested assignments across all worktrees; no hidden fanout or extra quota per wave/worktree.
A possibly live worker with an unknown stop outcome still occupies custody and capacity until
reconciled. Slots remain occupied until actual native release/exit evidence, not completion.
A plan does not authorize helper workers merely because spare capacity exists.

Stricter actual mandate limits win; historical two-paid-worker and one-file campaign limits
are not universal restrictions. Review freezes the candidate: no source mutation alongside
review, including an author's small fix. Separate read-only review storage does not authorize
an unfrozen writer or a second review of that candidate. Preserve all resource exclusions.

Record exclusive ownership before dispatch for files and shared APIs, schemas and
migration order, manifests/lockfiles, build outputs, ports, fixture data, databases and
external side effects. Distinct branches do not isolate a shared database, output path
or external account. Serialize dependency-manifest and lockfile updates through an
approved foundation task or exclusive owner; workers cannot install unapproved packages.
Resolve contention centrally, not by choosing a new port/schema or weakening exclusions
without authority. Reuse waits for verified cleanup/release, not a done message.

Dependencies, not fixed-wave barriers, select available work. A product task starts only
after each required predecessor's independent acceptance, authorized integration and
actual integrated-source smoke are recorded and its acceptance gate is completed by the
coordinator. Resource ownership may keep otherwise accepted work blocked.

## Exact candidate and stage ordering

For implementation, the order is:

1. Develop within the allowlist and bounds; produce an explicit ready handoff.
2. Exercise the real-runtime scenarios after the completed development/fix batch.
3. Freeze the candidate and commission independent review; obtain any separately required
   API/acceptance inspection without duplicating substantive code review.
4. Integrate only the reviewed source through the authorized operation; resolve conflicts
   through the implementation worker, then retest and independently review changed source.
5. Run post-integration smoke on the **actual resulting campaign source**.
6. Preserve source/evidence, complete the eligible acceptance gate and perform verified
   cleanup before resource reuse.

A commit arriving, workspace status, author self-review or successful analysis Task is
not readiness or acceptance. Bind every stage to repository/base/tip where available,
exact source manifest, build identity where relevant, scenario version and evidence
identity. Inventory required source, tests, dependencies, deletions, renames, untracked
and required ignored inputs. When commits are forbidden, preserved exact bytes and
SHA-256 manifests replace commit identity; do not demand a clean committed tree or
invent a resulting SHA. Freeze means immutable review inputs, not deletion of dirty work.

Changed source, build, relevant configuration or scenario invalidates earlier applicable
results. Preserve old receipts as historical evidence, never relabel them. A fix clears
current acceptance eligibility and returns the task to development; stale `in-review`
display state cannot trigger review. Readiness must include the final runtime evidence
and exact frozen candidate, not an intermediate handoff.

Document-only slices use assigned static checks and independent exact-byte document
review, not fabricated runtime scenarios. That narrow acceptance proves documentation,
not provider qualification, engine parity or a working implementation.

## Runtime testing contract

Unit and integration suites are supplemental signals, not substitutes for observable
production-path outcomes. Required runtime evidence must:

- Invoke the actual application, CLI, API or UI through its production entry point and
  test user-visible results, not internal call counts or mocked success.
- Record exact commands/actions, environment and build/source identity, scenario revision,
  inputs, expected and actual outcomes, exit/output and relevant artifacts for every
  required scenario. Resolve commands against the real environment before dispatch;
  unavailable capability blocks the affected acceptance rather than inviting invented syntax.
- Exercise rendered interaction in the real UI for a UI requirement. An endpoint response,
  unit component test or screenshot without the required interaction is not UI acceptance.
- Declare any external-dependency mocks and their limits. Never mock the feature under
  test or call mock-only/unexecuted integration verified. Synthetic negative fixtures and
  tabletops remain labeled synthetic; a tabletop is not a runtime result.
- Run after the worker declares the completed batch ready and after each completed fix
  batch, not after each line. A separate runtime executor is allowed where assigned;
  its report is evidence, not the independent code-review verdict.
- For concurrency, retries or durability, exercise real persistence boundaries and
  controlled overlap/fault injection when feasible. Sequential mocks cannot prove
  atomicity. Disclose probabilistic scheduling and unavailable safe fault injection;
  unexercised cases remain UNTESTED and required missing proof remains blocking.
- For a bug, retain the pre-fix failing observation/scenario and show the corrected
  behavior. A regression that also succeeds on broken behavior proves nothing. Do not
  re-expose user data or damage a host to manufacture a negative control.
- Preserve every acceptance failure and its load/environment conditions. Diagnose it
  and assess residual risk; one passing rerun cannot dismiss it as harmless flakiness.

Source and scenario versioning apply to runtime evidence equally. A changed test scenario
cannot inherit the old result. Long builds/tests require a predeclared bounded phase and
completion evidence; transport activity does not extend a deadline.

## Independent review boundary

The coordinator commissions one active review per exact candidate/packet/scenario,
reconciling an uncertain prior run before another. The neutral packet contains original
acceptance, shared contracts, exact base/candidate/diff, runtime/scenario evidence and
known findings. No expected verdict, reassuring author summary or implementer transcript.
A fresh independent context on the same model does not imply diverse failure modes.

Historical **roborev 0.75.0 to OMP 19.1.1 native ACP** success proves only its recorded scope,
not this user's qualification. Require actual scoped environment/configuration/source evidence
for the selected interface; reuse receipts only while those bindings remain valid. No inherited
PASS or automatic paid qualification probe. Follow [code-review admission](code-review.md#freeze-and-free-scope-preview)
for the external free scope preview and immutable no-hooks review-only snapshot outside
the live checkout, fresh private config/session and original source mapping. No live
checkout target, automatic fixes, hook/global changes, resumed author context or silent
provider substitution. Operational read-only tools are not an OS sandbox claim.

The [raw evidence contract](code-review.md#raw-result-and-coverage-receipt) requires
source/config/diff/hook guards, raw schema 3 findings, sanitized provider completion and
tool results, and external complete file-to-tool-ID-to-line-range-to-content/hash
reconciliation. Roborev has no native complete-coverage certificate. Exit zero, ACP
`end_turn`, empty findings or a file count alone never establish PASS. Missing, malformed,
failed, partial, skipped, unknown, truncated or zero-required coverage is INCONCLUSIVE;
binding drift INVALIDATES applicability. Complete critical/high/medium findings block;
low/style alone does not. Preserve all raw findings and independent blocker dispositions.

Reviewers never edit even temporarily, commit, merge, push or auto-fix the reviewed tree.
They may propose source-mutating probes; only an authorized executor runs them in an
isolated disposable copy and archives the results. Re-review covers corrected findings,
sibling paths of the defect class and introduced regressions. Out-of-scope findings go
to the coordinator for scope disposition, not reviewer expansion. The coordinator checks
bindings/coverage and derives gates; substantive source judgment stays with the reviewer.

FAIL goes to the implementation worker, then runtime retest and fresh exact-source review.
Preserve the initial FAIL, fix handoff, retest and new verdict before disposal. Productive
iterations and independently mandated fix/retry ceilings are governed by the actual bound
mandate and current contracts, not an unlimited legacy loop or universal historical campaign
limits. Original clocks survive fixes. Apply finite source/checkpoint/review bounds above and
the admitted concurrency/spend constraints through [handoff bounds](handoff.md#handoff-packet)
and [review bounds](code-review.md#bounded-invocation); historical numerical restrictions in
those references do not override current policy. Unsupported token/effort controls need
explicit bounded reconciliation before admission, not invented flags or dropped limits.
Exhausted bounds or unchanged provider/permission failure stops the affected path.

## Task integration

Persist an integration intent before mutation with operation identity, authority, pinned
source and destination, expected result and evidence pointers. Recheck real UTC, current
ownership, pause state, resource exclusions and both exact input identities immediately
before acting. If source or destination moved, hold integration and invalidate the old
prospective-result approval; preserve task evidence only under its original binding.
Reconcile the new composition, runtime-test it and obtain fresh exact-source independent
review before it can proceed. Never quietly re-hash drift into approval.

Use exactly the authorized route:

| Route | Required receipt and constraints |
|---|---|
| Commits and task integration authorized | Task-to-campaign integration is a squash merge. Record task source tip SHA, pre-squash campaign SHA, resulting squash commit SHA and tree, input/source manifest and evidence pointers. Do not merge the task directly to the original target. |
| No-commit delivery | Preserve the starting destination manifest, incoming reviewed source/test/dependency manifest, attributable diff including deletions/renames, untracked source and resulting integrated manifest. Record the authorized composition operation and original-to-result mapping; commit fields stay unknown/not applicable as appropriate, never fabricated. If all source already lives in the authorized worktree, freeze and identify that actual composition instead of inventing a merge. |

In either route, source conflict resolution is implementation: a bounded worker owns it,
never the coordinator. Freeze the resolved candidate, rerun affected runtime scenarios
and obtain independent review of the integrated candidate before accepting the result.
A conflict-free operation does not excuse verifying its resulting source identity. If
composition is not authorized, retain source and report the blocked operation rather
than substituting a merge, commit, reset or install.

After integration, smoke the actual resulting campaign source/build and record its exact
manifest/tree, scenario version, commands and outcomes. A failed smoke blocks dependents;
fix through the implementation worker within bounds, then retest, review and smoke the
new integrated source. Do not silently reset durable/published history to hide failure.

A lost result receipt is an idempotency problem, not permission to repeat integration.
Compare the recorded intent and actual destination with source/result receipts under
[crash reconciliation](state-and-recovery.md#crash-windows-and-reconciliation). A squash
source tip is normally not an ancestor of the squash commit; ancestry alone cannot prove
whether it was integrated. For no-commit work, reconcile byte manifests/diffs instead.
An unexplained mismatch or unknown outcome blocks a duplicate operation.

Product successors depend on a separate **blocked native acceptance Task**, never the
author/analysis Task. It is never dispatched or made ready as work. Only the coordinator
completes it after current exact-source independent review, required API evidence,
authorized integration and actual post-integration smoke pass. Attach all three core
review/integration/smoke bindings and any API receipt. A successfully delivered FAIL or
INCONCLUSIVE analysis, provider-readiness result or document verdict cannot open this gate.

## End of campaign

1. Account for every required task/stage, scenario and unresolved finding. Run full campaign
   acceptance and integration-seam runtime tests on the exact final campaign candidate,
   then independent final review on that same source, using the complete accumulated
   acceptance surface. Earlier per-task PASS is not final review.
2. Recheck the original named target. If it moved, reconcile its latest identity without
   clobbering user changes. When integration is authorized, incorporate that target into
   the campaign through the same worker fix/runtime/review rules and rerun final runtime
   acceptance and final independent review on the new exact candidate. If incorporating
   it needs missing permission, stop the affected finalization and report the blocker.
   A no-commit mandate does not authorize a hidden merge or erase the moved-target check.
3. Immediately before an authorized final merge, verify expected named target and campaign
   refs again under exclusive integration ownership. Another movement reopens validation;
   do not race ahead with an old verdict. The coordinator alone performs the authorized
   final operation, not source conflict resolution. Default final strategy is `--no-ff`
   only when recorded in the mandate; this reference supplies no merge permission.
4. Run post-final-merge runtime smoke **on the actual target** and bind target commit/tree,
   build and scenarios. If the mandate has no final merge, identify and smoke its actual
   authorized integrated delivery snapshot instead; explicitly record that no target
   merge occurred. Never call a campaign-tree run target smoke.
5. Preserve source and all evidence outside disposable workspaces, then perform scoped
   verified cleanup. Source delivery, runtime acceptance and native release are distinct
   receipts; none follows merely from another succeeding.
6. Produce the durable final report with exact deliverable identity, reproducible commands,
   acceptance matrix and PASSED, BLOCKED or UNTESTED per requirement, residual findings,
   retained resources and the next actual action. Ready-for-captain is not captain acceptance;
   failed, paused, cancelled and completed remain distinct outcomes.

Push, publication, deployment and installation each require separate authority. A merge
is not user delivery: when packaged/installable delivery is actually requested and
authorized, runtime acceptance must exercise that deliverable. Do not repoint loading paths,
alter legacy files or change installed consumers without separately authorized scope.

## Cleanup

Before release or any disposal, preserve full attributable source, not only summaries:
commits/recovery refs or bundles when authorized; otherwise the diff **and** untracked
source, base material and immutable manifests needed to reconstruct exact bytes. Retain
runtime failures/results, scenario definitions, build provenance, raw review findings,
sanitary tool/provider evidence, integration receipts and final smoke. Export a checksummed
archive and verify its inventory/hashes and recoverable source outside every disposable
worktree, including the campaign root. Never delete plans/evidence as test artifacts.

Inventory only owned disposable resources. Settle or guarded-stop exact assignments and
verify process exit; native task completion, fencing, silence, timeout or a stop request
is not exit. Preserve source/evidence and perform safety checks before any worktree removal.
Use supported native release/removal operations and read back their exact receipts. Verify
owned test processes stopped, owned ports released and removed worktrees absent. Unknown
stop/release state blocks replacement and resource reuse; do not kill unrelated sessions,
daemons, ports or services. Retain a workspace deliberately when safe release is unproven.

Dirty or untracked work must be rescued to durable authorized storage or cleanup pauses.
Do not discard another owner's changes, run broad clean/reset or force-delete a branch
because Git calls a squash source unmerged. Prove the squash receipt, resulting tree and
smoke, preserve recovery material when needed, then use only precisely scoped authorized
cleanup. Protect source/worktrees used by active consumers and resources retained for diagnosis
or ongoing work; successful cleanup of a disposable scope cannot authorize removing either.

Mark cleanup complete only after verified actual actions, never a promised removal.
Remove only obsolete owned native timers and ignore queued late wakes under the recovery
contract; cleanup must not resume paused work. Record retained resources and reasons
honestly. Source/evidence preservation is mandatory even when acceptance fails or bounds
expire, while destructive cleanup still requires authority and settled ownership.

## Sources and staged links

The [obligation ledger](obligation-ledger.md#reference-obligations) maps legacy entrypoint
sections 8-10 and 13 and the [legacy runtime reference](../../acd/references/runtime-review-and-integration.md)
to this document. Retain their safety guarantees, not obsolete START, provider-fallback,
watcher or unbounded-loop mechanics. Historical pending labels are provenance, not current
readiness prerequisites; the current skill/common and code-review contracts govern.

[Orca runtime](orca-runtime.md), [task template](../templates/TASK.md),
[TODO template](../templates/TODO.md) and [validation tabletops](validation-tabletop.md)
are part of the current tree, not unauthored/PENDING targets. Check the actual reviewed tree:
resolve every link, reconcile template/source/scenario/gate fields and bind independent review
to the current complete candidate. Static document checks and
synthetic tabletops are not execution, cleanup, provider or engine qualification.
