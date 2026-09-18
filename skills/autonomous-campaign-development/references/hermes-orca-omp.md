# Orca/OMP Operational Mechanics

Command shapes and dispatch mechanics for the campaign. Everything here was verified on a
reference environment; paths marked "example" are that environment's specifics - resolve
the equivalents in yours (prefer CLI names on `PATH`) before use. Run `--help` on any verb
you have not personally verified before scripting it.

Policy note: any fixed model or gate policy you may find in environment-specific
orchestration notes is NOT imported by this skill. Model choice comes from the campaign
questionnaire; gates come from the campaign approval and the applicable instruction
hierarchy.

## CLI identities

- Host CLI: `orca-ide`. Never invoke bare `orca` on the host - it is a different program.
- Container example: `docker exec orca /opt/orca/squashfs-root/resources/bin/orca-ide ...`.
- Pass `--json` on Orca commands and parse the structured response; do not screen-scrape.
- OMP (agent runtime): `omp` - container example needs a login shell for `PATH`:
  `docker exec orca sh -lc 'omp --help'`.

Verified OMP flags: `--model`, `--resume`, `--session-dir`, `--models` (round-robin
cycling, NOT automatic fallback), `--cwd`, `--tools`, `--no-lsp`, `--no-prewalk`.
There is NO verified fallback flag: the orchestrator owns fallback by stopping the
session and starting a new one with an approved model. Never invent `--fallback-model`.

## Model selection and verification

1. Ask the questionnaire once (coding / fallback / reviewer). Valid answers: `default`
   meaning the relevant runtime/profile's actual configured default - resolve it to a
   concrete ID before dispatch - or an exact available model ID; fallback may be `none`.
2. Record both the requested and the resolved value per role in state; pin resolved
   defaults so a restart reproduces them unless the user changes them.
3. Validate the fallback's availability at startup; do not claim provider calls were
   tested if they were not. Resolve availability without ever printing credentials.
4. After each agent start, verify the ACTUAL startup model from the session output, not
   just the command line. If it does not match the resolved approved ID: stop and
   reconcile - never let an unapproved model run silently.
5. `--models a,b` is cycling across listed models; do not use it to express fallback.
   Fallback happens only through the remediation ladder with an approved ID.

## Worktree topology commands

```bash
# Campaign integration worktree from the pinned start:
orca-ide worktree create --repo path:<repo> --name <prefix>-campaign \
  --base-branch <pinned-ref> --no-parent --json
orca-ide worktree show --worktree name:<prefix>-campaign --json   # learn REAL branch/path
# Task worktree from the current campaign tip:
orca-ide worktree create --repo path:<repo> --name <prefix>-<task_name> \
  --parent-worktree name:<prefix>-campaign --base-branch <current-campaign-ref> --json
```

- Orca may auto-generate git branch names (namespaced). Record the branch and path the
  command actually RETURNED in state; never invent CLI flags to force a name. Worktree
  naming is strict, branch naming may use the Orca namespace.
- Compare the returned HEAD to the expected SHA; on mismatch, do not start work -
  investigate the base ref first.
- Worktrees must be created BY Orca (never bare `git worktree add`): Orca-created ones
  respond to `--worktree name:<name>` selectors; a `selector_not_found` error means the
  worktree is not Orca-managed - repair it, do not paper over it with a `path:` selector.
- Creation can drop a startup shell into the new worktree. Do not paste the brief there.

## Dispatch recipe

```bash
orca-ide terminal create --worktree name:<prefix>-<task_name> \
  --command "omp --model <resolved-id>" --json
# modern response: result.terminal.handle (worktree-agent responses may differ - inspect)
orca-ide terminal wait --terminal <handle> --for tui-idle --timeout-ms 90000 --json
```

- Verify the real OMP is running before sending anything: session file appeared and is
  growing under the agent session directory, and `terminal read` tail shows activity -
  never send prose to a startup or fallback shell. Readiness failure stops dispatch.
- Briefing: overwrite the worktree's brief file (for example `BRIEF.md`) immediately
  after `worktree create` - a fresh worktree inherits whatever brief the base branch
  carries - then verify its title line matches this task before dispatch.

```bash
orca-ide terminal send --terminal <handle> --text "<brief>" --enter --json
```

- JSON success is NOT proof the prompt began executing. Promptly inspect `terminal read`
  output, session-file growth, and any ack. On an ambiguous send, reconcile with current
  request/state first - the current CLI may offer `--wait-submit`/`--retry-request`;
  verify via `--help` - never blindly resend (duplicate execution risk).

## Monitoring and liveness

```bash
orca-ide terminal list --worktree name:<name> --json
orca-ide terminal read --terminal <handle> --limit <n> --json
orca-ide worktree ps --json
```

- Liveness = session file growth plus terminal content evolution; compare processes,
  commands, and checkpoint evidence across polls. An idle-but-ready agent is not a crash;
  a long-running command is not a stall.
- A pending interactive `ask` in the session freezes the agent: detect it and answer it
  through the terminal; do not kill a session that is merely waiting for input.
- After `terminal close --terminal <handle> --json`, VERIFY the worker process actually
  stopped (scoped check by process working directory) - do not assume. No global
  kill/pkill sweeps; only precisely scoped process termination.

## Reviewer dispatch

- Prefer a genuinely independent reviewer mechanism: an inquisitor-style profile or
  read-only subagent if the runtime actually offers one. Availability of a profile does
  not mean its dispatcher is running - CONFIRM the reviewer session started and is
  progressing before treating review as in flight.
- Fallback: a separately spawned OMP session with an explicit read-only mandate, pinned
  to the task worktree, never the implementing session. Read-only is an enforced
  capability when available; otherwise it is a mandate - and a prompt-only restriction is
  not OS isolation, so treat its outputs accordingly.
- Kanban/board systems are optional tracking adapters only: they never replace canonical
  campaign TODO/state and are NEVER the coding executor. Do not create dormant cards and
  call that execution.
- If the coordinator runs an independent reviewer through a CLI session because no task
  mechanism exists, verify that CLI's help first; do not bake environment-specific
  commands into the campaign plan.

## Status handshake

```bash
orca-ide worktree set --worktree name:<name> --workspace-status in-review \
  --comment "<task> done: <what was verified>" --json
# fixes: back to
orca-ide worktree set --worktree name:<name> --workspace-status in-progress \
  --comment "<task> fix round N: <finding>" --json
```

- External status strings are exact: `in-review`, `in-progress`. Internal state may use
  `in_review`/`in_progress` only with an explicit written mapping.
- Status does not auto-revert. Reset `in-review` -> `in-progress` immediately when
  dispatching a fix round so a stale status cannot trigger early review.
- There is no "merge me" flag: `in-review` set by the executor on a clean tree IS the
  handshake to the coordinator - but the coordinator still validates the clean committed
  snapshot and runtime report before commissioning review.

## Teardown

```bash
orca-ide terminal close --terminal <handle> --json   # then verify process stopped
orca-ide worktree rm --worktree name:<name> --json   # selector form; AFTER archive+safety
```

- `worktree rm` fails while a terminal is open on the worktree, and must only run after
  evidence is archived outside the worktree and the cleanup inventory is satisfied.
- Forced-removal flags are not a routine recipe. Dirty or untracked work is rescued or
  cleanup pauses - see cleanup rules in
  [runtime-review-and-integration.md](runtime-review-and-integration.md#cleanup).
