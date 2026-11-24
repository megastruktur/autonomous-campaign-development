---
name: acd-orca
description: Evidence-led development campaigns on Orca
version: 1.0.0
---

# Autonomous campaign development on Orca

This staged, uninstalled candidate organizes multi-task development on Orca through
bounded source work, independent review and evidence-bound acceptance. It is a
procedure, not another scheduler or a grant of execution authority. Existing
`skills/acd/`, installed skills, Bots and loading paths remain unchanged.

## When to use

Use for campaigns with meaningful dependencies, shared contracts or resource exclusions
and independent review. Do not manufacture a DAG for a trivial fix, pure research or
operations without development. The actual mandate, repository instructions, hooks and
permission boundaries bind; reading this skill does not expand them.

## Responsibility and authority

Start with [roles and ownership](references/roles.md) and the existing
[common fleet contract](../../fleet/skills/fleet-campaign/references/common-contract.md),
not copied personas or a second policy. The
[handoff authority contract](references/handoff.md#authority-and-precedence) owns mandate
and amendment precedence. Local identities, exact model routes and credentials do not
belong in this portable entrypoint.

For this staged campaign, the
[runtime recovery amendment](../../fleet/execution/fullauto/AMENDMENT_03_RUNTIME_RESUME.md)
supersedes conflicting older runtime instructions, without rewriting historical verdicts.
It requires fresh supervised independent OMP document/acceptance reviewers in an existing
suitable workspace, with explicit Inquisitor constraints and an immutable exact-candidate
packet. Do not reuse the author as reviewer, create persistent Bot side chats for these
reviews, or attribute an independent worker's answer to a named Bot. Read-only is an
instruction unless enforced capability is evidenced. Substantive source review remains
selected roborev under [code review](references/code-review.md), not a critic substitute.

Apply that amendment's finite lifecycle: at most three outstanding runtime resources,
normally one source writer plus one reviewer, with one source writer per worktree.
Completion or end-turn alone does not free a slot; native release/exit evidence does.
Source attempts remain bounded to 15 minutes with checkpoint 10, reviews to 10 minutes;
no total cutoff does not remove these bounds. Other campaigns need their own authority.

## Ordered workflow

Follow the owning references in order; they contain the acceptance rules and exceptions.

1. Record intent and bounded repository discovery, then live research and reuse analysis
   under [planning and design](references/planning-and-design.md). Use
   [INTENT](templates/INTENT.md) and [RESEARCH](templates/RESEARCH.md).
2. Obtain independent design critique and current-hash convergence before a DAG, using
   [CRITIQUE](templates/CRITIQUE.md). Material changes return to the affected planning
   stage; the planning reference owns critic closure and reuse of unaffected evidence.
3. Describe work, contracts, exclusions and separate acceptance gates with
   [PLAN](templates/PLAN.md), [TASK](templates/TASK.md) and
   [PLANNING_STATE](templates/PLANNING_STATE.json). Transfer the frozen packet through
   [mandate-bound handoff](references/handoff.md) and [HANDOFF](templates/HANDOFF.md).
4. Establish execution-host loading and scoped capabilities through
   [Orca runtime](references/orca-runtime.md) and the startup sheets below. Discover the
   installed version-matched interface, rather than copying remembered CLI commands.
5. Execute the [runtime, review and integration chain](references/runtime-review-and-integration.md):
   develop, exercise real runtime paths, obtain independent review, integrate only as
   authorized, and smoke-test the integrated source. Use the selected provider's
   [exact-candidate review contract](references/code-review.md); readiness is not a
   candidate verdict. Distinct API inspection and runtime proof remain distinct gates.
6. Keep durable state and original attempt clocks under
   [state and recovery](references/state-and-recovery.md), using
   [STATE](templates/STATE.json) and [TODO](templates/TODO.md). Worker completion reports
   delivery, not product acceptance; follow the
   [native acceptance boundary](references/orca-runtime.md#acceptance-tasks-are-not-work).
7. Finish with exact-source verification, authorized delivery and source-preserving
   [cleanup](references/runtime-review-and-integration.md#cleanup). Follow native
   communication and release receipts; do not add watchers, polling or another supervisor.

## Engine loading

Use the sheet for the actual execution engine: [OMP](references/engines/omp.md),
[Hermes](references/engines/hermes.md) or [Codex](references/engines/codex.md).
These are loading and evidence checklists, not interchangeable qualification certificates.
This campaign admits only native OMP authors; the other sheets do not authorize a switch.
A resolved link is not proof that instructions loaded. Current accepted private receipts
control scoped readiness; older snapshot pending labels are not current gate evidence.

## Validation and migration

Use [static validation and synthetic tabletops](references/validation-tabletop.md) for
narrow document checks and the separately assigned final integration gate. Static success
and synthetic reasoning are not runtime proof or independent product acceptance.
The [obligation ledger](references/obligation-ledger.md) maps retained guarantees and
superseded legacy mechanics; it is not permission to execute historical recipes.

This entrypoint and its relative fleet links form a repository-local candidate, not a
standalone installed bundle. Any loading-path cutover, engine qualification or distribution
needs its own authority and evidence under the linked contracts.
