# Autonomous Campaign Development on Orca

**[acd-orca](skills/acd-orca/SKILL.md) 1.0.0** is an instruction skill for
evidence-led development campaigns: capture intent, design a small plan, obtain
independent review, implement in native OMP worktrees, test, review with roborev,
and integrate within the owner's delivery authority.

It is **not a server, daemon, scheduler, or validator application**. Installing it
starts no work and grants no permissions. Supervision uses native Orca tasks,
events and Automations with transient supervised OMP executions, independent
reviewers, and explicit release/exit receipts—not a homemade watcher or a fresh
persistent Bot chat for every code review.

Legacy **[acd 1.7.0](#legacy-acd-170)** remains available unchanged. These are two
skill versions, not a new global package version. [MIT license](LICENSE).

## Prerequisites

- [Orca](https://orca.dev/docs/agents/native-chat) with native OMP execution,
  worktrees, tasks/events and the permissions needed for the approved project.
  Resolve the actual executable on the execution host/container; do not assume
  every Linux `orca` is a screen reader or every installation uses `orca-ide`.
- [OMP](https://github.com/can1357/oh-my-pi) with skill discovery enabled and an
  approved model that actually completes the required tool calls in that environment.
  Record requested, resolved and observed model identities privately. Qualify any
  auxiliary model purpose used; primary-model success does not prove it works.
- Git, a target repository, and access to its real build/test/runtime surfaces.
  The Linux installation recipe below uses Bash and GNU coreutils.
- An independent **roborev → native OMP ACP** review route. The evidenced composition
  used roborev 0.75.0, OMP 19.1.1 and `acp.omp`; shared-home discovery was exercised
  with Orca 1.4.268. These are observed versions, not universal compatibility claims.
  Follow the [review contract](skills/acd-orca/references/code-review.md): use a
  neutral exact-candidate snapshot, an approved model/tool route, scoped capability
  evidence and raw findings. A configured model, help output or exit zero is not PASS.

Only OMP has operational evidence here. The
[Hermes](skills/acd-orca/references/engines/hermes.md) and
[Codex](skills/acd-orca/references/engines/codex.md) sheets are guidance, not parity
qualification. No models, credentials, reviewer binaries or automatic setup are bundled.
Python is needed only for the [optional local checks](#optional-local-checks).

## Install: preserve the dependency tree

**Do not copy only `skills/acd-orca`, or assume `npx skills add … --skill acd-orca`
alone is qualified.** Its relative links require both `fleet/` source and legacy
`skills/acd/` migration documents. Keep a complete, durable repository-shaped tree.
Orca `skills install` handles bundled skills, not this custom package. No native
Orca skill-share cloud publication is supplied; a GitHub push is not cloud publication.

The successful shared-home installation used a durable tree plus:

| Discovered path | Target / purpose |
|---|---|
| `~/.agents/skills/acd-orca` | Tree's `skills/acd-orca`; new skill |
| `~/.agents/fleet` | Tree's `fleet`; dependency-only bridge, not live Bot setup |
| `~/.agents/skills/acd` | Existing legacy files, preserved and hash-matched to the tree |

OMP retains the lexical discovered base directory. Consequently an external
`../../fleet` link needs the shared-root bridge even when `acd-orca` is a symlink.
The fresh-install recipe below supplies legacy `acd` as a third link **only when
all three names are absent**. An existing skill, directory or dangling symlink is
a collision: stop, compare contents and explicitly arrange a backup/migration.
Never overwrite an existing `acd` installation to make this recipe pass.

### Linux fresh install

Choose a reviewed, available full commit from this repository and set
`ACD_ORCA_REVISION` to its 40-character SHA. It must contain the complete dependency
tree. Review the source before enabling it as agent instructions. Run these blocks
in the same Bash shell on the host/container whose home OMP actually uses.

```bash
set -euo pipefail
repo="$HOME/.local/share/acd-orca/repo"
revision="${ACD_ORCA_REVISION:?Set a reviewed full commit SHA first}"
[[ "$revision" =~ ^[0-9a-f]{40}$ ]] || { echo 'STOP: invalid commit SHA' >&2; exit 1; }
for path in "$repo" "$HOME/.agents/skills/acd-orca" \
  "$HOME/.agents/skills/acd" "$HOME/.agents/fleet"; do
  if [[ -e "$path" || -L "$path" ]]; then
    printf 'STOP: existing path: %s\n' "$path" >&2
    exit 1
  fi
done
mkdir -p "$(dirname "$repo")"
git clone https://github.com/megastruktur/autonomous-campaign-development.git "$repo"
git -C "$repo" checkout --detach "$revision"
test "$(git -C "$repo" rev-parse HEAD)" = "$revision"
```

Then create guarded exact links. `ln -sT` has no force option: an intervening
collision fails instead of overwriting or nesting a link inside an existing directory.

```bash
set -euo pipefail
repo="$HOME/.local/share/acd-orca/repo"
for file in skills/acd-orca/SKILL.md skills/acd-orca/references/engines/omp.md \
  skills/acd/SKILL.md fleet/skills/fleet-campaign/references/common-contract.md; do
  test -f "$repo/$file" || { printf 'STOP: missing dependency: %s\n' "$file" >&2; exit 1; }
done
for path in "$HOME/.agents/skills/acd-orca" "$HOME/.agents/skills/acd" "$HOME/.agents/fleet"; do
  if [[ -e "$path" || -L "$path" ]]; then
    printf 'STOP: existing path: %s\n' "$path" >&2
    exit 1
  fi
done
mkdir -p "$HOME/.agents/skills"
ln -sT "$repo/skills/acd-orca" "$HOME/.agents/skills/acd-orca"
ln -sT "$repo/skills/acd" "$HOME/.agents/skills/acd"
ln -sT "$repo/fleet" "$HOME/.agents/fleet"
```

Keep the checkout at that revision, not on an automatically updated branch.
If interrupted, inspect any links already created; do not rerun with force.
This non-network link block was exercised in an isolated temporary home with the
full tracked tree, missing-dependency cases and name collisions—not against a real home.
The clone step still requires network access and availability of the selected commit.

### Verify discovery and actual loading

Use the resolved executables in the actual execution host/container and project cwd:

```bash
orca skills installed --json
omp skill list --json
```

Check the main UI **Skills** entry `acd-orca` and OMP's selected path/source for
collisions. In a **fresh native OMP session**, ask the agent to use its read tool on:

```text
skill://acd-orca
skill://acd-orca/references/engines/omp.md
```

Read external links as ordinary filesystem paths resolved from the discovered
base directory, for example `~/.agents/fleet/skills/fleet-campaign/references/common-contract.md`
after expanding the home path. Do not use `skill://../` traversal. Compare body and
reference hashes to the pinned tree. Fresh native body/reference reads and the external
common-contract read have been exercised against the installed layout; discovery,
body loading and useful task behavior remain three separate claims.

Long-running chats do not automatically replace instructions already consumed.
Start a fresh session after an approved update. See the
[OMP loading sheet](skills/acd-orca/references/engines/omp.md) and
[upstream skills guide](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md).
No invented slash command or hidden `.local` receipt is required to read the skill.

## Practical usage

Give the project coordinator an outcome, repository, constraints and delivery boundary.
Use reasonable bounded slices; do not manufacture a large DAG for a trivial fix.
The normal sequence is intent and repository discovery → small evidence-backed plan →
independent design critique → native OMP worktree implementation → tests and real-runtime
proof → independent roborev review → authorized integration and post-integration smoke.
Use the [planning](skills/acd-orca/references/planning-and-design.md),
[handoff](skills/acd-orca/references/handoff.md) and
[runtime/integration](skills/acd-orca/references/runtime-review-and-integration.md)
contracts with the current mandate, not a replay of frozen campaign amendments.

Example captain prompts:

> Read acd-orca and the references needed for this project. Add CSV export to the
> existing reports screen. Reuse the repository's patterns, keep dependencies unchanged,
> plan small bounded slices and obtain independent design and code review. I authorize
> implementation, real-runtime tests and MERGE to the named target branch after the
> gates pass. No PUSH or deployment. Proceed without routine intermediate approval
> questions inside this scope; report evidence for one final owner review.

> Use acd-orca to investigate and plan resumable uploads. Inspect the repository,
> research reuse options and obtain independent design critique. Planning only:
> no implementation, worktree launch, merge, push or deployment. Return the proposed
> acceptance criteria and risks so I can decide whether to authorize execution.

> Resume the authorized campaign from its durable state. Reconcile existing native
> tasks and worker exit/release evidence before starting replacements. Continue only
> unfinished work under the original constraints; preserve unrelated live work.
> Stop at a reviewed local commit—no merge, push or deployment.

The normal delivery boundary is **MERGE only when authorized**; PUSH and deployment
need separately named authority. Narrower or broader mandates are possible. No prompt
grants automatic destructive permissions or bypasses repository policy, hooks or runtime
approval controls. Within a fully authorized campaign, use one final owner review, not
routine human gates between every slice; an actual blocker or changed scope still escalates.

### Role setup is separate

Six Mechanicus-named role definitions are included: Magos Logis II, Logis Intent,
Logis Architect, Inquisitor Ferrum, Inquisitor Intent and Magos Fleet. See the
[role index and source SOUL links](skills/acd-orca/references/roles.md) and the
[Project Magos template](fleet/templates/magos-project/SOUL.md).
Installing the skill does not create or reconfigure these Bots. The owner must arrange
private peer bindings, actual role loading and one execution coordinator per project.
Missing or conflicting bindings block mutation; names alone are not identities.

Existing SOUL references to `fleet-campaign` are historical loading paths, not
automatically repointed to `acd-orca`. The fleet bridge exposes source dependencies,
not live configuration. Do not publish live bindings, chats, credentials or runtime state.

## Optional local checks

Python **3.11+**, standard library only. From this repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s qualification/manifest-validator -p 'test_*.py' -v
python qualification/manifest-validator/cli.py --help
```

The reviewed source passed **155 legacy tests and 60 pilot tests** with Python 3.14.9.
The legacy watcher test can emit unclosed `TextIOWrapper` ResourceWarnings while the
suite passes; those warnings are not a product failure. The CLI help command was also
executed. These checks do not replace a target project's runtime proof or independent review.

The [manifest validator](qualification/manifest-validator/validator.py) and
[CLI](qualification/manifest-validator/cli.py) are an **optional qualification example**:
they check a pinned local packet for consistency, not code authenticity or product
acceptance. Consult the [validator tests](qualification/manifest-validator/test_validator.py)
and [CLI tests](qualification/manifest-validator/test_cli.py) for the input contract and
examples. You can use the skill without running the validator.

CuteCare is pilot-project context only. This repository did **not** build or deploy a
complete CuteCare product or run its actual business tasks. Attaching connectors and
manual testing remain the captain's responsibility.

## Limitations, updates and uninstall

- Frozen `fleet/` campaigns/amendments and staged/uninstalled/PENDING wording in the
  immutable source are migration provenance. Installation and fresh loading were
  evidenced separately; those historical labels neither undo the installation nor
  authorize a new campaign. They do not establish universal engine qualification.
- Independent reviewer restrictions are not necessarily OS-enforced confinement.
  Static checks, synthetic qualification and successful analysis delivery are not
  product acceptance. Preserve exact-source, runtime and review evidence separately.
- Native worker completion or end-turn does not prove process exit. Do not promise
  that closing a tab kills OMP or `agentSession.release` unloads everything. For
  inaccessible Groups, the owner UI route is **Sleep → This Workspace**, only after
  source/evidence preservation and ownership checks. Exclude user-owned live work.
- Updating means reviewing a new pinned tree, comparing dependencies and existing
  local changes, explicitly approving any link repointing, then verifying discovery
  and reads in a fresh session. Do not `git pull` beneath active installed links.

To uninstall, first inspect with `readlink` each link created by your installation:
`~/.agents/skills/acd-orca`, `~/.agents/fleet`, and (fresh recipe only)
`~/.agents/skills/acd`. Unlink only names whose exact targets still equal your recorded
targets and whose dependencies are no longer in use. Never remove a pre-existing legacy
`acd`, another installation's bridge, or live project work. Keep the durable checkout
until nothing references it; removing discovery links does not unload existing chats.

## Legacy acd 1.7.0

The unchanged [legacy skill](skills/acd/SKILL.md) describes the Hermes-planner/OMP
workflow, explicit planning approval plus a separate fresh-session START, OCR-first
review, and bounded watcher/native-heartbeat alternatives. Its optional standard-library
observer scripts do not run merely because the skill is installed.

Use its own [handoff and START contract](skills/acd/references/handoff-and-start.md),
[OCR reference](skills/acd/references/ocr-review.md),
[wakeups](skills/acd/references/coordinator-heartbeat.md),
[observer usage](skills/acd/references/progress-watchdog.md), and
[state/recovery](skills/acd/references/state-and-recovery.md) for existing legacy
campaigns. Those mechanisms are **not acd-orca defaults**. Legacy source, templates,
scripts and [changelog](CHANGELOG.md) remain intact; do not migrate an existing campaign
or replace its installed skill without explicit authority and reviewed recovery state.
