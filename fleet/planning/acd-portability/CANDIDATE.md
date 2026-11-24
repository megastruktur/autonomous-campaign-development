# ACD portability — candidate R2

## Decision and authority

Migrate ACD 1.7.0 into a documentation-first, engine-neutral procedure **on Orca**, not a replacement orchestrator. Markdown plus native startup loading and a capability checklist are sufficient until a reproducible gap proves otherwise. No executable adapter or dependency is proposed.

This assignment produces a plan only. No implementation, Run, Task, worker, installation, configuration/SOUL changes, restart, commit/push, packaging/publication or old-Bot mutation is authorized. Future phases below require an actual development mandate, not a ritual START. Current CHARTER/BRIEF govern; original ACD is migration evidence. A ready plan is not development acceptance.

## Boundaries and responsibility

| Layer | Owns | Must exclude |
|---|---|---|
| Portable core | Authority; intent→discovery/research→independent critique→DAG; evidence/acceptance/recovery invariants; review-provider contract | Engine syntax, host identities, credentials |
| Role SOULs | Logis synthesis; complementary Intent/Architect reasoning; independent critics; project Magos execution; worker implementation | Duplicated CLI recipes, self-approval |
| Project charter | Mandate, outcomes, non-goals, named base, budgets, exclusions, delivery permissions, steering revisions | Invented authority |
| Private bindings | Discovered Bot/chat/Run/Dispatch/host identities, exact model routes, native receipts | Secrets, public export |
| Orca runtime reference | Version-matched commands, launch/reply/stop semantics, permissions, cleanup | Watchers, mailbox consumers, extra schedulers |
| Engine startup sheets | Supported instruction loading, executable/version, actual permission/model discovery and qualification checklist | Parity inferred from Markdown support |

Logis is sole planning writer. Critics own blocker closure. Existing project Magos is the sole execution-owner chat, not a Bot-wide mutex; reconcile native ownership before mutation. Coordinators neither implement nor resolve source conflicts. Project facts stay in project artifacts; shared memory remains generic.

## Original obligations: disposition ledger

Source abbreviations: A=`skills/acd/SKILL.md`; P=`references/planning-and-design.md`; O=`references/ocr-review.md`; S=`references/state-and-recovery.md`; I=`references/runtime-review-and-integration.md`; V=`references/validation-tabletop.md`. References are under `skills/acd/`.

| Source obligation | Disposition and migration rule |
|---|---|
| A§§1–3, P§§1–3 discovery/research/reuse | RETAIN bounded repository/interface/test discovery and current primary sources before design; native/stdlib, whole-library, partial-library order; registry/upstream license, maintenance, security and footprint checks before new dependencies. No dependency is selected here. Retrieval failure stays explicit; no invented research. |
| A§§3–4, P§§3–4 critique/DAG | RETAIN independent original-intent, architecture, Security, UX and readiness lenses; hash-bound convergence before native Tasks. REPLACE blanket repeated full review with critic-owned changed/affected-scope recheck plus explicit current-candidate attestation for reused unaffected evidence. |
| A§§5–7 questionnaire/WHAT/START | REPLACE routine human ceremonies with mandate-bound Logis→existing Magos handoff. RETAIN requested/resolved/actual model receipts, explicit execution identity, frozen inputs and drift reconciliation; no silent re-hash. Missing authority or consequential choices still escalate. |
| A§§7,11 watcher/heartbeat/poll cadence | REPLACE with native result wakes and exact-owner one-shot deadline reconciliation. End turns while waiting. Retain separate observed/assistant/tool/semantic-progress facts; a Run/status file is not a scheduler. No reboot-liveness promise. |
| A§§8–10, I topology/concurrency | RETAIN named target/base SHA, Orca child-worktree branch/HEAD receipts, one writer/worktree, maximum three coders including fixes, exclusive lockfile/schema/port/database/effect ownership, serialized integration. Native launch surface replaces TUI-only assumption; require discoverable session/output. |
| A§9, O, I review/runtime | RETAIN exact source/scenario binding, real production-path tests, independent OCR, fail-closed coverage, squash receipts, post-integration smoke before successors. Analysis delivery is separate from product acceptance. |
| A§§11–12, S durability/recovery | RETAIN sole-writer durable state/revisions, intent-before-mutation records, unknown=null, original attempt clock, source preservation and no duplicate launch/merge. REPLACE hard-expiry stop/restart implication with native guarded settlement; silence alone cannot authorize either. |
| A§13, I cleanup/endgame | RETAIN exact-tip final runtime/review, moved-target revalidation, named-ref check before authorized final merge, target smoke, durable source/evidence before disposal, verified release; push/publication/deployment require separate authority. |
| A§12, V validation | RETAIN bounded attempts and substantive-progress distinction. General default: checkpoint 20 minutes, attempt 35 minutes, at most two unproductive attempts before escalation; native three-failed-start breaker is an additional ceiling, never a bypass target. Adapt old START/watcher tabletops to native semantics. |
| Engine/provider/public distribution | DEFER Hermes/Codex parity, replacement review provider, broad crash/reboot recovery and packaging until separately qualified/authorized; defer claims, not safety guarantees. |

## Native execution and review contract

Resolve installed CLI, then read `skills get orchestration` / `skills get orca-cli` and narrow help. Current inspected native families: `run-create`, `task-create --deps`, `task-list --ready`, `worker-start --task … --worktree new-child`, `send --to bot:… --chat …`, `reply --id`, Dispatch-addressed steering, worker read/show/list/stop/release. Pin local execution with `--environment local`, exact Run when ambiguous, named branch and returned HEAD. Launch acceptance is not proof work began; unknown outcome blocks duplicate launch.

Represent a product successor's dependency as an **acceptance gate**, not the analysis worker's Task success. Magos completes that gate only after exact-candidate independent review, integrated source and actual smoke evidence. Failed/inconclusive reports may successfully complete analysis Tasks but never product prerequisites.

The acceptance gate is a separate native Task kept `blocked`, never dispatched as work and never made `ready`. Product successors depend on that gate. Only the coordinator sets it `completed`, attaching bound review/integration/smoke receipts after all three pass. Verify these native transitions in qualification; Task/report success cannot complete it implicitly.

OCR remains the initial provider. Before its first authorized use verify binary/version, actual configured tool-capable model, `ocr llm test`, secret-manager access and free preview coverage. Installation/configuration is not implied. Run independently under native supervision; record whether read-only is enforced or only instructed. Packet: original acceptance, contracts, exact base/tip, scenario/runtime evidence, known findings. Result: provider/version/model, raw output, coverage, completion, findings and source binding. Complete, acceptance-covering, nonzero-file results alone permit verdict derivation: critical/high/medium→FAIL; low alone does not block. Partial/failed/budget/skipped/malformed/zero-coverage→INCONCLUSIVE. No critic fallback, no routine double review. Provider replacement requires captain steering or granted selection policy plus independent same-packet qualification. Changed source invalidates old acceptance; no stale PASS relabeling.

Pause stops new dispatch/integration; no claim that in-flight work exited. Late output is revision-scoped and archived, never applied to another candidate. Native deadlines use discovered trigger options, `--once --by` and exact owner chat; they stop new affected dispatch at expiry, reconcile and report, not hard-kill. Clean obsolete timers and ignore terminal-state wakes. Cancellation requires exact owned guarded stop and confirmed receipt; `stop_unknown` blocks replacement. Retry only after diagnosed changed cause with same Task/retry identity and current authority. Primary-model failure or permission refusal stops the affected path; no blind retries or unauthorized model switches. Resume reconciles original authority, source, ownership and pending actions; operator pause never self-resumes.

Before every affected dispatch or integration, the coordinator checks the persisted absolute deadline against actual current time and refuses new work after expiry. The Automation may queue behind a busy turn: it provides delayed reconciliation, not an exact-time barrier. This procedural check does not promise hard enforcement against a malfunctioning agent.

## Capability and installation truth

| Capability | Current evidence | Required qualification |
|---|---|---|
| OMP native transport | Historical peer/deadline plus fresh no-approval evidence-worker result/wake/release | Useful development, OCR, negative/recovery cases remain untested |
| Primary model | Historical Astra success; planner replies now received | Actual worker startup model, not picker alone |
| Auxiliary routes | Qwen per-home config; historical Intent judge proven; five stale judges and all smol use unresolved | Purpose-specific actual calls in fresh Bots AND project workers; unknown stays unknown |
| Hermes/Codex | Primary docs describe native chat; Hermes minimum documented as 0.23.0 | Local installation, loading, tools, permissions, model use, wakes and release independently tested |
| OCR/other review | Contract retained; fleet qualification absent | Real complete review/coverage and failure handling; alternatives separately qualified |

Owner-controlled setup distinguishes Bot defaults, existing chats, engine-specific OMP launch override and existing workers. Changes do not retroactively migrate sessions; individual approval is not Full access. Full access is optional and broader future-engine scope must be disclosed. Owner-only creation/permission actions cannot be impersonated. Preserve existing Homes/history; never reset chats, sleep groups or restart services as implicit repair. Verify instructions inside the execution host. Secrets stay in the configured secret manager; no private runtime IDs enter portable content.

## Bounded future phases and acceptance

These are ordered work packages, not created Tasks or an execution DAG.

1. **Documentation cutover — Logis/Architect, independent critics.** Produce core, role references, Orca reference, engine loading sheets and full obligation ledger. One bounded revision round for this design exercise. Static checks: English, valid links/templates, no private IDs/secrets, no active watcher/START prescriptions; synthetic tabletops are labeled synthetic. No supported-engine claim from text alone.
2. **Recipient preflight — project Magos.** Read versions, identities, four permission scopes and actual primary/auxiliary evidence. Prove role loading, correlated native reply, exact-chat scheduled wake/cleanup and fresh worker tool/result/wake/release where not already valid for the same environment. No mutation outside permission; missing capability blocks only its dependent path. Auxiliary uncertainty bars robust unattended claims.
   Before the first coding dispatch, also verify OCR binary/version, authorized provider/model, secret-helper access and successful native tool-call preflight. Missing/unusable OCR blocks development qualification without automatic installation or provider replacement. Candidate-specific free preview coverage remains mandatory at review time.
3. **Useful OMP pilot — Magos plus bounded workers.** Isolated qualification repository, no new dependencies, one writer at a time: A read-only manifest validator for source/scenario/verdict identities and file hashes; B dependent CLI. Pilot is not an orchestration adapter. Predeclare each attempt at 15 minutes, checkpoint 10 minutes, at most two unproductive attempts; longer tests need prior bounds. Runtime cases: valid packet exits 0; missing file/evidence, stale source/scenario binding, non-PASS verdict, incomplete coverage and byte drift exit nonzero naming the field. A review/integration/smoke gate precedes B. Final integrated CLI checks and exact-tip OCR precede ready-for-captain. Archive commits when authorized, otherwise attributable diff plus untracked source and evidence before completion/release; verify release before reuse.
4. **Adversarial qualification — independent verifier.** On disposable authorized fixtures exercise failed/incomplete review (successor remains blocked), denied permission (no bypass), unknown launch (no duplicate), pause plus late reply/deadline (no resume), source drift (stale verdict rejected), and cleanup with dirty source (preserve or block). Distinguish actual scenarios from tabletops; unavailable fault injection remains unqualified, not PASS. No destructive host failure needed.
5. **Engine parity, then optional distribution.** Repeat the same loading/tool/model/permission/wake/acceptance/release matrix separately for Hermes and Codex; no inherited OMP PASS. Only proven command/receipt gaps justify a thin translation/validation adapter, never scheduling ownership. Alternate provider and packaging each need their own authorization/qualification. Existing Bots remain untouched.

## Evidence and unresolved scope

Local authority: unchanged `CHARTER.md`, `BRIEF.md`; planner evidence: `CONTRIBUTIONS.md`; installation/transport/model status and project Magos template under `fleet/`. Native CLI references were inspected read-only, not executed as campaigns.

Architect retrieved 2026-11-23: [Orca engines](https://onorca.dev/docs/agents/supported), [native chat](https://onorca.dev/docs/agents/native-chat), [security](https://onorca.dev/docs/bots/security) (redirected to orca.dev); [Hermes skill loading](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/guides/work-with-skills.md). Hermes docs landing page returned 403. On-demand `skill_view` is not proof of Orca startup injection. New-chat auxiliary use, OCR, development and cross-engine behavior remain unqualified. Critics will judge this exact frozen design; Magos Fleet readiness is assessment only, never START.
