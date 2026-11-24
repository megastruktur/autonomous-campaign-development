# Obligation ledger

## Status and authority

This is a migration inventory, not an execution guide or an acceptance verdict. The
candidate is staged, uninstalled, and separate from unchanged `skills/acd/`. Reading a
legacy source link does not authorize its commands. In particular, legacy watcher,
heartbeat, terminal-injection, fresh-session START and review-fallback instructions
are historical and non-operative for this candidate.

Technical authority: [S1 specification](../../../fleet/planning/doc-cutover/SPEC.md)
and [R2 candidate](../../../fleet/planning/acd-portability/CANDIDATE.md). Their historical
planning-only limits do not override an actual later owner mandate; the current
[execution charter](../../../fleet/execution/fullauto/CHARTER.md) authorizes this staged
document work, not installation. A document or native analysis Task completing does
not satisfy product acceptance or authorize successors. Acceptance remains a separate,
blocked, never-dispatched gate completed only by the coordinator with required evidence.

Owner-directed exceptions: [Amendment 1](../../../fleet/execution/fullauto/AMENDMENT_01_ROBOREV.md)
selects **roborev as the current substantive code-review provider**; OCR is superseded
history, not a ready provider. The independently reviewed A01 destination decision is
`references/code-review.md` (D05), with no alias or extra candidate file. Legacy source
identities, including R03's `skills/acd/references/ocr-review.md`, remain unchanged.
Frozen R2/S1 and their historical reviews do not approve roborev or these amended bytes.
This is a new bounded owner-amendment delta, not a retry or reset of the accepted ledger.

Existing independently reviewed host/container qualification establishes a scoped
roborev-to-fresh-OMP native ACP route. Preserve its exact private applicability receipt;
do not repeat bootstrap probes or promote it to full engine, auxiliary, API, runtime or
product qualification. Operational read/grep/glob restrictions are not OS confinement.
The [provider contract](code-review.md) owns qualification and every candidate review:
new neutral context, immutable no-hooks snapshot, exact source/base/tip/scenario and
source/test/dependency inventory, packet/diff/config/tool-policy hashes, before/after
source and hook guards, raw schema-3 findings, sanitized provider/tool completion and
external file-to-tool-ID-to-line-range-to-content/hash coverage reconciliation. Roborev
has no native coverage certificate. `rc=0` or `end_turn` alone is never PASS.

Complete nonzero acceptance coverage and explicit schema/severity mapping remain
mandatory: critical/high/medium block, low/style alone does not. Missing, malformed,
partial, failed, skipped, truncated, unknown or zero-required-coverage evidence is
INCONCLUSIVE; source/config drift invalidates the candidate. Preserve raw findings and
traces. Readiness does not accept a real candidate; independent API and actual runtime
integration/smoke remain distinct, with no routine second semantic code review. No
inferred compatibility, improvised adapter, automatic install or silent provider swap.

[Amendment 2](../../../fleet/execution/fullauto/AMENDMENT_02_OVERNIGHT.md) removes this
campaign's total cutoff and supersedes older fixed-cutoff, two-paid-worker and artificial
serial prescriptions, not guarantees. `campaign_cutoff_utc: null` is usable only with
`absent_by_authority` and the exact mandate binding; unknown is not unlimited authority.
Other campaigns use their own actual mandate. Original per-attempt clocks survive fixes,
retries, restarts and churn: attempt at most 15 minutes, checkpoint at 10, review at most
10, at most two unproductive attempts, one defect-fix round per slice and two integration
fix rounds. Before dispatch, integration or acceptance, check real UTC against all
applicable finite deadlines; stop affected source edits at attempt expiry. No automatic
kill/restart, sliding extension or operator-pause self-resume. Inherited low/500000-token
slice and medium/2000000-token final constraints require supported observation or explicit
bounded reconciliation before admission, not invented flags or silently dropped limits.

At most three paid working agents, including authors, reviewers and remediation; one
source writer per worktree. An independent reviewer may inspect only a frozen previous
file while the writer changes another independent file. One document (or code module
plus tests) per source assignment; administrative/review packets may group at most two
related small files, with separate exact-hash verdicts. Accepted references may remove
artificial ordering, never genuine prerequisites. Preserve native original-to-replacement
Task mapping; superseded nodes and receipts never become PASS. Coordinator-only blocked,
never-dispatched acceptance gates remain distinct from successful worker reports.

The ledger records migration obligations; their owning destinations below must implement
them before final candidate acceptance. RETAIN is semantic preservation, not permission
to copy a persona, stale command or obsolete mechanism. Source bytes and consulted-source
hashes belong in the private slice receipt, not in public runtime bindings.

## Reading the ledger

Each `OBL-` tag is permanent: do not renumber or reuse it. A source key resolves to one
exact repository file in the source inventory; a section or field following that key
narrows its scope. A destination key resolves to one candidate file below.
`A section 1 -> D03` names both an explicit source and an explicit destination without
repeating path prefixes in every row. Multiple rows for a source separate preserved
invariants from replaced mechanisms. New suffixed rows split mixed obligations without
renumbering or erasing original tags. Multiple destinations identify consumers; the
first named destination owns the rule and the others link or encode it.

| Disposition | Meaning |
|---|---|
| RETAIN | Preserve the named guarantee and its evidence requirements. |
| REPLACE | Remove the old operative mechanism; implement the named R2 substitute or explicit owner amendment without weakening its safety purpose. |
| DEFER | Do not claim the named capability until separate authority and qualification exist; safety constraints still apply. |
| EXCLUDE | Do not ship or execute the named legacy artifact in the candidate; keep the legacy file unchanged as historical evidence. |

Availability and acceptance are separate. The registry records the accepted-reference
packet at this amendment's freeze: exact per-file hashes and verdict pointers are in
the private slice receipt. Accepted means only that snapshot's document contract, not
current runtime or whole-candidate acceptance. Changed/affected bytes require a new
independent verdict; existence never clears PENDING. D01 is not yet authored, D09 is
present with independent review pending, and this D10 amendment awaits its own review.
The final cross-document gate must resolve every link and obligation at exact hashes.

## Candidate destination registry

Paths are relative to `skills/acd-orca/`. These are S1's 22 candidate slots with the
approved A01 D05 substitution, not a 23rd file. All nine templates exist. There is no
candidate scripts directory, OCR alias or replacement watcher.

| Key | Explicit destination | Status |
|---|---|---|
| D01 | [SKILL.md](../SKILL.md) | PENDING |
| D02 | [references/roles.md](roles.md) | Accepted snapshot, doc-02 |
| D03 | [references/planning-and-design.md](planning-and-design.md) | Accepted snapshot, doc-03 |
| D04 | [references/handoff.md](handoff.md) | Accepted snapshot, doc-04 |
| D05 | [references/code-review.md](code-review.md) | Approved A01 destination; accepted snapshot, doc-05 |
| D06 | [references/state-and-recovery.md](state-and-recovery.md) | Accepted snapshot, doc-06 |
| D07 | [references/runtime-review-and-integration.md](runtime-review-and-integration.md) | Accepted snapshot, doc-07 |
| D08 | [references/orca-runtime.md](orca-runtime.md) | Accepted snapshot, doc-08 |
| D09 | [references/validation-tabletop.md](validation-tabletop.md) | Present, doc-21; independent verdict PENDING at amendment freeze |
| D10 | [references/obligation-ledger.md](obligation-ledger.md) | Original doc-01 accepted; current A01/A02 delta independent verdict PENDING |
| D11 | [references/engines/omp.md](engines/omp.md) | Accepted snapshot, doc-09 |
| D12 | [references/engines/hermes.md](engines/hermes.md) | Accepted snapshot, doc-10 |
| D13 | [references/engines/codex.md](engines/codex.md) | Accepted snapshot, doc-11 |
| D14 | [templates/INTENT.md](../templates/INTENT.md) | Accepted snapshot, doc-12 |
| D15 | [templates/RESEARCH.md](../templates/RESEARCH.md) | Accepted snapshot, doc-13 |
| D16 | [templates/CRITIQUE.md](../templates/CRITIQUE.md) | Accepted snapshot, doc-14 |
| D17 | [templates/PLAN.md](../templates/PLAN.md) | Accepted snapshot, doc-15 |
| D18 | [templates/HANDOFF.md](../templates/HANDOFF.md) | Accepted snapshot, doc-16 |
| D19 | [templates/TASK.md](../templates/TASK.md) | Accepted snapshot, doc-17 |
| D20 | [templates/TODO.md](../templates/TODO.md) | Accepted snapshot, doc-18 |
| D21 | [templates/PLANNING_STATE.json](../templates/PLANNING_STATE.json) | Accepted snapshot, doc-19 |
| D22 | [templates/STATE.json](../templates/STATE.json) | Accepted snapshot, doc-20 |

## Legacy source inventory

This inventory covers all 23 legacy files: one SKILL entrypoint, nine references,
eleven templates (nine migrated and two excluded), and two scripts. The obligation
rows below cover all entrypoint sections and each listed file, including exclusions.

| Key | Explicit source | Obligation tags |
|---|---|---|
| A | [skills/acd/SKILL.md](../../acd/SKILL.md) | OBL-A-INTRO through OBL-A-VERIFY; OBL-A-00 through OBL-A-13 and their suffixed rows |
| R01 | [skills/acd/references/planning-and-design.md](../../acd/references/planning-and-design.md) | OBL-R01-KEEP, OBL-R01-CHANGE |
| R02 | [skills/acd/references/handoff-and-start.md](../../acd/references/handoff-and-start.md) | OBL-R02-KEEP, OBL-R02-CHANGE |
| R03 | [skills/acd/references/ocr-review.md](../../acd/references/ocr-review.md) | OBL-R03-KEEP, OBL-R03-CHANGE |
| R04 | [skills/acd/references/runtime-review-and-integration.md](../../acd/references/runtime-review-and-integration.md) | OBL-R04-KEEP, OBL-R04-CHANGE |
| R05 | [skills/acd/references/state-and-recovery.md](../../acd/references/state-and-recovery.md) | OBL-R05-KEEP, OBL-R05-CHANGE |
| R06 | [skills/acd/references/progress-watchdog.md](../../acd/references/progress-watchdog.md) | OBL-R06-KEEP, OBL-R06-EXCLUDE |
| R07 | [skills/acd/references/hermes-orca-omp.md](../../acd/references/hermes-orca-omp.md) | OBL-R07-KEEP, OBL-R07-CHANGE, OBL-R07-DEFER |
| R08 | [skills/acd/references/coordinator-heartbeat.md](../../acd/references/coordinator-heartbeat.md) | OBL-R08-KEEP, OBL-R08-CHANGE |
| R09 | [skills/acd/references/validation-tabletop.md](../../acd/references/validation-tabletop.md) | OBL-R09-KEEP, OBL-R09-CHANGE |
| T01 | [skills/acd/templates/INTENT.md](../../acd/templates/INTENT.md) | OBL-T01-KEEP, OBL-T01-CHANGE |
| T02 | [skills/acd/templates/RESEARCH.md](../../acd/templates/RESEARCH.md) | OBL-T02 |
| T03 | [skills/acd/templates/CRITIQUE.md](../../acd/templates/CRITIQUE.md) | OBL-T03-KEEP, OBL-T03-CHANGE |
| T04 | [skills/acd/templates/PLAN.md](../../acd/templates/PLAN.md) | OBL-T04-KEEP, OBL-T04-CHANGE |
| T05 | [skills/acd/templates/HANDOFF.md](../../acd/templates/HANDOFF.md) | OBL-T05-KEEP, OBL-T05-CHANGE |
| T06 | [skills/acd/templates/TASK.md](../../acd/templates/TASK.md) | OBL-T06-KEEP, OBL-T06-CHANGE |
| T07 | [skills/acd/templates/TODO.md](../../acd/templates/TODO.md) | OBL-T07-KEEP, OBL-T07-CHANGE |
| T08 | [skills/acd/templates/PLANNING_STATE.json](../../acd/templates/PLANNING_STATE.json) | OBL-T08 |
| T09 | [skills/acd/templates/STATE.json](../../acd/templates/STATE.json) | OBL-T09-KEEP, OBL-T09-CHANGE |
| T10 | [skills/acd/templates/WATCH.json](../../acd/templates/WATCH.json) | OBL-T10 |
| T11 | [skills/acd/templates/bounded_watcher.sh](../../acd/templates/bounded_watcher.sh) | OBL-T11 |
| X01 | [skills/acd/scripts/campaign_watch.py](../../acd/scripts/campaign_watch.py) | OBL-X01 |
| X02 | [skills/acd/scripts/omp_events.py](../../acd/scripts/omp_events.py) | OBL-X02 |

## Entrypoint section obligations

Section numbers refer to the legacy entrypoint, not to candidate section numbering.
The title/introduction, applicability, roles, Procedure container, every numbered
procedure section, Pitfalls and Verification are explicitly inventoried here.

| Stable tag | Explicit source section | Disposition | Destination | Guarantee or replacement |
|---|---|---|---|---|
| OBL-A-INTRO | A frontmatter and Autonomous Campaign Development introduction | REPLACE | D01 | Short engine-neutral Orca entrypoint with flat scalar frontmatter; link owning references instead of carrying Hermes-specific runtime policy. Preserve evidence-led delivery and role separation. |
| OBL-A-USE | A When to Use | RETAIN | D01 | Multi-task campaigns with contracts/dependencies and independent review; no artificial DAG for a trivial fix; repository instructions, hooks, permissions and actual mandate bind. |
| OBL-A-ROLES | A Roles | RETAIN | D02 | Coordinator never implements or resolves source conflicts; one bounded implementer owns source; runtime execution does not substitute for independent review; link existing role definitions. |
| OBL-A-PROCEDURE | A Procedure | REPLACE | D01 | Preserve ordered planning and acceptance chain while routing actual authority, native mechanics and engine loading to separate owners; no copied CLI manual. |
| OBL-A-00 | A section 0 Code-review engine gate; Amendment 1 | REPLACE | D05 | Captain-selected roborev replaces historical OCR selection, commands/configuration and candidate destination; accepted scoped readiness is not per-candidate acceptance. Apply the qualified interface, not translated OCR flags or automatic installation/fallback. Markdown review does not require code-provider qualification. |
| OBL-A-00-KEEP | A section 0 Code-review engine gate | RETAIN | D05 | Independently establish actual installed provider/model/tool/secret-access evidence, exact candidate coverage, protected credentials and read-only limits before relying on review. Qualification is purpose/environment-specific; unsupported or unknown capability blocks its dependent path. |
| OBL-A-01 | A section 1 Intent and mandatory repository discovery | RETAIN | D03, D14 | Record original intent, bounded read-only instructions/interfaces/manifests/lockfiles/test discovery, installed and stdlib reuse, dependency/license/footprint policies and whole/partial capability slices before a DAG. |
| OBL-A-02 | A section 2 Web research and architecture | RETAIN | D03, D15 | Actually retrieve current primary sources; search existing/stdlib, whole-feature, then partial libraries; verify registry and upstream license, adoption, maintenance/deprecation, compatibility, security and footprint; justify custom work and avoid micro-package bloat. Surface whole-coverage simplification, not padded tasks. Security/UX and shared contracts trace to intent; failed retrieval is a blocker, never invented research. |
| OBL-A-03 | A section 3 Independent critique and revision loop | RETAIN | D03, D16 | Original intent, architecture/research, Security, UX and readiness all receive independent critique; critic owns blocker closure; CONVERGED must bind current inputs before DAG creation; substantive intent/design changes reopen affected planning. |
| OBL-A-03R | A section 3 blanket fresh full critique on every revision | REPLACE | D03, D16 | Critic-owned changed/affected-scope recheck, including defect siblings/regressions, with explicit current-candidate attestation for reused unaffected evidence; never author self-closure or stale-hash convergence. Iterations remain bounded by actual mandate. |
| OBL-A-04 | A section 4 DAG and task decomposition | RETAIN | D03, D17, D19 | Durable English-slug artifacts after convergence; every task has goal, path allowlist, non-goals, dependencies, shared contracts, observable acceptance and verified runtime scenarios. Resource exclusions include lockfiles, schemas, migrations, outputs, ports, fixtures, databases and effects. Pin dependencies and serialize manifest/lockfile ownership; no ad-hoc installs or fixed-wave barriers. |
| OBL-A-05 | A section 5 Model questionnaire | REPLACE | D04, D18 | Actual mandate replaces routine questionnaire; retain requested, resolved and observed model identities per purpose, default resolution, restart reproducibility and mismatch reconciliation. Optional model choices create no automatic fallback right; no vendor ID embedded in portable policy. |
| OBL-A-06 | A section 6 One approval gate WHAT | REPLACE | D04, D17, D18 | Record actual owner mandate, scope, dependency decisions, delivery rights and consequential choices; do not manufacture routine approvals or infer execution authority from a plan. Push/publication/deployment and destructive actions require their actual grants. |
| OBL-A-07 | A section 7 HANDOFF and fresh-session START | REPLACE | D04, D18 | Mandate-bound Logis-to-existing-project-Magos handoff, unique owner identity, frozen input hashes, named repository/base and capability checks; drift blocks mutation until reconciled, never quiet re-hash. Fresh-session START ceremony is not operative. |
| OBL-A-07W | A section 7 watcher or heartbeat setup | REPLACE | D08, D06 | Native result wakes and exact-owner one-shot deadline reconciliation only; verified recipient and receipt, no terminal controller or script scheduler. Unverified wakes do not support autonomous claims. |
| OBL-A-08 | A section 8 Topology | RETAIN | D07 | Named target branch and full base SHA; Orca-managed campaign/child lineage, branch bases rather than raw SHA/HEAD, returned branch/HEAD verification before work. Detached or ambiguous target requires reconciliation; no assumed main/master. |
| OBL-A-09 | A section 9 Per-task loop | RETAIN | D07, D19, D20 | Develop, real-runtime test, independent review, authorized integration/conflict handling, actual integrated-tree smoke, preservation and cleanup in order. Exact source/build/scenario binding; fixed source after review invalidates verdict; FAIL routes to executor then retest/review, never coordinator edits. |
| OBL-A-09G | A section 9 successor release plus R2 Native execution and review contract | REPLACE | D07, D19, D22 | Separate analysis delivery from product acceptance with a blocked, never-dispatched native acceptance Task; only coordinator completion with bound review/integration/smoke evidence releases successors. Worker success alone never does. |
| OBL-A-10 | A section 10 Concurrency | RETAIN | D07, D17 | Maximum three active coders including fixes/remediation, subject to stricter mandate caps; one writer per worktree, reviewed candidate frozen against mutation, explicit exclusions, serialized integration and verified cleanup before resource reuse. |
| OBL-A-10R | A section 10 concurrency mechanism; Amendment 2 | REPLACE | D07, D17, D22 | Current maximum three paid working agents includes reviewers and remediation; one source writer per worktree. Independent next-file authoring may overlap only frozen previous-file review; preserve genuine prerequisites and separate per-file verdicts, not artificial serial barriers. |
| OBL-A-11 | A section 11 State and monitoring | RETAIN | D06, D22 | Sole-writer durable state, TODO projection, append-only events and evidence; distinct observation/assistant/tool/semantic-progress facts; unknown is not healthy and artifact change is not acceptance. |
| OBL-A-11R | A section 11 cadence, observer, TUI-only visibility | REPLACE | D08, D06 | Native receipt reconciliation and discoverable worker session/output replace ten-minute polling, optional observer and terminal-only dispatch. Bind actual native identity; unknown launch blocks duplication. No watcher building during execution. |
| OBL-A-12 | A section 12 Remediation and non-convergence | RETAIN | D06 | Diagnose correlated evidence; at most one scoped steer per checkpoint; original attempt clock survives restarts/churn; predeclared bounded long phases only; two unproductive attempts bar blind third retry; useful FAIL findings differ from empty attempts. Preserve dirty work; operator pause never self-resumes. |
| OBL-A-12R | A section 12 hard-expiry stop/restart, fallback and unbounded productive loops; Amendment 2 | REPLACE | D06, D22 | Persist finite attempt/review deadlines and check real UTC before dispatch/integration/acceptance. Total cutoff is nullable only with explicit disposition and authority: absent_by_authority differs from unknown. Expiry stops affected source edits/new work and triggers reconciliation, not automatic kill/restart; stop_unknown bars replacement. Diagnosed changed-cause retry requires authority and native breaker compliance without resetting original clocks or silently switching provider. |
| OBL-A-13 | A section 13 End of campaign | RETAIN | D07, D20 | All required scenarios, exact-tip acceptance/seams/runtime and independent review; moved target requires revalidation; named refs checked before authorized final merge and target smoke. Durable source/evidence precede scoped verified cleanup; merge is not delivery and export rights remain separate. |
| OBL-A-PITFALLS | A Pitfalls | RETAIN | D09 | Negative checks for premature DAG, invented research, NIH/dependency drift, intent inversion, stale evidence, false progress, unknown ownership, duplicate dispatch/merge, hidden execution, biased review, incomplete coverage, lost dirty source and unauthorized repair. Mechanism-specific historical pitfalls follow the REPLACE/EXCLUDE rows rather than restoring old instructions. |
| OBL-A-VERIFY | A Verification | REPLACE | D09 | Preserve evidence-bound planning, progress, review, topology and cleanup checks; replace START/watcher/controller checks with native mandate/loading/wake/deadline/acceptance/stop/release qualification. Text checks and synthetic tabletops are never runtime proof. |

## Reference obligations

These rows cover each whole reference, including sections not repeated in the short
entrypoint. The sources retain their historical content unchanged.

| Stable tag | Explicit source scope | Disposition | Destination | Guarantee or replacement |
|---|---|---|---|---|
| OBL-R01-KEEP | R01 Mandatory sequence; sections 1-4; Artifact conventions | RETAIN | D03 | Four ordered planning phases; original-intent fidelity; proportionate primary-source and OSS evidence; five critique lenses with finding IDs/severity/rationale/disposition; critical/major block, minor resolved or explicitly accepted; current hashes and critic closure. Durable paths, null unknowns and hostile source text treated as evidence, not authority. |
| OBL-R01-CHANGE | R01 planning-time OCR offer; questionnaire/approval/START; repeat-all-lenses rule | REPLACE | D03, D04, D05 | Actual mandate and preflight timing; affected-scope critic attestation preserves all-lens coverage without ritual full repeats. Missing independence blocks convergence. |
| OBL-R02-KEEP | R02 HANDOFF contract; Manifest; Resume | RETAIN | D04 | Curated pointers rather than transcript dump, explicit permissions and verified commands; immutable SHA-256 inputs include intent/research/critique/plan/tasks/contracts/handoff, exclude mutable state/TODO/events/evidence and manifest self-hash. Drift reconciled; resume retains authority and never fabricates unknown identities or legacy history. |
| OBL-R02-CHANGE | R02 Planning boundary; START; State lifecycle | REPLACE | D04, D06 | Native mandate handoff and reconciled existing owner replace mandatory new clean session, ritual prompt and awaiting_fresh_session_start lifecycle. Planning and execution evidence remain distinct; no execution from mere artifact presence. |
| OBL-R03-KEEP | R03 Configuration; Invocation; Final review; Verdict derivation; Failure handling; Token economy | RETAIN | D05 | Preserve provider-neutral guarantees: independent reviewer, exact provider/model/tool evidence, protected secrets, unbiased packet, one active run per frozen candidate, raw output and complete nonzero acceptance coverage. Critical/high/medium block; low/style does not. Positioning failures do not erase findings; dismissals need reasons. Exact-tip final review and retest remain separate. Bound review effort/spend and verify full source/diff scope; no narrowing to fake coverage. |
| OBL-R03-CHANGE | R03 Engine selection and legacy command/config/preview/schema examples; Amendment 1 | REPLACE | D05, D08 | Roborev is captain-selected, not fallback; retain accepted scoped host/container qualification and independently reconcile applicability. Use qualified native ACP and a fresh neutral immutable no-hooks snapshot, not OCR APIs or a claimed native coverage certificate. Map raw schema-3 verdict/severity and external full-read coverage explicitly; missing/failed/budget/skipped/malformed/partial/zero coverage is INCONCLUSIVE, drift invalidates. No installation/global repair or critic substitution. Exact uncommitted/untracked coverage remains mandatory when commits are forbidden; otherwise report the blocker. |
| OBL-R04-KEEP | R04 Runtime testing; Independent review; Git topology; Task squash integration; End; Cleanup | RETAIN | D07 | Production-path outcomes, actual rendered UI when relevant, declared external mocks only, real overlap/persistence for concurrency, failure reproduction and no unexplained flaky dismissal. Source/scenario revisions invalidate results. Read-only neutral review covers siblings/regressions; no temporary source edits. Squash receipt binds task tip, pre-integration tip, resulting commit/tree; ancestry alone is insufficient. Conflicts go to executor. Smoke precedes successor release. Rescue dirty/untracked source and archive recovery evidence outside disposable worktrees before deletion; verify owned processes/resources/release. |
| OBL-R04-CHANGE | R04 START prerequisites, session-review fallback and committed-clean-only handoff | REPLACE | D07, D04, D05 | Actual mandate and provider contract; native analysis/acceptance separation, source freeze as exact preserved bytes when commits forbidden. Integration/final merge only when authorized; absence of merge rights never weakens source retention or acceptance binding. |
| OBL-R05-KEEP | R05 Files/naming; Sole-writer; Schema; TODO; Crash windows; Resume; Remediation | RETAIN | D06 | Atomic durable shared-state revisions, event-before-mutation intent and result receipts, sanitized task-owned evidence, null unknowns; rebuild TODO from state. Reconcile ownership before takeover, source/ref truth before repeating launch/merge, and candidate identity before reusing review. Preserve attempts, resources and dirty source; no global kills, broad reset/clean or unauthorized service repair. |
| OBL-R05-CHANGE | R05 lifecycle migration, Ten-minute loop, hard expiry, fallback ladder | REPLACE | D06, D22 | Native state/receipts are live-work truth; project files are durable records, not a second scheduler. Honest legacy reconciliation without invented fields; absolute time admission checks, guarded settlement and stopped/released proof replace silence-driven recovery. Primary failure/permission denial blocks affected path; operator pause and late superseded replies cannot resume it. |
| OBL-R06-KEEP | R06 Activity; Event semantics; Distinct timestamps; Health; Checkpoints; Known constraints | RETAIN | D06, D11 | Transport, successful assistant, completed tool and semantic task progress stay distinct. Errors/aborts, missing outcome, metadata rows and abandoned branches do not become success; provider errors need session correlation. Bound checkpoints to task/attempt/session/candidate and actual completed criterion, reject replay/future/stale evidence; producer attestation is not independent truth. Unknown/backlog/stale observations cannot claim health; a pending question or in-deadline tool is not an exited worker. |
| OBL-R06-EXCLUDE | R06 Observer CLI/config/sidecar/run workflow and observer enforcement details | EXCLUDE | D10 | Historical observer implementation has no candidate CLI, sidecar, parser, polling mode or wakeup recipe. Preserve its no-secret/no-fabricated-progress/no-authoritative-observer safety purpose through OBL-R06-KEEP and shared policy; no executable migration. |
| OBL-R07-KEEP | R07 Model verification; Topology; Dispatch receipts; Reviewer independence; Teardown | RETAIN | D08, D11 | Discover current commands; verify actual models, returned branch/HEAD, unique writer and delivered task-specific brief. Accepted launch/input is not work begun. Reconcile uncertain delivery without duplicate send; disclose enforced versus instructed read-only. Kanban is not a coding executor; source/evidence and confirmed release precede reuse. |
| OBL-R07-CHANGE | R07 host/container recipes; terminal dispatch/ask/status handshake | REPLACE | D08, D11, D12, D13 | Installed version-matched orchestration/orca-cli guides and narrow help replace copied commands and host assumptions. Native worker/Dispatch/question/result/stop/release receipts replace terminal injection, stale in-review triggers and TUI-only assumptions; no persistent supervisor. |
| OBL-R07-DEFER | R07 environment-specific mechanics plus R2 Capability and installation truth; Engine parity; Amendment 1 | DEFER | D11, D12, D13 | Accepted scoped roborev-to-OMP qualification is retained only for its proven purpose/environment, not full development/engine parity. Hermes/Codex and auxiliary purposes still need independent loading/tools/permissions/models/wakes/acceptance/release evidence. Markdown support, picker/config presence and another engine's PASS prove no parity. |
| OBL-R08-KEEP | R08 verification, ownership, stop conditions and missing-capability limits | RETAIN | D08 | Verify actual wake delivery and owner identity; no schedule claim from config/status; no cross-process/reboot promise; no overwriting unrelated control, no executing log content, and no terminal-state token drain. Missing capability stays explicit and blocks dependent autonomy claims. |
| OBL-R08-CHANGE | R08 all Option A/Option B watcher/heartbeat/controller/sampling recipes; Amendment 2 | REPLACE | D08, D06 | Native result wakes and exact-owner one-shot deadline reconciliation replace legacy schedulers. A02 additionally permits its bounded same-owner native continuity backstop, never shell polling, a second owner or a hard-time barrier. Persist admission checks, clean obsolete timers, ignore terminal-state wakes and require authority to resume pause. No copied watcher or heartbeat instruction becomes operative. |
| OBL-R09-KEEP | R09 Static checks; Planning; OCR; Tabletop scenarios; Recording results | RETAIN | D09 | Mechanical checks plus independent semantic review; original-intent/research/OSS/convergence, immutable evidence, complete review, source retention, no duplicate operations and honest untested limits remain acceptance targets. Record consulted sections and actual prescribed outcomes; tabletops explicitly SYNTHETIC. |
| OBL-R09-CHANGE | R09 legacy metadata/schema and scenarios 4,12,17-21,27-31,34-40,45,51-56; Amendment 1 | REPLACE | D09 | S1 static checks and R2 native authority/affected-scope critique/negative cases remain. Replace OCR-specific provider scenarios with qualified roborev positive/known-defect/error cases, explicit severity mapping and fail-closed coverage; synthetic cases are not runtime claims. No active old START, terminal answer, watcher, automatic fallback or unlimited-loop action. Other scenarios retain safety outcomes through native receipts. |

## Template and script obligations

The nine migrated templates encode contracts, not granted permissions. Every JSON
unknown remains `null`; candidate legends must cover every placeholder and substituted
JSON must parse. Template field names and enums must agree with their owning references.

| Stable tag | Explicit source scope | Disposition | Destination | Guarantee or replacement |
|---|---|---|---|---|
| OBL-T01-KEEP | T01 entire intent/discovery record | RETAIN | D14 | Original outcome, constraints/non-goals, decisions, actual paths/symbols/policies/runtime discovery, acceptance, whole/partial reuse questions and no premature DAG. |
| OBL-T01-CHANGE | T01 coordinator identity and blanket phase restrictions | REPLACE | D14, D03 | Existing role ownership and actual mandate determine who authors or commissions bounded contributions; planning cannot grant implementation rights. |
| OBL-T02 | T02 entire research record | RETAIN | D15 | Actual accessed sources/limitations, registry/upstream OSS evaluation, evidence-backed choice, contracts, traceability, Security, UX and honest readiness/unknowns. |
| OBL-T03-KEEP | T03 ordered rounds, five lenses, inputs/findings/verdict | RETAIN | D16 | Exact hashes, independent critic identity, original request, finding severity/disposition, no unresolved blockers and no author self-PASS. Preserve prior rounds. |
| OBL-T03-CHANGE | T03 blanket fresh full round on every edit | REPLACE | D16, D03 | Changed/affected-scope review and critic attestation of reused unaffected evidence bound to current candidate; material design changes reopen proper phase. |
| OBL-T04-KEEP | T04 goal, convergence, traceability, DAG/contracts, runtime, bounds and artifacts | RETAIN | D17 | Named branch/base, verified scenarios, explicit resource/dependency owners, three-coder ceiling or stricter mandate cap, durable inventory and bounded original attempts. Retain requested/resolved/observed model, qualification, exact source/scenario, independent review/raw evidence and separate runtime/acceptance records. |
| OBL-T04-CHANGE | T04 questionnaire, ocr_or_session, approval/START and expiry semantics; Amendments 1 and 2 | REPLACE | D17 | Actual mandate/delivery rights and captain-selected roborev with scoped qualification applicability replace OCR selection/fallback. Separate provider from execution engine. Encode blocked coordinator-only acceptance, authorized nullable total cutoff and finite deadline admission; max three paid working agents, no ceremonial START or clock reset. |
| OBL-T05-KEEP | T05 goal/pointers, repository, model/evidence/permission records and companion manifest | RETAIN | D18 | Curated handoff, exact named base and immutable input hashes including standalone contracts; mutable state/evidence and manifest itself excluded from input self-hash. Unknown values null; actual command verification and blockers explicit. |
| OBL-T05-CHANGE | T05 fresh-session prompt/lifecycle, install offer/fallback, polling and watchdog | REPLACE | D18 | Mandate-bound Logis-to-existing-Magos handoff and private native bindings; native wake/deadline/acceptance/recovery evidence, no live IDs in portable template. Resume reconciles original scope rather than silently refreshing consent. |
| OBL-T06-KEEP | T06 goal/allowlist/non-goals/dependencies/contracts/traceability/acceptance/runtime/stages | RETAIN | D19 | One writer, no unapproved installs, observable production-path scenarios and out-of-scope findings; exact source/scenario evidence and explicit ready handoff. Worker never merges/pushes/deletes without authority. |
| OBL-T06-CHANGE | T06 completion dependency and committed-clean status handshake | REPLACE | D19 | Product successor depends on separate blocked acceptance gate, not analysis completion. Capture exact preserved candidate bytes when no commits allowed; native result, review/integration/smoke bindings and absolute attempt deadline replace in-review signaling. |
| OBL-T07-KEEP | T07 projection, per-task stages and final stages | RETAIN | D20 | Sole-writer state projection; check only observed completion; full runtime/review/integration/smoke/preservation/cleanup, moved-target and authorized final-delivery stages remain explicit. |
| OBL-T07-CHANGE | T07 start gates, reviewer fallback, unlimited loops and mandatory merge regardless of grant | REPLACE | D20 | Actual mandate/preflight and coordinator-completed acceptance gates; bounded diagnosed fix cycles, native wake/stop/release proof and delivery actions conditional on actual rights. No skipped stage disguised as checked completion. |
| OBL-T08 | T08 entire planning-state schema | RETAIN | D21 | Current phase, intent/research discovery flags and hashes, OSS completion evidence, independent critic and exact convergence input bindings. Unknowns null; current-candidate affected-scope attestation encoded consistently with D03/D16. |
| OBL-T09-KEEP | T09 owner/campaign/planning/models/tasks/evidence/merge/attempt/cleanup/final/pause records | RETAIN | D22 | Durable revisions, owner identity, named base, resource/dependency ownership, requested/resolved/actual models, provider binary/version/qualification, completion, coverage, raw findings and exact source/scenario/review history. Preserve integration receipts, original attempt clocks, cleanup proof and explicit pause. Unknowns remain null, never guessed. |
| OBL-T09-CHANGE | T09 lifecycle/start/approval/provider/stage/deadline fields; Amendments 1 and 2 | REPLACE | D22 | models.review_engine and tasks[].review.engine select roborev, independently of execution_engine; models.code_review replaces models.ocr, review.run_id/raw_output replace OCR-specific fields. Encode mandate/native lifecycle, scoped qualification applicability, fail-closed verdicts, private receipts, blocked never-dispatched coordinator acceptance and guarded settlement. Nullable campaign cutoff requires disposition/authority; finite original attempt/review clocks and max-three working ceiling remain. No operative ocr_or_session, START or poll cadence; schema/legend agree with owning references, never fabricated history. |
| OBL-T10 | T10 entire WATCH configuration | EXCLUDE | D10 | Historical non-operative legacy file only; no candidate WATCH.json, polling configuration or sidecar ownership. Legacy remains unchanged. |
| OBL-T11 | T11 entire bounded watcher shell template | EXCLUDE | D10 | Historical non-operative legacy file only; do not copy, source, spawn or adapt it for candidate execution. Native wakes replace its role; legacy remains unchanged. |
| OBL-X01 | X01 entire campaign_watch.py script | EXCLUDE | D10 | Historical non-operative observer CLI only; no candidate script/daemon/poll loop and no migration execution. Its safety semantics are retained via OBL-R06-KEEP, not its implementation. Legacy remains unchanged. |
| OBL-X02 | X02 entire omp_events.py script | EXCLUDE | D10 | Historical non-operative session adapter only; no candidate session-log consumer/parser. Native receipts replace this observation route; legacy remains unchanged. |

## Existing fleet policy and loading boundary

These are existing dependencies, not new candidate personas. D02 links them; it must
not copy their policy or reinterpret a display name as unique execution ownership.
Their historical OCR-first wording is superseded for this candidate by Amendment 1;
the files and installed loading paths remain untouched, not silently migrated.

| Stable tag | Explicit source | Disposition | Destination | Obligation |
|---|---|---|---|---|
| OBL-F-LOGIS | [fleet/bots/logis/SOUL.md](../../../fleet/bots/logis/SOUL.md) | RETAIN | D02 | Link unchanged synthesis ownership, original-intent preservation and critic-owned closure. |
| OBL-F-INTENT | [fleet/bots/logis-intent/SOUL.md](../../../fleet/bots/logis-intent/SOUL.md) | RETAIN | D02 | Link unchanged product contribution and non-self-approval boundary. |
| OBL-F-ARCHITECT | [fleet/bots/logis-architect/SOUL.md](../../../fleet/bots/logis-architect/SOUL.md) | RETAIN | D02 | Link unchanged technical evidence/reuse contribution and no planning-role implementation. |
| OBL-F-FERRUM | [fleet/bots/inquisitor-ferrum/SOUL.md](../../../fleet/bots/inquisitor-ferrum/SOUL.md) | RETAIN | D02 | Link independent scoped technical verdict and blocker closure; not substitute code provider. |
| OBL-F-CRITIC | [fleet/bots/inquisitor-intent/SOUL.md](../../../fleet/bots/inquisitor-intent/SOUL.md) | RETAIN | D02 | Link independent outcome critique and exact-candidate evidence; analysis is not acceptance. |
| OBL-F-MAGOS | [fleet/bots/magos-fleet/SOUL.md](../../../fleet/bots/magos-fleet/SOUL.md) | RETAIN | D02 | Link designated execution-owner chat, native supervision, no coordinator coding and preserved delivery evidence. |
| OBL-F-PROJECT | [fleet/templates/magos-project/SOUL.md](../../../fleet/templates/magos-project/SOUL.md) | RETAIN | D02 | Link generic project coordinator contract, with actual identities/mandate discovered privately. |
| OBL-F-COMMON | [fleet/skills/fleet-campaign/references/common-contract.md](../../../fleet/skills/fleet-campaign/references/common-contract.md) | RETAIN | D02, D01 | Link existing shared authority, English, independence, native supervision, steering, security and setup policy; do not duplicate it. |
| OBL-F-PROVIDER-CHANGE | Provider-specific OCR-first clauses in all linked fleet SOULs and common policy; Amendment 1 | REPLACE | D05, D04, D02 | Scoped captain-selected roborev overrides only historical provider/command/config prescriptions. Keep all unchanged fleet ownership, independence, safety and evidence guarantees; do not edit installed loading paths or treat old source text as current review authority. |
| OBL-M-LOAD | S1 Ownership/loading paragraphs; all seven linked SOUL inputs | DEFER | D04, D08, D10 | Later owner-controlled loading-path decision must coordinate these SOULs, their installed fleet-campaign entrypoint/common reference, each engine's supported loader and rollback/evidence. They still name `.agents/skills/fleet-campaign/SKILL.md`; staging acd-orca does not load it. No automatic repointing or standalone distributability claim. |
| OBL-M-ENGINE | R2 Capability and installation truth; Engine parity; Amendment 1 | DEFER | D11, D12, D13 | Purpose-specific primary/auxiliary and current-provider roborev use, plus each engine's loading/tools/permissions/wakes/release, require actual host evidence. OCR evidence is historical and does not qualify roborev. No inherited OMP PASS, installs, sign-in or global config repair implied. |
| OBL-M-PACKAGE | R2 Engine/provider/public distribution; Amendment 1 | DEFER | D04, D10 | Packaging, public sharing and broad crash/reboot recovery still need authority/qualification. Roborev selection and scoped readiness are established, not universal qualification; further provider changes need their own authority. No executable adapter absent a demonstrated native gap and implementation mandate. |
| OBL-M-STATIC | S1 Concrete validation recipe | REPLACE | D09 | Candidate-specific 22-file/flat-frontmatter/JSON/placeholder/link/anchor/hash/privacy checks and independent English/operative-policy review replace reliance on legacy wording tests. Legacy tests remain unchanged regression protection, not candidate proof. |
| OBL-M-PROVIDER | Amendment 1 Authority and precedence; Bounded qualification; approved A01 destination decision | REPLACE | D05, D10 | Approved D05 code-review.md, no alias, 22 candidate files/nine templates; OCR selection/commands/config/schema are superseded, not translated by inference. Retain accepted scoped roborev-to-OMP readiness with applicability evidence; proposal/qualification PASS never approves amended candidate bytes. |
| OBL-M-PROVIDER-KEEP | Amendment 1 Unchanged acceptance; R2 Native execution and review contract | RETAIN | D05, D07, D10 | Independent exact source/base/tip/scenario, raw findings/tool traces, complete nonzero coverage, critical/high/medium blocking and fail-closed errors remain mandatory per candidate. Provider readiness, document review, API evidence, actual runtime/integration/smoke and coordinator-only product acceptance prove different things. |
| OBL-M-BOUNDS | Amendment 2 Explicit captain mandate; Immediate acceleration; Unattended continuity; Morning deliverable and final gate | REPLACE | D04, D06, D07, D08, D17, D18, D19, D20, D21, D22 | Current campaign has no total cutoff, with null plus absent_by_authority and exact mandate binding, not unknown/unbounded attempts. Preserve finite original attempt/review clocks, spend/fix limits, max-three paid working ceiling, source custody and frozen-file review. Native replacement mapping retires obsolete Tasks as superseded, never PASS; retain final exact-manifest integration, actual artifact verification, durable source and honest captain handback. |

## Closure requirements

This ledger's author does not mark the amendment accepted. Its independent changed/affected
review must bind original S1 criteria, current ledger hash, original source identities,
R2 and both amendments. Preserve the accepted original ledger snapshot/verdict; neither
that verdict nor the A01 destination proposal approves these new bytes. Reuse unaffected
evidence only through explicit reviewer attestation at the current candidate hash, and
review affected provider rows, bound semantics, registry links and regression siblings.
The reviewer reads frozen bytes, never an actively changing sibling source.

At final cross-document acceptance, the coordinator reconciles every stable tag with its
implemented destination and current independent verdict, verifies all 22 files and nine
templates, resolves the pending entrypoint and all links/anchors, and checks shared
fields/enums/legends and A01/A02 precedence. Accepted older references/templates retain
their exact historical verdicts; superseded fixed-cutoff/two-worker/provider wording
cannot become operative through a link. Record remaining DEFER and EXCLUDE boundaries:
EXCLUDE never deletes legacy evidence; DEFER never postpones a safety guarantee.

Native analysis completion or this receipt's success is not product PASS. Only the
coordinator completes separate blocked, never-dispatched acceptance gates with required
exact-candidate review, API and integration/smoke evidence. Preserve source/evidence
before release; distinguish documentation acceptance, engine/runtime qualification,
installed loading and final owner delivery. This amendment does not authorize installation,
commits, Groups, global changes or provider bootstrap.
