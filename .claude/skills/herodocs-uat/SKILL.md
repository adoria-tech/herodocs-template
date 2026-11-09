---
name: herodocs-uat
description: Writes User Acceptance Tests for a HeroDocs project from its user stories and the CIs that deliver them, so the client can prove each piece of functionality works. Works for all stories, or the stories, requirements or areas the user names. Shows a test plan (the scenarios per story) for the user to steer, then writes client-runnable UATs with specific preconditions, numbered steps and a clear expected result, on a branch for review. Use whenever the user wants to write, draft, generate, create, update or refresh UATs, acceptance tests, test scripts or test cases in a HeroDocs repo ("write the UATs", "how will the client test this", "test cases for REQ-004", "update the tests for the changed stories"), even if they don't say "UAT".
---

# HeroDocs UAT

Writes the tests the client runs to accept the build. Each UAT is one scenario a person can run alone in Zoho: specific setup, numbered steps, and a result they can see. UATs come after design, because a good test names the real screens, fields and values the CIs build (FD-041).

It runs in two phases, each ending with the user:

1. **Test plan:** the scenarios for each story and each piece of system behavior, shown in chat for the user to steer
2. **Write:** the UATs, on a branch, for review

UAT files define tests only. Results (Hero's run and the client's run) are tracked outside the repo, keyed by UAT ID (FD-016). Never record pass or fail in a UAT file.

## Before you start

1. Confirm this is a HeroDocs repo, then `git checkout main` and `git pull`. Stop and ask if the working tree has changes you didn't make.
2. Read `CLAUDE.md` if you haven't this session. Its hard rules apply throughout.
3. Read `index.yaml`, `project.yaml` (especially `roles`), and for everything in scope: the stories, the requirements they serve, and **the CIs linked to each story** (the index's `linked_from` on each story lists them). Read the ERD files for the modules involved, for real field labels and picklist values.
4. Read the examples in `examples/` before writing your first UAT in a session.
5. Note existing UATs. If stories in scope already have them, this is a **rerun** (see Reruns below).

**Scope:** all stories and requirements (excluding `declined`), or just the stories, requirements or areas the user names.

## Phase 1: Test plan

### What can be tested, and what can't

- **A story with no CIs** (and not tagged `no-build`): the design isn't finished. Skip it, and suggest running the design skill for its requirement.
- **A story or CI with `[TBD]` details that the test depends on** (an undecided threshold, unsettled picklist values): skip the part of the test that depends on it, or the whole scenario if nothing testable is left, and list it with the decision or question behind it.
- **A requirement still carrying `open-questions`**: test it on its working assumption, tag the UAT `open-questions`, and say in the UAT's Notes which assumption it rests on, so it's revisited when the answer comes.

### Working out the scenarios

One UAT is one scenario with one outcome. For each story in scope:

1. **The main path.** One UAT for the story working as intended: the role does the thing and sees the benefit. Every story gets one, `no-build` stories included, since the client still needs to confirm standard behavior does what they expect.
2. **The exceptions the design defines.** One UAT per distinct behavior that a requirement point or a CI explicitly defines, beyond the main path: both sides of a layout rule's condition, a validation rule rejecting bad input, a threshold (just under and just over, when the boundary matters), an approval path versus no-approval path, a role that shouldn't see or do something.
3. **Don't invent edge cases.** If neither the requirement nor a CI defines how something behaves, don't write a test for it. If you think it's a real gap in the design, list it in the plan as a question instead.

Then, for **system behavior** (CIs linked to a requirement but no story: automatic assignments, scheduled rules, notifications), write one UAT per behavior, linked to the **requirement**, performed by the role who would observe the result.

As a rough check, a story usually gets one to three UATs. Much more than that usually means one scenario has been split into several, or tests are being written for behavior nothing defines.

### Show the plan

Present it in chat, by requirement, then story:

```
REQ-003: Referral partners are tracked on leads and deals
  US-001 Office Admin records who referred a lead
    UAT: Referrer fields appear and save when the lead source is Referral (main path)
    UAT: Referrer fields stay hidden for other lead sources (layout rule, CI-007)
  US-002 Sales Designer sees who referred a deal
    UAT: Referrer carries over when a referral lead is converted (main path)
REQ-004: Every lead is assigned and gets a first response within one business day
  System: unreached leads move to the shared queue (CI-015)
    UAT: An uncontacted lead moves to the shared queue after one business day
```

Then:

- tests tagged `open-questions`, and the assumption each rests on
- stories or scenarios skipped, and why (no CIs, `[TBD]` details)
- design gaps you noticed: behavior a requirement implies but nothing defines
- a count: N UATs across M stories and K requirements

Ask the user to steer: missing scenarios, scenarios that aren't worth a test, roles. Revise until they say to go ahead.

## Phase 2: Write

Create a branch: `git checkout -b uat-<YYYY-MM-DD>`.

One file per UAT in `uat/`, using `templates/uat.md`, next UAT number. See `examples/uats.md`.

- **File name:** `UAT-004-referrer-fields-hidden-for-other-sources.md`.
- **`title`:** the scenario and its outcome, plainly: "Referrer fields stay hidden for other lead sources."
- **`status: draft`**.
- **`module`:** where the test starts. Must have an ERD file.
- **`stories`:** the story it tests. **`requirements`:** the requirement, for system-behavior tests (and alongside the story if the test checks a specific requirement point). At least one of the two.
- **`performed_by`:** one role from `project.yaml`: the story's role, or for system behavior, the role who sees the result.
- **`tags: [open-questions]`** when the test rests on a working assumption.

**The body must be runnable by the client alone**, with no Hero person in the room:

- **`## Preconditions`:** exactly what must be true first. Who they're logged in as, which records must exist and with what values ("A lead named Test Referral, Lead Source Website"), any setting or time condition. Create test data in the steps if that's simpler than assuming it.
- **`## Steps`:** numbered, one action each, using the screen names, field labels and button names the client sees in Zoho, never API names. Use concrete test values ("Set Lead Source to Referral").
- **`## Expected result`:** what they should see, specifically enough that pass or fail is obvious: which fields appear, what values save, what message shows, where the record ends up.
- **`## Notes`** (only if needed): what the test covers and why, the CI or requirement point it checks (by ID, for Hero), the assumption it rests on for `open-questions` tests, or timing to allow for ("the scheduled rule runs hourly").

Write in plain language. Test what a person can see; never ask the client to check a setting in Setup, a log, or the API.

### Finish

1. Rebuild the index and build plan, then validate. Fix every error. In the index's `gaps`, `stories_without_uat` should list no story in scope that you could test, and `requirements_without_uat` should list no requirement with system behavior in scope.
2. Commit the UATs and refreshed `index.yaml` and `BUILD-PLAN.md` together on the branch: `UAT: N tests for M stories`. Push the branch.
3. Offer to open a pull request.

## Reruns

When UATs already exist for the stories or requirements in scope:

- **Story or CI changed:** update its UATs in place, keeping IDs. Read the changed CIs again; field names, values and conditions in the steps must match the current design.
- **Story or requirement declined:** set its UATs' `status: declined`.
- **New scenario** (a new exception defined, a new story): a new UAT with the next ID.
- **An open question answered:** update the steps if the answer differs from the assumption, and remove the `open-questions` tag.
- **Never delete** a UAT. Results tracked elsewhere are keyed by its ID.

The design skill's report lists UATs that test changed stories; start there on a rerun.

## Report back

- UATs written, by requirement and story, plus system-behavior tests
- tests tagged `open-questions`, and the assumptions behind them
- stories and scenarios skipped, and what would unblock each
- design gaps you noticed
- the branch, and the offer of a pull request

## What this skill never does

- Record test results, pass or fail, in the repo.
- Use API names or Setup screens in client-facing steps.
- Invent behavior for a test that neither a requirement nor a CI defines.
- Change stories, CIs or requirements. If a test reveals a design gap, it reports it.
- Mark UATs `approved` without the user's say-so.
- Write to a Zoho org.
