# CI Groups

A set of CIs built in the same place, in one sitting, usually with one ClickUp task. Examples: all the new and changed fields on Leads and Deals for referral tracking, or a standard set of social handle fields.

- **ID prefix:** CG
- **Example:** `CG-001-referral-tracking-fields.md`
- **Links upstream to:** nothing. CIs point to their group with `group: CG-###`.

Rules:

- A group is defined by **where the work happens and when**, not by CI type. All the field work in a module's field and layout editor (new fields, property changes, picklist value changes, removals) belongs together. A layout rule, workflow or report, built in a different screen, is a separate CI outside the group.
- Grouping is optional. A one-off CI doesn't need a group.
- A CI belongs to at most one group.
- Groups can span modules.
- Groups have no status of their own; progress comes from their CIs.

`BUILD-PLAN.md`, generated at the repo root, shows every group with its fields, CIs in build order, and notes.

A group is not how a feature is tied together. Everything built for a feature is found through its Requirement: every CI and group linked to it, ordered by `depends_on`.

Groups are the natural unit of reuse: a well-described group with its CIs is most of a recipe.
