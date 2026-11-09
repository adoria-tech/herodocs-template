# Data Model (ERD)

One file per module, listing every field (standard and custom) with its status in the client's org.

- **ID prefix:** ENT
- **Example:** `ENT-001-leads.md`
- **Links upstream to:** nothing. The reason a field exists or changed comes through the CI that builds it (matched on module and `api_name`), which links to its Requirements and Design Decisions.

Status applies to the module and to each field:

- **pending:** we're going to create it
- **exists:** it's in the org
- **flagged:** we're going to remove it
- **removed:** it's gone, kept only for troubleshooting

For an existing org, ERD files should be generated from the org's field metadata rather than typed by hand. Relationships come from `lookup` fields (`lookup_to`), so there is no separate relationships list.

The set of ERD files defines the valid `module` values for every other record.
