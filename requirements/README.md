# Requirements

What the system must do, derived from source material. Clients approve Requirements.

- **ID prefix:** REQ
- **Example:** `REQ-001-lead-auto-assignment.md`
- **Links upstream to:** Sources

The body says what the business needs, never how it's built. A Requirement is also the parent of a feature: every CI, group, story and UAT built for it links back here.

Two fields place a requirement:

- **`area`** (required): the business capability it belongs to, from the `areas` list in `project.yaml`. Always known.
- **`module`** (optional): the Zoho module the feature lives on, once it's known. On a mature system or a library requirement it's set from the start; on a new build it's set once guidance or a decision settles it. A module with no ERD file yet is a warning, not an error.
