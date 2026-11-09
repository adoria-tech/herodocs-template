# HeroDocs Project

This repo holds the HeroDocs records for one Zoho implementation project: requirements through to documentation, authored with AI assistance and reviewed by the Hero team.

It was created from `herocrm/herodocs-template`. For a complete worked example, see `herocrm/herodocs-sample` (Northshore Outdoor Living, lead source and referral tracking).

## Starting a new project

1. On GitHub, open `herodocs-template` and click **Use this template**, then **Create a new repository**. Owner `herocrm`, name `herodocs-<client>`, **Private**.
2. Clone it in GitHub Desktop and open it in VS Code.
3. In the VS Code terminal, set up validation (once per repo):

   ```
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```

4. Fill in `project.yaml`: client, project name, the Apps in use, and the client's roles. Leave `areas` empty; the requirements skill fills it in.
5. Add sources with the intake skill, then run the requirements skill (see Skills below).
6. Build the data model with the ERD skill, which reads the client's Zoho org. Before the client's subscription exists, it can start from Zoho's standard modules.
7. Design the solution with the design skill: user stories and the CIs that deliver them. Review the build in `BUILD-PLAN.md`, and coverage with the review skill.
8. Write the acceptance tests with the UAT skill.
9. Replace this section of the README with a short description of the project.

## Framework files

Everything listed in `framework.yaml` comes from the template: `schemas/`, `scripts/`, `templates/`, `.claude/skills/`, the VS Code and GitHub settings, `CLAUDE.md`, `FRAMEWORK-DECISIONS.md`, this README and the folder READMEs. A client repo owns everything else: its records, `project.yaml`, `index.yaml` and `BUILD-PLAN.md`.

Never edit framework files in a client repo. Improve them in `herodocs-template`, then pull the change into each client repo with a sync:

- **In Claude Code:** "Sync the framework." The `herodocs-sync` skill previews the change, runs the sync, and fixes any records the new rules break.
- **From the terminal:** `.venv/bin/python3 scripts/sync_framework.py` (add `--dry-run` to preview).

The sync pulls exactly the paths in the template's `framework.yaml`, records the template version in `.herodocs-version`, rebuilds the index and build plan, validates, and commits to `main`. It runs only on `main`, never touches project files, and won't commit if validation fails (FD-039).

`FRAMEWORK-DECISIONS.md` explains why the framework works the way it does. `CLAUDE.md` is the briefing Claude Code reads at the start of every session in this repo.

Hero's playbook library (`herocrm/hero-playbooks`) is separate and private. It's installed on Hero staff machines and never lives in a client repo (FD-035).

## How this repo is organized

```
project.yaml        Client, project metadata, Apps, Areas and Roles
index.yaml          Generated summary of every record (never hand-edit)
BUILD-PLAN.md       Generated view of the CIs by group, in build order (never hand-edit)
framework.yaml      Which paths the template owns (framework)
.herodocs-version   The template version this repo was last synced to
CLAUDE.md           Briefing for Claude Code sessions
sources/            Source References (where requirements came from)
  raw/              Extracted text from sources, for Claude to read
requirements/       What the system must do
decisions/          Design Decisions and why we made them
erd/                Data model, one file per module
stories/            User Stories: what a user must be able to do
cis/                Configuration Items: what we build or configure
ci-groups/          CI Groups: CIs built in the same place in one sitting
uat/                User Acceptance Test definitions
training/           Recommended training components
docs/               Documentation catalog
templates/          Blank starting file for each record type
schemas/            Validation rules for each record type
scripts/            Index and build plan builder, validator, framework sync, trace
.claude/skills/     HeroDocs skills for Claude Code
review/             Throwaway review documents (git-ignored, never committed)
```

To create a new record by hand, copy the matching file from `templates/` into the right folder and rename it with the next ID.

## File format

Every record is one markdown file with YAML frontmatter on top:

```markdown
---
id: REQ-001
title: Website quote requests are captured with their source and project details
status: draft
priority: must
area: Lead intake
module: Leads
sources: [SRC-001]
---

# Website quote requests are captured with their source and project details

Plain-language description goes here.
```

The frontmatter (between the `---` lines) is structured data that scripts and Claude read. The body below it is for people.

### YAML rules of thumb

- `key: value` with a space after the colon
- Lists can be written `[A, B]` on one line, or one item per line with a dash
- Indent with spaces, never tabs
- Quote any value that contains a colon
- `#` starts a comment

### What we don't store

No created/updated dates or authors on records. Git history already records who changed what and when.

## IDs and file names

| Record | Prefix | Example file |
|---|---|---|
| Source Reference | SRC | `sources/SRC-001-kickoff-call.md` |
| Requirement | REQ | `requirements/REQ-001-website-quote-requests.md` |
| Design Decision | DD | `decisions/DD-001-work-orders-in-creator.md` |
| Data Model (ERD) | ENT | `erd/ENT-001-leads.md` |
| User Story | US | `stories/US-001-rep-sees-claimable-leads.md` |
| Configuration Item | CI | `cis/CI-001-FLD-territory-field.md` (with the type code) |
| CI Group | CG | `ci-groups/CG-001-referral-tracking-fields.md` |
| UAT | UAT | `uat/UAT-001-referrer-fields-appear-for-referrals.md` |
| Training Component | TRN | `training/TRN-001-lead-management-basics.md` |
| Documentation | DOC | `docs/DOC-001-lead-management-guide.md` |
| App | APP | Listed in `project.yaml` |

IDs never change once assigned. The slug after the ID can be edited for readability. Open questions in source digests are numbered by source: `SRC-002-Q3`.

CI file names carry a type code after the ID: MOD module, FLD field, LAY layout, LRL layout rule, VRL validation rule, WFR workflow rule, BLU blueprint, FNC function, WDG widget, WEB web form, RPT report, DSH dashboard, ETPL email template, MTPL mail merge template, ITPL inventory template, INT integration, OTH other. See `cis/README.md`.

## Links point upstream only

Each record lists the records it comes from. The reverse view is computed in `index.yaml`, so links never drift out of sync.

| Record | Links to |
|---|---|
| Source Reference | nothing (start of the chain) |
| Requirement | Sources |
| Design Decision | Requirements; `supersedes` an older Decision |
| Data Model (ERD) | nothing (the why comes through the CIs that build each field) |
| User Story | Requirements |
| Configuration Item | Requirements, User Stories it delivers, Design Decisions, App, other CIs (`depends_on`), CI Group (`group`, optional), ClickUp task IDs |
| CI Group | nothing (CIs point to their group) |
| UAT | User Stories and/or Requirements |
| Training Component | User Stories, Apps |
| Documentation | Requirements, User Stories, Training |

Tasks live in ClickUp, usually one per CI Group. Level of effort lives on the task, never the CI.

## Controlled values

- **Modules:** a `module` value is valid only if an ERD file exists for that module. On requirements, a module with no ERD file yet is a warning rather than an error, since requirements usually come before the data model.
- **Areas:** a requirement's `area` must come from the `areas` list in `project.yaml`. The requirements skill writes this list from the approved solution outline.
- **Roles:** `role`, `performed_by`, and `audience` must come from the `roles` list in `project.yaml`. `audience` also accepts `[Everyone]` on its own.
- **Apps:** `app` and `apps` must match an `id` in `project.yaml`.

## Statuses

| Record | Status values |
|---|---|
| Requirement, CI, User Story, UAT, Training, Documentation | draft, review, approved, declined |
| Design Decision | proposed, decided, superseded |
| Data Model (module and each field) | pending, exists, flagged, removed |
| CI build | `deploy_status`: not_started, built, deployed |
| CI Group | none; progress comes from its CIs |

Data Model status describes the org: pending (we'll create it), exists (it's there), flagged (we'll remove it), removed (gone, kept listed for troubleshooting). The ERD skill records what exists, read from the client's org; the design skill adds pending and flagged changes. Fields are never deleted from an ERD file: one that's gone from the org is marked `removed` (FD-034).

A Design Decision with status `proposed` is an outstanding decision. A decision settled by a `guidance` source starts as `decided`, dated from that source, since guidance is Hero's written direction (FD-033). A decision you confirm while steering the solution outline is also `decided`.

UAT results (Hero's run and the client's run) live outside the repo. The UAT files only define the tests.

## Conventions

- **Requirements:** the body says what the business needs, never how it's built: no fields, workflows or Zoho terms. `area` (required) is the business capability; `module` (optional) is the Zoho module, set once it's known and left out while the choice is open. App and approach choices are Design Decisions.
- **Requirement size:** one requirement per deliverable the client would approve, defer or decline as a unit: each form, integration, report, workflow or process stage, with everything about it as points in the body. Split only for a separate design decision, a meaningfully different priority, or a different kind of deliverable. Minor nice-to-haves are a line marked `(optional)`, never their own requirement. Expect 2 to 5 per area. See FD-032.
- **Requirements with open questions:** when a requirement rests on an unanswered question, it's tagged `open-questions` and has an `## Open questions` section naming each question by ID, with any working assumption labeled as an assumption. The index lists these as the project's lock-down list.
- **Sources:** client sources are authoritative on what the business needs; `guidance` sources are authoritative on how we'll approach it. Conflicts on the what are flagged, never silently resolved. A later source that answers an earlier open question says `(resolves SRC-###-Q#)`.
- **Stories and CIs are designed together** (FD-040): for each requirement, who uses it and how (stories), then what to build to deliver that (CIs). Each CI lists the stories it delivers.
- **User Stories** are granular: one role, one piece of functionality. Edge cases belong in UAT. System behavior with no user action gets no story. A story standard Zoho fully delivers, with nothing to build, is tagged `no-build`.
- **ERD files** list every field in the module, standard and custom, so we always know what exists.
- **Field changes** (new picklist values, label changes) keep status `exists`; the ERD shows the target, the CI is the work.
- **Picklist values** live only in the ERD's `values` list, which is what gets built. The field's `notes` explain them if needed. CIs reference the ERD field ("Values as defined in ENT-001, `Referrer_Type`") and never restate the values.
- **Undecided values** are written `values: [TBD]`, with `notes` naming the proposed Design Decision that will settle them. The CI links to that decision.
- **CIs** are one per field or build item. `ci_type: field` covers any change to a field: creating it, changing its properties or picklist values, or removing it. The field's ERD status says which (`pending` create, `exists` modify, `flagged` remove). Templates are `email_template`, `mail_merge_template` or `inventory_template`. A build item can be a set of near-identical variants, such as reports or views that differ only by filter, sort, grouping or columns, built and tested together; the CI lists each variant. Fields are always one per CI, a field the ERD already has is never created twice, and a distinct report gets its own CI. See FD-031 and FD-036.
- **Playbooks:** a CI built from one of Hero's playbooks cites it in its optional `playbook` field (`quoting-transactional@3`). Playbook content itself never goes into a client repo (FD-035).
- **CI Groups** hold CIs built in the same place, in one sitting, whatever their type: all the field work in a module's field editor goes together, including picklist value changes. A layout rule, workflow, report or template built in another screen is its own CI. Groups are optional, one per CI, and can span modules. See FD-037.
- **A feature is tied together by its Requirement**, not by a group: everything built for it is every CI and group linked to that Requirement, ordered by `depends_on`.
- **UATs** are one scenario with one outcome, written so the client can run them alone: specific preconditions, numbered steps using the labels they see in Zoho, and a clear expected result. Each story gets a main-path test, plus one per distinct exception a requirement or CI defines; system behavior is tested against its requirement. See FD-041.
- **Confirm the org before touching it.** Before anything reads from or writes to a Zoho org, the connected org's name is checked against `client` in `project.yaml`. The connector may be signed in to Hero's own CRM or another client's org.

## The index and the build plan

`index.yaml` is a generated, one-file summary of the whole project, built by `scripts/build_index.py` from the frontmatter of every record. Claude and skills read it instead of opening every file. Its sections:

- **gaps**: requirements resting on open questions, or with no module, CIs, UAT or docs; stories no CI delivers, or with no UAT or training; pending ERD fields with no CI
- **open_decisions**: every Design Decision still `proposed`, and the CIs waiting on it
- **areas**: requirements grouped by capability area
- **requirements**: for each requirement, its area and module, decisions, stories, UATs, docs, CI groups, and CIs in build order (from `depends_on`)
- **fields**: every ERD field with the CI that builds it and that CI's requirements and decisions, which answers "why is this like that?"
- **records**: every record's key fields, its upstream `links`, and the computed `linked_from` (`needed_by` for CIs that depend on it)

`BUILD-PLAN.md`, built by the same script, is the human view of the build: each CI Group with its fields (`Label [type]: create / modify / remove`), its CIs in build order with type codes and the stories each delivers, and its notes; then ungrouped CIs by requirement, and a full build order. It's the quickest way to review a design run, and the natural source for ClickUp tasks: one task per group (FD-038).

Both hold nothing of their own; they can be deleted and rebuilt at any time. Never edit them by hand. Commit them along with the record changes they reflect.

One-off questions can be answered from the index or the records without changing anything. Add something to the index only when it's asked often or a skill needs it: change `scripts/build_index.py` here in the template, then sync it to client repos.

## The traceability review

For reviewing coverage, `scripts/trace.py` generates `review/TRACE-<date>.md`: one table per capability area, one row per user story, with four columns: **Requirement** (shown on the first row of its stories, with its points), **User story**, **Assessment**, and **Delivered by** (the CIs, "Standard Zoho" for `no-build` stories, or a warning when nothing delivers it). System behavior gets its own row. The `herodocs-review` skill runs it and fills in the Assessment column: a coverage verdict for the requirement on its first row, and a short note per story. It traces whatever branch is checked out, so you can review a design before merging it. The file is throwaway: `review/` is git-ignored, never committed, and regenerated whenever you want it (FD-042).

## Skills

HeroDocs skills live in `.claude/skills/` and run in Claude Code, opened on this repo. Ask for the work in plain language and Claude uses the matching skill.

| Skill | What it does | Commits to |
|---|---|---|
| `herodocs-intake` | Adds one source: fetches a Fathom meeting, Drive document, Gmail thread, file or pasted notes, saves the raw text, and writes a Source Reference with a digest and numbered open questions. Writes no requirements. | `main` |
| `herodocs-requirements` | Reads every source at once. Runs a readiness check on open questions, where you can answer Hero's questions, get a call agenda, or proceed with questions open. Then presents a solution outline for you to steer, saves the approved outline as a `guidance` source and writes its areas into `project.yaml`, then writes requirements and Design Decisions. | Outline and areas to `main`; requirements and decisions to a branch, for review |
| `herodocs-erd` | Builds the data model for every module the requirements need, or just the ones you name. Confirms the connected Zoho org is this client's, reads its real modules and fields, and writes ERD files. Refreshes existing ERD files one way from the org: fields gone from the org stay listed as `removed`, and planned changes are left alone. Read-only: it never writes to the org. Before the subscription exists, it can build from Zoho's standard modules, tagged `unverified`. | a branch, for review |
| `herodocs-design` | Designs the solution for requirements (all, or the ones you name; draft or approved). Shows a design plan per requirement (its stories, then the CIs that deliver them) for you to steer, including the grouping, then writes stories, CIs, CI Groups and the planned ERD changes. Uses Hero's playbook library when it's installed, and lists every build item with no playbook so you know what to write next. | a branch, for review |
| `herodocs-uat` | Writes acceptance tests after design. Shows a test plan (the scenarios for each story, plus system behavior) for you to steer, then writes client-runnable UATs from each story and the CIs that deliver it. | a branch, for review |
| `herodocs-review` | Generates a throwaway traceability review (a table per area: requirement, user story, assessment, delivered by) and fills in the assessments. Changes no records. | nothing (`review/` is git-ignored) |
| `herodocs-sync` | Pulls the latest framework from the template: previews what will change and which framework decisions are new, runs the sync, and fixes records the new rules break. | `main` |

Examples: "Add the Key2 kickoff call from Fathom." "Here's my guidance on how we'll handle work orders." "What questions are still open before requirements?" "Proceed with the rest open and show me the outline." "Build the ERD." "Design the solution." "Generate the trace for review." "Write the UATs." "Sync the framework."

The usual flow: intake each source, run the readiness check, hold a clarification meeting on anything blocking and intake its transcript, then steer the outline and let the skill write the requirements. Then build the data model from the client's org, design the solution, review coverage, and write the UATs. When you need to move before every answer is in, proceed anyway: open questions become labeled working assumptions, listed in the index until they're confirmed.

## Validating

Every record is checked against its schema in `schemas/`, then cross-checked: links point to real records of the right type, modules have ERD files, areas, roles and apps exist in `project.yaml`, and file names match IDs.

Warnings don't fail the check. They flag:

- records with no body text, or with text left over from a template
- CI file names whose type code doesn't match the `ci_type`
- requirements whose module has no ERD file yet
- CIs with no linked requirement or decision
- CIs marked built or deployed while a linked decision is still proposed
- ERD fields marked pending or flagged that no CI builds
- lookups to modules with no ERD file yet
- an `index.yaml` or `BUILD-PLAN.md` that's missing or out of date

How to run it:

- **In VS Code:** press **Cmd+Shift+B**. It rebuilds the index and build plan, then validates. Problems appear in the Problems panel; click one to jump to the file.
- **On GitHub:** validation runs on every push (it doesn't rebuild anything, so it warns if the committed index or build plan is stale). Commits show a green check or a red X.
- **From the terminal:** `.venv/bin/python3 scripts/build_index.py`, then `.venv/bin/python3 scripts/validate.py`

The `.venv` folder is ignored by git; each person creates their own. Files in `templates/` and folder README files are not validated.

## Working habits

- Fetch and pull before you start editing.
- Commit your work before you pull.
- Run Cmd+Shift+B before every commit, and commit the refreshed `index.yaml` and `BUILD-PLAN.md` with your changes.
- **Where changes go:** source intake, framework syncs and small edits you've asked for directly go straight to `main`. Anything a skill generates in bulk, or a change across many records, goes on a branch and gets reviewed as a pull request. See FD-027 and FD-039.
- **Framework changes update the README, `CLAUDE.md` and `FRAMEWORK-DECISIONS.md` in the same pull request.** Otherwise the docs drift from how things actually work.
- **A new framework file or folder goes into `framework.yaml` in the same change**, or the sync won't carry it to client repos.
