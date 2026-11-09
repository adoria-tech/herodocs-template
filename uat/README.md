# User Acceptance Tests

The tests the client runs to accept the build. Each UAT is one scenario a person can run alone in Zoho: specific preconditions, numbered steps, and a result they can see.

- **ID prefix:** UAT
- **Example:** `UAT-001-referrer-fields-appear-for-referrals.md`
- **Links upstream to:** User Stories and/or Requirements (at least one)

Rules:

- One scenario, one outcome. Each story gets a main-path test, plus one test per distinct exception a requirement or CI defines (both sides of a layout rule, a validation rejecting bad input, a threshold). Don't test behavior nothing defines.
- System behavior with no user action (an automatic assignment, a scheduled rule) is tested against its requirement, by the role who sees the result.
- Steps use the screen names, field labels and buttons the client sees, never API names or Setup screens.
- `performed_by` is one role from `project.yaml`.
- A test resting on a working assumption is tagged `open-questions`, with the assumption in its Notes.

UAT files define the tests only. Results (Hero's run and the client's run) are tracked outside the repo, keyed by UAT ID (FD-016). UATs are never deleted, so those results stay linked; a test that no longer applies is `declined`.

The `herodocs-uat` skill writes them, after the design skill has written the stories and CIs (FD-041).
