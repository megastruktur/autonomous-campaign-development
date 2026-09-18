# Skill Validation: Static Checks and Tabletop Walkthroughs

Use after authoring or modifying this skill, before relying on it for a live campaign.
Static checks are mechanical; tabletops are reasoned walkthroughs of the written
procedure against scripted situations - document actual reasoning and outcomes, and
never present a tabletop as a live feature test.

## Static checks

1. Frontmatter parses as YAML; `name` matches the directory; `description` <= 60
   characters; `version` present; `metadata.hermes.category` is `software-development`.
2. `templates/STATE.json` parses as valid JSON; every unknown is `null`; the only
   brace-bearing strings are the documented filename conventions (`{prefix}_*`); enums
   match the documented schema.
3. Every relative Markdown link in every file resolves to an existing file/anchor.
4. Every `{{placeholder}}` in templates appears in the template's own legend or is
   self-evident from context; templates stay valid after placeholder substitution
   (JSON especially).
5. English-only scan: no non-ASCII letters outside code examples; no credentials,
   tokens, or environment-specific absolute paths except clearly-labeled examples.
6. TODO templates contain the mandatory per-task stages AND the final campaign stages.

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

## Recording results

For each scenario record: files/sections consulted, the step the procedure prescribes,
and the observed outcome of following the text. A scenario whose prescribed action
contradicts its expected outcome is a documentation defect: fix the skill text, then
re-run that scenario and its neighbors. Keep validation notes out of the skill payload.
