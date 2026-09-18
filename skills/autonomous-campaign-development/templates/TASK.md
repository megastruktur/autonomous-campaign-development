# {{prefix}}_{{task_name}}

> Template legend: replace every `{{placeholder}}`; delete this block when instantiating.
> File name: `{{prefix}}_{{task_name}}.md` in `plans/{{campaign_name}}/`.
> Worktree display name: `{{prefix}}-{{task_name}}` (one writer only).

## Goal

{{one paragraph: what this task delivers as an observable user/runtime outcome}}

## Scope allowlist (explicit)

- {{path/or/file/you/may/touch}}
- {{path/or/directory/you/may/touch}}

Anything not listed is out of scope. No formatters with autofix; read-only linting only.
Found a problem outside the allowlist -> record it under "Out-of-scope findings" in your
report; do not fix it.

## Non-goals

- {{explicitly excluded work}}

## Dependencies

- Requires completion (reviewed + integrated + post-merge smoke) of: {{tasks_or_none}}
- Exclusive resources (do not share concurrently): {{files/apis/ports/fixtures_or_none}}

## Shared contracts (consume as-is; do not redesign)

- API: {{contract_reference}}
- Schema/data: {{contract_reference}}
- Other: {{contract_reference}}

## Acceptance criteria

1. {{observable_criterion}}
2. {{criterion}}

## Real runtime testing (actionable)

| # | Scenario | Exact command / interaction | Expected observable outcome |
|---|---|---|---|
| 1 | {{scenario}} | {{verified_command_or_ui_steps}} | {{outcome}} |

Runtime environment: {{real app/CLI/API/UI via production path; declared mocks of
EXTERNAL dependencies only, with limits}}. Record build/source identity (commit) with
each result. A green unit suite does not satisfy this section.

## Reporting and evidence

- Evidence slot: `{{prefix}}_evidence/{{task_name}}/`
- Report must include: commands/actions/results per scenario, commit SHA of the final
  state, out-of-scope findings, explicit ready handoff statement when done.
- When your work is committed and the tree is clean: set worktree status `in-review` with
  a comment summarizing what was verified. Do not merge, push, or delete anything.

## Stage checklist (mirrored in campaign TODO)

- [ ] develop
- [ ] runtime test-loop (test -> fix batch -> test)
- [ ] independent review-loop (FAIL -> fix -> retest -> fresh review)
- [ ] squash integration / conflict handling
- [ ] post-merge runtime smoke
- [ ] evidence preserved + cleanup verified
