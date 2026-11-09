---
name: herodocs-intake
description: Adds one source to a HeroDocs project repo. Fetches a Fathom meeting, Google Drive document, Gmail thread, local file or pasted notes; saves the full text to sources/raw/; writes a Source Reference (SRC) with a structured digest; rebuilds the index, validates and commits to main. Use whenever the user wants to add, ingest, intake, capture or log a source in a HeroDocs repo, such as a meeting, call, transcript, client document, spreadsheet, RFP, email thread, consultant notes or Hero guidance on approach ("add the Key2 kickoff call", "intake this doc", "here's my guidance on work orders"), even if they don't say "intake". Never writes requirements.
---

# HeroDocs source intake

Adds one source to the project. A source is anything requirements will be drawn from: a meeting, a client document, an email thread, an RFP, a consultant's notes, or Hero's own guidance on approach.

Intake deliberately stops short of requirements. Requirements are written later by a separate skill that reads every source at once, so the whole picture shapes them rather than whichever source arrived first. That skill reads the **digests** you write here before it goes back to the raw text, so a good digest is what makes large projects workable. Write it for that reader.

One source per run. If the user hands you several, process them one at a time, each with its own commit.

## Before you start

1. Confirm this is a HeroDocs repo: `project.yaml`, `schemas/` and `sources/` exist at the root.
2. Make sure you're on `main` with the latest changes: `git checkout main`, then `git pull`. If the working tree has uncommitted changes you didn't make, stop and ask the user before touching anything.
3. Read `index.yaml` to see existing sources. The new source's ID is the next number after the highest existing `SRC-###` (SRC-001 if there are none). IDs are never reused.
4. Read the example digests in `examples/` the first time you write a digest in a session.
5. Skim the **Open questions** in existing Source References, so you can notice when this source answers one.

## Step 1: Identify the source and its type

Work out what the user is pointing at and which type it is:

| Type | Use for |
|---|---|
| meeting | A recorded call or meeting, usually from Fathom |
| document | A client document: process docs, spreadsheets, existing system notes, forms |
| email | An email thread |
| notes | A Hero consultant's observations |
| guidance | Hero's direction on approach: which app, how something should be built, what's in or out of scope |
| rfp | A request for proposal |
| other | Anything that doesn't fit |

The difference between `notes` and `guidance` matters. Guidance is authoritative on *how* the project will be approached, and the requirements skill will follow it over a client document's suggestions. If you can't tell which the user means, ask.

Check `index.yaml` and the existing Source References for the same original (same URL, or obviously the same meeting or document). If it's already there, tell the user and ask whether to skip it or replace that source's raw text and digest.

## Step 2: Fetch the full text

Use the connectors available in this session:

- **Fathom meeting:** find it by company, title or date. If several meetings match, list them and ask which one. Fetch the full transcript, keeping speaker labels. The Fathom summary can help you orient, but the digest is built from the transcript. Record the attendees, the meeting date and the recording URL.
- **Google Drive document:** find and read the file. For spreadsheets, capture each sheet's contents as plain text, sheet by sheet. Use the document's own date if it states one, otherwise its last modified date. Record the Drive link.
- **Gmail thread:** fetch every message in order, with sender and date for each. Use the latest message's date. Record the thread link.
- **Local file:** read it from the path the user gives, or from `sources/inbox/`. Ask where the original lives so the Source Reference can point to it.
- **Pasted text:** use it as given. Ask where it came from.

If a fetch fails or you can't find the source, say so and ask. Never reconstruct a source from memory or from a summary.

For `url`: use the link to the original. If there genuinely isn't one (notes typed into the session, say), write a short description of where it came from, such as `Typed by Len in Claude Code session`.

## Step 3: Save the raw text

Write the full text to `sources/raw/SRC-###.txt`:

```
Title: <title>
Type: <type>
Date: <YYYY-MM-DD>
URL: <url>

<full text, unedited>
```

Don't summarize, tidy or trim the text. The raw file is the record of what the source actually said, and the requirements skill goes back to it for specifics. Length isn't a concern here.

## Step 4: Write the Source Reference

Create `sources/SRC-###-short-slug.md`. Frontmatter:

```yaml
---
id: SRC-###
title: <descriptive title, e.g. "Kickoff call with Northshore">
type: <type>
date: <YYYY-MM-DD>
url: <url>
raw_text: sources/raw/SRC-###.txt
---
```

The body is the digest. Use these headings, in this order:

```markdown
# <title>

<Two or three sentences: what this source is and what it mainly covers.>

**Attendees:** <meetings only: name, role, company>

## Needs
## Constraints
## Proposed approaches
## Decisions made
## Open questions
## Key quotes
```

For a `guidance` source, add a `## Direction` section right after the summary, before Needs. It holds the direction itself, stated plainly with the reasoning behind each point. The other sections may be short or empty for guidance.

What goes in each section:

- **Needs:** what the business says it needs, in business language, one bullet each. Attribute where useful ("Mark wants..."). This is the raw material for requirements, so be thorough here.
- **Constraints:** budget, timing, volumes, rules, existing systems, integrations, anything that limits the solution.
- **Proposed approaches:** any *how* the source suggests, in the source's own terms and attributed ("Client's process doc says quotes should be built in Creator"). Don't judge them here; the requirements skill weighs them against guidance.
- **Decisions made:** anything the source settles, with who settled it. If it answers an earlier source's open question, end the bullet with `(resolves SRC-###-Q#)`.
- **Open questions:** things left unresolved, raised but not answered, or that you noticed are missing (a process with no owner, a number that's never given). **Number each one** with this source's ID: `**SRC-002-Q1:** Who updates the website form?` The numbers let later sources and the requirements skill refer to them.
- **Key quotes:** up to five short, exact quotes where the precise wording matters: numbers, commitments, strong preferences. Name the speaker.

For a `guidance` source, a Direction point that answers an earlier open question also ends with `(resolves SRC-###-Q#)`.

Only mark a question resolved when this source clearly answers it. If it only partly answers one, leave the earlier question open and add a new numbered question for what's still missing.

Keep every heading even when a section is empty, and write `None stated.` under it. That tells the requirements skill the section was checked rather than skipped.

Two rules that matter more than the rest:

- **Never add anything the source doesn't contain.** No inferred needs, no filled-in numbers, no assumed decisions. If you think something is implied, put it under Open questions as a question.
- **Keep the digest proportional.** A 20-minute call might need 25 lines; a long RFP might need 120. Cover everything requirement-relevant, and skip small talk and logistics.

## Step 5: Rebuild, validate and commit

1. Rebuild the index, then validate (see CLAUDE.md for the commands).
2. Fix any errors. The new source shouldn't produce warnings; if it does, fix them.
3. Commit the raw text file, the Source Reference and the refreshed `index.yaml` together, directly on `main`, with the message `Add SRC-###: <title>`. Then push.

Intake commits straight to `main` because sources are inputs, not commitments, and they accumulate over time. See FD-026 in FRAMEWORK-DECISIONS.md.

## Step 6: Report back

Keep it short:

- the ID, title and type
- a one-line sense of what the digest found ("9 needs, 3 constraints, 2 proposed approaches, 4 open questions")
- which earlier open questions it resolves, if any
- anything notable: a direct contradiction with an existing source, a guidance point that overrides a client suggestion, a gap worth chasing before requirements
- how many sources the project now has, and a reminder that the requirements skill starts with a readiness check on open questions once the picture is complete

## What this skill never does

- Write requirements, design decisions, CIs or any record other than the Source Reference.
- Edit other sources, unless the user asked to replace a duplicate. (Resolving an earlier question is recorded in the *new* source, never by editing the old one.)
- Resolve conflicts between sources. It notes them; the requirements skill and the user resolve them.
