---
name: herodocs-requirements
description: Writes the requirements for a HeroDocs project from all of its sources at once. Runs a readiness check on open questions, presents a one-page solution outline (capability areas, process, app options, decisions, scope) for the user to steer, saves the approved outline as a guidance source, then writes requirements and Design Decisions on a branch for review. Can proceed with open questions unanswered, carrying them as labeled working assumptions. Use whenever the user wants to write, draft, generate, create, update or refresh requirements in a HeroDocs repo, asks what's still open before requirements, wants a solution outline or overview of the approach, says the sources are complete, or wants to push ahead with questions still open ("write the requirements for Key2", "what questions do we still need answered", "show me the outline", "sources are all in", "just proceed"), even if they don't say "requirements".
---

# HeroDocs requirements

Turns a project's sources into requirements and design decisions. It reads **every** source at once, so the whole picture shapes the requirements rather than whichever document arrived first, and it lets the user steer before anything is written.

It runs in four phases, and each one ends with the user:

1. **Readiness check**: which open questions still block requirements, and what to do about them
2. **Solution outline**: a one-page view of the approach, shown in chat for the user to steer
3. **Save the outline**: once approved, it becomes a `guidance` source, and its capability areas go into `project.yaml`
4. **Write**: requirements and Design Decisions, on a branch, for review

Never skip ahead. A phase only starts when the user says to go on. If an approved outline already exists and the user asks to go straight to writing, start at Phase 4 using that outline.

## Before you start

1. Confirm this is a HeroDocs repo: `project.yaml`, `schemas/` and `sources/` exist.
2. `git checkout main`, then `git pull`. If the working tree has changes you didn't make, stop and ask.
3. Read `CLAUDE.md` if you haven't this session. Its hard rules apply throughout.
4. Read `index.yaml`, then every Source Reference in `sources/`. The digests are your main input. Go to the raw text in `sources/raw/` only when you need a specific detail, number or exact wording. For a large project, work through the digests one capability area at a time rather than holding every raw transcript in mind at once.
5. Note what already exists: requirements, decisions, areas in `project.yaml`. If requirements exist, this is a **rerun** (see Reruns below).
6. Read the examples in `examples/` before writing your first outline or requirement in a session.

If there are no sources, stop and suggest the intake skill.

## Phase 1: Readiness check

Gather every open question across the digests. Intake numbers them `SRC-###-Q#`.

1. **Drop the resolved ones.** A question is resolved if a later source says so (`resolves SRC-001-Q3`) or a later source or guidance clearly answers it. When a later source answers it implicitly, say which source answered it, so the user can check.
2. **Sort the rest:**
   - **Blocking**: the answer changes the scope, the business need, or the approach for an area.
   - **Hero can answer**: about approach, app choice or scope, where Hero decides rather than the client.
   - **Can wait**: detail that only matters when building, such as exact picklist values, labels or report columns. Carry these forward.
3. **Present the result** grouped by topic, each question with its ID and one line on why it's in that group. See `examples/clarification-agenda.md`.

Then offer the user three choices, and let them mix them:

- **Answer the Hero questions now.** Take the user's answers in chat and save them as a `guidance` source through the intake skill's format (next SRC number, raw text, digest with `(resolves SRC-###-Q#)` on each answer, committed to `main`). Then re-check.
- **Draft a clarification agenda** from the blocking questions, for a call with the client. If the user asks, draft it as an email. The call's transcript comes back through the intake skill as a new source, and you rerun this phase.
- **Proceed.** Go on to the outline with questions still open: all of them ("just go"), or the ones the user hasn't answered yet ("I've answered these three, proceed with the rest"). This is normal, not a failure: testing the pipeline, or planning with some answers still outstanding. Unanswered questions get carried forward as described in the next phases, never dropped and never quietly turned into facts.

If nothing is blocking, say so and move on with the user's OK.

## Phase 2: Solution outline

Show the outline **in chat**. Write no files in this phase. Use this structure (see `examples/solution-outline.md`):

```markdown
# Solution outline: <client>

## Capability areas
<4 to 10 areas, each a short business name with one line on what it covers>

## Process
<the end-to-end flow as a short numbered list, from first contact to handoff>

## Approach by area
<for each area: the recommended app (and module, if known), the alternatives worth
considering, and which sources support the recommendation; mark where guidance decides it>

## Decisions needed
<real choices still open: each becomes a proposed Design Decision>

## Scope
<In / Deferred to a later phase / Out>

## Conflicts between sources
<where sources disagree, which side each is on, and how you suggest resolving it>

## Proceeding with open questions
<only when the user chose to proceed: each unresolved blocking question, by ID, with
how it will be carried (a proposed decision, or the working assumption you'll write)>
```

How to build it:

- **Areas are business capabilities**, named the way the client would name them ("Lead intake," "Quoting," "Handoff to operations"), never Zoho terms. If areas already exist in `project.yaml`, reuse them and propose new ones only where needed.
- **Guidance decides approach.** Where a `guidance` source settles an approach, use it and cite it, even if a client document suggests otherwise. Show the client's suggestion as the alternative that was set aside. Choices guidance has settled aren't "Decisions needed"; they're already made.
- **Client sources decide the need.** If guidance would change *what* the business gets rather than how, flag it under Conflicts. Don't resolve it yourself.
- **Name the module only when it's known**: guidance says so, it's an existing system's established module, or the choice is unambiguous. When it's a real choice (Leads, or Contacts with a contact type), list it under Decisions needed.
- **For each open question you're proceeding past**, say how it will be carried. An approach question becomes a proposed decision. A business-need question becomes a working assumption: state the assumption, and its basis in the sources, so the user can correct it now. If the sources give no reasonable basis, say so and propose writing the requirement with the question left open rather than guessing.
- **Keep it to about a page.** It's for steering, not specifying.

Then ask the user to steer: what to change, what's missing, what's wrong, which assumptions to correct. Revise and show it again until they explicitly approve it ("approved," "looks good, go"). Iterating here is cheap and expected.

## Phase 3: Save the approved outline

1. **Save it as a source.** Take the next SRC number. Write the final outline to `sources/raw/SRC-###.txt` (with the same Title/Type/Date/URL header the intake skill uses), and create `sources/SRC-###-approved-solution-outline.md`:
   - `type: guidance`, `date:` today, `url: Approved by <user's name> in Claude Code session`, `raw_text:` the raw file
   - Body: the intake digest format, with the outline's substance under `## Direction`: areas, approach by area, scope boundaries. Decisions the user confirmed while steering go under `## Decisions made`, noting any open questions they resolve (`resolves SRC-002-Q4`). Questions still open go under `## Open questions`, each with the working assumption the user approved, if any.
   - If an earlier approved outline exists, title this one with a revision number. The newer one takes precedence.
2. **Write the areas into `project.yaml`.** Add any new areas to the `areas` list, in the outline's order. Never remove an area that a requirement uses, and only rename one if the user asked.
3. Rebuild the index, validate, and commit both to `main` together: `Add SRC-###: Approved solution outline`. Push.

The outline is a source, so it follows the intake rule and goes straight to `main`.

## Phase 4: Write requirements and decisions

Create a branch: `git checkout -b requirements-<YYYY-MM-DD>`.

### Sizing requirements

Getting the size right matters more than anything else in this phase. Too fine, and the client is asked to approve dozens of fragments that only make sense together; every report detail, rule and filter becomes its own record, and CIs, stories and UAT multiply from there. Too coarse, and a requirement can't be approved, prioritized or tested on its own. Size by these rules (see FD-032):

1. **A requirement is something the client would approve, defer or decline as a unit.** If two pieces would always be decided together, they're one requirement.
2. **One requirement per deliverable the client would recognize**: each form, each integration, each report, each approval or other workflow, each process stage ("qualifying leads," "moving an opportunity to won or lost"). Everything about that deliverable goes in its body as points: what a form captures, what a report shows and how it's filtered, the rules a process follows, its exceptions.
3. **Split a deliverable only when a piece has its own design decision, a meaningfully different priority, or is a different kind of deliverable.** The quote document and the discount approval workflow around it are two requirements. Website lead capture and social ad lead capture are two, because one is a form and the other an integration, even though the client thinks of both as "capturing leads." Each report is its own requirement, even when several are closely related.
4. **Minor nice-to-haves become a line in the body, marked `(optional)`**, never a requirement of their own: an extra report filter, a convenience sort, a secondary notification.
5. **Check the total before writing.** A capability area usually lands at 2 to 5 requirements, and a project the size of the Northshore sample at roughly 12 to 20. If you're well past that, re-read rule 2: you're probably writing one requirement per sentence of the sources.

Work out the full list of requirements (titles and what each covers) before writing any files, check it against these rules, and only then write.

### Requirements

One file per requirement in `requirements/`, using `templates/requirement.md`. See `examples/requirements.md`.

- **The body is business language.** What the business needs and why, then the points that define the deliverable. No apps, modules, fields, workflows or Zoho terms. Name things in full so the requirement stands alone, since clients approve them one at a time.
- **`## Notes`** carries what the body shouldn't: context, the open questions it relates to (by ID), "how" hints from sources for whoever writes the CIs, and short quotes where the wording matters.
- **`area`**: one of the areas in `project.yaml`.
- **`module`**: only when known (from guidance, the approved outline, an established system, or an existing ERD file). Otherwise leave it out. The index lists requirements without a module, and the related Design Decision settles it.
- **`sources`**: every source that supports it, not just the first, plus the approved outline when it shaped the requirement.
- **`priority`**: `must` for what the client called essential, a legal or contractual need, or anything other requirements depend on; `should` for clearly wanted but not critical; `could` for nice-to-haves that are substantial enough to be their own requirement. When sources don't say, use `should` and mention it in the summary.
- **`status: draft`**, always. Leave out `approved_by` and `approved_on`.
- **Titles** name the deliverable or state the need as a short sentence: "Website quote requests are captured with their source and project details," "Pipeline report for the Owner."

### Open questions and working assumptions

When a requirement depends on a question that's still open:

- Add `tags: [open-questions]` to its frontmatter. The index lists every tagged requirement under `gaps` as `requirements_with_open_questions`, which is the project's lock-down list.
- Add an `## Open questions` section after the body, before Notes. One bullet per question, by ID. Where the approved outline carries an assumption, write it out and label it: `**SRC-002-Q4:** Who follows up on unreached leads? Working assumption: the assigned Sales Designer. Confirm with Mark.` Where there's no assumption, say the question is open and what it affects.
- Write the body so it holds whichever way the answer lands where you can. Where the answer would change the need itself, write the body on the working assumption, and make sure the Open questions section says so.
- An approach question goes in a proposed Design Decision instead. The requirement's Open questions section just points to it (`Depends on DD-001`), and the tag still applies until the decision is made.

Never write an assumption into a requirement as if it were fact, and never drop an open question because it was inconvenient.

### Design Decisions

One file per decision in `decisions/`, using `templates/decision.md`. See `examples/decision.md`.

- Write one for **each item under Decisions needed** in the approved outline, and for each approach the outline or guidance settled that someone might later question (an app choice, a module choice, a scope boundary).
- **Context** states the question and why it matters. **Options Considered** gives each option its trade-offs, including client suggestions that were set aside. **Decision** gives the choice (or recommendation) and the reasoning, citing guidance by source ID. **Consequences** says what it commits the project to or rules out.
- **Status: `decided`** when the user has already made the choice, in either of two ways (see FD-033):
  - **A `guidance` source settles it.** Guidance is Hero's written direction, so it counts as the user's say-so. Set `decided_on` to that guidance source's date, and cite the source in the Decision section. Only `guidance` counts; a `notes` source is observation, not direction.
  - **The user confirmed it while steering the outline.** Set `decided_on` to the approval date.
- **Status: `proposed`** for everything else: real choices still open, and recommendations you're making that no guidance or confirmation backs.
- If guidance settles a choice but a client source pushes the other way on *what* the business needs (not just how), keep it `proposed` and flag the conflict.
- **`requirements`**: the requirements the decision affects.

### Finish

1. Rebuild the index, then validate. Fix every error and every warning you caused. Expected warnings: requirements whose module has no ERD file yet.
2. Commit the requirements, decisions and refreshed `index.yaml` together on the branch: `Requirements first pass: N requirements, M decisions`. Push the branch.
3. Offer to open a pull request so the user can review the whole set as one diff.

## Reruns

When requirements already exist (new sources arrived, answers came in, or the outline was revised):

- **Same need, new detail:** update the existing requirement in place, keeping its ID. Add the new source to `sources`.
- **An open question gets answered:** replace the working assumption with the answer, citing the source that answered it. If the answer differs from the assumption, update the body to match and call it out in the summary. Remove the question from the requirement's Open questions section, and remove the `open-questions` tag once none remain.
- **New guidance settles a proposed decision:** set it to `decided`, with `decided_on` from the guidance source, and update the Decision section to cite it.
- **New need:** add it to the existing requirement for that deliverable if there is one; otherwise create a new requirement with the next ID.
- **Need no longer wanted:** never delete. Set `status: declined` and add a line to Notes saying why and which source said so.
- **Approved requirements:** don't change their wording. If new sources contradict one, flag it in the summary for the user to take back to the client.
- **Decided decisions:** don't reopen them. If new information challenges one, write a new proposed decision that `supersedes` it and flag it.

The pull request diff then shows exactly what changed and why.

## Report back

After Phase 4, summarize briefly:

- requirements written (or updated), grouped by area, with counts by priority
- decisions: how many decided (and by which guidance or confirmation), how many proposed, and the proposed ones by title
- requirements tagged `open-questions`, with the assumptions they rest on, so the user knows what to lock down
- requirements without a module, and which decision settles each
- open questions carried forward as "can wait"
- any conflicts you flagged, and any priority you defaulted to `should`
- the branch name, and the offer of a pull request

## What this skill never does

- Write CIs, ERD files, stories, UATs, training or documentation. Those come later, from approved requirements.
- Mark requirements `approved`, or decisions `decided` without the user's say-so (a `guidance` source they wrote, or their confirmation while steering).
- Invent needs, numbers or decisions that no source contains, or present a working assumption as fact.
- Resolve a conflict on *what* the business needs. It flags it.
- Delete requirements. It declines them.
