# Schemas

JSON Schema files defining the required fields, allowed values, and formats for each record type's frontmatter, plus `project.yaml`.

These are used by `scripts/validate.py`, which also checks cross-references (links point to real records, modules have ERD files, roles and apps exist in `project.yaml`, file names match IDs).

To add a field or allowed value, edit the matching schema here and update the template in `templates/`. Make framework changes in `herodocs-template`, not in a client repo.
