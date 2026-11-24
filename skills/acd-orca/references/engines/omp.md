# OMP startup and capability evidence

This sheet covers OMP instruction discovery and execution-host evidence for the staged,
uninstalled candidate. It is not a launch authorization, installer, provider configuration
or second orchestration manual. Read [roles](../roles.md), the
[common fleet contract](../../../../fleet/skills/fleet-campaign/references/common-contract.md),
[handoff admission](../handoff.md#execution-admission) and
[Orca runtime discovery](../orca-runtime.md#discover-the-installed-interface) first.
Their ownership, bounds, native communication and source-retention rules still apply.

The [owner amendment](../../../../fleet/execution/fullauto/AMENDMENT_01_ROBOREV.md)
selects **roborev** for code review; historical OCR-first instructions in unchanged
shared/legacy sources are not operative. [Code review](../code-review.md) owns the
qualified provider protocol. Keep three identities separate: OMP as the implementation
agent, roborev as the review provider, and OMP as the separately qualified ACP execution
engine. Sharing a binary or model does not permit sharing the implementer's context.

## Discover the actual execution environment

Resolve OMP inside the host/container and working directory that will execute the task,
not from another machine's PATH. Record executable identity/version/fingerprint, actual
host, OS user, cwd, active profile/agent directory, native worker identity and launch
surface privately. Orca's structured chat and terminal are different surfaces over an
agent; neither a model picker nor a visible tab proves the effective launch settings.
Use the installed Orca guides for native launch and returned receipts, not raw terminal
injection or a second ad-hoc OMP writer.

These read-only discovery shapes were available in OMP 19.1.1; verify them with the
installed version before use. `<OMP>` is the verified executable, not a literal command:

```text
<OMP> --version
<OMP> --help
<OMP> config --help
<OMP> skill --help
<OMP> skill list --json
<OMP> acp --help
```

Help establishes syntax, not model/tool/runtime success. Inspect only necessary
non-secret settings through supported narrow `config get` queries after help; never dump
auth files, all configuration or the environment. Do not run setup, install, login,
update, credential-export or permission-changing commands to make discovery succeed.
Missing identity/interface or a refusal is a scoped blocker, not permission to try
another host, engine, provider or credential route.

## Startup loading and discovery

OMP distinguishes context-file injection from skill discovery and body loading. The
[upstream skills guide](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md),
[configuration discovery guide](https://github.com/can1357/oh-my-pi/blob/main/docs/config-usage.md)
and [context-file guide](https://github.com/can1357/oh-my-pi/blob/main/docs/context-files.md)
describe the following locations and behavior. They are current upstream documentation,
not a promise that every installed version/profile has identical precedence. Match the
actual discovery result and launch controls before relying on a path.

| Input | Supported discovery and limit |
|---|---|
| Native authored skills | `<AGENT_DIR>/skills/<SKILL>/SKILL.md` at user scope; `.omp/skills/<SKILL>/SKILL.md` in discovered project ancestors. Native skill discovery walks ancestors within its repository/home boundary, unlike the nearest-directory rule for native context files. Conventional roots scan one directory level, not an arbitrary nested taxonomy. |
| Shared Agents skills | The `agents` provider supports `.agents/skills/<SKILL>/SKILL.md` and `.agent/skills/<SKILL>/SKILL.md` in its user/project roots. Verify source scope, resolved file and active source toggles; a directory name alone does not prove discovery. |
| Custom and other sources | Configured `skills.customDirectories` scan immediate child skill directories; enabled compatible providers/plugins and managed skills can also contribute. Inspect collisions, filtering and the selected file rather than assuming the bare name selects the intended copy. Do not add a custom directory or install a plugin under this sheet. |
| Native context | `<AGENT_DIR>/AGENTS.md` and the nearest non-empty ancestor `.omp/AGENTS.md`, subject to enabled discovery. The nearest non-empty `.omp` directory owns native project context; a missing `AGENTS.md` there does not cause fallback to a farther `.omp` directory. |
| Other project context | Standalone ancestor `AGENTS.md` and enabled compatible conventions use their own documented walks and precedence. Files at the same scope/depth can shadow one another. Do not equate the repository root, Bot home, primary checkout and actual worker cwd. |
| Staged candidate | `skills/acd-orca/` is repository source, not by itself an installed discovery root. File presence or a resolving Markdown link does not load its entrypoint or referenced instructions. |

`<AGENT_DIR>` means the effective OMP user agent directory, conventionally
`~/.omp/agent`, but relocatable by the active profile or `PI_CODING_AGENT_DIR`.
`<SKILL>` is the exact discovered skill name, including a resolved collision alias when
applicable. These are conventions/placeholders, not a private host path or an instruction
to move files. The current candidate remains `acd-orca`, separate from legacy `acd`.

At startup, enabled skills normally contribute **name/description metadata**, not their
complete bodies. The model loads a matching skill with the read tool at `skill://<SKILL>`;
assets under that skill use `skill://<SKILL>/<ASSET>`. `<ASSET>` is an existing relative
asset path inside its skill root. An enabled interactive `/skill:<SKILL>` command is a
user invocation, not a worker-to-worker steering channel or proof of startup injection.
Context files instead contribute their expanded instruction content at session opening.
A discovered catalog entry, successful body read and actual instruction use are separate
facts. Do not claim automatic loading of every linked reference or SOUL.

Record effective launch flags and discovery filters. In the inspected CLI,
`--no-skills` disables skill discovery/loading, `--skills` filters names, and
`--no-context-files` disables context-file loading; `--no-rules` is separate. Provider
and per-source settings, hidden skills, custom roots and collisions can alter the result.
`--cwd`, profile and `--config` overlays affect the environment being inspected. A
standalone `skill list` reflects that command's effective environment, not necessarily
an already-running worker with other flags. Never change controls merely to get a green
checklist or assume an existing session reloaded changed files.

Existing fleet SOULs still point to `.agents/skills/fleet-campaign/SKILL.md`; staging
neither repoints them nor migrates active Bots/chats. Follow
[the role loading boundary](../roles.md#loading-and-portability) for later authorized
cutover and rollback. Confirm the assigned role, common policy, current mandate and
required references inside each actual execution session; a parent Bot's loading receipt
does not establish its project worker's loading. OMP task-tool subagents are not Orca
native workers, and their context inheritance must not be assumed equivalent.

## Instruction loading receipt

Before relying on a session for an authorized task, retain a private receipt with:

- Actual host/profile/cwd and executable version, supported loader, relevant launch flags
  and settings provenance; unknown values are `null` with reason and observation time.
- Exact role/context/skill paths, source scopes and SHA-256 identities; catalog names,
  collisions/warnings and disabled or missing inputs. Preserve evidence of the selected
  content, not just the expected path.
- Distinct observations for injected context, discovered metadata, explicit skill/reference
  reads and the assigned role's use. Keep unrelated personal context and secrets out of
  exported receipts. Missing startup observability remains a stated limit.
- Native Task/Dispatch/session correlation and the delivered current task brief. Verify
  the returned worktree/branch/HEAD and sole-writer custody through the owning runtime
  reference; do not inherit an unrelated brief from the base checkout.

Use a fresh authorized session when changed startup inputs need observation; do not reset
other chats, rewrite installed SOULs or bypass permission to force reload. The isolated
roborev reviewer deliberately disables ambient context/skill discovery under its qualified
configuration and receives a neutral packet instead. That is a different purpose, not
proof that campaign instructions loaded in a development worker.

## Primary and auxiliary model checklist

Apply [model identity](../handoff.md#model-and-review-identity) separately for every
purpose and execution environment. Record requested, resolved and observed actual model,
selection authority, profile/config provenance, correlated invocation and sanitized
outcome. Explicitly unused is not unknown; unknown is `null`, never inferred success.

| Purpose | Evidence required before claiming it works |
|---|---|
| Primary author/planner | Approved request, exact resolved route, actual startup/session model and successful task-relevant assistant/tool interaction in this worker. Fuzzy model selection or launch argv alone does not prove which provider served inference. |
| Judge | Effective purpose-specific configuration plus an actual correlated judge call/outcome in the relevant fresh Bot or project-worker scope. A primary response or historical success in a different home does not qualify this route. |
| Smol | Effective lightweight-task route plus a successful actual smol-purpose invocation. An assigned fast model or its presence in configuration is not use; primary/judge success cannot substitute. |
| Other used auxiliary services | Inventory purposes that the installed runtime actually invokes, such as planning/slow routes or background services; bind each observed route/outcome rather than asserting all services use the primary. Do not trigger unused services just to fill a matrix. |
| Independent code reviewer | Roborev provider/version, OMP ACP execution-engine/version and requested/resolved/actual reviewer model in a new neutral context, with the evidence required by [code review](../code-review.md#raw-result-and-coverage-receipt). Author-model health does not qualify review. |

The inspected OMP help exposes `--smol`, `--slow` and `--plan`; it does not make every
auxiliary purpose a CLI flag. Discover the actual judge configuration rather than inventing
`--judge-model`. In this version `--no-judge` restricts judge calls to the active model's
provider; it is **not** proof judge inference is disabled. Likewise `--offline` restricts
auxiliary providers and is explicitly **not a network firewall**. `--models` lists models
for cycling, not automatic fallback. Presence of any option is not authorization to use it.

Primary failure, actual-model mismatch or a permission refusal stops the affected path
for native escalation and reconciliation. No silent model switch, blanket retry or
configuration repair. Reuse accepted same-environment purpose evidence where valid;
do not repeat paid greetings. Unresolved auxiliary use bars robust unattended claims
for that path without erasing independently supported observations.

## Four permission scopes

Inspect and record these separately, with timestamp, actual effective value, evidence and
whether enforcement is runtime/OS-backed, operational tool restriction or instruction-only:

| Scope | Required distinction |
|---|---|
| Bot defaults | What new conversations inherit, including any Bot-specific override; not proof of an existing chat's mode. |
| Existing chats | The selected coordinator/planner chat's actual current mode; changing a default does not migrate it. |
| Engine-specific OMP launch override | Effective engine arguments/settings for the intended launch, including approval/tool controls; not a grant from the task prose. |
| Existing workers | Each live worker's own launch/effective permissions and observed outcomes; neither parent chat nor a later setting change establishes these. |

Individual approval is not Full access. Full access is optional, not a prerequisite to
manufacture; owner-only creation/permission actions cannot be impersonated. Any requested
broader future-engine scope needs explicit disclosure and authority. Follow the installed
interface and [Orca security documentation](https://orca.dev/docs/bots/security), not a
cross-engine assumption about what an approval label enforces.

The inspected OMP help exposes tool and approval controls, but a read-only prompt, a
restricted tool list or ACP plan negotiation is not OS confinement. The accepted review
route establishes operational restrictions, not adversarial write/execute/outside-root
denial. Do not add auto-approval, loosen permissions or answer another agent's permission
menu to clear a blocker. Required denial scenarios need separately authorized disposable
runtime evidence; unsafe/unavailable injection remains UNTESTED, not a fabricated PASS.

## Qualification boundary and progress

The frozen planning evidence established historical OMP native transport: correlated peer
and deadline handling plus a worker result/wake/release. It did **not** establish useful
development, review, auxiliary parity or recovery acceptance. Preserve that historical
scope rather than upgrading it because a newer command works.

Later accepted evidence separately qualified **roborev 0.75.0 to OMP 19.1.1 via native
ACP**, configured as `acp.omp`, on the recorded host and actual Orca-container environment.
Its fresh approved model sessions exercised clean and known-defect/error fixtures.
Reuse only the accepted private receipt's exact scope under
[provider admission](../code-review.md#authorized-preflight-before-coding); this is not
full OMP development qualification, product acceptance, OS sandboxing, auxiliary inference,
Hermes/Codex parity or production-scale reliability. An earlier ledger's pending-provider
wording is historical and awaits its separately owned amendment, not a reason to rerun
qualification or restore OCR.

Keep transport, successful assistant response, completed tool and semantic task progress
separate under [progress semantics](../state-and-recovery.md#observation-and-semantic-progress).
The legacy observed OMP session-format-3 mapping treated `stop`/`toolUse` without an
`errorId` as assistant success, `error`/`aborted` as failure and authoritative `isError`
strictly false as tool success. Verify the current schema before applying that mapping;
missing outcomes stay unknown. Usage/title/compaction events, discarded branches, PID or
log growth do not prove progress. Provider errors require session correlation. ACP
`end_turn` and exit zero are not proof of successful provider inference or review PASS.
A checkpoint needs current task/attempt/session/candidate, criterion and inspected evidence;
a producer's assertion or stale/replayed checkpoint cannot qualify current work.

Before a broader working-pipeline claim, require actual same-environment loading,
purpose-model/tool evidence, useful production-path runtime results, exact-source
independent review and API evidence, integration/smoke, native blocked-gate transitions,
required negative/recovery cases and source-preserving stop/release. Apply
[stage ordering](../runtime-review-and-integration.md#exact-candidate-and-stage-ordering).
Unavailable, blocked and untested rows remain explicit; each other engine needs its own
matrix. Analysis delivery or this document's acceptance cannot release a successor:
only the coordinator can complete the separate blocked, never-dispatched acceptance gate
with its required bound evidence.

## Sources and staging

[Legacy operational mechanics](../../../acd/references/hermes-orca-omp.md) and
[legacy progress semantics](../../../acd/references/progress-watchdog.md) are migration
sources, not executable terminal, watcher, START or fallback recipes. The
[obligation ledger](../obligation-ledger.md#reference-obligations) retains their identities.
Native communication, original clocks, uncertain-launch reconciliation and cleanup stay
in [Orca runtime](../orca-runtime.md); this sheet adds no supervisor or session-log parser.
[Orca native chat documentation](https://orca.dev/docs/agents/native-chat) describes the
surface, not qualification of this candidate or permission to launch another session.

Placeholder inventory: `<OMP>`, `<AGENT_DIR>`, `<SKILL>` and `<ASSET>` have the meanings
defined above. Conventional tilde/project paths are documentation, not live host bindings.
This sheet adds no link to an unauthored engine/template. The planned candidate entrypoint,
other engine sheets and validation reference remain PENDING future artifacts at this
slice; final exact-manifest/link/template review is separate. Existing loading paths and
legacy files remain unchanged. No installation, publication, broad reboot recovery or
future-candidate acceptance follows from these instructions.
