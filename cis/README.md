# Configuration Items

The things we configure, customize, or build: custom modules and fields, reports, workflow rules, widgets, templates.

- **ID prefix:** CI
- **File name:** ID, then the type code, then a short slug: `CI-010-FLD-project-type-on-leads.md`
- **Links upstream to:** Requirements, Design Decisions, App, other CIs (`depends_on`), a CI Group (`group`, optional), ClickUp task IDs

## Types and codes

| `ci_type` | Code | Covers |
|---|---|---|
| module | MOD | Creating a custom module |
| field | FLD | Any change to a field: creating it, changing its properties (label, mandatory, picklist values), or removing it. The ERD says which: `pending` is create, `exists` is modify, `flagged` is remove. |
| layout | LAY | Layout-level work: sections, field arrangement, which profiles see which layout |
| layout_rule | LRL | Layout rules |
| validation_rule | VRL | Validation rules |
| workflow_rule | WFR | Workflow rules |
| blueprint | BLU | Blueprints |
| function | FNC | Custom functions |
| widget | WDG | Widgets |
| web_form | WEB | Web forms |
| report | RPT | Reports, including near-identical variants |
| dashboard | DSH | Dashboards |
| email_template | ETPL | Email templates |
| mail_merge_template | MTPL | Mail merge templates |
| inventory_template | ITPL | Inventory templates (quotes, sales orders, invoices) |
| integration | INT | Integrations |
| other | OTH | Rarer settings: conversion mapping, duplicate check rules |

The validator warns if a file name's code doesn't match its `ci_type`.

One CI per field or build item; near-identical variants share one CI (FD-031). Use a CI Group to tackle work done in the same place in one sitting.

Level of effort lives on the ClickUp task, never on the CI.
