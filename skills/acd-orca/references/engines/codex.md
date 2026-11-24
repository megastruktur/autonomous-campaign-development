# Codex startup and capability evidence

This sheet documents Codex instruction discovery and the evidence needed for a later
authorized Orca qualification. The candidate is staged and uninstalled. This sheet
permits no Codex launch, installation, update, sign-in, configuration change or migration
of an existing conversation. Read [roles](../roles.md), the
[common fleet contract](../../../../fleet/skills/fleet-campaign/references/common-contract.md),
[handoff admission](../handoff.md#execution-admission) and
[Orca runtime discovery](../orca-runtime.md#discover-the-installed-interface) first.
Those references own shared policy, authority and native command mechanics.

The [owner amendment](../../../../fleet/execution/fullauto/AMENDMENT_01_ROBOREV.md)
selects roborev for substantive code review. Historical OCR-first prescriptions in
unchanged shared and legacy sources are superseded, not operative. [Code review](../code-review.md)
owns the qualified provider protocol. Its scoped roborev-to-OMP ACP evidence does not
qualify Codex as an implementation agent or review execution engine. Codex's own review
command is not an authorized substitute, and no adapter or inherited OMP/Hermes PASS is
implied.

## Official support and evidence limits

The official [Orca supported-agent page](https://orca.dev/docs/agents/supported) lists
Codex; the [native-chat page](https://orca.dev/docs/agents/native-chat) describes eligible
local and paired-server structured Codex chats. WSL/SSH sessions use terminal-backed
surfaces. Record the actual returned surface and execution host, not what the picker
appears to promise. An advertised integration is not proof that Codex is installed,
signed in, loading these instructions or qualified for this campaign.

OpenAI's [AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md) and
[skills guide](https://developers.openai.com/codex/skills) were requested on 2026-11-23;
both direct retrievals returned HTTP 403. The loading statements below instead use the
official OpenAI repository's linked implementation, retrieved at revision
`c028016428b58d5b2062debdafc60255f7efa7d6`. Its `docs/agents_md.md` and `docs/skills.md`
point to those same guides. Context7 also supplied upstream source excerpts. This is
current upstream evidence, not proof of the behavior of an unobserved installed build.
Match the installed version and its supported help before relying on any mechanism.

Codex remains **unqualified for engine parity** until its own scoped runtime receipts
are independently accepted. Local absence, an inaccessible interface, an untested
capability and a failed provider call are different facts; preserve them separately.
Do not erase supported OMP deliverables because an optional Codex path is unavailable.

## Discover the execution host

Use the installed Orca guides to inspect already-installed agents on the assigned host.
Resolve the Codex executable there, not from a different coordinator machine or a
website's installation recipe. Retain privately the executable identity/fingerprint,
version, host, OS user, cwd, effective Codex home/profile, relevant launch arguments,
Orca surface and native session binding. A missing observation is `null` with reason
and time, not an assumed default.

For an already-installed executable, the official
[CLI definition](https://github.com/openai/codex/blob/c028016428b58d5b2062debdafc60255f7efa7d6/codex-rs/cli/src/main.rs)
supports these bounded identity/help shapes:

```text
<CODEX> --version
<CODEX> --help
```

`<CODEX>` is the verified executable, not a command executed by this document. Consult
narrow installed help for any further read-only discovery; do not invent a skill-list
subcommand, configuration flag or loader. Help proves syntax, not authenticated
inference, permissions or tool success. Record a missing CLI or unsupported command as
a boundary. Do not run bare Codex, setup, update, login, installers, service startup,
trust changes or permission bypasses to make discovery pass. An installed listing alone
does not prove that the approved credential route is usable.

## Context instruction discovery

OpenAI's [home resolution](https://github.com/openai/codex/blob/c028016428b58d5b2062debdafc60255f7efa7d6/codex-rs/utils/home-dir/src/lib.rs),
[personal instructions](https://github.com/openai/codex/blob/c028016428b58d5b2062debdafc60255f7efa7d6/codex-rs/codex-home/src/instructions/mod.rs)
and [project instructions](https://github.com/openai/codex/blob/c028016428b58d5b2062debdafc60255f7efa7d6/codex-rs/core/src/agents_md.rs)
establish these discovery rules for the cited revision:

| Input | Supported discovery and limit |
|---|---|
| Personal context | `CODEX_HOME` selects the Codex home, conventionally `~/.codex` when unset. The personal loader tries `AGENTS.override.md` before `AGENTS.md` and selects the first readable non-empty content. Record the effective home, selected file and warnings, not merely the conventional location. |
| Project boundary | Starting from the actual cwd, find the nearest configured `project_root_markers` boundary; the default marker is `.git`. Project instructions are collected from that root down to cwd, inclusive, not every descendant or parent above the root. Without a marker, only cwd is considered; an empty marker list disables parent traversal. |
| Per-directory selection | Try `AGENTS.override.md`, then `AGENTS.md`, then configured `project_doc_fallback_filenames`. The cited project implementation selects the first existing regular file at each directory and later ignores empty content; an empty override can therefore shadow the ordinary file. Do not assume the personal non-empty fallback rule applies identically to project files. |
| Assembly and scope | Personal/thread instructions precede the ordered project entries. Deeper project guidance is encountered later, but cannot grant authority over higher-priority instructions or runtime permissions. Record the actual selected files and conflicts rather than claiming every nearby Markdown file loads. |
| Fallback names | Additional fallback entries are filenames, not arbitrary paths. Record only existing approved configuration; do not add a fleet SOUL path to this field or create a second instruction convention. |
| Trust and limits | The cited project loader skips untrusted projects and a zero `project_doc_max_bytes` budget. A finite budget can truncate or skip later files and emits warnings. Observe trust, effective budget, selected content and read errors; do not enlarge limits or grant trust under this sheet. |

The personal loader can retain its last successfully read instructions after a failed
refresh. File modification, a restart assumption or a later successful read therefore
cannot establish what an existing session received. Verify actual session inputs and
warnings; unknown startup observability stays a stated limitation. Do not reset another
conversation or overwrite installed instructions to obtain evidence.

A fleet `SOUL.md`, the Bot's home, the Codex home, repository root and worker cwd are
not interchangeable. Codex's filename discovery does not itself establish that Orca
injected the assigned SOUL or common policy. Additional host/thread instructions need
their own observed provenance. Follow the existing
[role loading boundary](../roles.md#loading-and-portability): fleet roles still point to
`.agents/skills/fleet-campaign/SKILL.md`, not this staged candidate.

## Skill discovery and body loading

The official [skill-root implementation](https://github.com/openai/codex/blob/c028016428b58d5b2062debdafc60255f7efa7d6/codex-rs/ext/skills/src/host_roots.rs)
distinguishes skill roots from context files:

- User skills include `~/.agents/skills/` under the effective user's home. The cited
  implementation also retains `CODEX_HOME/skills` as a **deprecated** compatibility
  location; it is not the recommended destination for a new installation.
- Repository `.agents/skills/` roots are discovered along the project-root-to-cwd path,
  subject to the effective project markers and filesystem access. This is not a scan
  of every directory in the repository.
- Active configuration layers, system roots, plugin roots and configured extra roots
  can contribute. Record their actual origin, filtering, duplicate names, warnings and
  selected source locator. Do not infer selection from a bare name, add roots or install
  plugins to force visibility.
- `skills/acd-orca/` in this repository is staged source, not an automatically installed
  Codex root. Its presence does not expose `acd-orca`, replace legacy `acd`, repoint
  `fleet-campaign` or prove that any linked reference loaded.

The official [skill catalog contract](https://github.com/openai/codex/blob/c028016428b58d5b2062debdafc60255f7efa7d6/codex-rs/ext/skills/src/catalog_prompt.rs)
uses progressive disclosure: the session catalog supplies skill metadata and source
locators; selecting a skill requires reading its complete `SKILL.md`, then its required
references. Catalog visibility, entrypoint/body loading, reference loading and actual
instruction use are separate observations. A matching task or explicit `$SkillName`
mention can select a skill, but only the observed selected content establishes loading.

Use the locator/access mechanism reported by the installed runtime. A filesystem skill
is read at its resolved path; newer upstream package/custom sources have their own access
mechanism. Do not transplant OMP's `skill://` filesystem behavior, Hermes `skill_view`,
or a newer Codex tool name into an older or different session. A rendered skill picker
is not evidence of body injection. Orca's documented Codex picker inserts `$skill`;
that user-facing invocation is not a worker steering channel or launch authorization.

Keep effective disable/filter controls and cache/refresh behavior in the receipt. A
standalone discovery result may differ from an existing worker's environment. Missing,
blocked, ambiguous or truncated required instructions stop the affected qualification;
generic upstream fallback advice cannot waive campaign loading or provider requirements.

## Loading and model receipt

Before relying on a later authorized Codex session, preserve privately:

1. Host, user, cwd, home/profile, executable/build and returned Orca surface; relevant
   effective launch controls and version-matched documentation/help identities.
2. Selected context/skill/role/common-policy files or source locators and SHA-256
   identities; project boundary, ordering, trust/filter state, warnings and truncation.
3. Separate evidence for injected context, catalog metadata, complete body/reference
   reads and assigned-role use. A model's unsupported assertion is not a loading receipt.
   Record observation limits without exporting personal prompts, memory or credentials.
4. Native Task/Dispatch/session correlation, delivered current brief, returned worktree,
   branch/base/HEAD and sole-writer custody. A parent Bot's receipt does not establish
   its worker's loading. Codex-internal subagents are not Orca-native workers.

Apply [model identity](../handoff.md#model-and-review-identity) separately by purpose:
requested route, resolved exact model, observed actual model, selection authority,
profile/configuration provenance and sanitized correlated outcome. A picker, launch
argument, banner or successful primary reply alone is not purpose-specific provider/tool
qualification. An unknown observed route is `null`; an explicitly unused purpose is
unused, not failed or silently qualified.

Inventory only auxiliary purposes that the actual Codex/Orca environment uses. Do not
invent OMP judge/smol equivalents, assume every auxiliary operation uses the primary
model, or trigger extra inference merely to fill a table. Required used routes need
their own successful correlated evidence; unresolved use limits unattended claims.
Codex's presence does not qualify roborev with Codex. Any different review execution
engine requires authorization and independent qualification under code review.

Primary failure, actual-model mismatch or permission refusal stops the affected path
for native escalation. No silent model/provider substitution, sign-in repair, blind
retry or alternate-host search. Reuse accepted evidence only for the same qualified
scope, rather than repeating paid bootstrap greetings.

## Four permission scopes

Record effective value, evidence source, observation time and enforcement limits for:

| Scope | Required distinction |
|---|---|
| Bot defaults | What a new conversation would inherit, including any Bot-specific override; not the mode of an existing chat. |
| Existing chats | The exact chat's current mode; changing defaults does not migrate existing conversations or already-running work. |
| Engine-specific launch override | Actual Codex arguments, environment and approval/sandbox controls, including whether a custom override exists; an OMP-specific setting does not establish Codex permissions. |
| Existing workers | Each worker's actual launch/effective restrictions and observed outcomes; parent settings or later changes are not proof. |

Orca's supported-agent page documents permission-bypass defaults for Codex. That is a
warning to discover the actual launch, **not a recommendation to enable bypass**. The
[native-chat documentation](https://orca.dev/docs/agents/native-chat) says Codex Ask mode
keeps workspace access read-only until an edit request is approved; permission changes
affect the next turn, while running work keeps its starting permission. Plan mode and
permissions are separate. Check the installed surface instead of equating a UI label
with an OS sandbox or transferring another engine's enforcement claims.

The [Orca security reference](https://orca.dev/docs/bots/security) distinguishes enforced
controls from instructions. Disclose runtime/OS enforcement, operational tool restriction
and instructed read-only separately. A disposable checkout is not OS isolation; one
approved action is not Full access. Full access is optional, never a qualification
prerequisite. Owner-only creation/permission actions cannot be impersonated, and broader
future-engine permission scope needs explicit disclosure and authority. Do not answer
another worker's permission menu, loosen controls or fabricate a denial. Unsafe or
unavailable denial testing remains UNTESTED with its reason.

## Native qualification checklist

This checklist is for a separately authorized isolated qualification, not execution by
this documentation slice. Bind every observation to Codex's own environment, versions,
configuration, source/scenario and evidence hashes; reuse only matching accepted receipts.

| Capability | Required observed evidence |
|---|---|
| Loading | Assigned role, common policy, mandate, skill body and required references actually available; startup injection distinguished from later reads. |
| Primary and tools | Approved actual model performs a task-relevant assistant/tool interaction with correlated success; installation, help, greetings and launch acknowledgment are insufficient. |
| Auxiliary use | Actual purpose-specific outcomes for every required used route, with unused and unknown separated. |
| Permissions | The four scopes above and safely authorized actual denial behavior without bypass. |
| Native communication | Discoverable session/output, current brief delivery, correlated question/reply and result reaching the exact owner; stored mail is not action. |
| Continuation | Actual native result wake and exact-owner one-shot deadline handling/cleanup without operator nudges; configured timers or Codex-local background activity are not equivalent. |
| Acceptance | A separate blocked, never-ready, never-dispatched product gate; successfully delivered analysis containing FAIL/INCONCLUSIVE leaves successors unready. Only the coordinator completes the gate with required bound evidence. |
| Useful implementation | Production-path results, independent exact-source review, distinct required API evidence, authorized integration and resulting-source smoke under [stage ordering](../runtime-review-and-integration.md#exact-candidate-and-stage-ordering). |
| Recovery | Authorized unknown-launch/no-duplicate, permission-denial/no-bypass, pause/late-reply/deadline/no-self-resume and source-drift/no-stale-verdict cases; unsupported safe fault injection stays UNTESTED. |
| Retention and release | Dirty/untracked source and evidence preserved before possible automatic release; guarded stop, physical exit and native release observed separately. Unknown release blocks reuse. |

Use [native communication and waiting](../orca-runtime.md#native-communication-and-waiting),
not raw terminal injection, a CLI polling loop, legacy watcher/heartbeat, Codex automation
or another scheduler. Respect original clocks and actual UTC admission checks before
affected dispatch, integration or gate completion. A delayed deadline is reconciliation,
not proof of exit or authority to kill, retry, accept or resume a pause.

Keep observed activity, assistant success, completed tool and semantic task progress
separate under [progress semantics](../state-and-recovery.md#observation-and-semantic-progress).
Do not apply OMP event schemas to Codex. Establish completion/error meanings from the
actual supported Codex surface and sanitized correlated outcomes; absent evidence stays
unknown. Process activity, exit zero or an ended turn alone is not useful progress,
provider success or product acceptance. No broad unattended or reboot-recovery guarantee
follows from a loading test.

## Qualification disposition and staging

Report each capability as QUALIFIED only within accepted evidence scope; BLOCKED when
an observed prerequisite/refusal prevents the required path; UNAVAILABLE when actual
discovery establishes absence or unsupported capability; or UNTESTED when not exercised.
Documentation support and executable availability remain separate facts. A missing CLI
on the assigned host makes that path unavailable, not Codex universally unsupported and
not an invitation to install. Unqualified never means inferred parity.

[Legacy operational mechanics](../../../acd/references/hermes-orca-omp.md) and the
[obligation ledger](../obligation-ledger.md#reference-obligations) preserve migration
provenance, not operative terminal/START/fallback recipes. Earlier provider-pending labels
remain historical; current scoped readiness belongs to code review and never qualifies
Codex. Separately owned ledger updates and final cross-document acceptance remain required.

Placeholder inventory: `<CODEX>` means the discovered executable. `CODEX_HOME`, tilde
paths and `$SkillName`/`$skill` are documented environment/path/invocation conventions,
not private bindings. Keep live identities, host paths, model routes and credentials in
private project evidence. This sheet links only existing local targets; nine templates,
the validation reference and candidate entrypoint remain separate pending artifacts.
Staging changes no installed loading paths or personas, and is not standalone packaging.
Author completion does not provide independent document acceptance, runtime qualification,
successor authorization or permission to install the candidate.
