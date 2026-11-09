# Framework decisions

Why HeroDocs works the way it does. One entry per decision, newest last. Before proposing a change to how records work, check whether it's already been considered here.

When a framework decision changes, add a new entry that says which one it replaces, and update the README and CLAUDE.md in the same pull request.

---

## FD-001: Records live in git as markdown with YAML frontmatter

**Context.** Records could have lived in Zoho CRM or Creator custom modules, in WorkDrive, or in files.

**Decision.** Plain markdown files with YAML frontmatter, in a private GitHub repo per client project.

**Consequences.** Claude can read and write many records at once without API calls or rate limits. Every change is reviewable as a diff, reversible, and attributable. Recipes become folders of files that can be copied. Client visibility comes later through a read-only projection (a Creator portal), not by giving clients the repo.

## FD-002: Git, not a synced WorkDrive folder

**Context.** WorkDrive sync propagates changes instantly with no learning curve; git requires commits.

**Decision.** Git, with GitHub Desktop and Claude handling commits.

**Consequences.** Save points show exactly what changed across many files, a whole AI pass can be undone at once, and pull requests give a review gate before generated content goes live. Raw client files and published client documents can still live in WorkDrive, linked from Source References.

## FD-003: Links point upstream only

**Decision.** Each record lists only the records it comes from (a CI lists its requirements). The reverse view is computed in `index.yaml`.

**Consequences.** Links can't drift out of sync, because each exists in exactly one place.

## FD-004: No dates or authors on records

**Decision.** Git history records who changed what and when. The only dates stored are facts about the thing itself: a source's date, when a decision was made, when a client approved a requirement.

## FD-005: One file per record, named by ID and slug

**Decision.** `REQ-001-short-slug.md`. IDs never change or get reused; slugs can. (Extended by FD-036: CI file names add a type code after the ID.)

**Consequences.** A change to one record shows up as a change to one file. The sidebar stays readable. References survive renames.

## FD-006: Requirements say what, never how

**Context.** Client documents often prescribe an approach ("build it in Creator") without knowing Zoho.

**Decision.** Requirements stay in business language with no apps, modules, fields or workflows. Approach and app choices are Design Decisions, starting as `proposed`. (Refined by FD-028: the body stays business language, but a requirement may carry the Zoho module as metadata once it's known. Refined by FD-033: decisions settled by guidance start as `decided`.)

**Consequences.** Clients can approve requirements without understanding Zoho, and the approach can change without reopening sign-off. App options get weighed explicitly instead of being baked in by whichever document arrived first.

## FD-007: The ERD is its own record type, one file per module

**Decision.** Each module's file lists every field, standard and custom, each with a status: `pending` (we'll create it), `exists`, `flagged` (we'll remove it), `removed` (kept for troubleshooting). The module has the same status. Changing an existing field keeps it `exists`: the ERD shows the target, the CI is the work. (Refined by FD-034: the ERD skill records what exists from the org; the CI skill adds planned changes.)

**Consequences.** Anyone can check whether a field already exists before creating one. For existing orgs, ERD files are generated from field metadata, not typed. The set of ERD files defines the valid modules for every other record.

## FD-008: The ERD doesn't link Design Decisions

**Context.** An early version had `decisions` on ERD files.

**Decision.** Removed. The reason a field exists comes through the CI that builds it (matched on module and `api_name`), which links its requirements and decisions.

**Consequences.** "Why is this field like that?" is answered at field level in the index's `fields` section, not at a vague module level.

## FD-009: Picklist values live only in the ERD

**Decision.** The ERD's `values` list is what gets built. Field `notes` explain values when needed. CIs reference the ERD field and never restate values. Undecided values are `[TBD]`, pointing at a proposed decision.

**Consequences.** Values can't disagree between two places.

## FD-010: One CI per field or build item

**Context.** The alternative was one CI per logical change (several fields in one record).

**Decision.** One per item, so each has its own deploy status and the field-to-CI match is exact. (Refined by FD-031: a build item can be a set of near-identical variants, such as reports that differ only by a filter or sort. Fields stay one per CI.)

**Consequences.** High volume on real projects, absorbed by skills generating CIs and by CI Groups for doing the work together.

## FD-011: When a CI type earns its own value

**Decision.** A build item gets its own `ci_type` when it's common across projects, built in its own place in Zoho, and worth counting: hence `layout_rule`, `validation_rule` and `web_form`. Rarer settings (conversion mapping, duplicate check rules) use `other`. (Refined by FD-036: `picklist` is folded into `field`, and templates split into email, mail merge and inventory.)

## FD-012: CI Groups are same-kind work done in one sitting

**Decision.** A group holds CIs of the same kind, done in the same place, in one sitting (a set of fields), usually with one ClickUp task. Grouping is optional, a CI belongs to at most one group, and groups can span modules. A layout rule or conversion mapping that depends on grouped fields is its own CI. Groups have no status of their own. (Replaced by FD-037: groups are defined by place and sitting, not by CI type.)

**Consequences.** Groups match how the work is actually done, and a well-described group is most of a recipe.

## FD-013: The Requirement ties a feature together

**Context.** A "primary module" on groups was considered as a way to relate everything built for a feature.

**Decision.** Not added. Everything built for a feature is every CI and group linked to its Requirement, ordered by `depends_on`. The index computes this view.

## FD-014: Effort and tasks live in ClickUp

**Decision.** Tasks are created in ClickUp, not in the repo, usually one per CI Group. Level of effort lives on the task, never on the CI.

**Consequences.** Effort never reaches client-facing records, and task status isn't duplicated in files.

## FD-015: Stories are granular; UAT links to stories or requirements

**Decision.** One role and one piece of functionality per story. Edge cases belong in UAT. System behavior with no user action gets no story; its UAT links straight to the requirement.

## FD-016: UAT results live outside the repo

**Decision.** UAT files define tests. Hero's and the client's results are tracked elsewhere (a sheet or the portal), keyed by UAT ID.

**Consequences.** No hand-copying of results into files.

## FD-017: Controlled values come from the project itself

**Decision.** Modules are valid if an ERD file exists. Roles come from `project.yaml`, with `Everyone` built in and never mixed with roles. Apps come from `project.yaml`. (Extended by FD-028: capability areas also come from `project.yaml`.)

## FD-018: A proposed Design Decision is an outstanding decision

**Decision.** No separate open-items list. Every DD with status `proposed` is open, and the index lists them with the CIs waiting on each. The validator warns when a CI is marked built while its decision is still proposed.

## FD-019: Validation errors block; warnings flag gaps

**Decision.** Errors are structural (bad format, broken links, unknown roles). Warnings catch gaps between record types: CIs with no requirement, pending fields with no CI, empty or template-filled bodies, a stale index.

**Consequences.** Most real gaps in the hand-built sample were found by checking one record type against another, which is what the warnings automate.

## FD-020: The index is generated and committed

**Decision.** `scripts/build_index.py` builds `index.yaml` from record frontmatter. It's committed so Claude can read one file (including through the GitHub connector), rebuilt automatically with Cmd+Shift+B, and never edited by hand. The validator warns if it's stale. (Extended by FD-038: the same script builds `BUILD-PLAN.md`.)

**Consequences.** One-off questions are answered from the index or records. Something is added to the index only when it's asked often or a skill needs it.

## FD-021: The template repo is the framework's source of truth

**Decision.** `herodocs-template` owns schemas, scripts, templates, skills, CLAUDE.md, this file and the folder READMEs. Client repos are created from it and own their records, `project.yaml` and `index.yaml`. `herodocs-sample` is the worked example and may lag behind the template. (Extended by FD-039: client repos pull framework changes with `scripts/sync_framework.py`.)

**Consequences.** Framework improvements are made once, then copied to client repos.

## FD-022: Skills run in Claude Code, in the repo

**Decision.** Generation skills run in Claude Code against the local repo, so Claude can write files, rebuild the index, validate and fix its own output before the user reviews it. Quick questions happen in chat. Skills live in `.claude/skills/` and ship with the template, versioned alongside the schemas they depend on, with exemplary records bundled as references.

## FD-023: Source intake is separate from requirements

**Context.** A per-source pass writes requirements in whatever order sources arrive, so the first document wins by default.

**Decision.** Intake runs once per source, saving raw text and a digest, and writes no requirements. The requirements skill reads every source at once. Digests keep large projects within working limits.

## FD-024: `guidance` is a source type

**Decision.** Hero's direction on approach is a source of type `guidance`. Client sources are authoritative on what the business needs; guidance is authoritative on how we'll approach it. Conflicts on the what are flagged, never silently resolved.

**Consequences.** Hero can steer requirements before they're written, and the steering is traceable.

## FD-025: Requirements start with a solution outline

**Decision.** Before writing anything, the requirements skill presents a one-page outline: capability areas, the end-to-end process, app options, open decisions, scope boundaries and source conflicts. Once the user approves it, the outline is saved as a `guidance` source, and the requirements link to it.

**Consequences.** Redirection happens when it's cheap, before 40 records exist. The approved outline doubles as the core of a proposal's scope.

## FD-026: Source intake commits directly to main

**Context.** Accumulating sources on a branch until gathering was complete would have added a branch and pull request to every project, just to signal "all sources are in."

**Decision.** The intake skill commits each source straight to `main`. Everything downstream of sources is still written on a branch and reviewed.

**Consequences.** Sources are inputs, not commitments, and they accumulate over time. The project lead decides when the picture is complete and runs the requirements skill then.

## FD-027: Small direct edits commit to main; bulk changes go on a branch

**Context.** The original rule put every non-intake change on a branch with a pull request. In practice, a one-line roles change in `project.yaml` produced a branch and a pull request offer, which was ceremony for something the user had just asked for and could review at a glance.

**Decision.** Three paths. Source intake commits to `main`. A small edit the user asked for directly (a role, a typo, one field, one record) is shown to the user and, on their OK, committed to `main`. Anything a skill generates in bulk, or any change across many records, goes on a branch with a pull request for review. When unclear, Claude asks, and the user can always override.

**Consequences.** Branches and pull requests are reserved for the changes where a reviewable diff and a record of review actually matter. Refines FD-026's "everything downstream is on a branch."

## FD-028: Requirements carry an area, and a module once it's known

**Context.** Requirements originally required `module`, validated against ERD files. On a new project no ERD files exist when requirements are written, and sometimes the module itself is undecided (Leads, or Contacts with a contact type). Replacing module with a business "area" was considered and rejected: on a mature system, and for library requirements dropped into existing systems, knowing exactly which module a feature lives on is essential, and an area alone is too vague.

**Decision.** Two fields doing different jobs. `area` (required) is the business capability, from an `areas` list in `project.yaml`; it's always known and groups requirements in outlines, proposals and docs. `module` (optional) is the Zoho module, set as soon as it's known and left out while the choice is open. A requirement's module with no ERD file is a warning, not an error. The requirements skill writes areas into `project.yaml` from the approved outline, and library drop-ins add their own, so nobody maintains the list by hand.

**Consequences.** The index lists requirements without a module as a gap, which shows what's still unsettled. The requirement body stays in business language for client approval; the module is metadata for Hero. Refines FD-006 and extends FD-017.

## FD-029: Open questions are numbered and checked before requirements

**Context.** Intake surfaced many open questions per source, but as loose bullets nothing connected a later answer to the original question.

**Decision.** Intake numbers open questions `SRC-###-Q#`, and a later source that answers one notes `(resolves SRC-###-Q#)` in its own digest, never by editing the earlier source. The requirements skill starts with a readiness check: it gathers every unresolved question and sorts it as blocking, Hero can answer, or can wait. Blocking questions become the agenda for a clarification meeting, whose transcript comes back in through intake.

**Consequences.** Questions get answered before requirements are written, when answers are cheap. "Can wait" questions are carried forward to the build stage instead of being lost.

## FD-030: Requirements can proceed with questions open, as labeled assumptions

**Context.** The readiness check can surface more blocking questions than are worth answering before seeing a first draft: when testing the pipeline, or when planning has to move with only some answers in hand. Blocking on every question would stall the work; proceeding silently would turn guesses into facts nobody remembers were guesses.

**Decision.** The user can choose to proceed with any or all questions still open. An open approach question becomes a proposed Design Decision. An open business-need question becomes a working assumption, stated in the outline for the user to correct, then written into the affected requirement's `## Open questions` section, labeled as an assumption and naming the question by ID. Every requirement resting on an open question carries the tag `open-questions`, and the index lists them as `requirements_with_open_questions`. When an answer arrives, a rerun replaces the assumption and removes the tag.

**Consequences.** Work never stalls on unanswered questions, and every guess stays visible in one list until it's confirmed. Uses the existing `tags` field, so no schema change.

## FD-031: A CI can cover near-identical variants of one build item

**Context.** FD-010 put one build item in each CI. Applied strictly to reports, three reports that differ only by a filter, sort or grouping would be three CIs, three tasks and three things to test, for what is one sitting of work.

**Decision.** A build item can be a set of near-identical variants: reports or views that differ only by filter, sort, grouping or columns, or templates that differ only in small wording. They share one CI when they're built together, tested together, and would never be prioritized or deployed separately. The CI body lists each variant and how it differs. Fields remain one per CI, so the ERD-to-CI match stays exact. A distinct report (different data, different purpose) gets its own CI, even when one requirement covers several related reports.

**Consequences.** CI counts reflect real units of work, not every permutation. Refines FD-010.

## FD-032: A requirement is one deliverable the client approves as a unit

**Context.** The first test run of the requirements skill turned Northshore's sources into 35 requirements. The skill's rule was "one need per requirement," and with no definition of a need it wrote roughly one requirement per sentence of the sources: three requirements about the same report, separate requirements for a report's filters, a nurture sequence split from its own stop rules. Hand consolidation brought it to 18.

**Decision.** A requirement is something the client would approve, defer or decline as a unit, anchored on a deliverable they'd recognize: each form, each integration, each report, each approval or other workflow, each process stage. Everything about that deliverable is a point in its body. A deliverable is split only when a piece has its own design decision, a meaningfully different priority, or is a different kind of deliverable: website capture (a form) and social ad capture (an integration) are two requirements, the quote document and its discount approval workflow are two, and each report is its own requirement. Minor nice-to-haves are a line in the body marked `(optional)`, never their own requirement. As a check, an area usually has 2 to 5 requirements, and a project like Northshore roughly 12 to 20.

**Consequences.** Requirements read as a scope a client can actually review. Downstream CIs, stories, UAT and docs stop multiplying from fragments. A `could` priority is reserved for nice-to-haves substantial enough to stand alone.

## FD-033: Decisions settled by guidance start as decided

**Context.** The requirements skill marked a Design Decision `decided` only when the user confirmed it while steering the outline. In the first test run, all 11 decisions came out `proposed`, including the ones Hero's own guidance had already settled (quoting in CRM, the phase 1 scope), so the index's open decisions overstated what was actually open.

**Decision.** A `guidance` source is Hero's written direction, and counts as the user's say-so. A decision that guidance settles starts as `decided`, with `decided_on` set to that guidance source's date and the source cited in the Decision section. A decision the user confirms while steering the outline is also `decided`, dated from the approval. Everything else stays `proposed`. Only `guidance` counts: a `notes` source is observation, not direction. If guidance settles an approach but a client source conflicts on what the business needs, the decision stays `proposed` and the conflict is flagged.

**Consequences.** `open_decisions` in the index lists only real open choices. The hard rule against marking decisions decided without the user's say-so still holds; guidance is how that say-so gets written down. Refines FD-006 and FD-018.

## FD-034: The ERD skill records what exists; the CI skill records what's planned

**Context.** ERD files mix two kinds of truth: fields that exist in the client's org, and planned changes (`pending` fields, `flagged` removals, target picklist values). A single process writing both would risk a refresh from the org wiping out planned changes, or planned fields being mistaken for real ones.

**Decision.** A separate ERD skill, run after requirements and before CIs, builds and refreshes ERD files from the client's org. It works on every module the requirements need or only the ones the user names, from draft or approved requirements. It refreshes one way, from the org into the records: fields in the org are added or updated as `exists`, a `pending` field found in the org becomes `exists`, and planned values on fields a not-yet-deployed CI will change are left alone. **It never deletes a field from an ERD file**: a field that's gone from the org stays listed, marked `removed`, so the file keeps a full record of what was there. It never adds `pending` or `flagged` fields for new requirements; the CI skill does that, alongside the CIs that do the work. **The ERD skill itself is read-only** and never writes to the org; other HeroDocs automations may build in an org, but not this skill. Before reading anything, it confirms the connected org is this project's client, since the connector may be signed in to Hero's own CRM or another client's; that confirm-first rule applies to anything in HeroDocs that touches an org. Requirements and CIs often come before the client's subscription exists, so for a client with no org yet it can build from Zoho's standard modules, tagged `unverified` until the first real refresh.

**Consequences.** A refresh can be run any time without risk to planned work, and doubles as a check on what's actually been built. The ERD files keep a full history of fields, including removed ones. Refines FD-007.

## FD-035: Hero's build expertise lives in a private playbook library, never in client repos

**Context.** The CI skill needs Hero's expertise: how to spec an Analytics report well, which quoting approach fits which need and what it produces, the traps to avoid. That expertise is Hero's differentiation. Everything in the template, skills included, is copied into every client repo, so expertise placed there would ship to every client. It also changes at a different rate and for different reasons than the generic procedure of turning requirements into CIs.

**Decision.** The CI skill holds only the procedure. Expertise lives in a separate private repo, `herocrm/hero-playbooks`, packaged as a Claude Code plugin and installed user-level on Hero staff machines, so it's available in any client repo session without ever being committed to one. The library has two kinds of playbook: **CI-type playbooks** (how to spec and build a kind of item, with best practices, pitfalls and example CIs) and **process playbooks** (which approach fits a need, its selection criteria, and the CI set it produces). An `index.yaml` catalogs them so the CI skill loads only what matches. When a process playbook offers alternatives that guidance hasn't settled, the choice becomes a Design Decision. Records cite a playbook by ID and version in the CI's optional `playbook` field (`quoting-transactional@3`), and never contain its content. The CI skill works without the library, falling back to general Zoho knowledge, and reports every build item with no matching playbook.

**Consequences.** Clients get the build spec, never the expertise behind it. The library grows from real projects: each CI run's coverage gaps show which playbooks to write next, and a later skill can draft playbooks from a finished project's CIs. Playbooks differ from recipes: a playbook is how Hero builds something; a recipe is a deliverable pack of requirements and CIs, generated from playbooks, that can be shown or sold to a client.

## FD-036: CI types follow where the work happens, and file names carry a type code

**Context.** The first CI skill run showed two problems with the CI types. `picklist` split field work by what kind of field change it was, so a Lead Source value change couldn't sit with the other field work it's done alongside, and following that logic would mean a type per field type. And `template` lumped together email, mail merge and inventory templates, which are built in different places with different settings. Separately, scanning `cis/` gave no sense of the work without opening every file.

**Decision.** `field` covers any change to a field: creating it, changing its properties (label, mandatory, picklist values), or removing it. Whether it's a create, modify or remove comes from the field's ERD status (`pending`, `exists`, `flagged`), so the action isn't stored twice. `layout` narrows to layout-level work: sections, arrangement, profile assignment. `picklist` is removed. `template` splits into `email_template`, `mail_merge_template` and `inventory_template`. Each type has a three- or four-letter code that goes in the CI's file name after the ID: `CI-010-FLD-project-type-on-leads.md`. The codes: MOD, FLD, LAY, LRL, VRL, WFR, BLU, FNC, WDG, WEB, RPT, DSH, ETPL, MTPL, ITPL, INT, OTH. The validator warns when a file's code doesn't match its `ci_type`.

**Consequences.** The folder reads as a build inventory at a glance. Field work groups naturally regardless of the kind of change. Templates are counted and specced by the kind of template they actually are. Refines FD-005 and FD-011.

## FD-037: CI Groups are defined by place and sitting, not CI type

**Context.** FD-012 said a group holds CIs "of the same kind." In the first CI skill run, that kept a picklist value change out of the group of field additions it's built alongside, in the same screen, in the same session.

**Decision.** A group holds CIs built in the same place, in one sitting, whatever their type. In practice, all the field work in a module's field and layout editor (new fields, property changes, picklist value changes, removals) goes together, across modules if it's done in the same session. A layout rule, workflow, report or template, built in a different screen, stays outside a field group, though several of the same kind built together can form their own group. Grouping remains optional, one group per CI, with no status of its own. The CI skill shows proposed groups in its build plan so the user can steer them. Replaces FD-012.

**Consequences.** Groups match the builder's actual sessions, which is what makes one ClickUp task per group work.

## FD-038: A generated build plan shows CIs by group

**Context.** Reviewing a CI run meant opening dozens of files to see how the work had been grouped. Putting groups in subfolders of `cis/` was considered and rejected: groups change often during planning, and every regroup would become a file move, adding churn to exactly the diffs that most need to be reviewed cleanly.

**Decision.** `scripts/build_index.py` also generates `BUILD-PLAN.md` at the repo root, rebuilt by Cmd+Shift+B alongside the index and committed with it. It lists each CI Group with its requirements, a fields recap (each field as `Label [type]: create / modify / remove`, taken from the ERD), its CIs in build order with type codes, and the group's notes (the first paragraph of its body). Then it lists ungrouped CIs by requirement, and a full build order. Never edited by hand; the validator warns when it's stale.

**Consequences.** One file shows the whole build at a glance, and regrouping is a one-line change on a CI. It's also the natural source for ClickUp tasks: one task per group, with its CI list as the checklist. Extends FD-020.

## FD-039: Client repos pull framework changes with a deterministic sync

**Context.** Getting template changes into a client repo meant asking Claude Code to work out which files were framework, fetch them one by one, compare and copy them, with a permission prompt per file and a real chance of missing one. It was done four times in the first day of testing, and every framework change means doing it again in every client repo.

**Decision.** The template carries a manifest, `framework.yaml`, listing every framework path, and a script, `scripts/sync_framework.py`. Run in a client repo, the script links the template as a git remote, fetches it, reads the **template's** manifest (so new framework paths come across automatically), pulls exactly those paths, removes framework files the template no longer has, records the template version in `.herodocs-version`, rebuilds the index and build plan, validates, and commits to `main`. It never touches project files, and it won't commit if validation fails, leaving the changes staged instead. A `herodocs-sync` skill wraps it: it previews the change, lists new framework decisions, and fixes records the new rules break. The script syncs `scripts/`, so it updates itself; it's changed only in the template. Framework sync commits straight to `main`, like intake: it changes how the repo works, not what the project contains. Any new framework file or folder is added to `framework.yaml` in the same change.

**Consequences.** A sync is one command and the same every time. Each client repo shows which framework version it's on, which sets up a later GitHub Action that opens a sync pull request in every client repo at once. Sync fetches from the private template, so it only works for Hero staff. Extends FD-021.

## FD-040: Stories and CIs are designed together, and CIs link the stories they deliver

**Context.** The plan had been a CI skill followed by a separate stories and UAT skill. But stories are the bridge between a requirement (what the business needs) and the build (what we configure): designing CIs first, then writing stories to describe whatever got built, puts the build ahead of the experience. And two skills interpreting the same requirements separately can land in slightly different places, producing stories that describe a flow the CIs don't quite support.

**Decision.** One design skill, `herodocs-design`, replaces the CI skill. For each requirement, it works out who uses it and how (stories), then what to build to deliver that (CIs), in the same pass, and shows both together in its design plan for the user to steer. CIs gain an optional `stories` field listing the stories they deliver; the upstream direction holds (requirement, then story, then CI). The index lists stories no CI delivers as `stories_without_cis`, and the build plan shows which stories each CI delivers. System behavior with no user action still gets no story (FD-015), and its CIs link only to the requirement. A story that standard Zoho fully delivers, with nothing to build, is still written so the client sees the whole experience, and is tagged `no-build` so it isn't flagged. UAT stays a separate skill run after design, reading each story and the exact CIs linked to it. A later change skill will chain requirement changes, design and UAT for just the affected requirements.

**Consequences.** The same thinking shapes the experience and the build, and the story-to-CI links carry it forward to UAT, training and docs. Coverage becomes checkable in both directions. The design review is larger, but seeing stories next to the CIs that deliver them makes it easier to judge whether the build covers the experience. FD-034, FD-035, FD-036 and FD-037's references to "the CI skill" now mean `herodocs-design`.

## FD-041: UATs are written after design, one scenario each, from stories and their CIs

**Context.** UATs need to name the real screens, fields and values a client will use, which only exist once the CIs are designed. Without rules on scope, test writing tends toward one of two failures: a single vague test per story, or an explosion of invented edge cases nobody asked for.

**Decision.** A separate `herodocs-uat` skill runs after design. It reads each story, the CIs linked to it, and the ERD for real labels and values. One UAT is one scenario with one outcome. Each story gets a main-path test, `no-build` stories included; then one test per distinct exception that a requirement point or a CI explicitly defines (both sides of a layout rule, a validation rejecting bad input, a threshold, a role restriction). Behavior that nothing defines gets no test; if it looks like a real gap, the skill raises it as a design question. System behavior is tested against its requirement, by the role who sees the result. Tests are runnable by the client alone: specific preconditions, numbered steps using the labels they see (never API names or Setup screens), and an expected result that makes pass or fail obvious. A test resting on a working assumption is tagged `open-questions`. The skill shows a test plan for the user to steer before writing, works on a branch, never records results (FD-016), and never deletes a UAT, since results elsewhere are keyed by its ID.

**Consequences.** Test counts track the design, roughly one to three per story, and every test traces back to a story or requirement and to the CIs it exercises. Gaps in the design surface while tests are being written, before the client finds them.

## FD-042: A throwaway traceability review, with the assessment inline

**Context.** Reviewing a design run meant checking, requirement by requirement, which stories serve it and whether together they cover everything it asks for. The links exist in the records, but nothing laid them out side by side. Two shapes were considered for the AI's coverage assessment: a separate second pass the reviewer runs after writing their own notes (to avoid anchoring on the AI's view), or the assessment inline under each requirement. The second-pass approach was rejected as a hassle for a capable team, and as forcing reviewers to work every point out from scratch before seeing any notes.

**Decision.** `scripts/trace.py` generates `review/TRACE-<date>.md`: a summary table, then each requirement (its points, area, priority) followed by the stories that serve it, the CIs that deliver each story, the UATs that test each one, system-behavior CIs, and mechanical flags (no stories, only `no-build` stories, stories with no CIs, open questions, and missing UATs once tests exist). Each requirement ends with an assessment placeholder. The `herodocs-review` skill runs the script, then fills each placeholder with a short coverage assessment (point-by-point coverage, stories beyond the requirement, missing roles, build and test gaps, one suggestion) and writes an overall assessment. The reading order is requirement, stories, then assessment. The file is throwaway: `review/` is git-ignored, never committed or validated, and regenerated on demand, from whatever branch is checked out so a design can be reviewed before its pull request is merged. The skill changes no records.

**Consequences.** A design run can be reviewed one requirement at a time, with the links laid out and a second opinion right below. The same document covers stories, CIs and UATs, so it serves design and test review alike. A cleaned-up version, requirements with their stories in plain language, is a candidate for a client sign-off document later.
