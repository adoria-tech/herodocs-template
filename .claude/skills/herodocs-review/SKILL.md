---
name: herodocs-review
description: Generates a throwaway traceability review for a HeroDocs project, as a table per capability area with one row per user story (Requirement, User story, Assessment, Delivered by), and fills in an assessment of how well each story and requirement is covered. Use whenever the user wants to review, trace, check coverage of, or see requirements alongside their stories or CIs ("generate the trace", "show me requirements with their stories", "are all the requirements covered", "review the design before I merge", "assess the trace"), even if they don't say "trace" or "review".
---

# HeroDocs review

Produces a review document a person reads one row at a time: the requirement, a story that serves it, the assessment, and the CIs that deliver it (FD-042). One table per capability area, one row per story; the requirement sits on the first row of its stories.

The document is throwaway. It lives in `review/`, which git ignores, and is regenerated whenever it's wanted. It's never committed, validated or built on.

## Steps

1. **Confirm this is a HeroDocs repo.** Don't switch branches: a review often happens on a design branch before its pull request is merged, so trace whatever is checked out, and say which branch.
2. **Generate the table.** Run `scripts/trace.py` with the repo's `.venv` Python if it exists, otherwise `python3`:
   - everything: `scripts/trace.py`
   - one area: `scripts/trace.py --area "Lead intake"`
   - specific requirements: `scripts/trace.py --req REQ-004 REQ-009`

   It writes `review/TRACE-<date>.md`. Every Assessment cell holds a placeholder like `<!--a REQ-004 US-007-->_pending_<!--/a-->`, and there's one more under **Overall**.
3. **Read before judging.** For each requirement: its full body (including its open questions and Notes), every linked story in full, and the CIs in its Delivered by cells.
4. **Fill each Assessment cell.** Replace `_pending_` between the markers with the assessment below. Leave the markers in place.
5. **Fill the Overall placeholder.**
6. **Report back** briefly in chat: where the file is, which branch it was traced from, and the requirements needing the most attention. Suggest opening it with VS Code's preview (Cmd+Shift+V).

## The assessment cells

The table only works if cells stay short. **Each cell is one line of markdown**: no line breaks (use `<br>` at most once or twice), no pipes, and roughly 15 to 40 words.

**On the first row of each requirement**, start with the verdict for the whole requirement, then the note for that row's story:

`**Partly covered.** Point 3 (named follow-up owner) has no story.<br>This story covers points 1 and 2.`

Verdicts: **Well covered**, **Partly covered**, **Not covered**.

**On every other row**, just that story's note: which requirement points it covers, and anything wrong with it.

What a story note can say, only when it applies:

- the requirement points it covers
- it goes beyond what the requirement asks
- the role looks wrong, or a role the requirement implies has no story
- its CIs don't look like they'd fully deliver what the story describes, or it has none (`⚠ nothing yet`)
- a `no-build` story that standard Zoho doesn't actually deliver

For a **System behavior** row: whether those CIs cover the automatic parts of the requirement. For a **No stories** row: what's missing.

Rules for judging:

- **Judge against the requirement's own points.** A requirement is well covered when every point in its body is served by a story, or by system-behavior CIs. Don't invent needs it doesn't state.
- **`(optional)` points** can go uncovered without making a requirement partly covered.
- **Open questions:** judge against the working assumption, and add "revisit when answered" to the verdict.
- **Be direct and specific.** "Point 3 (named follow-up owner) has no story" helps. "Coverage could be improved" doesn't. A story that's fine gets a short note: "Covers point 1. Fine."

**Overall:** three to five bullets: how many requirements are well, partly and not covered, any pattern across them, and the few to look at first.

## What this skill never does

- Change any record. If the assessment suggests a fix, the user decides, and the design or UAT skill makes it.
- Commit, stage or validate the review file.
- Switch branches.
