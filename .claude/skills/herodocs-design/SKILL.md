---
name: herodocs-design
description: Designs the solution for HeroDocs requirements in one pass, writing User Stories (who uses it and how) and the Configuration Items that deliver them (the build spec), plus CI Groups and ERD updates. Works from draft or approved requirements, for all of them or the ones the user names. Shows a design plan per requirement (stories, then the CIs that deliver them) for the user to steer, then writes everything on a branch for review. Uses Hero's playbook library when it's installed and reports coverage gaps when it isn't. Use whenever the user wants to design the solution, write or update user stories, CIs, configuration items, the build spec or the build plan in a HeroDocs repo ("design the solution", "write the stories and CIs", "spec out REQ-004", "what do we need to build for quoting", "write the CIs"), even if they don't say "design".
---

# HeroDocs design

Turns requirements into the solution design: **User Stories** (who uses each requirement and how) and the **Configuration Items** that deliver them (one per field or build item), plus CI Groups and the ERD changes they imply. Stories and CIs are designed in the same pass so the thinking that shapes the experience also shapes the build (FD-040). Each CI links the stories it delivers, and that trail carries forward to UAT, training and docs.

It runs in two phases, each ending with the user:

1. **Design plan:** for each requirement, its stories and the CIs that deliver them, shown in chat for the user to steer
2. **Write:** the stories, CIs, groups and ERD changes, on a branch, for review

## The playbook library

Hero keeps its build expertise in a private playbook library, separate from this repo (FD-035). It's installed on Hero staff machines as the `hero-playbooks` skill, and never committed to a client repo.

- If the `hero-playbooks` skill is available in this session, read its `index.yaml` once at the start, then load only the playbooks that match the requirements in scope.
- If it isn't available, or the library is empty, say so once, use general Zoho knowledge, and carry on.

Either way, track which build items had no matching playbook. That list goes in your report, and it's how Hero decides which playbooks to write next.

**Playbook content never goes into this repo.** Stories and CIs hold the design, which is the client's deliverable. A playbook's reasoning, selection criteria, pitfalls and examples stay in the library. A CI built from a playbook cites it in its `playbook` field (`quoting-transactional@3`) and nothing more.

## Before you start

1. Confirm this is a HeroDocs repo, then `git checkout main` and `git pull`. Stop and ask if the working tree has changes you didn't make.
2. Read `CLAUDE.md` if you haven't this session. Its hard rules apply throughout.
3. Read `index.yaml`, `project.yaml` (especially `roles`), the requirements in scope, the Design Decisions that link to them, the ERD files for their modules, and `BUILD-PLAN.md` if it exists.
4. Read the examples in `examples/` before writing your first story or CI in a session.
5. Note any existing stories, CIs and groups. If the requirements in scope already have them, this is a **rerun** (see Reruns below).

**Scope:** all requirements (draft or approved, excluding `declined`), or just the requirements, areas or modules the user names.

## CI types and codes

| `ci_type` | Code | Use for |
|---|---|---|
| module | MOD | Creating a custom module |
| field | FLD | **Any change to a field**: creating it, changing its properties (label, mandatory, length, picklist values), or removing it |
| layout | LAY | Layout-level work: sections, field arrangement, which profiles see which layout |
| layout_rule | LRL | Layout rules |
| validation_rule | VRL | Validation rules |
| workflow_rule | WFR | Workflow rules |
| blueprint | BLU | Blueprints |
| function | FNC | Custom functions |
| widget | WDG | Widgets |
| web_form | WEB | Web forms |
| report | RPT | Reports, including near-identical variants |
| dashboard | DSH | Dashboards |
| email_template | ETPL | Email templates |
| mail_merge_template | MTPL | Mail merge templates |
| inventory_template | ITPL | Inventory templates: quotes, sales orders, invoices, purchase orders |
| integration | INT | Integrations |
| other | OTH | Rarer settings: conversion mapping, duplicate check rules |

A `field` CI covers create, modify and remove alike. **The ERD says which:** the field's status is `pending` (create), `exists` (modify) or `flagged` (remove). Don't encode the action anywhere else.

## Phase 1: Design plan

Work out the design for each requirement in scope before writing anything.

### What can be designed, and what can't

- **No module on the requirement:** the approach isn't settled. Skip it, and list it with the decision that settles it.
- **A module with no ERD file:** the data model hasn't been read. Skip it, and suggest running the ERD skill for that module first. (A new custom module the requirements call for may get a `pending` stub ERD file; see ERD changes below.)
- **A proposed decision that changes the approach** (which app, which module, which mechanism): skip the requirement, and list it with that decision.
- **A proposed decision or open question that only changes details** (picklist values, a threshold, wording): design it, link the decision, and use `[TBD]` where the detail would go.

### For each requirement: stories first, then the CIs that deliver them

1. **Who uses it, and how.** Identify each role that interacts with the requirement and what they need to do. Each becomes a story: one role, one piece of functionality. Roles come from `project.yaml`; if a requirement needs a role that isn't listed, flag it in the plan and propose adding it (a small direct edit, on the user's OK).
   - **System behavior with no user action** (an automatic assignment, a nightly sync, a notification nobody triggers) gets **no story** (FD-015). Its CIs link straight to the requirement.
   - **A story fully delivered by standard Zoho**, with nothing to build or configure, still gets written, so the client sees the whole experience, and is tagged `no-build`.
   - Keep stories granular. Edge cases and exceptions belong in UAT, not in extra stories.
2. **Check the playbooks.** A process playbook may say which approach fits and what CI set it produces. A CI-type playbook says how to spec that kind of item. If a process playbook offers alternatives that no decision or guidance has settled, that choice needs a Design Decision first (see Decisions below).
3. **What to build to deliver those stories.** List the build items using the types above, and map each one to the stories it delivers. A CI can deliver several stories, and a story usually needs several CIs.
4. **Check the ERD before planning any field work.** If the field already exists, a change to it is a `field` CI against the existing field, never a new one. Never plan a duplicate field.
5. **Size the CIs:**
   - **One CI per field.** Always, so the ERD-to-CI match stays exact.
   - **One CI per other build item.** A workflow rule, a web form, a report, a template.
   - **Near-identical variants share one CI** (FD-031): reports or views that differ only by filter, sort, grouping or columns, or templates differing only in small wording, built and tested together. A distinct report gets its own CI.
   - **A CI can serve several requirements and stories.** Link all of them rather than duplicating the CI.
6. **Check coverage** before showing the plan: every story (except `no-build` ones) is delivered by at least one CI, and every CI delivers at least one story or is clearly system behavior. A story with no CI means a gap in the build; a CI with no story and no system role means it may not be needed.
7. **Group work done in the same place, in one sitting** (FD-037). Grouping is about where and when the work happens, not CI type. All the field work in a module's field and layout editor belongs together: new fields, property changes, picklist value changes and removals, across modules if they're done in the same session. A layout rule, workflow, report or template is built in a different screen, so it stays outside a field group, though several of the same kind built together can form their own group. Grouping is optional, and a CI belongs to at most one group.
8. **Set build order** with `depends_on`: a layout rule depends on the fields it shows; a web form depends on the fields it maps; a report depends on the fields it reads.

### Show the plan

Present it in chat, by requirement:

```
REQ-004: Every lead is assigned and gets a first personal response within one business day
  US: Sales Designer sees the new leads assigned to them
      delivered by: My New Leads view [RPT], Lead Owner assignment rule [WFR]
  US: Sales Designer claims an unreached lead from the shared queue
      delivered by: Unreached Leads view [RPT], Claimed By field [FLD], Claim button [FNC]
  System: unreached leads move to the shared queue after one business day
      delivered by: Unreached lead escalation [WFR]
```

Then:

- proposed CI Groups, with their CIs and, for field work, each field as `Label [type]: create / modify / remove`
- the playbook each CI follows, if any
- other ERD changes (stub modules, target values)
- decisions you'd write (see below)
- roles you'd add to `project.yaml`
- requirements you're skipping, and why
- coverage problems: stories with no CI, CIs with no story or system role
- build items with no playbook
- a count: N stories and M CIs in K groups, across J requirements

Ask the user to steer: the stories (right roles, right granularity), the CIs, and the grouping. Revise until they say to go ahead.

## Phase 2: Write

Create a branch: `git checkout -b design-<YYYY-MM-DD>`. Write stories first, so CIs can link them.

### User Stories

One file per story in `stories/`, using `templates/story.md`, next US number. See `examples/stories.md`.

- **File name:** `US-003-designer-claims-unreached-lead.md`.
- **`title`:** the functionality in a few words, from the role's point of view: "Sales Designer claims an unreached lead."
- **`status: draft`**, **`role`:** one role from `project.yaml`. **`module`:** where the user does it; must have an ERD file. **`requirements`:** every requirement it serves.
- **`tags: [no-build]`** only for a story standard Zoho fully delivers.
- **Body:** "As a **role**, I want to **do something**, so that **benefit**." in business language a client can approve. No field API names or Zoho jargon in the sentence; plain screen and record names ("the lead," "my leads list") are fine. Add a `## Notes` section only when there's useful context: what triggers it, what the user sees, what's out of scope. For `no-build` stories, say in Notes which standard behavior delivers it.

### CIs

One file per CI in `cis/`, using `templates/ci.md`, next CI number. See `examples/cis.md`.

- **File name:** the ID, the type code, then a short slug: `CI-010-FLD-project-type-on-leads.md`, `CI-009-WEB-request-a-quote-form.md`, `CI-021-ITPL-quote-template.md`. The validator warns when the code doesn't match the `ci_type`.
- **`title`:** what's being built, plainly: "Project Type field on Leads," "Request a Quote web form," "Pipeline report."
- **`status: draft`**, **`deploy_status: not_started`**, `clickup_tasks: []`.
- **`ci_type`:** from the table above.
- **`app`** and **`module`:** where it's built. The module must have an ERD file.
- **`api_name`:** for field CIs, the field's API name, matching its ERD entry. For new fields, use Zoho's convention (`Project_Type`), unique within the module.
- **`requirements`:** every requirement it serves. Always at least one.
- **`stories`:** every story it helps deliver. Leave it out for system behavior.
- **`decisions`:** any Design Decision that shaped it, decided or proposed.
- **`depends_on`:** the CIs that must exist first.
- **`group`:** its CI Group, if any.
- **`playbook`:** the playbook it followed, as `id@version`, if any.

**The body is the build spec**: specific enough that a Hero builder could build it without asking. What to build, where, and the exact settings: field type and properties (or what changes, for an existing field), rule criteria and actions, form fields and hidden values, report columns, grouping, filters and each variant, template contents and merge fields. For picklists, reference the ERD ("Values as defined in ENT-001, `Project_Type`") and never restate the values. Mark anything undecided `[TBD]`, naming the decision or open question that settles it. Add a `## Notes` section for context a builder needs: why, edge cases, what to check.

### CI Groups

One file per group in `ci-groups/`, using `templates/ci_group.md`, next CG number. The title names the work ("Lead intake fields"). The body's first paragraph says what it covers and why these CIs are built together; that paragraph appears as the group's notes in `BUILD-PLAN.md`. `clickup_tasks: []`.

### ERD changes

The ERD skill records what exists; this skill records what's planned (FD-034). In the module's ERD file:

- **New field:** add it with `status: pending`, `standard: false`, and its label, type, `values` (for picklists) or `lookup_to` (for lookups). Values come from the requirements and sources; if they're not settled, write `values: [TBD]` with `notes` naming the decision or question.
- **Change to an existing field** (picklist values, label, mandatory): update the field's entry to the target, and keep `status: exists`. The `field` CI is the work.
- **Field to remove:** set `status: flagged`, with `notes` saying why. The removal is its own `field` CI.
- **New custom module:** if the ERD skill hasn't created a stub, create one: `module_kind: custom`, `status: pending`, with its name field `pending`, then add the planned fields.

Never delete a field from an ERD file, and never change a field's status to `exists` or `removed`. Only the ERD skill records what exists.

### Decisions

When a playbook (or your own judgment) shows a real choice between approaches that no guidance or decision has settled, write a Design Decision with status `proposed`, linked to the requirement, using `templates/decision.md`. Put the alternatives under Options Considered and your recommendation under Decision. Don't copy playbook text into it; state the options and trade-offs in your own words. The CIs that depend on it link it in `decisions`. If guidance settles the choice, the decision is `decided`, dated from the guidance (FD-033).

### Finish

1. Rebuild the index and build plan, then validate. Fix every error. Every `pending` field you added should have a CI building it, every CI file name should carry its type code, and `stories_without_cis` in the index should list nothing you wrote this run.
2. Commit the stories, CIs, groups, decisions, ERD changes, refreshed `index.yaml` and `BUILD-PLAN.md` together on the branch: `Design: N stories, M CIs, K groups for J requirements`. Push the branch.
3. Offer to open a pull request, and point the user to `BUILD-PLAN.md` as the quickest way to review the build, with each CI showing the stories it delivers.

## Reruns

When stories or CIs already exist for the requirements in scope:

- **Requirement changed:** update its stories and CIs in place, keeping IDs, unless a CI is `built` or `deployed`. For those, write a new CI for the change, depending on the original, and say so.
- **Requirement declined:** set its stories' and CIs' `status: declined`, unless they serve another requirement that's still active. Mark their `pending` ERD fields `flagged` only if nothing else needs them.
- **New functionality or build items:** new stories and CIs with the next IDs, linked.
- **A decision settled:** replace the `[TBD]`s it covered and fill the ERD values.
- **Regrouping:** change the `group` on the affected CIs. No files move.
- **Type changed:** rename the CI file to carry the new code; the ID stays the same.
- **Never delete** a story, CI or group.

UATs linked to changed stories may need updating; list them in your report for the UAT skill to pick up.

## Report back

- stories written, by requirement and role, with any `no-build` ones noted
- CIs written, by requirement and by type code
- coverage: any story with no CI, any CI with no story that isn't system behavior
- CI Groups and what's in each
- ERD changes: fields added as `pending`, existing fields changed, fields `flagged`, stub modules created
- `[TBD]`s and the decisions or questions behind them
- decisions written, and their status; roles added to `project.yaml`
- requirements skipped, and what would unblock each
- **playbook coverage:** which CIs followed which playbooks, and every build item with no playbook, grouped by type and process. This is Hero's list of playbooks worth writing.
- on a rerun, UATs that test changed stories
- the branch, `BUILD-PLAN.md` for review, and the offer of a pull request

## What this skill never does

- Copy playbook content into the repo, beyond the `playbook` citation on a CI.
- Create a field that already exists in the ERD.
- Restate picklist values in a CI body.
- Mark ERD fields `exists` or `removed`, or delete anything from an ERD file.
- Mark stories or CIs `approved`, CIs `built` or `deployed`, or decisions `decided` without guidance or the user's say-so.
- Write UATs, training or documentation. Those come later, from the stories and CIs.
- Write to a Zoho org.
