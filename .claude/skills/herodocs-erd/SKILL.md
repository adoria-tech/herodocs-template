---
name: herodocs-erd
description: Builds and refreshes the data model (ERD) records in a HeroDocs repo: one file per module, listing every field with its status. Reads the client's Zoho org through the connector, read-only, and records what exists. Two modes: every module the requirements need, or only the modules or requirements the user names. Refreshes existing ERD files one way, from the org into the records. Use whenever the user wants to build, generate, create, pull, refresh, update or sync the ERD, data model, modules or fields in a HeroDocs repo ("build the ERD", "pull the Leads and Deals fields", "refresh the data model from CRM", "what modules do the requirements need"), and before CIs are written for modules that have no ERD file yet.
---

# HeroDocs data model (ERD)

Creates and refreshes the ERD files in `erd/`: one file per Zoho module, listing every field with its status (`pending`, `exists`, `flagged`, `removed`). Every other record that names a module needs that module's ERD file, so this runs after requirements and before CIs.

This skill records **what exists**. It reads the client's org and writes down its modules and fields. It doesn't design the target: new fields, changed picklist values and removals are written by the CI skill, which adds them to the ERD as `pending` or `flagged` alongside the CIs that do the work. Keeping the two apart means a refresh can never wipe out planned changes, and planned changes can never be mistaken for things that already exist.

**This skill never changes the client's org.** Every connector call it makes is a read. (Other HeroDocs automations may build fields in an org; this skill only ever reads.)

**This skill never deletes a field from an ERD file.** A field that's in the ERD but no longer in the org stays listed, marked `removed`, so the file keeps a full record of what was there.

## Modes

- **All:** every module the project's requirements need.
- **Specific:** only the modules the user names ("Leads and Deals"), or only the modules behind the requirements they name ("the modules for REQ-004 and REQ-009").

Either mode works from draft or approved requirements. Either mode also refreshes any existing ERD file it touches.

## Before you start

1. Confirm this is a HeroDocs repo, then `git checkout main` and `git pull`. Stop and ask if the working tree has changes you didn't make.
2. Read `CLAUDE.md` if you haven't this session, then `index.yaml` and `project.yaml`.
3. **Confirm which Zoho org the connector is reading.** Fetch the org's details and compare its name with `client` in `project.yaml`. If they don't clearly match, stop and ask. The connector may be signed in to Hero's own CRM or another client's org, and pulling the wrong org's data model into this repo is the worst mistake this skill can make. Say which org you'll read before reading anything else.
4. If no connector is available, or the client has no Zoho org yet, see "New orgs" below.

## Step 1: Work out which modules are needed

From the requirements in scope (all of them, or the ones the user named):

- **Requirements with a `module`**: that module is needed.
- **Requirements without a module**: the module isn't settled. List them with the decision that settles each (the index's `requirements_without_module` gap and `open_decisions`). Don't guess a module for them.
- **Modules the approved outline or decided Design Decisions name** but no requirement does yet: list them too.
- **Modules that lookups point to**: if a module you're building has a lookup to another module, note it. Building the target as well stops the validator's "lookup to a module with no ERD file" warning.

Show the user the list: modules to build, modules to refresh (existing ERD files), modules that would be new custom modules, and requirements you can't place yet. Wait for their OK, or for them to add or drop modules.

## Step 2: Build or refresh each module

For each module, fetch its full field list from the org: API name, label, data type, whether it's a standard or custom field, whether it's required, picklist values, and lookup targets. Then:

### A module with no ERD file

Create `erd/ENT-###-<module-slug>.md` using `templates/erd.md`, with the next ENT number.

- `module`: the module's API name. `title`: its display name. `app`: the matching app ID in `project.yaml`. `module_kind`: `standard` or `custom`. `status: exists`.
- **List every field the org has**, standard and custom, each with `status: exists`. Map Zoho's data types to the schema's types (single line to `text`, multi-line to `textarea`, pick list to `picklist`, multi-select to `multiselect`, lookup to `lookup` with `lookup_to`, owner/user to `user`, and so on); use `other` for anything that doesn't map, with the Zoho type in `notes`.
- Picklists get their current `values`. Lookups get `lookup_to`, using the target module's API name.
- The body: one or two sentences on what the module holds in this client's business, drawn from the requirements, and a `## Relationships` Mermaid diagram from its lookups.

### A module with an existing ERD file: refresh, one way

The org is the source of truth for what exists. Compare it with the file, field by field:

| In the org | In the ERD file | Do |
|---|---|---|
| Present | Missing | Add it, `status: exists` |
| Present | `exists` | Update label, type, required, values and lookup to match the org, **unless** a CI that isn't deployed yet plans a change to that field (match on module and `api_name`). Then leave the target in place and report the difference. |
| Present | `pending` | Set `status: exists`: it's been built. Report it, so the matching CI's `deploy_status` can be updated. |
| Present | `flagged` | Leave it `flagged`: the removal hasn't happened yet. |
| Present | `removed` | Set `status: exists`: it's back. Report it. |
| Missing | `exists` | Keep the field listed and set `status: removed`. Report it as an unexpected removal: something was deleted outside the plan. |
| Missing | `flagged` | Keep the field listed and set `status: removed`: the planned removal is done. Report it. |
| Missing | `pending` | Leave it `pending`: it hasn't been built yet. |
| Missing | `removed` | Leave it as is. |

A refresh only ever adds fields or changes their status. Every field already in the file stays in the file. Never change a `pending` or `flagged` field's planned values.

If the whole module is gone from the org, keep its file and set the module's `status: removed`, with every field marked `removed`, and report it.

### A module that doesn't exist in the org yet

When the requirements or decisions call for a new custom module (Work Orders, say), create its ERD file with `module_kind: custom` and `status: pending`, and a single field: its name field, `status: pending`. The CI skill adds the rest of its fields along with the CIs that build them.

## New orgs

Requirements and CIs often come before the client's Zoho subscription is set up. When there's no org to read, ask the user how to proceed:

- **Build from Zoho's standard modules.** Create ERD files for the standard modules the requirements need, listing the standard fields that come out of the box, all `status: exists`. Tag each file `tags: [unverified]` and say in the body that it's from the standard field set, not a real org. List only standard fields you're confident ship with that module; leave out anything you're unsure of rather than guessing. This lets CI work go ahead before the subscription exists.
- **Wait** until the org exists, and run this skill then.

Once the org exists, a refresh replaces the standard field set with what's actually there and removes the `unverified` tag. A standard field the org turns out not to have is marked `removed`, like any other.

## Step 3: Validate and commit

1. Rebuild the index, then validate. Fix every error. Expected warnings: lookups to modules you didn't build this run.
2. This is a bulk change, so work on a branch: `git checkout -b erd-<YYYY-MM-DD>`. Commit the ERD files and refreshed `index.yaml` together: `ERD: build N modules, refresh M`. Push, and offer a pull request.

## Report back

- which org you read (by name), and the modules built, refreshed, and created as pending custom modules
- field counts per module
- from refreshes: fields that changed status (pending to exists means built; anything to removed), unexpected removals, fields that came back, and target values you kept because a CI plans a change
- requirements you couldn't place because their module isn't decided, and the decisions that settle them
- any `unverified` files, and the reminder to refresh once the org exists
- the branch, and the offer of a pull request

## What this skill never does

- Write to the client's Zoho org. It only reads.
- Read an org without first confirming it's this client's.
- Delete a field or module from an ERD file. Gone from the org means `removed`, never deleted.
- Add `pending` or `flagged` fields for new requirements. Planned changes come from the CI skill.
- Overwrite planned values on `pending` or `flagged` fields.
- Guess a module for a requirement whose module is still undecided.
- Write CIs, requirements or any record other than ERD files.
