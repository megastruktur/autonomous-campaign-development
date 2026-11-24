# Mandate-bound handoff

A handoff transfers a bounded plan and its evidence to the designated project Magos;
it does not create authority. Follow [roles and ownership](roles.md) and the existing
[common fleet contract](../../../fleet/skills/fleet-campaign/references/common-contract.md).
This reference owns the authority, frozen-input, model and admission boundary, not a
second persona or a copied native CLI manual.

## Authority and precedence

Use the actual owner's development mandate and recorded steering revisions. Logis
hands the converged plan to the existing designated execution-owner chat; create or
replace that owner only when the mandate expressly requires it and native ownership
has been reconciled. A plan, charter written by an agent, peer recommendation, imported
skill, successful analysis Task or handoff document cannot grant additional rights.
Higher-priority instructions, repository policy and enforced permissions still bind.

The historical questionnaire, WHAT approval ceremony, exact START prompt and mandatory
fresh-session transition are non-operative here. Do not ask for those rituals when the
actual mandate already settles the decision. Conversely, planning-only authority is
not development authority: stop before execution if the owner has not authorized it.
A fresh session required by an actual mandate still binds; removing a ceremony does
not remove explicit owner constraints. Record planning provenance and execution
identity separately, without claiming an enforced clean context from a display name.

The current [execution charter](../../../fleet/execution/fullauto/CHARTER.md) supersedes
historical planning-only limits for its named campaign, not for other projects or
future work. Its [owner amendment](../../../fleet/execution/fullauto/AMENDMENT_01_ROBOREV.md)
selects roborev as the initial code-review provider for this candidate. Bind readiness
to the exact accepted qualification receipt and its execution-host scope, not a universal
qualified/unqualified label in this portable document. OCR-first instructions in unchanged
linked SOULs, common policy and
legacy sources are superseded only for that provider choice and its obsolete mechanics;
their independence, binding, completeness, severity and evidence guarantees remain.
Do not execute old provider setup, tests or fallback recipes. Frozen historical reviews
did not approve roborev or future candidate bytes. The approved destination is
[code review](code-review.md), with no alias or second provider reference.

Escalate missing authority or consequential choices not already settled: changed scope
or contracts, dependency/license decisions, destructive effects, new host prerequisites,
missing capability or access, exhausted bounds, or a provider/model change outside the
granted selection policy. Do not invent routine intermediate human gates or silently
turn a recommendation into consent. Record the owner's answer as a revision, preserving
the prior mandate and the affected evidence.

## Handoff packet

The durable HANDOFF is a curated pointer set, not a transcript dump. Use repository-relative
artifact links. Keep actual host paths, owner/chat/Run/Task/Dispatch identities, exact
model routes and native receipts in private project bindings, never portable skill text
or exported templates. Unknown values remain `null`, with their consequence stated;
`null` does not mean none, healthy, authorized or verified.

The packet must identify:

| Record | Required content |
|---|---|
| Mandate | Original owner request and provenance, charter/revision identities and hashes, intended outcome, scope allowlist, non-goals, consequential decisions and explicit grants/exclusions. |
| Design | INTENT, RESEARCH and complete CRITIQUE history; current-hash convergence, critic-owned blocker closure and current affected-scope attestations under [planning and design](planning-and-design.md). |
| Work | PLAN, every task and standalone shared contract, acceptance/runtime scenarios, dependencies, resource exclusions and blocked coordinator-owned acceptance gates. |
| Repository | Verified repository identity and private location, original named target branch, full starting SHA, intended campaign/task lineage, existing worktree custody and dirty/untracked baseline. Never assume main/master or infer a named target from detached HEAD. |
| Delivery | Separate rights for implementation, tests, review, integration/merge strategy, commits, cleanup, push, publication, deployment and installation; preserve explicit denials. No generic development grant implies all delivery operations. |
| Models | Requested, resolved and actual model per purpose, resolution and startup evidence, selection authority, fallback absence or bounded policy, provider and execution engine as distinct facts. |
| Capabilities | Execution-host instruction loading, versions, four permission scopes, discoverable session/output, verified runtime commands with exact verification receipts, provider qualification and known blockers. |
| Bounds | Original attempt start, checkpoint and absolute attempt deadline; fixed campaign cutoff; review/long-phase limits, effort/token constraints, concurrency and resource caps, fix and unproductive-attempt limits. |
| Continuation | Native result-wake and exact-owner one-shot deadline evidence, outstanding questions/operations, pause state and recovery pointers; no external scheduler. |
| Durability | Immutable input manifest and its private state binding, mutable STATE/TODO/EVENTS/evidence pointers, source snapshot/archive custody and unresolved findings. |

Record grants independently from capability: an available command is not permission to
use it. For the current no-commit mandate, preserve attributable diffs, untracked source
and checksummed immutable snapshots; do not manufacture commits to satisfy a legacy
review recipe. Lack of merge permission changes the permitted integration/delivery
operation, not the obligation to bind review and actual smoke to the resulting source.
Source and evidence must survive before any authorized worktree disposal or release.

Carry the actual mandate's numerical limits without resetting or rounding them away.
The current charter has attempts at most 15 minutes, a 10-minute checkpoint, at most
two unproductive attempts, one defect-fix round per slice and two feature-integration
fix rounds. It permits at most two paid workers concurrently and one writer or independent
review at a time per worktree; review freezes the source. Review is at most 10 minutes
unless a prior bounded extension is authorized, with inherited low effort/500000-token
slice and medium effort/2000000-token final constraints. These are constraints, not
asserted roborev flags: unsupported controls require explicit bounded reconciliation
before admission. Persist the actual campaign cutoff privately; a handoff or fix never
restarts its clock. General defaults in other references cannot weaken a stricter mandate.

## Model and review identity

For each implementation, planning/critique, code-review, optional final-review and
auxiliary purpose actually used, retain three distinct facts:

1. **Requested:** the owner's exact route or authorized `default`, and the decision
   permitting its use. An optional role or fallback expressly disabled is recorded as
   absent; an unknown choice is `null`, not permission to choose arbitrarily.
2. **Resolved:** the exact available model selected from that request on the execution
   host, with runtime/profile and resolution evidence. `default` means that relevant
   runtime's actual configured default, never an orchestrator-chosen substitute. Pin
   the resolved value for reproducibility across restarts unless the owner changes it.
3. **Actual:** the model observed at startup and in the purpose-specific execution,
   with correlated native/provider evidence. Picker/configuration presence or a launch
   request proves neither actual use nor successful tool calls. Record missing evidence
   as `null` and block only the claims and paths that depend on it.

Do not embed a vendor model into portable policy. A startup mismatch stops the affected
path for reconciliation before its output can satisfy acceptance. Primary-model failure
or permission refusal is not authority to switch routes, retry blindly or broaden
permissions. A recorded optional fallback is not an automatic recovery instruction;
any use needs the granted policy, diagnosed cause and original attempt bounds. A
same-model session repair still requires reconciled ownership and no duplicate writer.
Without authorized alternative selection, ask the owner rather than silently substituting.

Keep code-review provider and execution engine separate. For this candidate,
`models.review_engine` and `tasks[].review.engine` select `roborev`; neither field means
OMP. `models.code_review` records binary/version, independently resolved `execution_engine`,
requested/resolved/actual model route and qualification evidence/status. Record each
review's `run_id` and `raw_output`, completion, coverage, findings, verdict and exact
source/base/tip/scenario binding. Do not retain operative OCR-specific field aliases.
PLAN, HANDOFF, TASK, TODO and state templates must agree on these meanings.

Resolve OMP or another supported review execution engine from the exact actual qualification
receipt, including its host/container, binary, model and interface limits. Accepted scoped
readiness may be reused only within those evidenced boundaries; do not repeat paid bootstrap
greetings or invent extra qualification gates. Unknown or changed environments cannot inherit
that result. Shared executable or model never permits reuse of the implementer's reasoning
context: review runs in a fresh neutral session under the
[independence contract](roles.md#critic-independence). Preserve qualification evidence for
installed identity/interface, actual approved model/tool use, exact uncommitted/untracked
scope, bounded synthetic clean and known-defect/error-or-incomplete cases, raw findings,
explicit schema/severity mapping and operational versus OS-enforced read-only limits.
No inferred adapter support or unauthorized install, global configuration, hook, permission
or service change; any tool-internal daemon needs explicit ownership/lifetime authority.

Each candidate review uses a new private neutral session/config and an immutable no-hooks
review-only snapshot outside the live checkout. Preserve exact source, tests and relevant
dependencies with provenance; no commits are implied. Bind reviewer/model/host/binaries,
base/tip or explicit unborn snapshot, inventory and all hashes, neutral packet/diff/config/
tool-policy hashes, before/after source and hook guards, actual invocation, working directory,
timeout and exit. Keep raw schema3 JSON separate from rendered output and preserve sanitized
provider stop reasons/errors and tool results; never export credentials or hidden reasoning.

Require external complete file-to-tool-ID-to-line-range-to-returned-content/hash full-read
coverage reconciliation. Roborev has no native coverage certificate. Process exit zero or
ACP `end_turn` alone cannot prove success: a provider error may still end the turn. The
receipt must demonstrate provider and tool completion, complete required reads and preserved
raw findings against the frozen candidate. This is independently reconciled evidence, not
a claim that an automated acceptance gate exists.

Qualification success opens only its dependent readiness gate; each real candidate
still needs its own complete independent review. Missing, partial, failed, skipped,
malformed, budget-failed, unknown, truncated, zero-required-coverage or unmappable results
are INCONCLUSIVE regardless of process exit. Source or config drift is INVALIDATED.
A valid fail verdict or critical/high/medium acceptance or security findings means FAIL;
low alone does not block. PASS requires a valid pass verdict, complete provenance,
provider/tool success, full-read reconciliation, preservation and no blocking findings.
Document critique does not require code-tool qualification and does not qualify the
code provider. Real candidate, API, integration and runtime gates remain separate.
Detailed provider mechanics belong to the code-review reference.

## Frozen input manifest

Freeze the exact input bytes after the required planning convergence and within the
actual mandate. The manifest enumerates repository-relative paths and SHA-256 hashes
for INTENT, RESEARCH, complete CRITIQUE history, PLAN, every task file, every standalone
shared-contract file and HANDOFF. Preserve immutable authority revisions or snapshots
and their hashes as part of the handoff's authority binding; do not let a mutable
charter silently replace the mandate that was used.

Exclude mutable STATE, planning phase state, TODO, EVENTS and execution evidence from
the frozen planning payload. Exclude the manifest itself: no recursive self-hash.
Hash the finished manifest separately and record that digest in private campaign state
and the execution-admission receipt, not back inside the HANDOFF it hashes. Store
subsequent actual execution identities, model observations and operational updates in
those mutable receipts; do not edit a frozen HANDOFF to add them.

Each frozen manifest version is immutable. Preserve its bytes and referenced source
outside disposable workspaces. A new authorized revision produces a separately identified
manifest and current independent affected-scope evidence; it never overwrites the old
hashes, authority or verdict history. Mutable evidence may grow without invalidating the
planning freeze, but each review/runtime result still binds its own exact candidate,
build where applicable, scenario version and evidence identity. Changed source cannot
inherit acceptance from an unchanged planning manifest.

## Execution admission

The designated project Magos performs admission before the first affected mutation;
worker launch success alone is not admission. Use installed version-matched discovery
through [Orca runtime](orca-runtime.md), not copied historical command recipes.

1. Confirm the actual mandate authorizes this phase, repository, host, scope and delivery
   actions. Record its revision independently from when execution is admitted. Planning
   convergence and file presence establish neither permission nor implementation readiness.
2. Reconcile the exact execution-owner chat and native Run/assignment bindings, planning
   provenance, worktree ownership and outstanding operations. No Bot-wide mutex or second
   coordinator is assumed. Unknown/conflicting identity blocks mutation; an unavailable
   runtime ID must remain unknown, not be replaced by a fabricated clean-session claim.
3. Recompute every frozen file hash and the manifest's own digest; compare with the
   recorded manifest binding and current required critique. Missing or changed bytes
   stop affected mutation for drift reconciliation, not silent re-hashing.
4. Verify repository, named target branch and full starting SHA, returned worktree
   branch/HEAD, one-writer custody and resource exclusions. Preserve existing dirty and
   untracked source; a worktree's presence is neither a clean-base nor ownership proof.
   Moved or ambiguous refs require explicit reconciliation before dependent operations.
5. Verify actual execution-host loading and capabilities, requested/resolved/actual model
   evidence and real runtime entry points. Inspect permission scopes separately: Bot
   defaults, existing chats, engine-specific launch override and existing workers.
   A setting does not retroactively migrate another scope; individual approval is not
   Full access. Missing command/access/model evidence is a scoped blocker, not a reason
   to install, sign in, impersonate an owner or rewrite permissions.
6. Confirm required provider qualification before coding. Keep document-only work separate
   from code readiness. Resolve runtime commands against actual installed capabilities;
   mark unavailable commands honestly instead of inventing syntax or substitutes.
7. Verify native continuation addressed to the exact owner and persist original clocks.
   Check actual UTC against the absolute attempt deadline and campaign cutoff before
   every affected dispatch or integration. Refuse new affected work after expiry; queued
   deadline delivery may be late and is not a hard-time barrier. Native reconciliation
   never proves exit or permits an automatic kill/restart.
8. Record admission time, exact owner, mandate revision, manifest digest, verified
   capabilities/models, source identity, blockers and pending operations in durable state
   with the transition receipt. Only then perform the authorized next operation under
   [runtime review and integration](runtime-review-and-integration.md).

No first-start ceremony or `awaiting_fresh_session_start` lifecycle is required. Planning
provenance, mandate, admission and execution outcome remain separate records; labels
must describe observed facts rather than manufacture authority. A successful author or
analysis report never releases successors: product acceptance is a separate blocked
native Task, never dispatched or made ready for a worker. Only the coordinator completes
it with exact-candidate independent review, integrated source and actual smoke receipts.
Document gates instead require the assigned static evidence and independent exact-byte
document verdict, not invented runtime results.

## Drift and resume

On drift, stop affected dispatch/integration and preserve the expected and observed
hashes, source/ref identities, authority revisions and outstanding native receipts.
Classify the cause before acting: unintended edits, owner-directed revision, moved target,
changed model/provider, scenario drift or uncertain custody. Preserve dirty/untracked
work before any authorized restoration; never reset or delete it merely to match a hash.

Restore the authorized frozen bytes only within explicit restoration rights, or obtain
an authorized revision where scope/permission needs a decision. Return changed design
to Logis and the relevant planning phase; the independent critic owns affected-scope
recheck and current-hash attestation for any reused unaffected evidence. Rebind runtime
and review evidence to the actual revised candidate. Record a new immutable manifest
when frozen inputs change. An agent's fresh hash or edit to an old verdict cannot
reconcile drift, grant consent or clear a blocker.

Resume reconciles the original mandate, manifest, native owner, pending launch/stop/merge
operations, source snapshots, actual models and original attempt/campaign clocks under
[state and recovery](state-and-recovery.md). Do not create a duplicate launch or merge
when its outcome is unknown. A timeout or silence is not proof of exit; replacement
requires guarded settlement and confirmed ownership/stop receipts. Operator pause never
self-resumes, and a late reply or obsolete timer cannot accept a superseded revision.
Existing authority need not be ceremonially re-approved, but a restart cannot broaden it,
reset bounds, conceal missing history or inherit a stale verdict.

## Staging and pending links

The [obligation ledger](obligation-ledger.md) preserves legacy provenance; its frozen
historical destination wording awaits separately owned amendment work and does not
reverse the approved `code-review.md` destination. Mapping sources remain unchanged:
[legacy model and start sections](../../acd/SKILL.md),
[legacy handoff reference](../../acd/references/handoff-and-start.md) and
[legacy handoff template](../../acd/templates/HANDOFF.md) are migration evidence only.

Use the planned [HANDOFF template](../templates/HANDOFF.md) and
[STATE template](../templates/STATE.json) when independently accepted. At this slice,
code-review, orca-runtime, runtime-review-and-integration, state-and-recovery and both
templates are PENDING future link targets, not resolved-link or acceptance claims.
Final cross-document acceptance must resolve all targets, fields and enums at exact hashes.

This candidate remains staged and uninstalled. Existing fleet SOULs still load
`.agents/skills/fleet-campaign/SKILL.md`; a link or handoff does not load `acd-orca`.
A later owner-controlled cutover must cover loading-path coordination, supported engine
loaders, rollback and observed host loading. No installation, packaging/public sharing,
engine parity or broad crash/reboot recovery is implied by this document.
