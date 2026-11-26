# Onboard one new PROJECT Magos with your agent

This brief prepares exactly one new PROJECT Magos Bot for fleet use on an execution host
where the instruction stack is already installed and pinned. The owner creates the Bot in
the Orca UI first; the agent then verifies, installs the reviewed per-Bot instructions,
binds the project privately and proves fresh loading. It does not install or update the
shared stack ([Install guide](INSTALL_AGENT.md)), create Bots, or start a campaign.
Related: [Setup](SETUP.md) · [Operations](OPERATIONS.md) ·
[Project Magos SOUL template](../fleet/templates/magos-project/SOUL.md) ·
[Common contract](../fleet/skills/fleet-campaign/references/common-contract.md).

## 1. Confirm scope and preconditions before writing

- Verify the shared stack is already installed: the durable release tree at the reviewed
  full SHA, the shared pair `~/.agents/skills/acd-orca` and `~/.agents/skills/acd`, and the
  lexical `~/.agents/fleet` bridge must resolve one consistent reviewed dependency set.
  Missing, mixed or unreviewed installation stops this brief; report it and use the
  [install guide](INSTALL_AGENT.md) instead. Do not install the shared stack here.
- The owner creates the Bot in the UI: **Bots → + (New bot or group) → New bot → Start from
  scratch → name/purpose → Change** (select computer and OMP agent) **→ Create**, per
  [Bot creation](SETUP.md#3-create-five-shared-bots-and-one-project-bot). Verify the actual
  home folder `~/.orca/bots/<name>` on the selected execution computer; a display label is
  not a folder name. One new PROJECT Magos only: no takeover, duplicate owner, extra
  coordinator or replacement chat as a workaround.
- Identify the actual execution host/user, project display name, repository path and
  identity, and the authorized target branch; never assume `main` or `master`. Ask only for
  missing consequential facts or authority. Read the current
  [skill](../skills/acd-orca/SKILL.md), common contract and SETUP at the pinned revision.
- Discover exact addresses from installed help: `orca bot list --json` and
  `orca bot chats --bot <actual-bot-name> --json`. A title is not an ID; there is no
  `orca bot show`. Record the selected Home Chat, not an old closed one. Do not infer
  execution facts from the desktop. Do not invent CLI/configuration keys or print
  credentials, environment secrets or account files.
- Authority: ordinary new setup for this one Bot, plus adding this one project's admission
  records to the five shared peers' private binding indexes while preserving every existing
  entry. No SOUL, bridge, permission or model change to an existing Bot; no campaign, Run
  binding, GitHub activation, connector setup or paid probe. Missing authority stops the
  affected step; report it instead of working around it.

## 2. Prepare and install the reviewed SOUL privately

- Make a private copy of the [Project Magos SOUL template](../fleet/templates/magos-project/SOUL.md).
  Replace only both occurrences of `{{PROJECT_NAME}}` with the project's display name; do
  not insert repository paths or IDs into the portable voice.
- Compare the generated SOUL with the reviewed replacement. Protected SOUL replacement
  requires actual interactive owner approval: export `APPROVED_SOUL_SHA256` as the generated
  file's owner-reviewed `sha256sum` value and `SOUL_BACKUP_DIR` as a new absolute directory
  inside the Bot home. Shell approval variables do not bypass the interactive approval.
- Use the literal `install-bot` Bash block in
  [SETUP](SETUP.md#3-create-five-shared-bots-and-one-project-bot) with
  `repo="${ACD_ORCA_RELEASE:?Set reviewed release}"` exported as the verified absolute
  SHA-addressed release path. Keep every dependency, collision and SOUL guard intact; never
  remove a guard to make the block pass.
- The block links the per-Bot bridge `.agents/skills/fleet-campaign` into the same reviewed
  tree; do not copy the bridge without its dependencies. An existing SOUL or bridge
  (including a copied regular directory with old policy) is a collision: compare contents
  and customizations, retain private backups and exact prior link targets, and obtain
  scoped migration approval per [Setup](SETUP.md) and [Operations](OPERATIONS.md) instead
  of overwriting. Partial runs need inspection, never a blind rerun or force.

## 3. Bind the project privately, on both sides

- Create private `FLEET_BINDINGS.md` in the new Bot home with `role: project-magos`, using
  the [binding shape](SETUP.md#4-bind-one-owner-and-the-shared-peers-privately). Replace
  every placeholder with verified execution-host facts before admitting development;
  `owner_run` stays null until a native receipt binds it. Keep the referenced charter
  outside tracked source; ignore rules alone are not privacy proof.
- Both-sided admission: each of the five shared peers must admit the same
  project/repository, designated owner, authorized request/revision and readable private
  charter in its own private binding index. Add this one project's mapping after
  comparison and owner approval; preserve every other project's entry and never leak
  records into shared memory. Owner-side bindings alone are insufficient. Unknown or
  refused projects stay blocked until separately authorized correction; never bypass the
  roster or silently expand peer scope.
- Before freezing, using or admitting project records, follow the
  [mandatory private template-instantiation preflight](INSTALL_AGENT.md#mandatory-private-template-instantiation-preflight)
  for new private copies of the planning templates. Placeholder replacement alone is
  insufficient. A setup-only charter is not campaign START and grants no development
  authority.

## 4. Obtain actual loading evidence without starting work

- The legitimate owner sends the existing bootstrap/reread prompt from
  [SETUP](SETUP.md#4-bind-one-owner-and-the-shared-peers-privately) (literal form in the
  [install guide](INSTALL_AGENT.md#5-obtain-actual-loading-evidence-without-starting-work))
  in the new Bot's **existing designated Home Chat**. The Bot reports its own state, not an
  inherited parent receipt.
- Require fresh own-session read-tool evidence of the actual SOUL, private bindings, full
  `skill://acd-orca` body, the bound bridge/common contract and relevant runtime/recovery
  instructions, with exact source paths and revision/hash. Catalog discovery, symlink
  targets, configuration and acknowledgment text do not prove loading or adoption.
- `no_active_sender_terminal` means activation-pending. Ask the legitimate owner to send
  that Home-Chat message; never forge `--from`, edit a runtime database, change permissions
  or create a new Home/coordinator as a workaround.
- A successful main reply does not prove auxiliary-purpose health. Report each required
  purpose's failures or unknown status separately; no automatic paid probing and no
  provider/model/temperature or global settings changes to force a result.

## 5. Report readiness and stop

| Status | Required evidence; not implied by another row |
|---|---|
| Configured | Approved SOUL/bridge/private bindings match the reviewed release. |
| Discovered | The Bot's session can discover the skill; not body loading. |
| Actually loaded | Fresh own-session full body/SOUL/bound bridge/common reads with source identity. |
| Current peer admission | Both-sided authorized project mapping and readable charter; unknown/refused stays blocked. |

Review readiness and the tiny native smoke are separately authorized scope under
[SETUP](SETUP.md#5-establish-review-readiness-then-one-tiny-native-smoke); onboarding does
not perform them. Do not start a product Run, development campaign, GitHub automation or
permission change during onboarding.

Return the exact source SHA/release path, approved changed paths, backup locations and
rollback targets, actual check results, each readiness status, failures/untested
limitations and the exact next owner steps. Never include secrets or other projects' data.
Stop after setup; no silent transition into development or publication.
