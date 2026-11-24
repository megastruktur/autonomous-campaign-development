# Set up a project-first Orca fleet

Install once per execution computer, share five planning Bots across projects, and give
 each project one PROJECT Magos. You send work to that project Bot, not manually to Logis.
This guide configures instructions; it does not grant access or prove runtime readiness.

## 1. Prerequisites on the execution computer

- Install and open [Orca](https://orca.dev/), then follow its
  [Bot setup](https://orca.dev/docs/bots) and [security guidance](https://orca.dev/docs/bots/security).
- Install [OMP](https://github.com/can1357/oh-my-pi), authenticate your chosen provider
  using its supported login/configuration flow, and select an available approved model.
  Do this on the computer/container selected for execution, not just your laptop.
- Install [roborev](https://www.roborev.io/) using its official installation instructions;
  configure its [native ACP client](https://www.roborev.io/docs/advanced/acp.md) for OMP below.
- Have Git, Bash and GNU coreutils (`ln -sT`), a local project checkout, and its actual
  build/test commands. Python 3.11+ is only needed for this repository's optional tests.

Inspect `orca --help`, `omp --help`, `omp acp --help`, `roborev --help` and
`roborev review --help` on that computer. A missing executable stops setup; install it
through its official instructions, not a fallback engine. OMP is the supported path;
Hermes/Codex guidance does not establish parity. Do not print credentials into a chat.
Bot permissions and the non-Bot OMP worker override are separate. Check permissions in a
fresh worker as well as the Bot chat; Full access is not assumed or required by this guide.

## 2. Clone, review and pin the complete tree

**Existing installation? Stop and compare first.** Never force these links, overwrite a
SOUL, or pull underneath active installed links. Review a separate new tree, compare local
changes, obtain explicit backup/migration approval, then verify fresh-session loading.

Download without enabling instructions. These network commands are owner-run, not exercised
by the offline tests. Run in Bash; an existing destination (including dangling links) stops:

```text
set -euo pipefail
repo="$HOME/.local/share/acd-orca/repo"
command -v git >/dev/null || { echo 'STOP: install Git'; exit 1; }
[[ ! -e "$repo" && ! -L "$repo" ]] || { echo 'STOP: existing checkout'; exit 1; }
mkdir -p "$(dirname "$repo")"
git clone https://github.com/megastruktur/autonomous-campaign-development.git "$repo"
git -C "$repo" rev-parse HEAD
```

Review that downloaded commit and confirm it includes this guide and the full dependency
tree. Record its full SHA as `ACD_ORCA_REVISION`; do not invent a release SHA. Pin it:

```text
export ACD_ORCA_REVISION='<reviewed-40-character-SHA>'
[[ "$ACD_ORCA_REVISION" =~ ^[0-9a-f]{40}$ ]] || exit 1
git -C "$repo" checkout --detach "$ACD_ORCA_REVISION"
test "$(git -C "$repo" rev-parse HEAD)" = "$ACD_ORCA_REVISION"
```

Keep the whole tree: `skills/acd-orca`, legacy `skills/acd` dependencies and `fleet`.
Do not copy only SKILL.md or use an unverified single-skill installer. The lexical OMP
shared-root discovery path needs the fleet bridge even when the skill is a symlink.
Run this **offline install block** only after review/pinning (fresh names only):

```bash
# install-shared
set -euo pipefail
for tool in ln mkdir; do
  command -v "$tool" >/dev/null || { echo "STOP: missing executable: $tool" >&2; exit 1; }
done
repo="$HOME/.local/share/acd-orca/repo"
for file in skills/acd-orca/SKILL.md skills/acd-orca/references/engines/omp.md \
  skills/acd-orca/references/code-review.md skills/acd/SKILL.md \
  fleet/skills/fleet-campaign/SKILL.md fleet/skills/fleet-campaign/references/common-contract.md; do
  [[ -f "$repo/$file" ]] || { echo "STOP: missing dependency: $file" >&2; exit 1; }
done
for path in "$HOME/.agents/skills/acd-orca" "$HOME/.agents/skills/acd" "$HOME/.agents/fleet"; do
  [[ ! -e "$path" && ! -L "$path" ]] || { echo "STOP: existing path: $path" >&2; exit 1; }
done
mkdir -p "$HOME/.agents/skills"
ln -sT "$repo/skills/acd-orca" "$HOME/.agents/skills/acd-orca"
ln -sT "$repo/skills/acd" "$HOME/.agents/skills/acd"
ln -sT "$repo/fleet" "$HOME/.agents/fleet"
```

Missing dependency means obtain the complete reviewed tree, not skip the check. Existing
files, directories, valid or dangling symlinks are collisions. Reruns deliberately stop.
If interrupted, inspect any links already created; never retry with `-f` or delete blindly.

## 3. Create five shared Bots and one project Bot

Owner UI: **Bots → + (New bot or group) → New bot → Start from scratch → name/purpose →
Change** (select computer and OMP agent) **→ Create**. The agent must already be installed
and authenticated on that computer. These are documented UI labels, not an automated installer.

Create these five once, using the corresponding complete SOUL text:

| Shared Bot | Source |
|---|---|
| Magos Logis II | [Canonical planning synthesizer](../fleet/bots/logis/SOUL.md) |
| Logis Intent | [Product contributions](../fleet/bots/logis-intent/SOUL.md) |
| Logis Architect | [Technical contributions](../fleet/bots/logis-architect/SOUL.md) |
| Inquisitor Ferrum | [Independent technical critique](../fleet/bots/inquisitor-ferrum/SOUL.md) |
| Inquisitor Intent | [Independent outcome critique](../fleet/bots/inquisitor-intent/SOUL.md) |

Create **Magos YOUR_PROJECT** using the complete
[Project Magos SOUL](../fleet/templates/magos-project/SOUL.md). Replace only both occurrences
of `{{PROJECT_NAME}}` with its display name; do not insert repo paths or IDs in portable voice.
[Magos Fleet](../fleet/bots/magos-fleet/SOUL.md) is the coordinator for fleet development,
not an extra required owner. Add another project Magos, not another copy of all five shared Bots.

Bot homes are `~/.orca/bots/<name>` on the selected execution computer; verify the actual
folder name, not a display-label guess. Before replacing an existing generated SOUL, compare
it with the source, save an owner-approved backup outside the destination and explicitly approve
replacement. The following block intentionally refuses existing SOULs, including generated ones.
For a new/approved empty destination, set `BOT_HOME` to the verified absolute Bot home and
`SOUL_SOURCE` to a reviewed complete SOUL file (a renamed private copy for PROJECT Magos).
Both variables must be exported. Run once for each Bot:

```bash
# install-bot
set -euo pipefail
for tool in ln mkdir cat; do
  command -v "$tool" >/dev/null || { echo "STOP: missing executable: $tool" >&2; exit 1; }
done
repo="$HOME/.local/share/acd-orca/repo"
: "${BOT_HOME:?Set verified absolute Bot home}" "${SOUL_SOURCE:?Set reviewed SOUL source}"
[[ "$BOT_HOME" = /* && -d "$BOT_HOME" && -f "$SOUL_SOURCE" ]] || { echo 'STOP: invalid Bot inputs' >&2; exit 1; }
[[ -f "$repo/fleet/skills/fleet-campaign/SKILL.md" ]] || { echo 'STOP: missing bridge' >&2; exit 1; }
for path in "$BOT_HOME/.agents/skills/fleet-campaign" "$BOT_HOME/SOUL.md"; do
  [[ ! -e "$path" && ! -L "$path" ]] || { echo "STOP: existing path: $path" >&2; exit 1; }
done
mkdir -p "$BOT_HOME/.agents/skills"
ln -sT "$repo/fleet/skills/fleet-campaign" "$BOT_HOME/.agents/skills/fleet-campaign"
(set -o noclobber; cat "$SOUL_SOURCE" > "$BOT_HOME/SOUL.md")
```

This bridge links into the preserved tree; do not copy it without its dependencies.
A concurrent collision fails rather than overwrites. A partial run needs inspection, not force.

## 4. Bind one owner and the shared peers privately

Open the new project Bot's **Home Chat** in the UI. Its first greeting is setup-only.
After reading installed help, the owner or authorized setup agent can discover exact addresses:

```text
orca bot list --help
orca bot list --json
orca bot chats --help
orca bot chats --bot <actual-bot-name> --json
orca orchestration run-current --help
orca skills get orchestration
```

`bot list` gives names/addresses; `bot chats` gives exact chat IDs. A title is not an ID;
there is no `orca bot show`. Record the selected Home Chat, not an old closed one.
Bind/create a Run only through the installed native orchestration guide when the smoke is
explicitly authorized. Until then `owner_run` stays unbound, not a fabricated identifier.

Create private `FLEET_BINDINGS.md` in each Bot home, outside tracked source, with a referenced
private charter. This Markdown example is an operational record, not an Orca parser schema.
Replace every placeholder with verified values before admitting development:

```yaml
role: project-magos
source_tree: /path/to/durable/acd-orca/repo
source_revision: <reviewed-full-SHA>
discovery_root: /path/to/execution-home/.agents
bridge: /path/to/durable/acd-orca/repo/fleet/skills/fleet-campaign/SKILL.md
common: /path/to/durable/acd-orca/repo/fleet/skills/fleet-campaign/references/common-contract.md
project: example-project
repository: /path/to/project
repository_identity: <verified-repository-identity>
target_branch: main
owner_bot: <verified-bot-address>
owner_chat: <verified-home-chat-id>
owner_run: null # bind from native receipt before dispatch
peers:
  logis: <verified-logis-bot-id-or-address>
  intent: <verified-intent-bot-id-or-address>
  architect: <verified-architect-bot-id-or-address>
  ferrum: <verified-ferrum-bot-id-or-address>
  outcome: <verified-outcome-bot-id-or-address>
commands: {build: '<repo build command>', test: '<repo test command>', smoke: '<real scenario>'}
model: <approved-exact-OMP-model-route>
review: {provider: roborev, engine: acp.omp, readiness: unverified}
resources: {slots: 3, writers_per_worktree: 1, source_minutes: 15, checkpoint_minutes: 10, review_minutes: 10}
charter: /path/to/private/project/CHARTER.md
mandate: setup-only # later reference exact authorized request, scope and revision
request_state: /path/to/private/project/REQUESTS.md
delivery: {merge: false, push: false, deploy: false}
github: {enabled: false} # optional: trusted repository, actor, event and source reply route
```

Required: verified source/paths, role, project/repository/branch, owner chat, peers, actual
commands, model, limits and charter. Run binding and successful review readiness are required
before coding dispatch. GitHub is optional; unset credentials never belong here. The charter
records allowed paths/actions, exclusions, request/revision/dedup identity and delivery authority;
it cannot create permission. Unknown or conflicting bindings block mutation.

Each shared Bot's home has one binding index with its role/source/peer records and a map such
as `projects: {cutecare: /path/to/private/cutecare/BINDINGS.md, machina: /path/to/private/machina/BINDINGS.md}`.
Keep each project's charter, owner/chat/Run and request state separate. Add a mapping after
comparison/approval, never overwrite one project's bindings with another's. Resolve the project
from each commission; missing/ambiguous identity stops work. Do not put project facts in shared memory.

Setup-only bootstrap prompt for each Bot:

> Read your SOUL and verified bindings. Discover/propose missing exact peers, paths and owner
> chat from the repository and permissions I supply. Persist only verified private bindings
> and charter after resolving conflicts. Read `skill://acd-orca`, then
> `skill://acd-orca/references/engines/omp.md`, and the bound filesystem bridge/common contract.
> Report actual loaded paths/hashes, model, permission limits and missing setup. No development,
> new coordinator or automatic permission changes. A catalog listing or parent receipt is not loading proof.

## 5. Establish review readiness, then one tiny native smoke

Follow the current [code-review protocol](../skills/acd-orca/references/code-review.md) and
[OMP loading sheet](../skills/acd-orca/references/engines/omp.md), not historical private receipts.
Roborev is the client; OMP supplies native ACP. The official configuration shape is:

```toml
[acp.omp]
command = "/path/to/verified/omp"
args = ["acp"]
model = "<approved-advertised-model>"
timeout = 600
read_only_mode = "plan"
disable_mode_negotiation = false
```

This shape is not a complete isolation policy. Before use, have the setup agent read actual
`omp acp --help` and `roborev review --help` and propose a private configuration implementing
the review contract: fresh neutral sessions, read/grep/glob only, ambient context/skills and
extensions disabled, no retries/fallback, no automatic fixes, secrets via approved auth only.
Owner approves configuration/spend; do not copy someone else's overlay or assume old qualification.
The supported review shape, after admission, is `roborev review --local --dirty --repo <snapshot>
--agent acp.omp --model <model> --panel none --type exhaustive --min-severity medium`.
Use a separate frozen no-hooks snapshot and private data/temp/session directories as the contract
requires; never aim local review at the live checkout merely to try it. No OCR fallback.

Authorize a bounded tiny clean fixture and a known-defect fixture in disposable storage.
Require clean acceptance and detection of the known defect, complete source/read coverage,
raw verdict, actual model/tool/provider completion and unchanged reviewed bytes. Error/refusal
must remain failure or INCONCLUSIVE; rc=0 is not PASS. Record your own readiness scope privately.
Do not start production coding until this route works on the actual worker computer.

Then authorize this one native smoke in PROJECT Magos's designated owner chat:

> In a disposable test repository, use one bound Run and native orchestration only. Ask Logis
> for a tiny deterministic change and obtain fresh independent critique. Return the exact
> revision to this owner. Dispatch one OMP worktree worker to implement and run its real test;
> verify its completion message wakes this owner. Review frozen source through qualified
> roborev, verify runtime results independently, and report back here. No merge/push/deploy.
> Preserve source/evidence, then obtain native worker release/exit receipts. Do not poll or
> create a persistent per-file review Bot. Stop on missing capability rather than bypass it.

Pass requires correlated peer question/reply, same-owner handoff, actual worker test output,
completion wake, independent exact-source review and native release/exit evidence. At most
three occupied slots, normally writer plus reviewer; done/end-turn does not free a slot.
Read-only instructions are not an OS sandbox. A missing wake or release is a scoped blocker.
These UI/auth/provider/native paths are user-run acceptance steps, **not tested by this guide's
static/offline tests**. No whole validator campaign is required.

## 6. Use the project Bot

Now send the authorized request to PROJECT Magos. It commissions Logis; you do not manually
handoff. For example: “Add CSV export, reuse existing patterns, run the named business scenario;
MERGE to the bound branch after independent review/tests. No push or deploy.” Default MERGE
requires explicit bound-branch mandate; push/deploy are separately authorized. Pause/cancel
and scope changes go to the same owner, without routine intermediate human START gates.

- **CuteCare:** repository `/path/to/cutecare`, target `main`; owner manually attaches external
  connectors. Require the actual business acceptance scenario, not only unit tests. No automatic connector setup.
- **Machina:** repository `/path/to/machina`, target `master`; no production restart, migration
  or other production side effects without a separate explicit mandate.

GitHub intake is optional and configured separately; chat-only setup works now. Until authorized
repository/actor/event bindings and source replies are verified, paste an Issue URL into the
owner chat as data. Issue bodies/comments never grant authority; edits/redelivery update the
same request/revision and must not create duplicate work. Do not add a watcher as a fallback.
Further GitHub and operations walkthroughs are separate; the current
[common contract](../fleet/skills/fleet-campaign/references/common-contract.md) and
[role index](../skills/acd-orca/references/roles.md) define the operational boundaries.
