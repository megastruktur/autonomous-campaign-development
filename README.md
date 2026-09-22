# Autonomous Campaign Development (Agent Skill)

Reusable orchestration instructions for running autonomous, multi-task development
campaigns: an orchestrator (the coordinator) plans, dispatches OMP coding agents into
Orca-managed worktrees, integrates, and verifies — without writing source code itself.
Designed for the
[Hermes](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/) planner
profile; portable to other orchestrating agents with adapter changes.

This is a **procedure-first [Agent Skill](https://agentskills.io/specification)**:
`SKILL.md` plus references and templates, bundled since v1.1.0 with a small **optional**
observer utility (`scripts/`, Python 3 standard library only) that helps a coordinator
monitor agent progress.

- The skill is **not** a running scheduler or service — nothing executes on its own, and
  the observer scripts run only when explicitly invoked. Unattended coordinator wakeups
  rely on the runtime's native session heartbeat (verified per procedure, v1.1.1), not
  on anything bundled here.
- It bundles **no** coding model, reviewer ("inquisitor") binary, or other executables
  beyond the two read-only observer scripts.
- It provides **no guarantee** of fully hands-off, safe execution. A human approves the
  plan and separately starts execution; destructive actions still stop for explicit
  permission.

Version 1.1.1 · MIT License.

## Requirements

- [Orca](https://github.com/stablyai/orca) — worktrees, terminals, and its Skills UI.
  On a Linux host the local CLI is `orca-ide`; resolve the Orca executable per
  platform/runtime (inside Orca terminals: `orca`; dev checkouts: `orca-dev`; WSL exports
  `ORCA_CLI_COMMAND`).
- [OMP (Oh My Pi)](https://github.com/can1357/oh-my-pi) — the harness driving the coding
  agents; see its [skills documentation](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md).
- Python 3 — only for the optional progress-observer scripts; standard library only, no
  auto-start, no network, no dependencies.
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
`--agent omp` target: place or point the skill at OMP's documented skill path, or after
the project install above have OMP read the installed copy at
`.agents/skills/autonomous-campaign-development/SKILL.md` explicitly.

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
`orca-ide skills installed --json` on a Linux host (substitute the Orca executable your
platform/runtime resolves). It returns safe selectors without exposing local paths;
`orca-ide skills list` resolves only Orca's bundled registry, not third-party installs.

Two Orca mechanisms are **not** routes to install this GitHub repo:

- `orca-ide skills install --skill …` only resolves Orca's **bundled** skill registry;
  it cannot install third-party skills from GitHub.
- The Orca UI's **Skills → Install from link** expects a published **Orca skill-share
  URL**, not an arbitrary GitHub URL.

### About native Orca skill sharing

Orca can share skills natively via **Skills → Share skills → Publish new version**
(requires an Orca account; CLI publication additionally requires the default-off
*Settings → Share Skills → Allow agents and the Orca CLI to publish skill links*
permission). Per Orca's
[sharing documentation](https://github.com/stablyai/orca/blob/main/docs/reference/sharing-agent-skills.md):

- Published skill **versions are immutable**; publishing always creates a new version.
- Share management lives in **Settings → Share Skills**; only the original publishing
  account/package can publish new versions — publishing from one host does not magically
  sync files installed on another host, and pushing to GitHub does **not** update any
  Orca cloud snapshot.
- Recipients manage installs via **Skills → Manage installs**: they can update to the
  latest published version or roll back to a retained version. Do **not** assume an old
  share link always serves the latest version unless you verify it.
- On update, Orca's **Keep local** default preserves locally modified files; they are
  replaced only when you explicitly discard them.
- Native share URLs are unlisted capability links: do not publish them inside this
  repository.

The owner of this skill may have published an Orca share from another device. No share
URL is embedded here (none was provided for this repo), which is why the GitHub route
above is the documented one. A publisher who installs this skill may share their own
copy through Orca's Share skills flow.

### Optional: Hermes route

If you use Hermes with an existing profile:

```bash
hermes -p planner skills install \
  megastruktur/autonomous-campaign-development/skills/autonomous-campaign-development
# then preload it in a chat:
hermes -p planner chat --skills autonomous-campaign-development
```

#### Updating an existing Hermes installation

How you update depends on how the skill was originally installed — check before acting:

- **Hub-installed source** (`hermes -p planner skills` shows a hub/registry source):
  `hermes -p planner skills update autonomous-campaign-development` updates it.
  Avoid `--force`: it overwrites local edits.
- **Locally authored source** (`source=local`, e.g. a hand-placed or edited copy):
  there is no safe blanket update. Back up the installed copy, review the incoming
  payload, stage the replacement, and record what was replaced (a provenance receipt).
  Never let an updater silently delete local drift.
- In **any** case, a currently running session keeps the skill text it already loaded —
  a fresh session is required to pick up the updated version.

## What it does

The skill is a coordinator contract for one development campaign:

- **Intake & plan**: focused clarification questions and improvement proposals before
  locking the plan; durable English campaign artifacts (`PLAN.md`, per-task files,
  `HANDOFF.md`, `MANIFEST.json`, `TODO.md`, `STATE.json`, `EVENTS.jsonl`, evidence,
  final report) written inside the repository — never chat memory.
- **Planning/execution boundary (v1.1.0)**: one explicit plan approval authorizes WHAT
  may happen — it never starts agents. The planning session writes a durable HANDOFF
  plus a SHA-256 manifest of the frozen plan files and stops; execution begins only in a
  **distinct fresh coordinator session** on an explicit START bound to that manifest
  (drifted files invalidate consent). Already-started campaigns resume without
  re-gating. No per-task human gates are added.
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
- **Per-task loop**: develop → runtime test loop → independent review loop → squash
  integration and conflict handling → post-merge runtime smoke → evidence and cleanup.
  Runtime tests run after the executor declares readiness and after every fix batch.
- **Independent review**: a read-only reviewer that never edited the code returns an
  explicit complete **PASS/FAIL** verdict with actionable findings, commissioned by the
  coordinator with a raw, unbiased evidence packet.
- **Coordinator wakeups via native heartbeat (v1.1.1)**: campaign START and adoption
  of a running campaign must establish AND verify a `/heartbeat every 5m` recurring
  instruction in the coordinator's session — two automatic no-nudge cycles with
  observer-timestamped duty receipts, completion/stall handling, and stop control —
  before claiming autonomous monitoring. Completion notifications (`notify:true`),
  one-shot observer polls, and watch-pattern notifications are explicitly rejected as
  schedulers; without a verified heartbeat the campaign is honestly not autonomous.
  Contract: `references/coordinator-heartbeat.md`.
- **Strict progress semantics (v1.1.0)**: transport/process activity (streams, bytes,
  PID, file growth), a successful model response, and actual task progress are never
  conflated; only explicit structured checkpoints count as progress. An optional
  stdlib-only watchdog (`scripts/`) reports activity/health snapshots — observer-only:
  no kills, no nudges, no network, writes only its own sidecar directory.
- **Loops with evidence-based escalation**: no fixed iteration cap while evidence shows
  progress; non-convergence is an evidence-based pause (identical failure fingerprints,
  oscillating fixes, model cycling, scope growth, missing capability), not a counter.
- **Bounded execution attempts (procedural)**: each attempt runs under an approved
  budget (default 35 minutes from actual launch, checkpoint inspection at 20 minutes,
  at most one scoped steer, max two unproductive attempts per slice before an approved
  fallback or pause); budget expiry settles the attempt with partial work preserved —
  never a permanent FAIL, never auto-acceptance. Enforcement is coordinator procedure,
  not an observer-script flag.
- **Durable state**: canonical `STATE.json` (schema 2: campaign lifecycle plus planning
  and execution session records)/`TODO.md`/`EVENTS.jsonl`/evidence under the campaign
  directory; the coordinator polls every active session on a **ten-minute cadence only
  while the campaign is running**.
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

The skill then drives intake → plan → model questionnaire → **one approval gate** (WHAT
may happen) → HANDOFF + manifest written → the planning session **stops**. You begin
execution by pasting the START prompt (from the HANDOFF) into a **new, clean coordinator
session**; that session validates the manifest, the repo state, and its own capabilities
before creating any worktree or agent. To resume a started campaign after a restart or
crash:

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
│   ├── coordinator-heartbeat.md              # native /heartbeat wakeup contract (v1.1.1)
│   ├── handoff-and-start.md                 # planning boundary, HANDOFF, manifest, START
│   ├── hermes-orca-omp.md                   # dispatch mechanics and command shapes
│   ├── progress-watchdog.md                 # progress semantics, observer CLI contract
│   ├── runtime-review-and-integration.md    # topology, review, integration, cleanup
│   ├── state-and-recovery.md                # state schema, lifecycle, resume
│   └── validation-tabletop.md               # static checks and tabletop walkthroughs
├── templates/
│   ├── PLAN.md                              # campaign plan template
│   ├── TASK.md                              # per-task file template
│   ├── HANDOFF.md                           # execution handoff + manifest shape
│   ├── TODO.md                              # campaign TODO template
│   ├── STATE.json                           # campaign state template (schema 2)
│   └── WATCH.json                           # observer config template (schema_version 1)
└── scripts/                                 # optional observer utility (v1.1.0)
    ├── omp_events.py                        # metadata-only OMP session log adapter
    └── campaign_watch.py                    # deterministic progress watcher CLI
```

`templates/WATCH.json` mirrors the implemented `campaign_watch.py` config schema;
replace its `/path/to/...` placeholders and `registered_at` before first use. Command
surface, validation rules, and known constraints:
`references/progress-watchdog.md`.

## Customization and porting

Fork and edit freely (MIT). The procedure in `SKILL.md` is runtime-agnostic in intent,
but the mechanics live in `references/hermes-orca-omp.md` — port those dispatch commands
to your orchestration runtime as needed. After modifying a copy, run the static checks
and tabletop walkthroughs in `references/validation-tabletop.md` before relying on it.

## Update / uninstall

With the community skills CLI, in the project where it is installed:

```bash
npx skills remove autonomous-campaign-development   # remove from agent directories
```

For updates, re-run the exact `skills add` command from [Install](#install-recommended-orca-workspace-project-scope)
against the same scope: it re-fetches the repo's current payload and walks you through
any conflicts with local files — review the prompts and keep backups of local edits.
(The CLI's positional-name `update` form is not advertised here because its targeting
was not verified against upstream.)

## Safety, trust, and license

- Read `SKILL.md` and the references before use; this is third-party instruction content
  for agents — treat it with the same scrutiny as any other dependency.
- The skill defers to repository instructions (e.g. `AGENTS.md`), hooks, permission
  systems, and your campaign approval; conflicts are surfaced, not bypassed.
- Autonomous execution requires BOTH your explicit plan approval and a separate explicit
  START in a fresh session; push/deploy remain separate permissions. No guarantee of
  unattended safety is offered or implied.
- The observer scripts are read-only helpers: they never kill, nudge, merge, or talk to
  the network, and they write only their own sidecar directory.
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
- Campaign state written by v1.0.0 (`schema_version` 1 or missing) remains resumable:
  already-started campaigns keep their original approval; approved-but-never-started
  ones require a fresh-session START under the v1.1.0 contract
  (`references/state-and-recovery.md` describes the migration; nothing is auto-enforced).
- The full workflow additionally requires Orca + OMP + an independent reviewer.

## Sources

- [Orca skills registry & MCP (CLI docs)](https://github.com/stablyai/orca/blob/main/docs/site/content/docs/cli/skills.mdx)
- [Orca: sharing agent skills](https://github.com/stablyai/orca/blob/main/docs/reference/sharing-agent-skills.md)
- [vercel-labs/skills — install a skill](https://github.com/vercel-labs/skills#install-a-skill)
- [skills.sh CLI reference](https://skills.sh/docs/cli)
- [Agent Skills specification](https://agentskills.io/specification)
- [Hermes skills documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/)
