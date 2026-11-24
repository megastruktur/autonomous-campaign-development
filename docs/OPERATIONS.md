# Operate the project fleet

Use the same designated PROJECT Magos owner chat/Run for status, steering and delivery.
[Setup](SETUP.md), [optional GitHub intake](GITHUB_ISSUES.md) and the
[common contract](../fleet/skills/fleet-campaign/references/common-contract.md) define the
bindings and authority. Shared Logis plans; the owner accepts and dispatches. Do not create
a duplicate owner or a separate fleet to recover a stalled request.

## Daily steering

Send these prompts to the already bound project owner, with the actual request/revision:

- **Status:** “For this request, report current revision, exact source, completed checks,
  blocking findings, active workers and retained resource slots. Separate product acceptance
  from analysis delivered, and settled tasks from released workers.”
- **Pause:** “Pause this request now. Stop new dispatch and integration; account for in-flight
  work and preserve source/evidence. Report what remains running. Do not interpret pause as exit.”
- **Resume:** “Resume only the unfinished authorized scope. Reconcile the existing owner Run,
  tasks, Dispatch identities and actual worker stop/release receipts before replacements.
  Keep the original bounds and source identity; report a capability blocker rather than bypass it.”
- **Scope revision:** “Record this change as a new request revision: [bounded change]. Preserve
  previous intent and evidence, settle affected work, return changed design through Logis,
  and re-review affected contracts. Stale results cannot satisfy superseded acceptance.”
- **Delivery:** “Report exact candidate, real test/runtime results, independent review and
  authorized delivery location. MERGE only to the explicitly bound branch within my mandate;
  no push or deployment unless I separately authorize each.”

A request, charter or automation cannot override repository policy or runtime permissions.
Untrusted Issue/comment/tool content never expands authority. No routine intermediate START
approval is added inside a valid mandate; real scope, capability, security or budget conflicts
still stop the affected path. A paused/finished request is never revived by a stale timer.

## Workers, completion and cleanup

Follow [native recovery and release](../skills/acd-orca/references/orca-runtime.md#recovery-and-source-preserving-release)
and [source-preserving cleanup](../skills/acd-orca/references/runtime-review-and-integration.md#cleanup).
Reconcile exact Task/Dispatch/session ownership before touching a worker. On an unknown start,
stop or release outcome, inspect that same receipt; do not launch a replacement writer.
One source writer per worktree; at most three occupied resource slots, normally writer plus
reviewer. Use fresh transient review contexts, not persistent per-file Bot chats.

Completion/end-turn is NOT process exit or native release. Closing a tab and
`agentSession.release` are not universal process-exit guarantees. An idle screen, report,
falling process count or timeout does not prove the specific owned process exited. Preserve
committed source or attributable dirty/untracked work, manifests and raw review/test evidence
outside disposable storage before release; retain native release/exit receipts afterward.
Read-only instructions are an agent mandate, not an OS sandbox unless independently evidenced.

The [historical runtime amendment](../fleet/execution/fullauto/AMENDMENT_03_RUNTIME_RESUME.md#correct-runtime-lifecycle)
records a retained-runtime problem. The **53 retained ACP processes** are a historical unresolved
observation, not a claim that these docs fixed them or that every installation has 53 processes.
Use current scoped evidence rather than replaying that campaign's cleanup authority.

For an inaccessible Group, cleanup requires owner intervention, not an agent bypass. The
owner UI route is **Sleep → This Workspace**, only after all of the following are checked:

1. Exact workspace/session ownership and intended scope are verified.
2. Source and evidence are preserved outside disposable storage.
3. The workspace is quiescent: no working turn, awaited reply, approval or required live job.
4. Protected Group sessions and unrelated/user-owned live work are excluded; if they cannot
   be excluded, stop and ask the owner for a narrower supported action.
5. Native receipts and actual owned process identity/exit are checked; unknown remains unknown.

**With Descendants** has broader scope and is not a fallback for an inaccessible Group.
Never use broad kills, identity impersonation, backing-file/runtime-database edits or service
restarts to defeat a refusal. Do not assume tab closing substitutes for Sleep or release.
A retained resource can be deliberately needed: report the reason, not “all cleaned.”

## Update without changing live instructions underneath work

1. Settle active consumers first: pause dispatch, preserve work, reconcile workers and record
   which Bots/chats still consume the old tree. Link changes do not reload already-read text.
2. Obtain a separate complete new tree and review its full pinned revision using
   [clone/review/pin setup](SETUP.md#2-clone-review-and-pin-the-complete-tree). Keep
   `skills/acd-orca`, referenced legacy `skills/acd` and `fleet` in their relative layout.
   **Do not git pull beneath live instructions.** Never replace a tree merely to satisfy a check.
3. Preserve the old pinned tree, local changes, private bindings and SOUL backups. Compare
   old/new dependencies and intended changes, including any locally customized legacy skill.
4. Record every current link and exact target: shared `~/.agents/skills/acd-orca`,
   `~/.agents/skills/acd`, `~/.agents/fleet`, and each verified Bot home's
   `.agents/skills/fleet-campaign`. A regular directory/file is not an owned install link.
5. Only after owner approval, repoint the explicitly selected owned links to reviewed exact
   targets. Refuse unexpected targets and file/directory/dangling collisions; do not force,
   nest links inside directories or migrate unrelated installations. Keep rollback targets.
6. In fresh actual execution sessions, verify discovery and explicit body/reference/common
   reads under the [OMP loading procedure](../skills/acd-orca/references/engines/omp.md#startup-loading-and-discovery).
   Compare paths/hashes to the pinned source. Test affected capabilities before admitting work;
   a parent receipt, catalog listing or resolving link is not instruction loading.

No update automatically changes permissions, models, credentials or live SOULs. Use the
[approved SOUL backup transition](SETUP.md#3-create-five-shared-bots-and-one-project-bot)
only when a separately approved role update actually requires it.

## Rollback or uninstall only your exact links

First settle consumers and preserve current work/evidence as above. Compare each path using
readlink with the exact target recorded at installation; also verify ownership and consumers.
Unlink only an actual symlink whose target still equals that recorded target, including each
per-Bot bridge. If it became a directory, points elsewhere or is an unexplained dangling link,
stop and investigate; never remove the destination tree by following a link.

For rollback, restore only owner-approved exact prior targets from the retained installation
record after removing the matching new links; verify fresh-session loading again. Restore a
SOUL only from its verified backup with explicit approval and current-content comparison.
For uninstall, leave preexisting legacy acd, other installations, private bindings, SOUL backups
and live project work intact. Retain the durable tree until no consumers reference it.
**Removing links does not unload chats** or revoke their permissions. No blanket recursive deletion.

## Diagnose the failing boundary, not a different model

| Symptom | Check and next action |
|---|---|
| Skill absent | Check selected execution computer/profile and discovery filters, full tree and exact symlinks in [OMP discovery](../skills/acd-orca/references/engines/omp.md#startup-loading-and-discovery). Do not reinstall over collisions. |
| Listed but not loaded | Explicitly read `skill://acd-orca`, its OMP asset and bound filesystem common contract in that session; record actual paths/hashes using the [loading receipt](../skills/acd-orca/references/engines/omp.md#instruction-loading-receipt). |
| Bot succeeds, worker denied | Follow [permission setup](SETUP.md#1-prerequisites-on-the-execution-computer): Bot header gear → Settings → Agent → Permissions is separate from Settings → Agents → OMP future-worker override. Existing chats retain their own settings; verify a fresh worker and [all four scopes](../skills/acd-orca/references/engines/omp.md#four-permission-scopes). No automatic elevation. |
| Model/provider failure | Verify requested/resolved/actual model and authenticated route on the execution host via the [model checklist](../skills/acd-orca/references/engines/omp.md#primary-and-auxiliary-model-checklist). Auxiliary success is separate; no silent fallback or repeated unchanged retry. |
| Review cannot complete | Apply the [roborev contract](../skills/acd-orca/references/code-review.md#authorized-preflight-before-coding): provider and native OMP ACP engine are distinct, fresh context and real coverage required. rc=0/report delivery is not PASS. |
| GitHub event or post fails | Native App connector, local `gh` login and Git push credentials are separate. Follow [GitHub intake](GITHUB_ISSUES.md#1-owner-connects-only-approved-repositories); do not infer one identity/permission from another. Stay chat-only if unproven. |
| Missing binding or scope conflict | Follow [private owner/peer setup](SETUP.md#4-bind-one-owner-and-the-shared-peers-privately); stop mutation until exact ownership and the actual mandate are reconciled. |

Keep secrets in the configured manager, not logs/prompts/config snippets. Report safe error
messages, source and scope; do not dump account files, environment or other projects' chats.
Read [review readiness and native smoke](SETUP.md#5-establish-review-readiness-then-one-tiny-native-smoke)
for the small user-owned checks, not an invitation to run paid qualification on every change.

## Optional local repository checks

From the complete installed source repository root, with **Python 3.11+**, standard library
only. These commands exercise legacy tests plus current focused docs and the optional example:

```bash
python3 -B -m unittest discover -s tests -v
python3 -B -m unittest discover -s qualification/manifest-validator -p 'test_*.py' -v
python3 -B qualification/manifest-validator/cli.py --help
```

Report the actual counts/results from your revision, not fixed historical totals. The
[manifest validator](../qualification/manifest-validator/validator.py) is an optional pinned-packet
consistency example. It is not required to use the stack, not code authenticity or product
acceptance, and its synthetic tests do not replace the project's real runtime/business tests.
Only the owner completes product acceptance with current exact-source evidence under the
[native acceptance boundary](../skills/acd-orca/references/orca-runtime.md#acceptance-tasks-are-not-work).

## Historical references are not new-run authority

Frozen [fleet campaign material](../fleet/execution/fullauto/AMENDMENT_03_RUNTIME_RESUME.md)
and the [migration ledger](../skills/acd-orca/references/obligation-ledger.md) preserve provenance.
Historical staging labels and private receipts neither authorize nor block ordinary new use;
your installation needs actual current loading/capability evidence, not access to our old receipts.

Unchanged [legacy acd 1.7.0](../skills/acd/SKILL.md) has its own
[START/handoff](../skills/acd/references/handoff-and-start.md),
[OCR review](../skills/acd/references/ocr-review.md) and
[watchdog](../skills/acd/references/progress-watchdog.md) contracts. They remain for explicitly
legacy campaigns, not current acd-orca defaults. Current execution uses native Orca events and
Automations, qualified roborev and temporary OMP workers; no mandatory watcher, service,
relay or duplicated fleet is added. Public instructions stay English; private project facts stay private.
