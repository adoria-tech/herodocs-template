# User Stories

What a user must be able to do, from their point of view. One role, one piece of functionality.

- **ID prefix:** US
- **Example:** `US-001-rep-sees-claimable-leads.md`
- **Links upstream to:** Requirements
- **Linked from:** the CIs that deliver it (`stories` on the CI), and the UATs that test it

Format: "As a **role**, I want to **do something**, so that **benefit**." The role comes from `project.yaml`. Edge cases belong in UAT, not in the story.

Stories and CIs are designed together by the `herodocs-design` skill: for each requirement, who uses it and how, then what to build to deliver that (FD-040). The index lists stories no CI delivers under `stories_without_cis`. A story fully delivered by standard Zoho behavior, with nothing to build, is tagged `no-build` so it isn't flagged.

System behavior with no user action (an automatic assignment, a nightly sync) gets no story. Its CIs and UAT link straight to the requirement.
