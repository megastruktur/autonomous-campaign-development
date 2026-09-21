# {{prefix}} Campaign HANDOFF

> Template legend: replace every `{{placeholder}}`; delete this block when instantiating.
> Written by the PLANNING session after approval, together with
> `{{prefix}}_MANIFEST.json`. This file is the execution entrypoint - a curated pointer
> set, never a transcript dump. Every unknown stays null. After writing it, the
> planning session records `lifecycle: awaiting_fresh_session_start` and STOPS.

- Campaign: `{{campaign_name}}` (prefix `{{prefix}}`)
- Planning session identity: {{session_identity_or_null}}
- Written: {{date}} - plan approved by {{user}} on {{date}}

## Goal and scope (summary)

{{two to five sentences: what this campaign delivers and the approved scope. Key
decisions and clarifications: link the PLAN section, do not re-paste the transcript.}}

## Artifacts (repo-relative links)

- Plan: `plans/{{campaign_name}}/{{prefix}}_PLAN.md`
- Tasks: {{list every plans/{{campaign_name}}/{{prefix}}_{{task_name}}.md}}
- State: `plans/{{campaign_name}}/{{prefix}}_STATE.json` (lifecycle:
  `awaiting_fresh_session_start`)
- TODO: `plans/{{campaign_name}}/{{prefix}}_TODO.md`
- Manifest: `plans/{{campaign_name}}/{{prefix}}_MANIFEST.json`

## Repository and topology inputs

- Repo path: {{repo_path}}
- Original NAMED target branch: {{target_branch}} - starting SHA (full): {{starting_sha}}
- Campaign integration worktree (to create in the execution session):
  `{{prefix}}-campaign`

## Models (from the questionnaire)

| Role | Requested | Resolved |
|---|---|---|
| Coding | {{requested_or_default}} | {{resolved_id}} |
| Fallback | {{requested_or_default_or_none}} | {{resolved_id_or_none}} |
| Reviewer | {{requested_or_default}} | {{resolved_id}} |

## Permissions

- Authorized by the plan approval: {{authorized_scope_summary}}
- Push / publication / deployment: {{not_authorized_or_exact_explicit_grant}}
- Final merge strategy: `--no-ff` (or the recorded override)

## Verified runtime commands, prerequisites, blockers

| Command / capability | Verified how | Status |
|---|---|---|
| {{command}} | {{verification}} | {{verified_or_blocker}} |

Prerequisites: {{prereqs_or_null}}. Known blockers: {{blockers_or_null}}.

## Monitoring and recovery policy

- Polling cadence while active: every 10 minutes across every active session; progress
  semantics per [../references/progress-watchdog.md](../references/progress-watchdog.md).
- Optional watchdog: {{intent_and_config_pointer_or_none}} (observer-only; never
  authoritative).
- Remediation ladder: [../references/state-and-recovery.md](../references/state-and-recovery.md#remediation-and-non-convergence).

## Exact START prompt

Hand this prompt to the user; the user pastes it into a NEW, clean coordinator session.
The planning session never executes it itself.

```text
START campaign {{campaign_name}}.
Repo: {{repo_path}}. Plans directory: plans/{{campaign_name}}/.
Validate {{prefix}}_MANIFEST.json against {{prefix}}_STATE.json and the frozen plan
files, run the START checks from {{prefix}}_HANDOFF.md, then begin execution.
```

## Companion manifest (`{{prefix}}_MANIFEST.json`)

The planning session materializes this shape as a separate file in the same directory -
never embedded here (the manifest hashes this file; no recursive self-hash):

```json
{
  "manifest_version": 1,
  "campaign": "{{campaign_name}}",
  "prefix": "{{prefix}}",
  "created_at": "{{iso8601}}",
  "algorithm": "sha256",
  "files": {
    "plans/{{campaign_name}}/{{prefix}}_PLAN.md": "{{sha256}}",
    "plans/{{campaign_name}}/{{prefix}}_{{task_name}}.md": "{{sha256}}",
    "plans/{{campaign_name}}/{{prefix}}_HANDOFF.md": "{{sha256}}"
  }
}
```

Include every task file and every standalone shared-contract file under `files`. Never
include STATE, TODO, EVENTS, evidence, or the manifest itself - those are mutable or
self-referential. The manifest is immutable once written; any frozen-file change after
approval invalidates consent until the user re-approves.
