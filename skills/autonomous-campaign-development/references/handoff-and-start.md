# Planning Boundary, HANDOFF, and Fresh-Session START

Execution authorization is two-step by design: ONE plan approval authorizes WHAT may
happen; a separate explicit START in a distinct fresh coordinator session authorizes
execution to BEGIN. Approval of a plan is never START. This boundary is mandatory; it is
not a per-task human gate - it happens once per campaign.

## Planning session boundary

The planning session performs intake, clarification, plan authoring, the model
questionnaire, and approval capture. It writes ONLY planning artifacts under
`plans/{campaign_name}/`: PLAN, task files, HANDOFF, MANIFEST, and the initial STATE
(`lifecycle: planning`). It must NOT create execution worktrees or the integration
worktree, start agents or terminals, or dispatch anything - even after the plan is
approved. On approval it:

1. Writes `{prefix}_HANDOFF.md` and `{prefix}_MANIFEST.json` (templates:
   [../templates/HANDOFF.md](../templates/HANDOFF.md)).
2. Records the plan approval and `plan_manifest.sha256` in STATE; sets
   `lifecycle: awaiting_fresh_session_start`; appends the transition event.
3. Presents the exact START prompt (from the HANDOFF) and STOPS.

If the user asks the planning session to "go ahead", "start now", or similar: refuse,
restate that approval is not START, and hand over the START prompt. A same-session start
is forbidden even under user pressure in that session - the user's instruction belongs to
the NEW session. If runtime session identity is technically unavailable (no verifiable
session ID), a session cannot claim enforced clean context: get explicit operator
confirmation that the target session is fresh - and still never knowingly start in the
planning session itself.

## HANDOFF contract

The HANDOFF is the execution entrypoint - a curated pointer set, never a transcript
dump. It contains: campaign goal and scope summary with key decisions; links to PLAN,
every task file, TODO, and STATE (repo-relative); repository path, original NAMED target
branch, full starting SHA; requested AND resolved model IDs per role; the authorized
permission scope (push/deploy/publication excluded unless explicitly granted - record
which); verified runtime commands and how each was verified, prerequisites, and known
blockers (null if none); monitoring and recovery policy (cadence, optional watchdog
intent, remediation ladder); and the exact START prompt. Every unknown stays null -
never invented.

## Manifest

`{prefix}_MANIFEST.json` freezes the planning payload: SHA-256 of the PLAN file, every
task file, every standalone shared-contract file, and the HANDOFF. Excluded: STATE,
TODO, EVENTS, evidence (mutable execution artifacts - their later changes must not
invalidate the plan approval), and the manifest itself (no recursive self-hash). The
manifest is written once by the planning session and is immutable afterwards; its own
SHA-256 is recorded in STATE (`plan_manifest.sha256`) and again in the start record.

## START (first execution start)

Execution begins only in a DISTINCT, NEW, CLEAN coordinator session when the user
explicitly says START (the exact prompt from the HANDOFF; a paraphrase naming the
campaign and manifest is acceptable). File presence alone is never authorization. On
START, in order:

1. Record this session's runtime identity (`sessions.execution.identity`).
2. Recompute every file hash in the manifest and the manifest's own hash; both must
   match STATE. Any mismatch means the approved plan changed: consent is invalidated -
   stop and reconcile with the user (re-approve or restore the frozen files). Never
   quietly re-hash the manifest to match drift.
3. Validate the repo: path exists, original target branch and starting SHA unchanged or
   consciously re-pinned by the user; no pre-existing execution worktrees conflicts;
   coordinator ownership is unique.
4. Verify capabilities actually available this session: worktree/terminal commands,
   reviewer mechanism, runtime test capability. Resolve every runtime command honestly -
   never guess or invent a command shape; an unresolvable command is a blocker recorded
   as such.
5. Record the start (`start.started_by/at`, `start.manifest_sha256`,
   `start.startup_checks`), set `lifecycle: executing`, append the event - then proceed
   to topology creation.

A failed check stops before any worktree or agent exists. START succeeds at most once;
later restarts are resumes, not new STARTs.

## Resume versus first START

Once `start.started` is recorded, the original approval and start remain bound: crashes,
restarts, and coordinator replacement follow the resume protocol in
[state-and-recovery.md](state-and-recovery.md) without a new approval and without a new
START gate. The fresh-session gate protects the planning-to-execution transition only;
it never re-gates an already-authorized campaign.

## State lifecycle

`planning` -> `awaiting_fresh_session_start` -> `executing` -> `completed` (pause is
orthogonal and reversible). Planning-session identity and execution-session identity
are recorded independently in `sessions`; the plan approval (in `approval`) and the
start (in `start`) are independent records. Schema and legacy migration:
[state-and-recovery.md](state-and-recovery.md#state-lifecycle-and-legacy-migration).
