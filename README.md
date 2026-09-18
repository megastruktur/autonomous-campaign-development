# Autonomous Campaign Development (Agent Skill)

Reusable orchestration instructions for running autonomous, multi-task development
campaigns: an OMP coordinator plans, dispatches OMP coding agents into Orca-managed
worktrees, integrates, and verifies — without writing source code itself. Designed for the
[Hermes](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/) planner
profile; portable to other orchestrating agents with adapter changes.

This is a **procedure document** (a standard [Agent Skill](https://agentskills.io/specification):
`SKILL.md` plus references and templates), not software:

- It is **not** a running scheduler or service — nothing executes on its own.
- It bundles **no** coding model, reviewer ("inquisitor") binary, or other executables.
- It provides **no guarantee** of fully hands-off, safe execution. A human approves the
  plan, and destructive actions still stop for explicit permission.

Version 1.0.0 · MIT License.

## Requirements

- [Orca](https://github.com/stablyai/orca) — worktrees, terminals, and its Skills UI.
  On a Linux host the local CLI is `orca-ide`; resolve the Orca executable per
  platform/runtime (inside Orca terminals: `orca`; dev checkouts: `orca-dev`; WSL exports
  `ORCA_CLI_COMMAND`).
- [OMP](https://github.com/stablyai/orca) — the harness driving the coding agents.
- Node.js/npm — only for the installer CLI below.
- Git.
- Model access for the coding model, fallback model, and independent reviewer.
- The ability to run real runtime tests in the target repository.
- At least one independent reviewer session (read-only).

## Install (recommended: Orca workspace, project scope)

Run this in a terminal **inside the Orca workspace/folder of the project** where you want
the skill available. It uses the same community skills CLI Orca itself uses
([vercel-labs/skills](https://github.com/vercel-labs/skills#install-a-skill)):

```bash
npx --yes skills add megastruktur/autonomous-campaign-development \
  --skill autonomous-campaign-development --agent universal -y
```

- No `--global`: the skill installs **project-scoped** into that project's
  `.agents/skills/` and does not touch any other agent's global profile.
- `--agent universal` keeps the installation narrowly scoped instead of spraying every
  detected agent directory.
- `-y` skips confirmation prompts (CI-friendly).

Loading prerequisites: Orca's Skills UI scans installed skill homes — including the
shared Agent Skills directory and OMP's `~/.omp/agent/skills` — so installed skills show
up without manual symlinking. For OMP specifically, the community CLI has no
`--agent omp` target: place or point the skill at OMP's documented skill path, or have
OMP read `skills/autonomous-campaign-development/SKILL.md` explicitly.

Note: `npx skills` collects anonymous telemetry by default; opt out with
`DISABLE_TELEMETRY=1` ([docs](https://skills.sh/docs/cli)).

## Preview and verify

```bash
# Preview what this repo offers, without installing anything
npx --yes skills add megastruktur/autonomous-campaign-development --list

# List what is installed in the current project (community CLI)
npx skills list
```

To verify from the Orca side, check the Skills page in the Orca UI, or run
`orca-ide skills list` on a Linux host (substitute the Orca executable your
platform/runtime resolves; prefer `--json` for scripting).

Two Orca mechanisms are **not** routes to install this GitHub repo:

- `orca-ide skills install --skill …` only resolves Orca's **bundled** skill registry;
  it cannot install third-party skills from GitHub.
- The Orca UI's **Skills → Install from link** expects a published **Orca skill-share
  URL**, not an arbitrary GitHub URL.

### About native Orca skill sharing

Orca can share skills natively via **Skills → Share skills** (requires an Orca account;
CLI publication additionally requires the default-off *Settings → Share Skills → Allow
agents and the Orca CLI to publish skill links* permission). Share links are unlisted:
anyone with the link can inspect and install, with version/files/digest preview, skill
subsetting, global/workspace scope, and keep-local conflict protection. Recipients
install such links through **Skills → Install from link**.

**There is currently no published Orca share URL for this skill** (skill sharing is not
available for it at this time), which is why the GitHub route above is the documented
one. The GitHub install works immediately and needs no Orca Cloud login. A publisher who
installs this skill may later share their copy through Orca's Share skills flow.

### Optional: Hermes route

If you use Hermes with an existing profile:

```bash
hermes -p planner skills install \
  megastruktur/autonomous-campaign-development/skills/autonomous-campaign-development
# then preload it in a chat:
hermes -p planner chat --skills autonomous-campaign-development
```

## What it does

The skill is a coordinator contract for one development campaign:

- **Intake & plan**: focused clarification questions and improvement proposals before
  locking the plan; durable English campaign artifacts (`PLAN.md`, per-task files,
  `TODO.md`, `STATE.json`, `EVENTS.jsonl`, evidence, final report) written inside the
  repository — never chat memory.
- **DAG and resource ownership**: explicit dependency edges and resource exclusions
  (files, APIs, migration ordering, schema ownership, lockfiles, build output, ports,
  fixture data, databases, external side effects); shared contracts are settled
  centrally, never designed independently by sibling tasks.
- **Model questionnaire**: one question set fixes the coding model, fallback model, and
  independent reviewer model (`default` resolves to the runtime's actual configured
  default, or an exact ID); resolved IDs are recorded, verified at startup, and pinned.
- **Concurrency cap**: at most **three** simultaneously active coding agents (fix and
  remediation agents included), one writer per worktree.
- **Topology**: a dedicated campaign integration worktree created from a pinned start
  SHA and a recorded **named** source branch (never assumes `main`/`master`).
- **One approval gate**: a single explicit plan approval authorizes development, tests,
  reviews, task squash merges, the final merge, and cleanup. Push, publication, and
  deployment stay separate explicit permissions.
- **Per-task loop**: develop → runtime test loop → independent review loop → squash
  integration and conflict handling → post-merge runtime smoke → evidence and cleanup.
  Runtime tests run after the executor declares readiness and after every fix batch.
- **Independent review**: a read-only reviewer that never edited the code returns an
  explicit complete **PASS/FAIL** verdict with actionable findings, commissioned by the
  coordinator with a raw, unbiased evidence packet.
- **Loops with evidence-based escalation**: no fixed iteration cap while evidence shows
  progress; non-convergence is an evidence-based pause (identical failure fingerprints,
  oscillating fixes, model cycling, scope growth, missing capability), not a counter.
- **Durable state**: canonical `STATE.json`/`TODO.md`/`EVENTS.jsonl`/evidence under the
  campaign directory; the coordinator polls every active session on a **ten-minute
  cadence only while the campaign is running**.
- **Endgame**: full-campaign acceptance/seam runtime tests plus independent final review
  at the exact campaign tip, coordinator-only merge (default `--no-ff`) to the recorded
  source branch, post-merge smoke on the target, evidence archived **before** worktree
  cleanup.

## Usage

Installing the skill starts nothing and grants no permissions. Once your planning agent
has loaded it, request a campaign in plain words, for example:

> Start an autonomous campaign: add OAuth login and a profile settings page to this
> repo. Plan the tasks, ask me the model questions, and get my approval before any
> agent starts working.

The skill itself then drives intake → plan → model questionnaire → **one approval gate**
→ execution. To resume after a restart or crash:

> Resume the campaign from its state files in plans/ and continue where evidence left
> off.

## Evidence policy

- **Runtime test evidence** is the standard of done: the real application exercising the
  changed behavior. A green unit/integration suite alone never substitutes.
- Mocks are for external boundaries only; mock-only verification is not "verified".
- The author's self-review is optional preparation and **cannot replace** the
  coordinator-commissioned independent review.

## Repository contents

```
skills/autonomous-campaign-development/
├── SKILL.md                                 # the skill: contract, procedure, pitfalls
├── references/
│   ├── hermes-orca-omp.md                   # dispatch mechanics and command shapes
│   ├── runtime-review-and-integration.md    # topology, review, integration, cleanup
│   ├── state-and-recovery.md                # state schema, crash windows, resume
│   └── validation-tabletop.md               # static checks and tabletop walkthroughs
└── templates/
    ├── PLAN.md                              # campaign plan template
    ├── TASK.md                              # per-task file template
    ├── TODO.md                              # campaign TODO template
    └── STATE.json                           # campaign state template
```

## Customization and porting

Fork and edit freely (MIT). The procedure in `SKILL.md` is runtime-agnostic in intent,
but the mechanics live in `references/hermes-orca-omp.md` — port those dispatch commands
to your orchestration runtime as needed. After modifying a copy, run the static checks
and tabletop walkthroughs in `references/validation-tabletop.md` before relying on it.

## Update / uninstall

With the community skills CLI, in the project where it is installed:

```bash
npx skills update autonomous-campaign-development   # refresh to the repo's latest
npx skills remove autonomous-campaign-development   # remove from agent directories
```

## Safety, trust, and license

- Read `SKILL.md` and the references before use; this is third-party instruction content
  for agents — treat it with the same scrutiny as any other dependency.
- The skill defers to repository instructions (e.g. `AGENTS.md`), hooks, permission
  systems, and your campaign approval; conflicts are surfaced, not bypassed.
- Autonomous execution is gated on your explicit plan approval; push/deploy remain
  separate permissions. No guarantee of unattended safety is offered or implied.
- License: MIT — see [LICENSE](LICENSE).

## Compatibility boundaries (facts)

- Designed and worded for the Hermes planner profile driving OMP agents in Orca
  worktrees; other runtimes need adapter changes.
- The host CLI on Linux is `orca-ide`; bare `orca` outside Orca's terminals is the GNOME
  screen reader. Resolve the Orca executable per platform/runtime.
- The community skills CLI's global install path differs across versions
  (`~/.config/agents/skills` or `~/.agents/skills`) — one reason this README recommends
  project scope.
- The community skills CLI does not target OMP (`--agent omp` does not exist); use
  OMP's documented skill path or an explicit read.
- The full workflow additionally requires Orca + OMP + an independent reviewer.

## Sources

- [Orca skills registry & MCP (CLI docs)](https://github.com/stablyai/orca/blob/main/docs/site/content/docs/cli/skills.mdx)
- [Orca: sharing agent skills](https://github.com/stablyai/orca/blob/main/docs/reference/sharing-agent-skills.md)
- [vercel-labs/skills — install a skill](https://github.com/vercel-labs/skills#install-a-skill)
- [skills.sh CLI reference](https://skills.sh/docs/cli)
- [Agent Skills specification](https://agentskills.io/specification)
- [Hermes skills documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/)
