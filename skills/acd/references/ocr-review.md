# OCR Code-Review Protocol (v1.7.0)

OCR = [alibaba/open-code-review](https://github.com/alibaba/open-code-review), a
deterministic-plus-agent code-review CLI (`ocr`). This contract applies ONLY to code
review: per-task candidate reviews and the final campaign review. The planning critic
and runtime testing keep their existing mechanisms. OCR is an optional external tool:
the skill bundles no OCR binary and installs nothing by itself.

## 1. Engine selection gate (start of planning)

1. Detect OCR once at the start of planning: resolve the binary (`command -v ocr`;
   also probe the runtime's npm global bin dir - e.g. `~/.npm-global/bin/ocr` - when
   sandboxed PATHs hide it), then run `ocr version`. Record the resolved absolute path
   and version in the plan/HANDOFF prerequisites.
2. **Installed and working** -> code review runs EXCLUSIVELY through OCR for the whole
   campaign. No inquisitor-style reviewer session is commissioned for code review, and
   no silent fallback exists: an OCR failure is remediated (fix configuration, retry,
   `--resume`) or escalated to the user as a blocker - never swapped for another engine.
3. **Not installed** -> OFFER installation once, at the very start of planning, before
   architecture work: `npm install -g @alibaba-group/open-code-review` (Node.js + npm
   required; git >= 2.41 recommended - older git only warns but is unsupported). The
   offer states what OCR is and that accepting makes it the exclusive code-review
   engine. User accepts -> install, verify (`ocr version` + `ocr llm test`), proceed
   under rule 2. User declines -> record the decision; code review uses the standard
   independent reviewer session (inquisitor-style/read-only OMP) for this campaign.
4. **Installed but unusable** (no LLM configured, `ocr llm test` fails, endpoint
   unreachable): stop and ask the user for endpoint/credentials per the secrets
   contract below; never invent credentials. If the user cannot provide a working
   endpoint, record the blocker and the user's explicit engine decision; do not
   silently fall back.
5. Record the engine decision in HANDOFF (`review_engine`: `ocr` or `session`) and in
   STATE (`models.review_engine`). A running campaign keeps its recorded engine across
   restarts; switching engines mid-campaign requires explicit user approval.

## 2. Configuration and the reviewer model

- OCR config lives at `~/.opencodereview/config.json` (real user home). Provider entry:
  built-in (`anthropic`, `openai`, `openrouter`, `dashscope`, ...) or **custom** for
  self-hosted OpenAI-compatible gateways (e.g. LiteLLM): `providers.<name>.url`,
  `.model`, optional `.protocol` (`openai` default), and credentials.
- **Secrets contract**: never store API keys in the config or pass them as shell
  arguments. Use `api_key_cmd` pointing at a secret-manager helper (e.g.
  `ocr config set providers.<name>.api_key_cmd "<helper that prints the key>"`); the
  helper reads from the host's secret store at runtime (1Password `op read` or
  equivalent). The helper must resolve under the REAL user home - a sandboxed `$HOME`
  breaks token-file lookups; verify the helper in the same environment OCR will run in.
- The **reviewer model from the questionnaire is OCR's model**: resolve it to an exact
  ID that OCR's endpoint actually serves (verify against the endpoint's model catalog),
  then pin it with `ocr config set providers.<name>.model <id>` and pass
  `--provider <name> --model <id>` explicitly on every run. Never rely on ambient env
  resolution (`OCR_LLM_*` / `ANTHROPIC_*`) for campaign determinism.
- Verify before first dispatch: `ocr llm test` must pass, including its tool-call round
  trip. The review model MUST support native tool calling (reasoning-only models such
  as deepseek-r1 do not work: OCR reports "No tool calls parsed" and produces no
  findings). Re-verify after any model/provider change.
- Optional: `ocr config set language English` for English findings.

## 3. Invocation protocol (per-task review)

One OCR run per frozen candidate, dedupe by candidate SHA (same rule as session review).
Prefer commit mode on the task's committed candidate tip:

```bash
ocr review --repo <task-worktree> --commit <candidate-tip-sha> \
  --effort low --audience agent --format json \
  --output <evidence>/ocr_<task>_<sha>.json \
  --background-file <packet.md> \
  --provider <name> --model <resolved-reviewer-model> \
  --max-tokens-budget 500000 --concurrency 4 --timeout 10 --max-tools 60
```

- Before the paid run, verify coverage for free: same mode flags plus `--preview`
  (no LLM calls). Check the will-review/excluded file lists against the acceptance
  surface; record the preview in evidence. If acceptance-relevant files are excluded
  (default path filters, oversize diffs), resolve via `--exclude`/rule adjustments or
  split the candidate - never review a silently narrowed scope.
- `--background-file` carries the unbiased packet: acceptance criteria, exact diff
  base/tip, contracts, runtime-evidence pointers, known findings. Raw material only -
  never the author's reassuring summary, never "already PASS, please confirm".
- Effort defaults: per-task `low` (one review round; the economical mode), final review
  `medium`. `high` only on explicit user choice. `--effort` scales the per-task timeout
  (rounds x `--timeout`).
- Budget guard: `--max-tokens-budget` caps total input+output tokens for the run
  (enforced per round since v1.12.2+; on exceed, the group gets one final round, is
  reported `failed(budget)`, and partial results are published). Defaults: 500000 per
  task, 2000000 for the final review; overrides recorded in the plan. A budget stop is
  NOT a verdict (see section 5).
- Never use `ocr scan` for campaign review: whole-file scan has a different, much
  heavier token model (per-file PLAN + repeated MAIN loops). Campaign review is always
  diff-based `ocr review`.
- OCR is an MCP CLIENT, not an MCP server: it can consume external MCP servers for
  context, but cannot itself be embedded as an MCP tool. The CLI is the integration
  surface. Delegation mode (`ocr delegate`) is NOT used: the review must run on OCR's
  own configured model, not the host agent's.
- Long runs: launch as a supervised background process with completion notification;
  the JSONL session file under `~/.opencodereview/sessions/<repo-slug>/<session-id>.jsonl`
  is the transport evidence (progress semantics unchanged: transport activity is not
  progress). Interrupted runs resume with `ocr review --resume <session-id>` (strict
  identity check on diff/rules/model); never silently restart from zero.

## 4. Final review

Same protocol at the exact campaign tip, range mode:

```bash
ocr review --repo <campaign-worktree> --from <target-branch> --to <campaign-tip-sha> \
  --effort medium --audience agent --format json \
  --output <evidence>/ocr_final_<sha>.json --background-file <packet.md> \
  --provider <name> --model <resolved-reviewer-model-or-approved-final-model> \
  --max-tokens-budget 2000000 --concurrency 4 --timeout 15 --max-tools 60
```

The optional questionnaire final-review model, when approved, is passed here as
`--model`. Moved-target integration re-runs this review at the new tip; old verdicts
are stale by construction.

## 5. Verdict derivation (coordinator-owned)

OCR emits findings, not PASS/FAIL. The coordinator derives the verdict from the JSON
and records it exactly like a session-review verdict (bound to commit/tree/build):

1. **Run validity first.** rc=0 alone is not a verdict. Require `status: complete`
   (manifest present) or `success` (legacy shape), `summary.files_reviewed > 0`, and
   coverage of every acceptance-relevant file (`manifest.coverage.excluded` checked).
   `partial`, `failed`, `failed(budget)`, `skipped`, zero reviewed files, or an empty
   result file are NOT verdicts: remediate (retry/resume/fix config) or escalate.
   `comments: []` with `files_reviewed > 0` means clean; with 0 files it means skipped.
2. **Severity policy (blocking set): `critical`, `high`, AND `medium` block.** Any
   blocking finding -> FAIL with actionable findings routed to the executor; fix ->
   runtime retest -> fresh OCR run on the new SHA. `low` and style-only findings never
   block and are not fix-card material (record them in evidence only).
3. **Positioning failures are still findings.** `start_line = end_line = 0` means OCR
   could not locate the lines; the comment remains valid - locate it via `existing_code`
   before triage. Never drop a blocking finding because of positioning.
4. **Triage ownership.** The coordinator triages the JSON itself (severity + category +
   relevance to acceptance criteria). False positives are dismissed with a recorded
   reason, never silently; disputed findings go to the user. No separate reviewer
   session is layered on top of OCR - that would reintroduce the replaced engine.
5. Record in STATE `tasks[].review`: verdict, `bound_to` (exact SHAs), plus OCR evidence:
   `session_id`, output JSON path, summary token counts, and the run manifest's
   `terminal_state`. Archive the JSON under `{prefix}_evidence/`; optionally
   `ocr session export --session <id> -o <evidence>/review.html` for the human report.
6. The verdict binds the exact reviewed SHA; any new commit invalidates it. The
   runtime-test layer stays separate and mandatory: OCR reviews code, it does not
   exercise the application.

## 6. Failure handling (no fallback)

- LLM/config failure: `ocr llm test`, check provider URL/model/key helper under the real
  home; fix and retry the same candidate. Repeated identical failures -> evidence-based
  pause and user escalation, per the remediation ladder.
- Budget stop (`failed(budget)`): partial findings are evidence, not a verdict. Options:
  raise the budget with user approval, narrow the candidate, or `--resume` after a
  transient failure. Never accept partial as PASS.
- Tool-round exhaustion ("Max tool requests reached", zero findings): suspect a
  non-tool-calling model or an oversized group; verify the model, reduce scope, retry.
- git version warning (< 2.41): record it; recommend upgrading git. If review behavior
  is actually broken, treat as blocker, not as a reason to switch engines.
- At every failure the rule is the same: remediate OCR or escalate to the user. An
  inquisitor/session reviewer is never silently substituted while OCR is the recorded
  engine.

## 7. Token economy (why this mode)

- `review` effort low = 1 round (medium = 2, high = 3): the primary cost lever; the
  upstream benchmark reports ~1/9 the tokens of a general-agent review at higher
  precision, with lower recall - the blocking-severity policy plus runtime tests
  compensate for recall.
- The per-group PLAN pre-pass auto-skips for small diffs (largest file < 50 changed
  lines and group total < 100): context-sized ACD slices usually avoid it. There is no
  `--no-plan` flag on `review`; do not try to defeat the thresholds mid-campaign.
- Keep the LLM post-filter ON (no `--no-filter`): precision over raw recall; the
  coordinator's triage is cheaper than noise-driven fix rounds.
- Observed baseline (v1.13.10, LiteLLM endpoint, effort low, one small commit):
  ~37k total tokens, ~53s wall, cache reads absorbed ~57% of input. Use this as an
  order-of-magnitude sanity check, not a guarantee; record actuals per run in evidence.
