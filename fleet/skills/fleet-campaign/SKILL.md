---
name: fleet-campaign
description: >-
  Coordinate the local reasoning-first Orca bot fleet: Logis synthesis, independent critique,
  one Magos coordinator per project, native handoffs and supervised execution. Use for fleet
  planning, steering, review or bounded development. Installation and greetings are setup-only.
compatibility: Orca native Bots, orchestration and Automations. OMP first; actual role loading, messaging and wakes must be tested on the local host.
---

# Local reasoning-first fleet

Read your SOUL, [common contract](references/common-contract.md), `FLEET_BINDINGS.md` in your
Bot home and the project charter path it names. All operational instructions and artifacts
must be in English. Missing bindings require setup, not invented identities. This skill is
prepared for the local fleet, not evidence that the Bots exist or the runtime path is qualified.

## Startup and intake

Identify your role, project, original request and existing campaign/owner before creating work.
A greeting/import is setup-only. Derive authority from the actual owner request; the charter
records it but grants none. No routine plan/START/per-feature human gates inside the mandate.
Genuine permissions, safety, missing capability and finite resource bounds still apply.

Resolve local role keys to actual Bot IDs; discover current native capabilities through the
installed `orca skills get orchestration` and `orca agent-context --json`. Verify returned
receipts. All shared-role conversations stay project-scoped; no private project data in
shared long-term memory. Do not copy working Bot homes into the repository.

## Planning

Any Logis bot may receive the captain. Magos Logis II synthesizes one canonical candidate;
Intent contributes user journeys; Architect contributes real interface/reuse analysis. Research
current primary sources and license/footprint/security of meaningful reused dependencies.
Critique precedes DAG creation. Activate roles proportionately; substantial changes need
technical and outcome lenses, small requests need an explicitly adequate independent check.

Critics receive original requirements, exact candidate, relevant rationale and evidence in
fresh sessions. Authors may rebut but cannot close their own blockers. Critics recheck changed
and affected scope and issue PASS/FAIL/INCONCLUSIVE bound to the current candidate. Nonconvergence
must be settled within bounds or reported, never disguised as PASS or resolved by vote.

## Handoff and execution

After convergence, automatically hand the exact plan revision and bounded tasks to the project's
Magos within the existing mandate. Include source/artifact hashes, repo/base, acceptance, resource
exclusions, test/runtime commands and authorized delivery scope. On drift, reconcile the change;
do not quietly re-hash and call the old verdict current. Existing campaign changes go to its
owner, not a second Run.

Magos creates native Tasks/dependencies and starts OMP workers in Orca-managed worktrees,
never main. One writer per worktree; serialize shared lockfiles, schema/migrations, databases,
ports and externally visible effects as needed. Pin locally resolved engine/model and source
base. Each assignment includes paths, non-goals, checks, evidence and source-receipt policy.
Commits need actual authority; otherwise preserve an attributable diff before task completion.

Represent product acceptance separately from analysis delivery. Review-analysis success means
a report exists, not a product PASS. FAIL/INCONCLUSIVE cannot unlock product successors.
Dependents require independent review, integrated source and appropriate post-integration
runtime checks, not an author's done message. Coordinators do not code or resolve conflicts.

## Code review and verification

OCR is the initial code-review provider, never silently replaced by a planning critic. Run it
from an independent read-only native-supervised session with exact candidate/context and
actual test evidence. Preserve raw output; rc=0 alone is not PASS. Incomplete, partial, failed,
skipped or malformed review is INCONCLUSIVE; critical/high/medium findings block, low alone
does not under the initial ACD-derived mapping. Verify installed OCR behavior before first use.

Later provider change requires captain steering or an already-granted selection policy and a
qualified adapter. A CLI tool need not itself be a Bot. Keep independence, raw evidence,
exact-candidate coverage and honest failure semantics. Explicit unaffected-evidence reuse needs
a new attestation for the current candidate; no stale PASS relabeling. Bounded same-packet
comparisons are allowed when authorized, not mandatory dual reviews on every task.

Authors self-test; independent code review and real-runtime verification remain separate.
Run accepted scenarios against integrated source. Final handback names observed checks, exact
candidate, deliverable, limits and what remains unknown. Ready-for-captain is not accepted.
Preserve source/evidence outside disposable workspaces before native release/cleanup.

## Native supervision and steering

Use the installed Orca skill/help for exact syntax. Native worker messages wake their owner;
peer requests use `orchestration send --to bot:<id>` with question/handoff/status and exact
chat routing; answers use `reply --id`. Steer workers through Dispatch-addressed messages.
No terminal poking, external watcher, mailbox polling daemon or extra scheduler.

Run identity belongs to a session/pane, not the whole Bot. One execution-owner chat per project
is a protocol, not a mutex. Reconcile actual Run/Dispatch/revision on every wake. Unknown
ownership or unknown start outcome cannot justify duplicate work. Follow receipts and native
circuit breakers; some recovery explicitly requires the owner and cannot be automated away.

Where necessary, use native Bot one-shot deadline reminders (`--once --by`), exact owner chat
and timezone. The inspected catalog has no worker-completed Automation trigger. Completion
and deadlines are separate; disable obsolete deadlines and ignore stale queued messages.
Deadline delivery may queue behind a current turn and is not a hard kill timeout. Silence
is not exit. No unauthorized stop/retry/abandon solely because time elapsed.

Captain pause prevents new dispatch/integration; it does not prove in-flight process exit.
Cancel uses guarded native stop and confirmed receipts. Scope changes become recorded revisions
and affected replanning. Late results cannot satisfy the wrong revision. No timer resumes an
owner pause. End turns while legitimately waiting so native wakes can deliver.

## Setup boundary

Native Bot creation is owner-gated in inspected Orca 1.4.268. Do not manufacture caller
identity, edit runtime databases or invoke owner UI endpoints as an agent to defeat it.
Creating SOUL source files and avatars is preparation, not Bot creation. First-run configuration
can report readiness but must not launch an implementation campaign automatically.
