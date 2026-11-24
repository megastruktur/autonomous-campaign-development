# Orca runtime boundary

This reference connects the staged, uninstalled candidate to the installed Orca runtime.
It defines discovery and receipt obligations, not a second CLI manual or scheduler.
Read [roles](roles.md) and the [common fleet contract](../../../fleet/skills/fleet-campaign/references/common-contract.md)
for ownership and shared policy, [handoff](handoff.md#execution-admission) for admission,
and [state and recovery](state-and-recovery.md) for durable decisions and original clocks.
An available command does not grant authority to run it.

The [owner amendment](../../../fleet/execution/fullauto/AMENDMENT_01_ROBOREV.md) selects
roborev instead of historical OCR prescriptions in unchanged shared and legacy sources.
[Code review](code-review.md) owns scoped provider qualification and candidate evidence.
Accepted provider readiness is neither product acceptance nor engine, auxiliary-model,
permission-denial or recovery qualification. Earlier snapshots' pending labels do not
replace the current accepted private receipts, and this document does not upgrade them.

## Discover the installed interface

Resolve the executable using the installed Orca discovery stub for this session, not a
remembered host/container path. The current discovery order is `ORCA_CLI_COMMAND` when
set, the dev executable for an identified dev session, the Linux host executable outside
managed terminals, otherwise the managed-session executable. Bare `orca` outside a
managed Linux terminal can be the unrelated screen reader. Verify identity before
execution; a selected executable failing is not permission to fall through to another
build or host.

The following are discovery calls only. `<ORCA>` is the verified executable, not a
literal command or shell variable to create:

```text
<ORCA> --version
<ORCA> skills get orchestration
<ORCA> skills get orca-cli
<ORCA> --help
```

Record the resolved executable, version/fingerprint, actual execution environment,
runtime identity/version when available, and loaded guide identities privately. Use the
same executable for subsequent calls. Consult narrow command help before using an
unverified option; prefer supported structured JSON receipts over screen scraping.
An installed CLI and connected runtime may differ: retain both observations and any
capability refusal rather than assuming the client version proves server support.

Load only the version-matched reference named by the relevant guide's action gate:

| Operation | Discovery source |
|---|---|
| Run ownership, Task DAG and dependency queries | Orchestration guide's coordinator-loop reference and task command help. |
| Placement, child worktrees or another host | Orchestration placement-and-remote reference plus installed worktree help. |
| Unknown launch, failed start, retry, stop or release | Orchestration recovery-and-cleanup reference and the actual operation receipt. |
| Exact-owner deadline | Orca CLI automations reference, trigger-options discovery and create/show/remove help. |
| Agent identity, output and native mail | Installed orchestration and orca-cli guides, then the relevant read/show/send/reply help. |

Use the guide's supported `--reference` retrieval; if refused, follow its documented
`--full` alternative and read the named section. If guides or required commands are
unavailable, report the exact version/error and limit work to supported read-only
discovery. Do not guess flags, inspect runtime databases to manufacture support, install
an adapter or change global configuration. Follow the selected guide's connection-error
recovery within existing permissions; a refusal is not permission to restart a service,
open another runtime or broaden access. Version-matched syntax is necessary, not runtime
qualification.

## Bind identity and placement

Before mutation, reconcile the actual sole coordinator chat, owning Run, Task and Dispatch,
worker session, execution environment and worktree. Native IDs are distinct identities:
a display name, Bot definition, provider conversation ID or terminal title is not a
substitute. Copy the exact returned selector/handle for its supported operation; never
fabricate a sender or use another actor's `--from`. A worker uses only its own injected
identity and assignment, never coordinator-only Run adoption or Task-gate mutation.

Pin locally intended Run/Task/worker operations to the installed interface's explicit
local environment selection; ambient routing must not silently choose another machine.
For authorized remote work, load the placement guide and discover that server's exact
selectors. Local `current`, local paths and local handles do not identify remote
resources. Do not create a remote setup, choose a different host or switch models to
repair an unapproved placement. Keep live routes and IDs in private project records.

Apply [topology and exclusions](runtime-review-and-integration.md#git-topology): named
branch/full starting SHA, actual returned parent/branch/HEAD comparison, one writer,
resource custody and stricter charter limits. Orca lineage and Git base are different
facts; neither can be inferred from a worktree name. A new worker must receive the current
task-specific brief, not an inherited brief from its base. Use native supervised launch
with the verified specification and approved agent/model, not a Kanban coding executor,
a startup shell or terminal-injected prose.

The native launch surface may be a chat or terminal. Preserve what actually launched,
its discoverable session/output and user-visible location where available. Do not demand
TUI-only execution, invent a worker surface flag or claim foreground visibility from a
successful launch. Moving or reopening a surface must not leave a duplicate writer.

## Native receipt chain

Persist intent before side effects and the resulting sanitized native receipt under
[state ownership](state-and-recovery.md#intent-before-mutation). Keep native observation
separate from the coordinator's decision and from product evidence:

| Transition | Required evidence and limit |
|---|---|
| Task creation and dependency binding | Owning Run, exact specification/revision, Task IDs, prerequisite gate IDs and native states. A file describing a DAG does not create it. |
| Worker launch | Task/Dispatch, actual host/worktree/session, requested/effective agent/model, setup effects, delivery stage, observed turn start, residual resources and `next` or recovery action. Accepted input or exit zero alone does not prove work began. |
| Model and instruction use | Requested, resolved and observed startup/purpose model, actual execution-host role/skill loading and correlated tool evidence. Picker/configuration presence is not actual use. |
| Native mail | Sender/recipient, request/message identity, Task/Dispatch/revision and delivery receipt. Stored mail is not proof of reading or action. |
| Result | Exact assignment, succeeded/failed delivery outcome, source manifest, commands/results, evidence pointers and unresolved work. Analysis delivery and acceptance remain separate. |
| Stop and release | Assignment settlement, physical agent/process state and resource release as distinct observations, including unknown or retained resources. A stop request or done message does not prove all three. |

Record missing facts as `null` with a reason and observation time, not inferred success.
Use native worker show/read/list and agent inspection for bounded reconciliation when an
event or uncertainty requires it; do not turn these commands into a polling loop. Preserve
complete relevant output or disclose truncation. The four progress facts in
[state and recovery](state-and-recovery.md#observation-and-semantic-progress) remain
separate: observation, successful assistant, completed tool and semantic checkpoint.

For an ambiguous launch or send, retain the exact native request/operation/retry identity
and follow that receipt's supported recovery. Never repeat a start, send a second brief
or create a new Task merely to obtain a clearer answer. Replay is allowed only when the
installed interface explicitly supports it for that same operation and the receipt
instructs it; a retry token from another command family is not interchangeable.

## Acceptance Tasks are not work

After planning convergence and actual execution admission, the coordinator materializes
work, independent analysis and acceptance as distinct native Tasks. A product successor
depends on the **acceptance Task**, not the author or analysis Task.

Establish each acceptance Task as **blocked** before enabling ready-work selection. Use
the installed task-create/dependency and task-update interfaces; discover their supported
creation/status sequence rather than inventing a create-blocked option. Keep dispatch
disabled during any creation-to-block transition, preserve the actual intermediate
receipt, and verify the gate is blocked before the graph can run. If safe native setup
cannot be established, do not activate dependent dispatch.

Acceptance Tasks are **never made ready and never dispatched**, including through a
generic ready-task loop. The installed guide's advice to start ready Tasks applies only
to admissible work, not permission to treat gates as work or bypass campaign bounds.
Only the designated coordinator sets a gate completed, attaching current exact-candidate
independent review, required API evidence, authorized integrated-source identity and
actual post-integration smoke receipts. [Integration](runtime-review-and-integration.md#task-integration)
owns those bindings. Document gates instead require their assigned static evidence and
independent exact-byte verdict; never invent a runtime result for Markdown.

A successfully delivered analysis containing FAIL or INCONCLUSIVE may settle that
analysis Task; its product gate stays blocked and its successor unready. Provider
readiness, author self-review, a deadline or an unbound PASS cannot open it. Preserve
failed outcomes rather than marking failed work completed. Changed source/configuration/
scenario invalidates affected acceptance until reconciled and independently rebound.
Gate enforcement must be tested on authorized disposable native objects during runtime
qualification; this contract and a matching status label alone are not that proof.

## Native communication and waiting

Steer only through native mail to the verified live assignment, normally Dispatch-addressed
for workers. Retain request and revision correlation; never inject guidance or answer a
permission prompt through another agent's terminal. A supported send to a settled worker
can reopen it with a follow-up Task: inspect the receipt and require authority, custody
and original bounds for that new work. It is not a harmless status probe.

Workers follow the injected preamble: ask the coordinator with native `ask`, then end
the turn until its correlated reply arrives; report a genuine blocker with escalation;
finish once with `worker_done`, the active Task/Dispatch and an honest succeeded/failed
outcome. Follow a failed send's printed recovery, not a fresh message identity. The
coordinator answers through native reply to the exact message ID when authorized, not
through a local prompt the worker cannot receive. Mail is from the actual agent, never
a forged owner decision.

A native wake carrying a complete message is acted on directly. If it explicitly names
a `check` command for the recipient's own mailbox, that recipient runs it once and
handles the result. Do not consume another actor's mail, run scripted mailbox consumers,
repeated checks, sleep loops, external watchers, cron bridges, heartbeat emulation or
background supervisors. When waiting on native work or input, end the turn. Run/status
files are records, not schedulers; missing native continuation blocks unattended claims.

## Exact-owner deadlines

Only native result/question/escalation wakes and native one-shot Automations provide
continuation. Before yielding, the coordinator verifies an expected native continuation
or saves one bounded deadline to its **exact existing owner chat** and retains the
receipt. Use the installed automations guide and trigger options: the inspected interface
supports Bot waits with `--once`, `--by` and an explicit `--runs-in chat:<OWNER_CHAT>`.
Those options are not a complete command or authority to invent a trigger. Resolve the
actual supported reminder/event form and owner Bot/chat before saving it.

`<OWNER_CHAT>` is the verified coordinator chat ID, supplied privately. Do not rely on a
Bot's default Chat, a new conversation, implicit creator-chat fallback or session reuse.
Verify the saved exact recipient and deadline: an explicit closed-chat failure is safer
than a silent reroute to another owner. Record Automation ID, current revision, Run/task/
attempt, original absolute UTC cutoff, exact event filter when used, and a bounded prompt
that reconciles only that scope. A deadline wake does not prove an event filter matched.
Unknown creation outcome requires reconciliation of the existing operation, not another
timer. Never overwrite an unrelated automation.

Apply [original clocks](state-and-recovery.md#native-continuation-and-original-clocks):
check actual UTC against persisted absolute bounds immediately before every affected
dispatch, integration and gate completion. Refuse new affected work after the earliest
cutoff. A busy coordinator can receive the deadline late; scheduling is delayed
reconciliation, not a hard-time enforcement barrier or proof of process exit. Neither
late output nor recovery resets the original attempt/campaign clocks.

On each wake, check owner, current revision, pause/terminal state and deadlines before
acting. Archive late results under their old bindings; ignore superseded wakes for
execution. Remove only obsolete owned timers at completion, cancellation, pause or
needs-user state and preserve the removal/uncertainty receipt. Operator pause never
self-resumes. No terminal-state idle cycles or perpetual deadline renewal.

Autonomous-supervision claims need observed native event delivery and exact-chat deadline
handling with correlated duty/cleanup receipts in the actual environment, without an
operator nudge between those steps. Saving a schedule, seeing a counter or receiving one
worker report proves only that observed part. No cross-process-death or reboot-liveness
promise follows. Missing proof stays unqualified; do not restore the legacy watcher or
terminal-controller mechanisms as a fallback.

## Recovery and source-preserving release

Use installed recovery guidance and [guarded settlement](state-and-recovery.md#guarded-settlement-and-duplicate-prevention),
not silence-driven intervention. Unknown liveness, a startup timeout or an accepted
launch never proves exit or authorizes autonomous stop, abandon, retry or release.

- For authorized cancellation, request guarded stop of the exact owned Dispatch and
  respect identity, custody, permission and Keep open refusals. On `stop_unknown`, inspect
  the same worker/receipt and report unresolved physical state; replacement stays blocked.
- Intentional abandonment requires its own authority. Fencing settles an assignment, not
  the possibly live process; it cannot free a write surface for a second writer. An
  in-flight stop must settle first.
- Retry a failed/stopped attempt only after a diagnosed changed cause, reconciled custody
  and current admission. Use the same Task and newest eligible failed Dispatch/retry
  identity; placement is freshly verified, not inherited. Primary-model failure or
  permission refusal does not authorize bypass or silent provider/model switching.
- Honor the native failed-start breaker and the stricter charter attempt/fix limits.
  Never evade them by resetting coordination state, replacing a Run/Task or relabeling an
  attempt. User-directed reopening after a breaker belongs to the current coordinator,
  preserves the same Task/history and reconciles every retained predecessor first.
- Before resource disposal, preserve attributable source, dirty/untracked files, exact
  manifests and evidence outside disposable storage under [cleanup](runtime-review-and-integration.md#cleanup).
  Worker completion can trigger native automatic release; plan durable preservation
  before that report and retain the actual release receipt. Keep-open resources require
  explicit accounting. `release_pending` or `release_unknown` follows the receipt's
  recovery, never terminal-close substitution. Unknown release prevents reuse.

No broad kill, reset/clean, runtime-database edit, permission weakening, unrequested
service restart or source deletion is recovery. A task may be settled while resources
remain deliberately retained; report both facts and the next authorized action.

## Qualification and staged loading

Inspect four permission scopes independently: Bot defaults, existing chats,
engine-specific launch override and existing workers. A setting does not retroactively
change another scope; one approved action is not Full access. Creation or permission
changes reserved to the owner cannot be impersonated. Disclose instructed versus
enforced read-only behavior; operational tool restrictions are not an OS sandbox.

Runtime qualification requires actual same-environment loading, primary and any used
auxiliary purpose/model evidence, native tool/result/wake behavior, gate transitions,
stop/release and source-retention receipts. Reuse valid scoped evidence rather than
repeating paid greetings. Unsupported or unsafe fault injection stays UNTESTED with the
exact limitation; synthetic tabletops are not runtime tests. OMP transport and the scoped
roborev-to-OMP review path do not qualify Hermes/Codex or every OMP capability.

The planned [OMP](engines/omp.md), [Hermes](engines/hermes.md) and
[Codex](engines/codex.md) startup sheets own supported engine loading and its evidence
checklist. All three, plus [validation tabletops](validation-tabletop.md), are **PENDING**
future targets at this slice. Final cross-document review must resolve links and reconcile
native/gate/model fields at exact current hashes; file existence is not independent
acceptance. `<ORCA>` and `<OWNER_CHAT>` are the only placeholders in this reference.

The [obligation ledger](obligation-ledger.md#reference-obligations) preserves the
[legacy operational mechanics](../../acd/references/hermes-orca-omp.md) and
[legacy wakeup contract](../../acd/references/coordinator-heartbeat.md) as migration
sources, not executable recipes. Its historical provider filename/readiness wording
awaits separately owned amendment and does not override `code-review.md` or scoped
readiness. Existing SOULs still load `.agents/skills/fleet-campaign/SKILL.md`; staging
loads or installs nothing. Any later cutover needs coordinated loading paths, supported
engine loaders, rollback and observed host-loading evidence. No standalone distribution,
installation, runtime acceptance or successor authorization follows from this document.
