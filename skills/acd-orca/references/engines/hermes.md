# Hermes startup and capability evidence

This sheet documents supported Hermes loading discovery and the evidence needed to use
it with the staged, uninstalled candidate. It does not authorize a Hermes launch, install,
sign-in, profile/configuration change or migration of an existing conversation. Read
[roles](../roles.md), the
[common fleet contract](../../../../fleet/skills/fleet-campaign/references/common-contract.md),
[handoff admission](../handoff.md#execution-admission) and
[Orca runtime discovery](../orca-runtime.md#discover-the-installed-interface) first.
Keep native command mechanics and shared policy in those owning references.

The [owner amendment](../../../../fleet/execution/fullauto/AMENDMENT_01_ROBOREV.md)
selects roborev for substantive code review; OCR-first instructions in unchanged shared
and legacy sources are superseded, not operative. [Code review](../code-review.md)
owns provider qualification. Its accepted roborev-to-OMP ACP path does not establish a
Hermes review engine or Hermes implementation capability. No compatibility adapter,
provider substitution or inherited OMP PASS is implied.

## Official support and its limits

The official [Orca supported-agent page](https://orca.dev/docs/agents/supported) lists
Hermes. The [native-chat page](https://orca.dev/docs/agents/native-chat), retrieved on
2026-11-23, states that **Hermes Chat requires Hermes 0.23.0 or later on the workspace
host**. This is a documented minimum for that Orca surface, not a claim about the
installed version, every Hermes CLI feature or campaign qualification. The page supports
eligible local and paired-server Hermes Chat, but not SSH Hermes Chat; general WSL/SSH
sessions use terminal-backed surfaces. Record the actual returned surface rather than
assuming the picker created a structured chat.

Current upstream documentation describes loading APIs and configuration below. Match
those descriptions to the actual installed build, profile and launch surface before
relying on them. A current `main` document is not version-pinned implementation proof.
An advertised agent, Markdown support, installed executable or successful help command
proves neither authenticated inference nor instruction loading, tools, permissions,
native result wakes or source-preserving release.

Hermes remains **unqualified for this campaign's engine-parity claims** without its own
accepted runtime receipts. This documentation slice performs no Hermes launch, provider
probe or credential check. It does not turn unknown local availability into unavailable,
or an installed but unusable agent into qualified.

## Discover the execution host

Use the installed Orca guides to identify the assigned workspace host and already-installed
agent. Resolve the Hermes executable there, not from the coordinator's PATH on another
machine. Record privately its exact identity, version/fingerprint, OS user, cwd, active
profile/home, native session and intended surface. Observe effective launch arguments
and settings provenance without dumping auth files, all configuration or environment
values. A missing version observation remains `null` with reason and time.

For an already-installed executable, consult narrow help before relying on discovery:

```text
<HERMES> --help
<HERMES> skills --help
<HERMES> skills list
```

`<HERMES>` is the verified executable. These are discovery shapes, not commands executed
by this sheet or authority to launch a chat. Obtain version identity through the installed
build's documented interface; do not invent flags. The upstream skills guide documents
`hermes skills list`, while the actual profile/cwd/filters determine what it lists.
Do not run setup, update, login, installation, trust changes, config setters or gateway
start/restart to make discovery pass. Stop the affected path on a missing interface,
permission refusal or unusable approved provider; report the actual error without secrets.

## Skill discovery and body loading

The official [working-with-skills guide](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/guides/work-with-skills.md)
and [skills-system reference](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md)
distinguish an index from loaded instructions:

| Input | Documented discovery and qualification limit |
|---|---|
| Profile-local skills | The conventional root is `~/.hermes/skills/`, under the effective Hermes home/profile. Skills are directories containing `SKILL.md`, optionally grouped in categories with references or other support files. Record the selected root and actual file, not just this convention. |
| Project-local skills | Current upstream documents `<PROJECT_ROOT>/.hermes/skills/` and `<PROJECT_ROOT>/.agents/skills/`. The project root is the nearest ancestor containing `.git`, including worktrees/submodules. Discovery requires existing project trust and enabled `skills.project_discovery`; arbitrary repositories are not automatically trusted. Non-interactive surfaces inherit trust, not permission to create it. |
| Configured roots | Existing `skills.create_dir` and `skills.external_dirs` can contribute skills. Missing external paths are silently skipped. A user-level `.agents/skills` location is not automatically proof of Hermes discovery: verify its actual configuration/source. Do not add roots under this sheet. |
| Selection and collisions | Current documented precedence is project, profile-local, creation directory, then external directories. Higher-precedence copies shadow lower ones; ambiguous different skills within one directory require their exact relative names. Record warnings and chosen content hashes. |
| Visibility and restrictions | Platform/tool availability, disabled skills, project trust and scan-time quarantine can exclude a skill. A trusted repository is not a guarantee that every skill passed scanning. Inspect the actual index and load result; do not bypass a refusal. |
| Staged candidate | `skills/acd-orca/` is source in this repository, not an installed skill root. Its presence does not expose `acd-orca` to Hermes or replace legacy `acd` or `fleet-campaign`. |

The documented progressive-disclosure interfaces are:

- `skills_list()` returns the compact name/description/category index. Startup index
  inclusion is not full `SKILL.md` injection.
- `skill_view(name)` loads a selected skill's full content when requested.
- `skill_view(name, file_path)` loads a particular support/reference file when requested.
  A loaded entrypoint does not prove that its linked references or fleet SOUL were read.

The skills guide also describes slash invocation of installed skills. Verify that the
actual surface exposes that command before relying on it: current CLI documentation
limits the gateway-backed classic CLI's slash registry, while the TUI has a broader
registry. Never inject a slash command into another worker's terminal to steer it.
Plugin-provided skills can be explicitly namespaced and absent from the ordinary index;
a missing index entry alone is not proof that every possible loader is unavailable.

External roots are **not a read-only boundary**. Upstream documents that `skill_manage`
can modify existing skills where found if the process can write there. Do not expose
shared or installed instructions to unapproved maintenance, install a plugin, or weaken
permissions to satisfy the checklist. Preserve existing skills and role files.

## Explicit preload and context files

The official [CLI reference](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/user-guide/cli.md)
documents explicit `-s` skill names, including repeated or comma-separated names, rendered
into the session prompt before its first turn. It also documents profile-scoped
`skills.auto_load` for new sessions. These are supported loading mechanisms to discover,
not instructions to change launch arguments or configuration here. Verify that Orca's
actual launch passes the approved setting and that the selected bytes reached the session.
Do not infer automatic Orca startup injection from a later successful `skill_view`.

The current CLI reference says missing/disabled auto-load entries warn and are skipped;
`--ignore-rules` or `HERMES_IGNORE_RULES=1` skips auto-load and context/memory injection,
while explicit `-s` skills still load. Record relevant effective controls and any skipped,
shadowed or truncated input. Do not use those controls to bypass campaign instructions.
Config presence is not actual use, and changing a file does not prove an existing
conversation refreshed it. The skills guides describe differing cache/update behavior
across surfaces and versions; preserve observed behavior rather than reset a real chat.

The official [prompt-assembly reference](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/developer-guide/prompt-assembly.md)
describes a separate context-file path:

| Context source | Documented startup rule |
|---|---|
| Hermes project context | `.hermes.md` or `HERMES.md`, discovered from cwd toward the Git root, takes precedence. |
| Compatible project context | Otherwise `AGENTS.md` in startup cwd, then `CLAUDE.md`, then Cursor rules in cwd; first matching project context type wins, not all types concatenated. Later subdirectory discovery is not proof that parent instructions were present at startup. |
| Identity | `SOUL.md` in the effective Hermes home is loaded separately when present and enabled. It is not automatically the repository's assigned fleet SOUL. |
| Limits | Context inputs can be scanned, blocked or truncated; skip-context/ignore controls and embedding behavior can alter loading. Record the effective content, not an assumed full-file injection. |

Do not equate a repository SOUL path, Bot home, Hermes profile, primary checkout and
worker cwd. An Orca wrapper may supply additional instructions; its actual session
receipt, not a filename convention, establishes what arrived. Existing fleet role files
still name `.agents/skills/fleet-campaign/SKILL.md`; follow
[the loading boundary](../roles.md#loading-and-portability). This sheet does not repoint
those files, copy personas, install the candidate or claim standalone distribution.

## Instruction and model receipts

Before relying on a future authorized Hermes session, retain a private loading receipt:

1. Host/profile/cwd, executable/build and actual Orca surface; relevant launch controls
   and version-matched documentation/help identities.
2. Exact selected skill/context/role/common-policy paths and SHA-256 identities, discovered
   names, precedence, trust/filter state and warnings. Unknown observations are `null`
   with reason and timestamp, not assumed defaults.
3. Separate evidence for index visibility, startup/preload content, explicit body/reference
   reads and the assigned role's use. If prompt observability is missing or content is
   truncated, state that limit without exporting private prompts or unrelated memory.
4. Native Task/Dispatch/session correlation, the current delivered brief, actual returned
   worktree/base identity and sole-writer custody. A parent Bot's receipt does not establish
   its worker's loading, and Hermes-internal subagents are not Orca-native workers.

Apply [model identity](../handoff.md#model-and-review-identity) per purpose: requested,
resolved and observed actual model, authorized selection, profile/config provenance and
correlated sanitized outcome. A model picker, API-route configuration, banner or successful
primary response alone cannot qualify every auxiliary route. Inventory only purposes the
installed Hermes build actually uses; do not import OMP judge/smol flags or assume those
names exist in Hermes. An unused purpose is explicitly unused; an unknown one stays unknown.
Used auxiliary inference requires its own actual correlated evidence. Unresolved required
auxiliary use limits unattended claims.

Provider authentication must be evidenced on the approved route without printing credentials.
Installed availability does not prove sign-in or successful task-relevant tool use. On actual
model mismatch, primary failure or permission denial, stop the affected path for native
escalation; no blind retry, silent model/provider switch or sign-in repair. Reuse valid
same-environment evidence where available, rather than repeating paid greetings. A future
Hermes review route requires separate authorization and qualification under code review,
not transfer of the accepted OMP ACP result.

## Four permission scopes

Record effective value, observation time, source and enforcement limits separately for:

| Scope | Required distinction |
|---|---|
| Bot defaults | What a new conversation would inherit, including Bot overrides; not the mode of an existing chat. |
| Existing chats | The selected chat's actual mode; default changes do not migrate it. |
| Engine-specific launch override | Whether an override exists and the actual Hermes arguments/environment/tool/backend controls; do not treat the OMP-specific override as a Hermes setting. |
| Existing workers | Each worker's own effective launch/permissions and observed outcomes; parent settings or later changes do not establish these. |

The official Orca supported-agent page describes permission-bypass defaults, including
Hermes `--yolo`; that is a discovery warning, **not a recommendation to enable it**.
The [Orca security page](https://orca.dev/docs/bots/security) distinguishes enforced
controls from instructions and says available approval modes depend on the agent.
Do not infer a Hermes sandbox or approval guarantee from another engine's labels.
Individual approval is not Full access; Full access is optional, not a qualification
prerequisite. Owner-only creation/permission actions cannot be impersonated.

Disclose runtime/OS enforcement, operational tool restrictions and instructed read-only
behavior separately. A disposable worktree is not OS isolation. If a required denial
scenario cannot be exercised safely under current authority, record UNTESTED with reason;
do not loosen permissions, answer another agent's permission menu or fabricate a refusal.
Any broader future-engine permission scope needs disclosure and actual authority.

## Native qualification checklist

A later authorized isolated qualification must bind each row to Hermes's own environment,
versions, configuration, scenario and exact source/evidence hashes. Reuse only matching
accepted receipts. This checklist is not an instruction to run the scenarios now.

| Capability | Required observed evidence |
|---|---|
| Loading | Selected role, common policy, mandate, skill body and necessary references actually available in the execution session; startup and later reads distinguished. |
| Primary and tools | Approved actual provider/model performs a task-relevant assistant/tool interaction with correlated outcomes, not merely help, a greeting or a launch acknowledgment. |
| Auxiliary use | Actual purpose-specific evidence for every used required route, with unused and unknown separated. |
| Permissions | Four scopes above, actual effective restrictions and authorized denial behavior without bypass. |
| Native communication | Discovered session/output, delivered current brief, correlated native question/reply and result reaching the correct owner. Stored mail is not proof of action. |
| Continuation | Real native result wake and exact-owner one-shot deadline handling/cleanup without operator nudges; configured timers or Hermes background notifications alone are insufficient. |
| Acceptance | Actual blocked, never-ready, never-dispatched product gate; successful analysis containing FAIL/INCONCLUSIVE leaves the successor unready. Only the coordinator may complete the gate with required bound evidence. |
| Useful implementation | Production-path outcomes, independent exact-source review, distinct required API evidence, authorized integration and actual resulting-source smoke under [stage ordering](../runtime-review-and-integration.md#exact-candidate-and-stage-ordering). |
| Recovery | Authorized cases for unknown launch/no duplicate, denied permission/no bypass, pause/late reply/deadline/no self-resume and stale source/no reused verdict. Missing safe fault injection stays UNTESTED. |
| Retention and release | Dirty/untracked source and evidence durably preserved before possible automatic release; guarded stop, physical exit and native resource release observed separately. Unknown release blocks reuse. |

Use [Orca-native communication and waiting](../orca-runtime.md#native-communication-and-waiting),
not the legacy Hermes terminal `notify` watcher, heartbeat/controller or session-log polling
recipe. Do not add Hermes cron, loops, gateway automation or a second scheduler to imitate
Orca wakes. The current Hermes CLI documentation notes that closing a gateway-backed
terminal can detach while accepted work continues: terminal closure or process activity
is not completion. Follow the native guarded stop/release receipt, not a guessed terminal
teardown. No gateway/service start or restart is authorized here.

Keep observed activity, assistant success, completed tool and semantic task progress
separate under [progress semantics](../state-and-recovery.md#observation-and-semantic-progress).
Do not apply OMP event-schema success mappings to Hermes without observed schema evidence.
Native wakes may arrive late; preserve original clocks and check actual UTC before affected
dispatch, integration and gate completion. A late deadline cannot authorize retry, kill,
resume or acceptance. No reboot/process-death recovery or broad unattended reliability
claim follows from a successful loading test.

## Qualification disposition and staging

Report each capability independently as QUALIFIED only within accepted evidence scope,
BLOCKED when an observed prerequisite/refusal prevents the required path, UNAVAILABLE
when actual discovery establishes absence or unsupported capability, or UNTESTED when
not exercised. Missing observations remain `null`; unqualified is not a hidden PASS.
Documentation support and local availability are separate facts from all four outcomes.
Do not erase independently supported OMP deliverables because optional Hermes is unavailable.

[Legacy operational mechanics](../../../acd/references/hermes-orca-omp.md) and the
[obligation ledger](../obligation-ledger.md#reference-obligations) retain migration
provenance, not active terminal/START/fallback instructions. Earlier provider-pending
labels are historical; current scoped readiness belongs to code review and never qualifies
Hermes. Final cross-document acceptance must reconcile those separately owned ledger bytes.

Placeholder inventory: `<HERMES>` is the discovered executable; `<PROJECT_ROOT>` is the
actual discovered Git project root. Conventional tilde/relative paths are documentation,
not private host bindings. No private runtime IDs, model routes or credentials belong in
this portable sheet. No link to an unauthored engine or template is added here; the future
Codex sheet, templates, validation reference and entrypoint remain separate pending work.
Final zero-missing-link and exact-manifest review, independent document acceptance and
any later runtime qualification remain separate. This sheet's author completion cannot
release a successor or install the staged candidate.
