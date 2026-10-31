# {{prefix}} Campaign TODO

> Projection of `{{prefix}}_STATE.json` (authoritative). Coordinator writes both. A box
> is checked only after the action is ACTUALLY verified - cleanup boxes require proven
> removal, never promises. If no todo-list tool exists, this file on disk is the
> operational checklist. Rebuild from state after any restart.

## Start gates (once per campaign)

- [ ] plan approved (single WHAT gate - approval is NOT execution start)
- [ ] `{{prefix}}_HANDOFF.md` + `{{prefix}}_MANIFEST.json` written; manifest sha256 in state
- [ ] planning session STOPPED (no execution worktrees or agents were created)
- [ ] explicit START by the user in a distinct fresh session; manifest validated;
      start recorded in state (lifecycle `executing`)

<!-- Resumes of an already-started campaign skip these gates; the recorded start and
approval remain bound. -->

## Tasks

### {{prefix}}-{{task_name}} - stage: {{stage}}

- [ ] develop
- [ ] runtime test-loop (test -> fix batch -> test; no fixed iteration cap)
- [ ] independent review-loop (FAIL -> fix -> retest -> fresh review)
- [ ] squash integration / conflict handling (receipt recorded)
- [ ] post-merge runtime smoke on campaign tree
- [ ] evidence preserved + cleanup verified (inventory proven removed)

<!-- Duplicate the block above per task. Dependencies release only after the
prerequisite's post-merge smoke passes - not on the executor's done message. -->

## Final campaign stages

- [ ] every task TODO above done
- [ ] full campaign acceptance + seams runtime test at exact campaign tip
- [ ] independent final review at exact campaign tip (explicit complete verdict)
- [ ] moved-target integration handled (if target moved: fix/test/review rules re-run)
- [ ] refs verified immediately before final merge (`--no-ff` per approval record)
- [ ] final merge to original target executed by coordinator
- [ ] post-final-merge runtime smoke ON target
- [ ] receipts + evidence archived OUTSIDE every disposable worktree
- [ ] scoped test resources stopped (proven)
- [ ] campaign worktree removed (after smoke success)
- [ ] `{{prefix}}_REPORT.md` written

Campaign status: {{in_flight|paused|done}} - next action: {{next_action}}
