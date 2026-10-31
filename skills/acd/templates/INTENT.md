# {{prefix}} Intent and Repository Discovery: {{campaign_name}}

> Replace every placeholder; delete this legend. Phase 1 artifact. Do not add a DAG or
> task decomposition here. Update the artifact path/hash in STATE after every revision.

- Status: `draft` / `intent_captured`
- Date / coordinator: {{date}} / {{coordinator}}
- Original user request: {{verbatim_or_faithful_request}}

## Observable outcome and functionality

{{what the user wants to achieve; observable behavior and value}}

### Requested capabilities

1. {{capability}}

### Constraints and non-goals

- Explicit constraints: {{constraints}}
- Explicit non-goals: {{non_goals}}
- Assumptions requiring validation: {{assumptions_or_none}}

## Brainstorm and coordinator recommendations

| Option / improvement | Benefit and trade-off | Recommendation | User decision |
|---|---|---|---|
| {{option}} | {{analysis}} | {{recommended_or_alternative}} | {{accepted_rejected_or_not_needed}} |

The coordinator may choose sensible design details; it must not silently convert an
unapproved suggestion into user-required scope.

## Clarifications and decisions

| # | Question or ambiguity | Why it matters | Answer / decision | Date |
|---|---|---|---|---|
| 1 | {{question}} | {{impact}} | {{answer}} | {{date}} |

## MANDATORY read-only repository discovery

- Repository instructions inspected: {{paths}}
- Manifests/dependencies inspected: {{paths_and_relevant_dependencies}}
- Architecture/docs inspected: {{paths}}
- Relevant modules/public interfaces and traced symbols: {{paths_symbols_consumers}}
- Existing implementation patterns: {{patterns_with_paths}}
- Test/runtime entry points and commands discovered: {{paths_commands}}
- Integration, compatibility, data, and resource constraints: {{findings}}

Record only actual bounded, read-only inspection. Deep implementation, exhaustive history
research, source edits, agents, and worktrees are forbidden in this phase.

## Proposed acceptance outcomes

1. {{observable_user_outcome}}
2. {{security_ux_or_integration_outcome}}

## Remaining unknowns and next research questions

{{unknowns_or_none_and_questions_for_phase_2}}
