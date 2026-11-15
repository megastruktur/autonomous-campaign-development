# Skill Validation: Static Checks and Tabletop Walkthroughs

Use after authoring or modifying this skill, before relying on it for a live campaign.
Static checks are mechanical; tabletops are reasoned walkthroughs of the written
procedure against scripted situations - document actual reasoning and outcomes, and
never present a tabletop as a live feature test. Tabletops are SYNTHETIC reasoning
exercises: they validate what the text prescribes, not what any runtime does. Runtime
evidence for the observer scripts comes from their own test suite plus a real-session
smoke before release - prose alone enforces nothing.

## Static checks

1. Frontmatter parses as YAML; `name` matches the directory; `description` <= 60
   characters; `version` present; `metadata.hermes.category` is `software-development`.
2. `templates/STATE.json` parses as valid JSON; embedded JSON blocks in other templates
   (for example the manifest shape in `templates/HANDOFF.md`) parse; every unknown is
   `null`; the only brace-bearing strings are the documented filename conventions
   (`{prefix}_*`); enums and `schema_version` match the documented schema.
3. Every relative Markdown link in every file resolves to an existing file/anchor.
4. Every `{{placeholder}}` in templates appears in the template's own legend or is
   self-evident from context; templates stay valid after placeholder substitution
   (JSON especially).
5. English-only scan: no non-ASCII letters outside code examples; no credentials,
   tokens, or environment-specific absolute paths except clearly-labeled examples.
6. TODO templates contain the mandatory per-task stages AND the final campaign stages,
   plus the campaign start gates.
7. Version coherence: the SKILL.md frontmatter version, the README version claim, and
   the STATE schema version notes agree; no stale v1.0.0-era claims survive
   (approval-immediately-starts-execution, "no executables", session-growth-as-progress
   wording).


## Planning validation

Static checks additionally require the four gated phases, mandatory repository/web evidence,
the five critique lenses (including Security and UX), and hash-bound convergence before DAG
creation, plus the mandatory live-verified open-source library evaluation covering whole
and partial functionality, anti-NIH critique enforcement, and lockfile ownership for any
adopted dependency. INTENT, RESEARCH, and CRITIQUE belong in the frozen manifest; the
mutable planning phase state does not. Tabletop scenarios 42-50 exercise these requirements.

## OCR engine validation (v1.7.0)

Static checks additionally require: the section-0 engine gate in SKILL.md; the
`references/ocr-review.md` contract; `review_engine` recorded in the HANDOFF and STATE
templates; the exclusive-engine rule (no silent fallback); the blocking severity set
critical/high/medium; and the not-a-verdict list (partial/failed/budget/skipped/zero
files). Tabletop scenarios 51-56 exercise these requirements.

## Tabletop scenarios

Walk the written procedure (SKILL.md Procedure + referenced contracts) and record what
the text instructs at each step. Expected outcomes below are the pass criteria.

| # | Scenario | Expected outcome per the written procedure |
|---|---|---|
| 1 | Unit suite green, application broken at runtime | Task stays blocked in `runtime_test`; unit results recorded as supplemental only; no PASS |
| 2 | Executor delivers a fix batch after a FAIL | Full retest of runtime scenarios, then fresh independent review of the new commit; old verdicts invalidated |
| 3 | Reviewer asked to apply a small fix during review | Refused: no edits even temporary; probe proposals go to executor in a disposable copy |
| 4 | Repeated review FAILs, each with measurable progress | Loop continues; no fixed iteration cap; progress evidence drives continuation |
| 5 | Repeated identical failure fingerprint, no progress after materially different attempts | Evidence-based pause of task + descendants; safe branches continue; options presented |
| 6 | Operator pauses the campaign | No self-resume; restart requires explicit continue; approval scope unchanged |
| 7 | Reboot; state holds stale session handles | Resume protocol: read state/TODO/plan, reconcile ownership, refresh handles via terminal list, no duplicate workers |
| 8 | Crash after squash merge, before state checkpoint | Receipt comparison against campaign log/tree; already-integrated => no duplicate merge |
| 9 | Original target branch moved before final merge | Latest target integrated into campaign via fix/test/review rules; final verification re-run; refs verified immediately before merge |
| 10 | No todo-list tool available in the environment | `{prefix}_TODO.md` on disk is the operational checklist; stages still tracked |
| 11 | Worktree slated for removal has untracked files | Rescue into evidence/plans or pause cleanup; never destroy; checkbox only after verified removal |
| 12 | Model questionnaire answered `default` | Resolve to the runtime/profile's actual configured default, record requested+resolved, verify startup model, pin for restart; fallback (if any) uses only the approved ID |
| 13 | Author's own subagent "already reviewed" the candidate | Coordinator still commissions its own independent review with the unbiased packet; self-review is preparation only |
| 14 | Fix lands for one path of a defect class (e.g. claim) | Re-review covers release/rebind siblings of the same class plus introduced regressions |
| 15 | Acceptance test fails once, passes on rerun | Not dismissed as flaky: conditions recorded, reproducible explanation sought, risk assessed; unresolved stays unresolved |
| 16 | Review process exits rc=0 with no verdict text | Not PASS: explicit complete verdict required for the expected snapshot; re-commission |
| 17 | Plan approved; user says "start now" in the planning session | Refusal: approval is not START; HANDOFF + manifest written, lifecycle `awaiting_fresh_session_start`, START prompt handed over; no execution worktrees/coding agents created (the earlier phase-3 read-only planning critic is not execution) |
| 18 | Fresh session receives the exact START prompt; manifest matches state | Session identity recorded; all file hashes recomputed and matched; repo/target/SHA/worktree-ownership/capability checks pass; start recorded; lifecycle `executing`; only then topology begins |
| 19 | START with a PLAN file edited after the manifest was written | Hash mismatch = consent invalidated; stop and reconcile (re-approve or restore); never quietly re-hash the manifest |
| 20 | Legacy STATE (schema 1), approved, nothing begun | No fabricated start/manifest; lifecycle set to `awaiting_fresh_session_start`; fresh-session START required; null manifest handled via recorded operator confirmation |
| 21 | Legacy STATE (schema 1), execution verifiably under way | Original approval retained; lifecycle `executing` recorded from evidence; sessions/start stay null where unknown; migration event appended; resume continues |
| 22 | SSE stream open, bytes flowing, no complete assistant turn | Transport activity only; no success/progress recorded; observation timestamp at most |
| 23 | Assistant record `stopReason` `error` or `aborted`, with `completedAt`/usage | Never success; counted as error/aborted observation |
| 24 | `model_usage` / `custom` / title / model-change / compaction rows only | Not progress; semantic progress timestamp unchanged |
| 25 | Repeated identical transport failures while successful steps continue | Health `degraded`; continue; no kill; watch |
| 26 | No successful step past the diagnostic budget; tool within its per-tool deadline | Health `suspect_stall`: inspect pending ask/tool deadline; diagnosis, not permanent FAIL; no kill |
| 27 | Pending interactive `ask` freezes the agent | Activity `waiting_input`; answer through the terminal; never kill |
| 28 | Watchdog snapshot stale (old mtime) or malformed/rotated/partial session log | Reported `unknown`/fault, never healthy; bounded reads; no fabricated progress; no raw content or error strings in output |
| 29 | `branch_summary` discarded-entry-branch records replayed/dropped work | Discarded branch is not progress; only the live parent branch counts |
| 30 | Watchdog process restarted mid-campaign | Per-task ages persist via sidecar state; no reset to zero; canonical STATE/TODO/EVENTS untouched |
| 31 | Watchdog sidecar/output inspected for leakage | Only structural metadata and aggregated fingerprints; no raw messages, tool args, secrets, or output blowup |
| 32 | SSE/log metadata churn, empty verdict shell, watcher restart, or coordinator restart mid-attempt | Attempt budget clock does NOT reset; `attempt.started_at` recorded in state stands; only a genuinely new scoped attempt starts a new budget |
| 33 | Reviewer writes a partial verdict document, exits rc=0, or hits budget expiry | Not PASS: only a complete explicit verdict for the expected snapshot counts; the skeleton's existence/mtime is not progress - substantive completed criteria with evidence are; incremental skeleton updates are the useful signal |
| 34 | Attempt reaches the 35-minute budget without completion | Scoped settle: fence the writer, preserve partial work + logs, shorten the brief, restart scoped; not a permanent feature FAIL, never auto-acceptance |
| 35 | Two unproductive provider attempts on the same slice vs substantive review FAIL/fix cycles | No blind third same-route retry: approved fallback for this task/attempt or pause with evidence/options; substantive test/fix/review cycles keep no fixed limit while evidence shows progress; useful FAILs with fixable findings are productive |
| 36 | Build/test legitimately exceeds the default attempt budget | Allowed only under a predeclared bounded phase deadline recorded before launch with real completion/checkpoint evidence; retroactive or open-ended extensions refused |
| 37 | Remediation wants a different or heavier model mid-campaign | Only the approval-bound fallback (and optional final-review) model may be used; any other switch pauses for explicit user approval |
| 38 | Watchdog output looks wrong mid-campaign | Report unknown, apply the declared attempt budget, continue with the packaged observer or bounded manual status as shipped; watcher improvement becomes a separate maintenance task - no mid-execution edits |
| 39 | Agent dispatched hidden/headless; `terminal focus` returns `navigated:false` | Not treated as user-visible: verify discoverability/link, disclose to the user, bind handles + session identity, no duplicate writer when moving UI |
| 40 | Bounded watcher running; a session JSONL is already 26m silent at spawn; later the campaign reaches `completed` | First poll fires `SILENCE_NUDGE`: exactly one bounded nudge to the pinned handle, exit 0, completion notification wakes the coordinator; at `completed` the coordinator spawns NO next slice (auto-stop - no daemon, no token burn); a dead watcher-hosting terminal is reported as monitoring-down, never claimed as coverage |
| 41 | Coordinator resolves the current campaign tip to a raw SHA and passes it as `--base-branch` | Refused: task worktrees take `--base-branch <campaign-branch>` (the branch Orca returned) plus `--parent-worktree` under `{prefix}-campaign`; re-resolve the branch tip against the recorded current tip, then create |

| 42 | Coordinator tries to create a DAG immediately after intake | Forbidden: mandatory read-only repository discovery, cited web research/architecture, and independent hash-bound CONVERGED critique must complete first |
| 43 | Web search/source retrieval is unavailable | Record blocker and pause for restored access/user direction; no model-knowledge-only architecture, invented citations, or DAG |
| 44 | Critic finds that the chosen architecture contradicts explicit user intent | Preserve intent; revise architecture or surface genuine infeasibility/trade-off; no silent requirement change; fresh critique required |
| 45 | Critique finds a major Security or UX omission; revision fixes only that section | Coordinator responds to finding, updates hashes, and obtains a FRESH full five-lens independent critique; previous verdict is stale |
| 46 | Critique says CONVERGED but INTENT or RESEARCH changed afterward | Hash mismatch invalidates convergence; no DAG/task files until a fresh critique binds current artifacts |
| 47 | Small conventional feature vs big user-facing/security-sensitive feature | Both require repository discovery and web research; breadth scales, but big features receive substantive scenario-based Security and UX analysis rather than N/A |
| 48 | Coordinator designs a custom parser/scheduler/UI component without searching for or evaluating mature open-source libraries | Critic flags a major Lens 2 finding (`REVISE`); no convergence or DAG until a live-verified OSS evaluation and a reuse-or-justified-custom disposition land in RESEARCH |
| 49 | Coordinator selects a package from model memory, or picks an archived/deprecated/license-incompatible library | Critic flags a critical/major Lens 2/3 finding (`REVISE`); coordinator must verify live registry + upstream repository status and switch to a maintained compatible library or a justified alternative |
| 50 | Live OSS evaluation finds (a) one library covers ~90% of the feature, or (b) the repository enforces `stdlib-only`; when new packages ARE adopted, parallel tasks need them | (a) whole-coverage option surfaced to the user rather than padding custom tasks to justify a DAG; (b) `stdlib-only` constraint honored and recorded as the justification; adopted packages pinned in shared contracts with manifest/lockfile updates serialized in a prerequisite/exclusive-owner task |
| 51 | OCR is installed and `ocr llm test` passes at planning start | `review_engine: ocr` recorded in HANDOFF/STATE; all per-task and final code review commissioned exclusively as OCR runs; no inquisitor code-review session; reviewer model pinned as OCR's model |
| 52 | OCR is not installed at planning start | Installation offered exactly once at the start; accepted -> install + verify then exclusive OCR engine; declined -> decision recorded and standard session reviewer used for this campaign; no silent auto-install |
| 53 | OCR run exits rc=0 with `status: partial`, `failed(budget)`, or zero reviewed files | Not a verdict: remediate (retry/resume/config) or escalate to the user; never PASS, never a silent switch to an inquisitor session |
| 54 | OCR JSON contains one medium, one high, and two low findings | FAIL: medium and high block; low findings recorded in evidence only, never fix-card material; executor fixes, runtime retest, fresh OCR run on the new SHA |
| 55 | Blocking finding has `start_line=end_line=0` (positioning failed) | Finding stays valid: locate via `existing_code` before triage; never dropped because of positioning |
| 56 | OCR endpoint unreachable mid-campaign; an inquisitor profile is available | No fallback: remediate OCR (config/endpoint/resume) or pause and escalate; the recorded engine binds the campaign; switching engines requires explicit user approval |

## Recording results

For each scenario record: files/sections consulted, the step the procedure prescribes,
and the observed outcome of following the text. A scenario whose prescribed action
contradicts its expected outcome is a documentation defect: fix the skill text, then
re-run that scenario and its neighbors. Keep validation notes out of the skill payload.
