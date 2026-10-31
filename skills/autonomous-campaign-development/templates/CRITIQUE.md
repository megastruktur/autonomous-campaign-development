# {{prefix}} Design Critique and Convergence: {{campaign_name}}

> Replace every placeholder; delete this legend. Preserve ordered rounds; never overwrite
> prior findings. A fresh independent critique covers ALL five lenses on every revision.
> CONVERGED is valid only for the exact input hashes and with no unresolved blocking findings.

- Critic identity/session (independent of plan author): {{identity}}
- Current round: {{number}}
- Current verdict: `IN_PROGRESS` / `REVISE` / `CONVERGED`
- Convergence INTENT SHA-256: {{hash_or_null}}
- Convergence RESEARCH SHA-256: {{hash_or_null}}

## Round {{number}}

### Inputs

- Original user request supplied to critic: {{yes_and_where}}
- INTENT path + SHA-256: {{path_and_hash}}
- RESEARCH path + SHA-256: {{path_and_hash}}
- Repository evidence supplied: {{paths_symbols}}
- Critique date: {{date}}

### Lens 1 - Intent fidelity

{{findings_about_requested_functionality_constraints_scope_and_acceptance_or_no_findings}}

### Lens 2 - Architecture and research evidence

{{findings_about_pattern_fit_sources_repository_contracts_and_feasibility_or_no_findings}}

### Lens 3 - Security

{{findings_about_threats_trust_boundaries_abuse_cases_controls_and_verification_or_no_findings}}

### Lens 4 - UX

{{findings_about_journeys_states_accessibility_feedback_and_consistency_or_no_findings}}

### Lens 5 - Execution readiness

{{findings_about_acceptance_runtime_scenarios_task_boundaries_and_dependencies_or_no_findings}}

### Findings and dispositions

| ID | Severity | Lens | Finding and evidence | Required resolution | Revision / response | Status |
|---|---|---|---|---|---|---|
| {{round}}-F1 | critical/major/minor | {{lens}} | {{finding}} | {{resolution_required}} | {{concrete_change_or_user_decision}} | open/resolved/accepted |

### Round verdict

- Verdict: `REVISE` / `CONVERGED`
- Rationale: {{rationale}}
- Unresolved critical/major findings: {{ids_or_none}}
- Unresolved minor findings: {{ids_or_none_or_accepted_with_rationale}}
- Contradiction of user intent: {{none_or_details}}

`REVISE` -> update INTENT and/or RESEARCH, answer every finding, record new hashes and STATE,
then add a complete fresh round. Material intent change returns to phase 1; material research
or architecture change returns to phase 2. Never proceed to a DAG on this file's existence
alone: the final verdict must be CONVERGED and bound to the current exact inputs.
