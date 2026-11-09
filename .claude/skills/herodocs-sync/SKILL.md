---
name: herodocs-sync
description: Updates a HeroDocs client repo's framework (skills, schemas, scripts, templates, CLAUDE.md, FRAMEWORK-DECISIONS.md, README and folder READMEs) to the latest herocrm/herodocs-template, using scripts/sync_framework.py, then fixes any existing records the new rules break. Use whenever the user wants to sync, update, upgrade, refresh or pull the framework, the template, the skills or the latest HeroDocs changes into a project repo ("sync the framework", "pull the latest template", "update this repo's skills", "get the new framework changes"), even if they don't say "sync".
---

# HeroDocs framework sync

Brings this client repo's framework files up to date with `herocrm/herodocs-template`. The mechanical part is done by `scripts/sync_framework.py`, which pulls exactly the paths listed in the template's `framework.yaml` and never touches project files (records, `project.yaml`, `index.yaml`, `BUILD-PLAN.md`). This skill runs it, explains what changed, and handles the part that needs judgment: existing records the new rules break.

Framework sync commits straight to `main`, like intake (FD-039). It changes how the repo works, not what the project contains.

## Before you start

1. Confirm this is a HeroDocs repo, then `git checkout main` and `git pull`.
2. If the working tree has uncommitted changes, stop and ask the user whether to commit or discard them. The script refuses to run on a dirty tree.
3. Use the repo's `.venv` Python if it exists, otherwise `python3`.
4. **If `scripts/sync_framework.py` doesn't exist**, this repo predates it. Bootstrap once: fetch `scripts/sync_framework.py` and `framework.yaml` from `herocrm/herodocs-template` (through git or the GitHub connector), write them into the repo, commit them to `main` (`Add framework sync script`), then continue.

## Step 1: Preview

Run `scripts/sync_framework.py --dry-run`. Tell the user:

- the template version it will sync to
- the files that will be updated, added and removed, grouped plainly (skills, schemas, scripts, docs)
- **new framework decisions**: compare `FRAMEWORK-DECISIONS.md` here with the template's, and list each new FD entry's title with a one-line summary, since those say what's changed in how records work

If it's a large change, wait for the user's OK. If they've already said to go ahead, carry on.

## Step 2: Sync

Run `scripts/sync_framework.py`. It pulls the files, records the template version in `.herodocs-version`, rebuilds the index and build plan, validates, and commits if validation passes.

- **It committed:** push (`git push`) and go to Report back.
- **It stopped on validation errors:** the changes are staged but not committed. Go to Step 3.

## Step 3: Fix records the new rules break

Validation errors after a sync usually mean a framework change made existing records invalid. Use the new FD entries to understand why, then fix the **records**, never the framework files:

- Group the errors by cause (a removed `ci_type`, a newly required field, a renamed status).
- Propose the fix for each group: which records change and how. For example, CIs with `ci_type: picklist` become `ci_type: field`; a newly required `area` gets proposed values from `project.yaml`.
- Fixes that need judgment (choosing an area, picking a new type) go to the user before you apply them. Purely mechanical ones (a renamed value, adding a type code to a file name) can be applied, and listed.
- After fixing, rebuild the index and build plan, validate, and commit everything together on `main`: `Sync framework to herodocs-template <sha> and migrate records`. Push.

Warnings that appear after a sync are worth reporting, but don't block the commit. A common one is CI file names missing their type code; offer to rename them (`git mv`, keeping the ID).

## Report back

- the template version synced to
- what changed, in plain terms: skills added or updated, schema changes, new docs
- the new framework decisions, by number and title
- records migrated, and any warnings left for the user
- that the commit is on `main` and pushed

Suggest starting a fresh Claude Code session if skills changed, so the new versions load.

## What this skill never does

- Edit framework files by hand, here or in the template. Framework changes are made in `herodocs-template`; this skill only pulls them.
- Touch records, `project.yaml`, `index.yaml` or `BUILD-PLAN.md` except to fix records the new rules break, or to rebuild the generated files.
- Commit a sync that leaves validation errors.
