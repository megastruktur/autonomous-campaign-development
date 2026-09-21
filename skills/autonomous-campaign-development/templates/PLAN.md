# {{prefix}} Campaign Plan: {{campaign_name}}

> Template legend: replace every `{{placeholder}}`; delete this block when instantiating.

- Campaign name (lowercase slug): `{{campaign_name}}`
- Prefix (unique short abbreviation): `{{prefix}}`
- Repository: `{{repo_path}}`
- Original NAMED target branch: `{{target_branch}}` (never assumed to be main/master)
- Starting SHA (full, pinned): `{{starting_sha}}`
- Date / coordinator: `{{date}}` / `{{coordinator}}`

## Goal and context

{{what the campaign delivers and why - bounded context discovery only, no deep code exploration}}

## Clarifications and decisions

| # | Question asked | User answer / decision | Date |
|---|---|---|---|
| 1 | {{question}} | {{answer}} | {{date}} |

## Improvement proposals (pre-approval)

{{improvements proposed to the user before locking the plan; note accepted/rejected}}

## Model questionnaire

| Role | Requested | Resolved | Pinned |
|---|---|---|---|
| Coding model | {{requested_or_default}} | {{resolved_id}} | {{yes/no}} |
| Fallback model | {{requested_or_default_or_none}} | {{resolved_id_or_none}} | {{yes/no}} |
| Reviewer model | {{requested_or_default}} | {{resolved_id}} | {{yes/no}} |
| Final-review model (optional) | {{requested_or_default_or_none}} | {{resolved_id_or_none}} | {{yes/no}} |

`default` = the runtime/profile's actual configured default. Verify the actual startup
model of every agent; never silently substitute an unapproved model. The optional
final-review row pins a heavyweight model for exact-head final reviews; it is the
user's choice, never a hard-coded requirement.

## Task DAG

| Task | Depends on | Exclusive resources | Worktree (display) |
|---|---|---|---|
| {{task_name}} | {{deps_or_none}} | {{files/apis/ports/etc}} | `{{prefix}}-{{task_name}}` |

Parallel-group view (explanatory only, NOT a fixed wave barrier):

- Group A (no shared exclusive resources): {{tasks}}
- Group B: {{tasks}}

Max THREE simultaneously active coding agents, fix/remediation included. A task starts
only after its prerequisites are independently reviewed, squash-integrated, and
post-merge smoke tested.

## Shared contracts (settled centrally)

- API contracts: {{endpoints/signatures/error shapes owned here}}
- Schema/data contracts: {{migrations, ownership, ordering}}
- Resource ownership: {{files, lockfiles, build output, ports, fixtures, external side effects}}

Sibling tasks consume these contracts as-is; they never redesign them independently.

## Campaign acceptance criteria

1. {{observable user outcome}}
2. {{seam/interaction outcome}}

## Campaign real runtime testing

| # | Scenario | Production path | Observable outcome | Environment |
|---|---|---|---|---|
| 1 | {{scenario}} | {{actual cli/api/ui invocation}} | {{expected observable result}} | {{env/mocks declared with limits}} |

Every command below was actually verified to exist on target (how): {{verification}}

## Execution policy (bounded attempts)

- `attempt_budget_seconds`: 2100 (35 min default per execution attempt; starts at
  actual attempt launch, never resets on transport activity, watcher/coordinator
  restarts, or metadata churn)
- `checkpoint_due_seconds`: 1200 (20 min: inspect progress evidence; at most ONE
  scoped steer)
- `max_unproductive_attempts`: 2 (no blind third same-route retry on the same slice)
- Extensions: {{none_or_predeclared_per_task_long_job_budgets}} - only explicit,
  predeclared, task-specific measured long-job budgets (for example a known long
  build/test phase with a bounded deadline); no retroactive or open-ended extensions.
- Enforcement is procedural (coordinator/runtime scoped control), not an automated
  flag in the observer scripts. A budgeted stop settles the attempt; it is NOT a
  permanent feature FAIL.

## Approval record (the single WHAT gate)

- Approved by: {{user}} on {{date}}
- Authorized scope: scoped development, tests, independent reviews, task squash merges,
  campaign completion merge, safe cleanup.
- Final merge strategy to target: `--no-ff` (default) - change only with user decision.
- Push/publication/deployment: NOT authorized by this approval (separate permission).
- Non-convergence policy: evidence-based pause (default) - configured overrides: {{none/listed}}
- Execution policy: attempt budget 2100s / checkpoint due 1200s / max 2 unproductive
  attempts (defaults) - configured overrides or predeclared extensions: {{none/listed}}
- Approval is NOT START: it authorizes what may happen, not that execution begins.
  After this record, the planning session writes `{{prefix}}_HANDOFF.md` and
  `{{prefix}}_MANIFEST.json`, sets state lifecycle `awaiting_fresh_session_start`, and
  STOPS. Execution starts only on an explicit START in a distinct fresh coordinator
  session bound to the manifest
  ([../references/handoff-and-start.md](../references/handoff-and-start.md)). No new
  per-task human gates are introduced by this boundary.

## Artifacts

State: `plans/{{campaign_name}}/{{prefix}}_STATE.json` | TODO: `{{prefix}}_TODO.md` |
Events: `{{prefix}}_EVENTS.jsonl` | Evidence: `{{prefix}}_evidence/` | Report: `{{prefix}}_REPORT.md`
| Handoff: `{{prefix}}_HANDOFF.md` | Manifest: `{{prefix}}_MANIFEST.json`
