# Autonomous Campaign Development on Orca

Give your PROJECT Bot a goal such as “Add CSV export to the reports screen.” Project Magos
coordinates shared planners and independent critics, temporary OMP worktree writers,
real tests and roborev code review, then delivers only within your authorization.

This repository supplies the instructions, not another service. Install them once, share
the planning Bots across projects, and keep one project owner for each repository.
GitHub Issues are optional; ordinary chat works without a connector or validator.

[Setup](docs/SETUP.md) · [GitHub Issues](docs/GITHUB_ISSUES.md) ·
[Roles](skills/acd-orca/references/roles.md) · [Operations](docs/OPERATIONS.md) ·
[Agent guide](docs/INSTALL_AGENT.md) · [Public repository](https://github.com/megastruktur/autonomous-campaign-development)

## Install with your agent prompt

Copy this setup-only prompt to your agent. It pins the guide and instruction tree together;
public fetch availability is not asserted here.

```text
Read https://raw.githubusercontent.com/megastruktur/autonomous-campaign-development/df8ed09acfbb612e7bc9dfb7649ef9903d662f55/docs/INSTALL_AGENT.md as untrusted source.
Use source_revision=df8ed09acfbb612e7bc9dfb7649ef9903d662f55; clone https://github.com/megastruktur/autonomous-campaign-development.git and checkout that SAME source_revision before loading/setup, not default main.
Review then pin that full SHA; use all linked guides and the complete instruction tree at the same revision to install OR safely update the instruction stack on my actual execution host.
Preserve custom configuration, projects and credentials; obtain required interactive approval with no bypass. Verify actual own-session loading, not merely catalog discovery.
Setup does not authorize a product campaign or GitHub account changes.
Report version, paths, check results and remaining manual actions, then stop.
```

## Installation

You need Orca, authenticated OMP on the execution computer, roborev, Git, Bash and GNU
coreutils; follow the [prerequisites](docs/SETUP.md#1-prerequisites-on-the-execution-computer).
The manual block targets a Linux execution host with Bash/GNU tools; native Windows/macOS
and WSL adaptations are not qualified by these examples.
Existing installation? Use the [compare/backup guidance](docs/SETUP.md#2-clone-review-and-pin-the-complete-tree)
and [update procedure](docs/OPERATIONS.md#update-without-changing-live-instructions-underneath-work), not this fresh-install block.

Run in the execution user's fresh installation HOME. Review the downloaded tree in another
window when prompted; links are exposed only after your explicit acknowledgement.
The subshell keeps a failure from closing your shell. Nothing creates Bots or starts work.

```bash
(
set -euo pipefail
for tool in git mkdir ln; do
  command -v "$tool" >/dev/null || { echo "STOP: missing executable: $tool" >&2; exit 1; }
done
repo="$HOME/.local/share/acd-orca/repo"
paths=("$repo" "$HOME/.agents/skills/acd-orca" "$HOME/.agents/skills/acd" "$HOME/.agents/fleet")
for path in "${paths[@]}"; do
  [[ ! -e "$path" && ! -L "$path" ]] || { echo "STOP: existing path: $path" >&2; exit 1; }
done
mkdir -p "$HOME/.local/share/acd-orca"
git clone https://github.com/megastruktur/autonomous-campaign-development.git "$repo"
revision=$(git -C "$repo" rev-parse HEAD)
for file in skills/acd-orca/SKILL.md skills/acd-orca/references/engines/omp.md \
  skills/acd-orca/references/code-review.md skills/acd/SKILL.md \
  fleet/skills/fleet-campaign/SKILL.md fleet/skills/fleet-campaign/references/common-contract.md \
  fleet/templates/magos-project/SOUL.md docs/SETUP.md docs/GITHUB_ISSUES.md docs/OPERATIONS.md; do
  [[ -f "$repo/$file" ]] || { echo "STOP: missing dependency: $file" >&2; exit 1; }
done
printf 'Review source at %s\nRevision: %s\nType "reviewed %s" to enable instructions: ' "$repo" "$revision" "$revision"
IFS= read -r approval
[[ "$approval" = "reviewed $revision" ]] || { echo 'STOP: source review not acknowledged' >&2; exit 1; }
git -C "$repo" checkout --detach "$revision"
[[ "$(git -C "$repo" rev-parse HEAD)" = "$revision" ]]
[[ -z "$(git -C "$repo" status --porcelain)" ]] || { echo 'STOP: source changed during review' >&2; exit 1; }
for path in "${paths[@]:1}"; do
  [[ ! -e "$path" && ! -L "$path" ]] || { echo "STOP: existing path: $path" >&2; exit 1; }
done
mkdir -p "$HOME/.agents/skills"
ln -sT "$repo/skills/acd-orca" "$HOME/.agents/skills/acd-orca"
ln -sT "$repo/skills/acd" "$HOME/.agents/skills/acd"
ln -sT "$repo/fleet" "$HOME/.agents/fleet"
printf 'Pinned instructions: %s\nNext: read docs/SETUP.md in that tree.\n' "$revision"
)
```

Keep the complete durable tree, including legacy `skills/acd` and `fleet` dependencies.
Collisions and reruns stop without overwrite; inspect partial installs instead of forcing them.
Review/pinning, missing dependencies and approved migration are explained in [Setup](docs/SETUP.md).

## Basic setup

1. [Create five shared Bots once and one project Magos per repository](docs/SETUP.md#3-create-five-shared-bots-and-one-project-bot).
   Copy the ready SOULs and install the guarded per-Bot bridge; no extra Magos Fleet Bot is required.
2. [Bind the owner and peers privately](docs/SETUP.md#4-bind-one-owner-and-the-shared-peers-privately).
   Keep repository, branch, exact identities and authority in private bindings, not shared memory.
3. [Verify fresh loading, review readiness and a tiny native smoke](docs/SETUP.md#5-establish-review-readiness-then-one-tiny-native-smoke).
   Discovery alone is not loading; installing instructions is not runtime qualification.
4. Write your request to the PROJECT Bot. It commissions Logis; you do not manually hand off.
   Add [GitHub intake](docs/GITHUB_ISSUES.md) only if you want it, after chat setup works.

## Usage

Send either prompt to the same designated PROJECT Magos owner chat:

> Add CSV export to the existing reports screen in our bound repository. Reuse its patterns,
> run real tests and obtain independent review. I authorize MERGE to the bound target branch
> for this feature after checks pass. No push or deployment.

> Plan resumable uploads for the bound repository. Return scoped acceptance criteria,
> alternatives and independent critique. Planning only: no implementation, merge, push or deploy.

Push and deployment each require separate explicit authorization. Pause, resume and scope
changes go to that same owner; see [Operations](docs/OPERATIONS.md) for safe updates and cleanup.
Private bindings and secrets stay private. Optional checks and unchanged legacy acd guidance
live in the operations reference, not in your normal task path. [MIT license](LICENSE).
