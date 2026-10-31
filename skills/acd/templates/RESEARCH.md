# {{prefix}} Research and Architecture: {{campaign_name}}

> Replace every placeholder; delete this legend. Phase 2 artifact, revised during phase 3.
> Research must be actually retrieved and read; never invent sources or claims. Record the
> exact artifact hash in STATE after every revision. No DAG/task decomposition here.

- Status: `draft` / `researched` / `revised`
- Intent input (path + SHA-256): {{intent_path_and_hash}}
- Research access date: {{date}}

## Research scope

Feature size/novelty/risk and why this research breadth is proportionate: {{rationale}}

Research questions: {{questions}}

## Sources actually consulted

| ID | Title / publisher | URL | Published/updated (if available) | Accessed | Claims used / limitations |
|---|---|---|---|---|---|
| S1 | {{title_publisher}} | {{url}} | {{date_or_unknown}} | {{date}} | {{claims_and_limits}} |

Prefer primary/current sources. Search-result snippets are not sufficient evidence.

## Patterns and options compared

| Pattern / option | Evidence | Benefits | Costs / risks | Repository fit |
|---|---|---|---|---|
| {{option}} | {{source_ids_and_repo_paths}} | {{benefits}} | {{tradeoffs}} | {{fit}} |

## Chosen architecture and rationale

{{decision_and_why_it_best_satisfies_intent}}

- Components and boundaries: {{components}}
- Data and control flow: {{flow}}
- Shared API/schema/resource ownership: {{contracts}}
- Compatibility and migration: {{approach}}
- Failure behavior and recovery: {{behavior}}
- Verification/runtime seams: {{seams}}

## Decision traceability

| Decision | User intent | Repository evidence | Research evidence | Rationale |
|---|---|---|---|---|
| {{decision}} | {{intent_section}} | {{paths_symbols}} | {{source_ids}} | {{rationale}} |

If a pattern conflicts with explicit user intent, preserve the intent and revise the pattern;
surface genuine infeasibility or trade-offs instead of silently changing requirements.

## Security analysis

- Assets, actors, trust boundaries, and exposure: {{analysis}}
- Threats and abuse cases: {{analysis}}
- Data handling and authentication/authorization: {{analysis}}
- Relevant attack/failure classes and mitigations: {{analysis}}
- Secure defaults and security verification scenarios: {{analysis}}

Scale depth to exposure; big/sensitive features require scenario-based treatment.

## UX analysis

- Users and end-to-end journeys: {{analysis}}
- Loading, empty, error, success, and recovery states: {{analysis}}
- Accessibility, responsiveness, and feedback: {{analysis}}
- Consistency with existing product UX: {{repository_evidence_and_design}}
- UX acceptance/runtime scenarios: {{scenarios}}

Scale depth to user impact; big/user-facing features require scenario-based treatment.

## Assumptions, unknowns, and readiness for critique

- Assumptions: {{assumptions_or_none}}
- Unresolved technical unknowns: {{unknowns_or_none}}
- User decisions required: {{decisions_or_none}}

All material unknowns must be resolved before the DAG gate; record blockers honestly.
