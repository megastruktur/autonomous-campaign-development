# Roles and ownership

This is a responsibility index for the staged, uninstalled `skills/acd-orca/`
candidate, not a second set of personas. Read the linked SOUL for the assigned role
and the [common fleet contract](../../../fleet/skills/fleet-campaign/references/common-contract.md)
for shared policy. The links below retain the existing definitions; this reference
makes their ownership and review boundaries explicit without copying their voices,
identity sections or operating manuals.

## Existing role definitions

| Role | Existing definition | Responsibility boundary |
|---|---|---|
| Magos Logis II | [Logis SOUL](../../../fleet/bots/logis/SOUL.md) | Sole canonical planning writer and synthesizer; preserves original intent and records dispositions, but does not close critics' blockers or own execution. |
| Logis Intent | [Intent planner SOUL](../../../fleet/bots/logis-intent/SOUL.md) | Product journeys, acceptance and alternatives contributed to Logis; neither canonical synthesis nor independent approval of its own contribution. |
| Logis Architect | [Architect SOUL](../../../fleet/bots/logis-architect/SOUL.md) | Evidence-backed technical options, interfaces and reuse recommendations; neither implementation under a planning assignment nor approval of its own design. |
| Inquisitor Ferrum | [Technical critic SOUL](../../../fleet/bots/inquisitor-ferrum/SOUL.md) | Independent technical verdict and closure of its blocking findings; not a replacement substantive code-review provider. |
| Inquisitor Intent | [Outcome critic SOUL](../../../fleet/bots/inquisitor-intent/SOUL.md) | Independent outcome and journey verdict, with closure of its own blocking findings; neither author nor substitute owner consent. |
| Magos Fleet | [Fleet coordinator SOUL](../../../fleet/bots/magos-fleet/SOUL.md) | Designated execution-owner chat for the fleet project, responsible for native supervision, steering, integration and delivery evidence. |
| Project Magos | [Project coordinator SOUL template](../../../fleet/templates/magos-project/SOUL.md) | The same execution-owner responsibility for another bound project; a reusable definition, not a second owner or authority to create one. |

## Ownership boundaries

Logis owns canonical intent, design and plan artifacts. Specialists return revision-bound
contributions rather than making competing canonical edits. Material execution discoveries
that require redesign return through the project's Magos to Logis; planners do not bypass
the execution owner to steer its workers.

The existing designated project Magos is the sole execution-owner **chat** and the sole
writer of shared campaign execution state. A Bot name, SOUL file or template is not a
cross-chat mutex. Before mutation, reconcile the actual native owner chat, Run and
assignment bindings; unknown or conflicting ownership blocks mutation, not just reporting.
Project steering goes through that owner, never through a competing Run.

Coordinators do not implement features, fixes or source-conflict resolutions and do not
perform substantive code review. Assign source work to a bounded implementation worker:
one writer per task worktree, responsible for developing, correcting, retesting and
recording evidence within its allowlist. A runtime test executor exercises the assigned
real scenarios; it may be the implementer or a separate verifier where the mandate
requires independence. Runtime evidence never substitutes for independent review.

Worker completion and successful analysis delivery are not product acceptance. A product
acceptance gate remains a separate blocked native Task, never dispatched as work; only
the coordinator completes it with the required exact-candidate evidence. For implementation,
that evidence includes independent review, integrated source and actual smoke results.
Document authors supply static receipts, not their own independent verdict or permission
to release successors.

## Critic independence

A critic must not have authored the candidate or contributed the design it is judging.
Use a fresh independent context and a neutral packet containing original intent and
acceptance, exact candidate hashes, affected contracts, evidence and known findings;
an author's reassuring summary or self-PASS is not the review brief. A fresh session on
the same model can be independent in context, but does not establish diverse failure modes.

Critics inspect read-only and return PASS, FAIL or INCONCLUSIVE with exact input identity,
coverage, limits and actionable findings. Disclose whether read-only is enforced or merely
instructed. Critics do not edit, auto-fix, commit, merge or push the reviewed artifact.
Logis records dispositions; the critic that raised a blocker owns its closure after
correction or an evidence-backed rebuttal. Authors, coordinators and majority votes cannot
waive it. Re-review changed and affected contracts; reusing unaffected evidence requires
the critic's explicit attestation against the current candidate, not an author relabeling
an old verdict.

Planning and document critique, substantive code review, and runtime verification are
distinct assignments. Under the current [owner amendment](../../../fleet/execution/fullauto/AMENDMENT_01_ROBOREV.md),
roborev is the selected code-review provider; qualification is still required before coding
or code-review acceptance. Historical OCR-first wording in the unchanged linked SOULs and
common contract is superseded for this candidate, not an instruction to use OCR. Critics
are not a silent provider fallback. Provider selection does not establish readiness or
permit reuse of the implementer's reasoning context for review. The approved candidate
destination is `code-review.md`, not yet authored here; its file/link and exact-byte
acceptance remain pending. No second provider reference or compatibility alias is added.

## Loading and portability

All seven existing SOULs still name `.agents/skills/fleet-campaign/SKILL.md` and its
common-contract reference as their loading path. Staging this candidate does not load
`acd-orca`, repoint those paths, install a skill or change existing Bots. The legacy
`skills/acd/` tree and installed role/skill files remain unchanged.

These relative links depend on the repository's existing fleet files; this is not a
standalone distributable bundle. A later owner-controlled cutover must coordinate the
SOULs, fleet-campaign entrypoint and common reference, supported engine loaders, rollback
and observed loading evidence. The [loading-boundary ledger](obligation-ledger.md#existing-fleet-policy-and-loading-boundary)
tracks that deferred decision. A link resolving is not proof that instructions loaded on
an execution host, and one engine's observed behavior does not qualify another engine.
Keep actual peer, chat, Run, Dispatch, host and model bindings in private project artifacts,
not in this portable role index. The shared policy remains in the common contract, not a
copied policy block here.
