# Pre-Group R2 phase 1 — documentation specification S1

## Decision and scope

Stage **uninstalled `skills/acd-orca/` alongside unchanged `skills/acd/`**. This is the default, not a live cutover. No installed loading path changes. Later explicit owner cutover authority is required to promote the candidate or change legacy references. Preserve existing fleet SOULs, common contract, legacy scripts/tests and frozen R2 artifacts. Groups are deferred: no dependency, message or experiment.

Authority: this directory's BRIEF; reviewed R2 candidate SHA-256 `89fa202f0d82ba2655e65a338e1eac2780a1e5d27cf5ce4771e18fcf934b629b`. This specification authorizes no implementation. No worker, Run, branch, configuration, installation, commit/push or publication now.

## Exact proposed tree and ownership

All paths below are proposed, not installed. Prefix `C = skills/acd-orca/`.

```text
C/SKILL.md
C/references/roles.md
C/references/planning-and-design.md
C/references/handoff.md
C/references/ocr-review.md
C/references/state-and-recovery.md
C/references/runtime-review-and-integration.md
C/references/orca-runtime.md
C/references/validation-tabletop.md
C/references/obligation-ledger.md
C/references/engines/omp.md
C/references/engines/hermes.md
C/references/engines/codex.md
C/templates/INTENT.md
C/templates/RESEARCH.md
C/templates/CRITIQUE.md
C/templates/PLAN.md
C/templates/HANDOFF.md
C/templates/TASK.md
C/templates/TODO.md
C/templates/PLANNING_STATE.json
C/templates/STATE.json
```

| Owner/content | Placement and linking rule |
|---|---|
| Portable procedure | SKILL entrypoint links references; invariants live once in their owning reference |
| Role responsibility | roles.md links unchanged `fleet/bots/{logis,logis-intent,logis-architect,inquisitor-ferrum,inquisitor-intent,magos-fleet}/SOUL.md` and `fleet/templates/magos-project/SOUL.md`; no copied personas |
| Shared policy | Link `fleet/skills/fleet-campaign/references/common-contract.md`; do not duplicate it |
| Mandate/local identities | handoff.md specifies project charter and private bindings supplied at execution; no live IDs/paths in payload |
| Orca mechanics | orca-runtime.md tells recipient to discover installed CLI, version-matched skills/help and native receipts; not a copied CLI manual |
| Engine loading | Three startup sheets document supported loading and evidence checklist; OMP observed transport only, Hermes/Codex unqualified |
| Migration accountability | obligation-ledger.md indexes every legacy section/reference/template/script with disposition and destination |

Existing SOUL/template paths still point to `.agents/skills/fleet-campaign/SKILL.md`. Staging does not load acd-orca. Ledger records that a later coordinated loading-path decision is needed; no automatic repointing or standalone distributability claim.

## Source → destination ledger contract

`A = skills/acd/SKILL.md`; `R/T = skills/acd/references/ or templates/`. RETAIN means semantic guarantee, not literal copy. All replacement text is English.

| Source | Destination under C | Disposition |
|---|---|---|
| A roles, fleet SOULs/common policy | roles.md + SKILL links | RETAIN ownership, independence, existing definitions |
| A§§1–4; R/planning-and-design.md | references/planning-and-design.md | RETAIN discovery/live research/reuse/five lenses/critique-before-DAG; REPLACE blanket repeat review with critic-owned affected-scope/current-hash attestation |
| A§§5–7; R/handoff-and-start.md | references/handoff.md | REPLACE WHAT/fresh-START/model-questionnaire ceremony with actual mandate; RETAIN requested/resolved/actual models, frozen hashes, identity/drift reconciliation |
| A§§0,9; R/ocr-review.md | references/ocr-review.md | RETAIN initial independent fail-closed OCR, raw coverage/severity evidence; REPLACE automatic planning install offer/session fallback with authorized preflight before coding, no silent swap |
| A§§8–10,13; R/runtime-review-and-integration.md | same reference basename | RETAIN topology, three-coder ceiling, exclusions, squash receipts, integration/smoke/moved-target checks and source retention before release |
| A§§11–12; R/state-and-recovery.md; progress distinctions in R/progress-watchdog.md | references/state-and-recovery.md | RETAIN sole writer, null unknowns, durable intent/state, clocks, no duplicates; REPLACE poll cadence/hard-expiry restart with native receipt reconciliation/guarded settlement |
| R/hermes-orca-omp.md, coordinator-heartbeat.md | references/orca-runtime.md + engines/*.md | REPLACE Hermes-specific execution, terminal injection and watcher/heartbeat with native wakes; DEFER parity claims |
| R/validation-tabletop.md | same reference basename | RETAIN synthetic labeling; REPLACE obsolete START/watcher expected actions with R2 native cases |
| T/INTENT,RESEARCH,CRITIQUE,PLAN,HANDOFF,TASK,TODO.md; PLANNING_STATE,STATE.json | corresponding templates | RETAIN evidence/contract structure; REPLACE legacy authority/lifecycle/poll/provider semantics explicitly |
| scripts/campaign_watch.py, omp_events.py; T/bounded_watcher.sh,WATCH.json | ledger only | EXCLUDE from candidate; legacy retained unchanged, no executable migration |

Templates must encode blocked, never-dispatched coordinator-completed product acceptance gates; exact review/integration/smoke bindings; persisted absolute deadline checked before dispatch/integration; unknown=null; immutable input hashes. Remove operative `ocr_or_session` fallback, fresh-session START, ten-minute polling and unbounded-loop language; preserve diagnosed productive iterations within declared bounds. Historical explanations remain labeled non-operative.

## Ordered one-document slices

Future execution: project Magos coordinates OMP in an Orca-managed worktree, never a Kanban coding profile. Reuse existing feature worktree only after verifying sole-writer custody, named branch/base SHA and no conflicting work; otherwise request native placement within the mandate. Never infer a clean base from this plan.

Each table entry containing multiple names expands into **separate serial slices, one file each**. Allowlist per slice: exactly its document plus `fleet/.local/doc-cutover/validation/<slice>.md` receipt; no other substantive edits. Frozen R2 and mapped original source are prerequisites for every slice.

| Order | File(s), individually | Additional prerequisite / done criterion |
|---|---|---|
| 1 | references/obligation-ledger.md | Inventory all sources above; every obligation tagged and destination named |
| 2 | references/roles.md | Ledger accepted; existing links and loading-path non-change explicit |
| 3 | planning-and-design, handoff, ocr-review, state-and-recovery, runtime-review-and-integration, orca-runtime references | Roles/ledger accepted; each source guarantee and R2 replacement made operational without duplicate policy |
| 4 | engines/omp, hermes, codex references | Runtime reference accepted; loading location/discovery and qualification limits explicit |
| 5 | Each of nine templates | Owning procedural references accepted; fields/enums/placeholder legend agree; no obsolete active prescriptions |
| 6 | references/validation-tabletop.md | References/templates accepted; complete static recipe and synthetic negative cases |
| 7 | SKILL.md | All preceding documents accepted; short entrypoint, flat frontmatter, all links resolve |

Every slice receipt contains source/candidate hashes, actual static commands/results, unresolved findings and independent changed/affected-scope verdict. No author self-PASS. Intermediate links to not-yet-authored planned files are explicitly pending, never falsely passed; final cross-document gate requires zero missing links. An independent reviewer must bind each verdict to exact current hashes. OCR runtime qualification is not required for Markdown-only planning acceptance; no code-provider substitution is implied.

## Concrete validation recipe

Existing `tests/test_planning_contract.py` and `tests/test_ocr_review_contract.py` hardwire legacy `skills/acd` and legacy wording. Future command `python3 -B -m unittest discover -s tests -p 'test_*contract.py'` protects legacy only, not candidate acceptance. Do not rewrite those tests to manufacture candidate PASS.

No candidate harness exists in inspected sources. Use a one-shot read-only `python3 -B -c '<stdlib checks>'` from repo root; retain exact command in the slice receipt, not a new framework. Restrict authoring to flat scalar frontmatter (`name: acd-orca`, nonempty description <=60 characters, version), ordinary inline relative links and unique simple heading anchors. Reject unsupported YAML constructs rather than pretending to parse general YAML. Use pathlib/re/json/hashlib/unicodedata to check:
- explicit 22-file allowlist; frontmatter grammar; JSON files and fenced JSON parse;
- relative targets/anchors resolve (including external-to-candidate fleet links); no traversal beyond repository;
- declared placeholder inventory matches uses; substitute representative values and parse resulting JSON;
- source/R2 hashes unchanged; no credentials, actual UUID/runtime IDs or host paths;
- report non-English-letter and obsolete-term candidates as file:line diagnostics, not automatic semantic verdicts.

Human independent review verifies English semantics and operative instructions. Ledger history, prohibitions, angle-bracket examples and intentional placeholders receive narrow documented exemptions; blanket suppression is forbidden. Synthetic tabletops cover stale hash, failed review gate, deadline while busy, permission denial, pause/late reply and dirty cleanup; record prescribed outcomes, never label them runtime tests. Final acceptance requires static receipts, all template/reference consistency, complete ledger and independent exact-manifest PASS.

## Stop and later pilot boundary

After documentation acceptance, stop: candidate remains uninstalled; no phase-2 launch. Later authority must name intended repository/base, delivery rights, resource exclusions and attempt bounds. Before coding pilot require execution-host loading, four permission scopes, actual primary/auxiliary/OCR purpose evidence; OCR authorized binary/provider/model/secret/tool-call preflight, then candidate preview/complete coverage; actual blocked acceptance-gate transitions, native deadline admission and source-retention/release proof. Auxiliary/OCR/engine uncertainty limits execution qualification, not this specification. No Groups prerequisite.
