# HeroDocs project: briefing for Claude

This repo holds the HeroDocs records for one Zoho implementation: sources, requirements, design decisions, data model, configuration items, stories, UAT, training and documentation. Each record is one markdown file with YAML frontmatter. The Hero team reviews everything Claude writes, either directly or through pull requests.

## Read first

1. `index.yaml`: generated summary of the whole project. Start here instead of opening every record. Sections: `gaps`, `open_decisions`, `areas` (requirements by capability area), `requirements` (with CI build order), `fields` (why each field exists), `records` (with reverse links in `linked_from`).
2. `BUILD-PLAN.md`: generated view of the CIs by CI Group, in build order, with each group's fields and notes, and the stories each CI delivers.
3. `project.yaml`: client, apps in use, capability areas, and the roles list.
4. `README.md`: the full rules. Consult the relevant section before writing a record type you haven't written in this session.
5. `FRAMEWORK-DECISIONS.md`: why the rules are what they are. Check it before suggesting a change to how records work.
6. `templates/`: the starting file for each record type. `schemas/`: what the validator enforces.

## Commands

Use the repo's `.venv` Python if it exists, otherwise `python3`:

```
.venv/bin/python3 scripts/build_index.py      # rebuild index.yaml and BUILD-PLAN.md
.venv/bin/python3 scripts/validate.py         # validate all records
.venv/bin/python3 scripts/sync_framework.py   # pull the latest framework from the template
.venv/bin/python3 scripts/trace.py            # throwaway traceability review in review/
```

Always rebuild before validating.

## Where changes get committed

Pick the path by the kind of change (see FD-026, FD-027 and FD-039):

| Change | Path |
|---|---|
| Source intake, including an approved solution outline | Commit straight to `main` |
| Framework sync from the template | Commit straight to `main` |
| A small edit the user asked for directly (a role, a typo, one field, one record) | Show the user the change, and on their OK commit straight to `main` |
| Anything a skill generates in bulk, or a change across many records | Work on a branch named for the work (e.g. `requirements-2026-10-26`), push it, and offer a pull request for review |

If you're not sure which applies, ask. The user can always override: "commit this to main" or "put this on a branch" wins. Review documents in `review/` are never committed.

Whichever path, every change goes through the same steps:

1. Write or edit the records.
2. Rebuild `index.yaml` and `BUILD-PLAN.md`, then validate.
3. Fix every error. Fix warnings you caused; report any you can't resolve.
4. Commit the records with the refreshed `index.yaml` and `BUILD-PLAN.md`, with a clear message, and push.
5. Tell the user what changed and what needs their judgment.

## Hard rules

- Never edit `index.yaml` or `BUILD-PLAN.md` by hand. They're generated.
- Never edit framework files (everything listed in `framework.yaml`: `schemas/`, `scripts/`, `templates/`, `.claude/skills/`, `CLAUDE.md`, the folder READMEs and the rest) in a client repo. They change only through `scripts/sync_framework.py`, which pulls them from `herocrm/herodocs-template`. Framework changes are made in the template. If a rule seems wrong, say so instead of working around it.
- Before reading from or writing to any Zoho org, confirm it's this project's client: check the connected org's name against `client` in `project.yaml`, and stop and ask if they don't clearly match. The connector may be signed in to Hero's own CRM or another client's org.
- Never copy content from Hero's playbook library (the `hero-playbooks` skill) into this repo. Records may cite a playbook by ID and version; its reasoning, criteria, pitfalls and examples stay in the library. See FD-035.
- IDs never change and are never reused. A new record takes the next number for its prefix (highest existing + 1). File names are `ID-short-slug.md`; CI file names add the type code: `CI-010-FLD-short-slug.md`.
- Links point upstream only (a CI lists its requirements and stories; a requirement never lists its CIs). Never add reverse links.
- Don't store dates or authors on records, except `date` on sources, `decided_on` on decisions and `approved_on` on requirements. Git records the rest.
- Never mark a requirement `approved` or anything `deployed` unless the user says so. Mark a Design Decision `decided` only on the user's say-so: a `guidance` source that settles it (dated from that source), or their explicit confirmation. See FD-033.
- Never invent picklist values, prices, names or facts. If a source doesn't say, write `values: [TBD]` or raise it as an open question. A working assumption is allowed only when labeled as one.
- Never record UAT results in the repo. They're tracked outside it, keyed by UAT ID (FD-016).

## Writing records

- **Requirements:** the body says what the business needs, never how. No fields, modules, workflows, apps or Zoho terms in the body. Each stands alone: name things in full, since clients approve requirements one at a time. Link every source that supports it. `area` (required) is the capability area from `project.yaml`. `module` (optional) is the Zoho module once it's known; leave it out while the choice is open.
- **Requirement size:** one requirement per deliverable the client would approve as a unit: each form, integration, report, workflow or process stage, with its details as points in the body. Split only for a separate design decision, a meaningfully different priority, or a different kind of deliverable. Minor nice-to-haves are an `(optional)` line in the body. See FD-032.
- **Open questions on requirements:** when a requirement depends on an unanswered question, tag it `open-questions` and add an `## Open questions` section naming each question by ID, with any working assumption clearly labeled as an assumption. The index lists tagged requirements as the project's lock-down list. Remove the tag once every question is answered.
- **App and approach choices** (CRM vs Creator, Leads vs Contacts) are Design Decisions: Context, Options Considered, Decision, Consequences. `decided` when guidance or the user's confirmation settles them, otherwise `proposed`.
- **Sources:** client sources are authoritative on what the business needs; `guidance` sources are authoritative on how we'll approach it. When they conflict on the what, flag it. Never resolve it silently. Open questions are numbered `SRC-###-Q#`; a later source that answers one says `(resolves SRC-###-Q#)`.
- **ERD files** list every field in the module with status `pending`, `exists`, `flagged` or `removed`. The ERD skill records what exists, reading the client's org; the design skill adds planned changes as `pending` or `flagged`. Fields are never deleted from an ERD file: a field gone from the org is marked `removed`. A change to an existing field keeps `exists`; the CI is the work. Picklist values live only here. See FD-034.
- **Stories and CIs are designed together** (FD-040): for each requirement, who uses it and how (stories), then what to build to deliver that (CIs). Each CI lists the stories it delivers in `stories`.
- **User Stories** are one role, one piece of functionality: "As a **role**, I want to **do something**, so that **benefit**." System behavior with no user action gets no story; its CIs and UAT link straight to the requirement. A story standard Zoho fully delivers, with nothing to build, is tagged `no-build`.
- **CIs** are one per field or build item. `ci_type: field` covers any change to a field (create, modify or remove; the field's ERD status says which). Templates are `email_template`, `mail_merge_template` or `inventory_template`. A build item can be a set of near-identical variants (reports or views differing only by filter, sort, grouping or columns) built and tested together; list each variant in the body. Never duplicate a field the ERD already has. CIs reference the ERD for picklist values and never restate them. Every CI links a requirement, and the stories it delivers unless it's system behavior. Use `depends_on` for build order. A CI built from a Hero playbook cites it in `playbook` (`quoting-transactional@3`). See FD-031, FD-035 and FD-036.
- **CI Groups** collect CIs built in the same place, in one sitting, regardless of type: all the field work in a module's field editor goes together. A layout rule, workflow, report or template built in another screen is separate. See FD-037.
- **UATs** are one scenario with one outcome, runnable by the client alone: specific preconditions, numbered steps using the labels they see in Zoho (never API names or Setup screens), and a clear expected result. Each story gets a main-path test, plus one per distinct exception a requirement or CI defines; system behavior is tested against its requirement. Don't test behavior nothing defines. See FD-041.
- **Bodies** are never left empty or with template wording. The validator warns on both.

## When unsure

Ask. If the question can't wait, record it: an open question in your summary, a labeled working assumption on the affected record, or a `proposed` Design Decision if it's a real choice between approaches. A visible gap is better than a confident guess.

## Skills

HeroDocs skills live in `.claude/skills/`. Use them for the work they cover instead of improvising:

- **herodocs-intake** (one source at a time): fetches a Fathom meeting, Drive document, Gmail thread, file or pasted notes; saves the raw text to `sources/raw/`; writes a Source Reference with a digest and numbered open questions; commits to `main`. Writes no requirements.
- **herodocs-requirements** (all sources at once): readiness check on open questions (answer Hero ones, draft a call agenda, or proceed with them open), then a solution outline for the user to steer, then saves the approved outline as a `guidance` source and writes its areas to `project.yaml` (on `main`), then writes requirements and Design Decisions on a branch for review.
- **herodocs-erd** (all modules the requirements need, or specific ones): confirms the connected Zoho org is this client's, then builds ERD files from the org's real modules and fields, and refreshes existing ERD files one way from the org. Read-only: it never writes to the org, and never deletes a field from an ERD file. Records what exists; planned changes come from the design skill. Can build from Zoho's standard modules, tagged `unverified`, before the client's subscription exists. Works on a branch.
- **herodocs-design** (all requirements, or the ones named; draft or approved): designs the solution in one pass. Shows a design plan per requirement (its stories, then the CIs that deliver them) for the user to steer, then writes stories, CIs, CI Groups and the planned ERD changes, on a branch. Uses Hero's playbook library when installed, and reports every build item with no playbook.
- **herodocs-uat** (all stories, or the ones named): after design, shows a test plan (the scenarios per story, plus system behavior) for the user to steer, then writes client-runnable UATs from each story and its linked CIs, on a branch.
- **herodocs-review** (all requirements, an area, or specific ones): generates a throwaway traceability review in `review/` with `scripts/trace.py` (each requirement with its stories, their CIs and UATs, and mechanical flags), then writes a coverage assessment under each requirement and an overall one. Changes no records and commits nothing.
- **herodocs-sync**: pulls the latest framework from the template with `scripts/sync_framework.py`, explains what changed (including new framework decisions), fixes records the new rules break, and commits to `main`.

Hero's playbook library (`hero-playbooks`) is installed separately on Hero staff machines and never lives in this repo.
