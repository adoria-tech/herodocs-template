# Example CIs

Reference examples for the design skill, from the Northshore sample. They show the expected structure, the level of detail in a build spec, and how stories, CIs, groups and the ERD fit together. Read them before writing your first CI in a session.

File names carry the type code after the ID: `CI-010-FLD-project-type-on-leads.md`, `CI-007-LRL-referrer-fields-rule.md`, `CI-009-WEB-request-a-quote-form.md`, `CI-020-RPT-pipeline-report.md`.

---

## A CI Group of field work: new fields and a picklist change

Creating fields and changing an existing picklist's values happen in the same place (the Leads field and layout editor) in the same sitting, so they share a group. The group carries one ClickUp task later.

```markdown
---
id: CG-002
title: Lead intake fields
clickup_tasks: []
---

# Lead intake fields

Field work on Leads for lead capture: the new Project Type and Ad Campaign fields, and
replacing Lead Source's default values. All done in the Leads field editor in one sitting.
```

`CI-010-FLD-project-type-on-leads.md`, a new field (its ERD entry is `pending`) delivering a story:

```markdown
---
id: CI-010
title: Project Type field on Leads
status: draft
ci_type: field
app: APP-CRM
module: Leads
api_name: Project_Type
requirements: [REQ-001]
stories: [US-004]
group: CG-002
deploy_status: not_started
clickup_tasks: []
---

# Project Type field on Leads

Create a picklist field on Leads. Values as defined in ENT-001, `Project_Type`.
Not mandatory on the layout: the web form (CI-009) makes it required on the form
instead, so staff can still create a lead before the project type is known.

Place it in the Lead Information section, after Lead Source.
```

`CI-006-FLD-lead-source-values.md`, a change to an existing field (its ERD entry is `exists`, with target values):

```markdown
---
id: CI-006
title: Lead Source values on Leads
status: draft
ci_type: field
app: APP-CRM
module: Leads
api_name: Lead_Source
requirements: [REQ-001, REQ-002]
stories: [US-004]
group: CG-002
deploy_status: not_started
clickup_tasks: []
---

# Lead Source values on Leads

Replace Zoho's default Lead Source values with the values defined in ENT-001,
`Lead_Source`. Remove the defaults rather than leaving them, so reports only ever show
the real sources.

## Notes

The layout rule (CI-007) and web form (CI-009) both depend on the Referral and Website
values existing.
```

And the matching ERD entries in `erd/ENT-001-leads.md`:

```yaml
  - api_name: Lead_Source
    label: Lead Source
    type: picklist
    standard: true
    status: exists
    values: [Website, Social Ads, Referral]

  - api_name: Project_Type
    label: Project Type
    type: picklist
    standard: false
    status: pending
    values: [Deck, Pergola, Patio, Combo]
```

In `BUILD-PLAN.md`, the group shows as:

```markdown
### CG-002: Lead intake fields

**Fields**

- Lead Source (`Leads.Lead_Source`) [picklist]: modify
- Project Type (`Leads.Project_Type`) [picklist]: create
```

---

## A layout rule that depends on grouped fields

Built in a different screen from the fields, so it's its own CI outside the group.

`CI-007-LRL-referrer-fields-rule.md`:

```markdown
---
id: CI-007
title: Show referrer fields on Leads when source is Referral
status: draft
ci_type: layout_rule
app: APP-CRM
module: Leads
requirements: [REQ-003]
stories: [US-001]
decisions: [DD-001]
depends_on: [CI-001, CI-002, CI-006]
deploy_status: not_started
clickup_tasks: []
---

# Show referrer fields on Leads when source is Referral

Layout rule on the Leads standard layout.

- **Condition:** Lead Source is Referral
- **When true:** show Referrer Type and Referral Contact
- **Otherwise:** both fields hidden
```

---

## System behavior: no story

No user triggers this, so it links only to its requirement.

`CI-015-WFR-unreached-lead-escalation.md`:

```markdown
---
id: CI-015
title: Unreached lead escalation
status: draft
ci_type: workflow_rule
app: APP-CRM
module: Leads
requirements: [REQ-004]
depends_on: [CI-013]
deploy_status: not_started
clickup_tasks: []
---

# Unreached lead escalation

Scheduled workflow rule on Leads.

- **Criteria:** Lead Status is Not Contacted, and Created Time is more than one business
  day ago
- **Action:** set Lead Owner to the Shared Queue user, and notify the Owner role
```

---

## A web form

`CI-009-WEB-request-a-quote-form.md`:

```markdown
---
id: CI-009
title: Request a Quote web form
status: draft
ci_type: web_form
app: APP-CRM
module: Leads
requirements: [REQ-001]
stories: [US-004]
depends_on: [CI-006, CI-010, CI-012]
deploy_status: not_started
clickup_tasks: []
---

# Request a Quote web form

Zoho CRM web form replacing the Request a Quote form on northshoreoutdoor.ca. Every
submission creates a Lead with the source set automatically.

## Field mapping

| Form field | Lead field | Required on form |
|---|---|---|
| First name | `First_Name` | Yes |
| Last name | `Last_Name` | Yes |
| Email | `Email` | Yes |
| Phone | `Phone` | Yes |
| Project type | `Project_Type` | Yes |
| Size, budget, timeline, how they heard | `Description` | No |
| Photo upload | Lead attachment | No |

## Hidden fields

| Lead field | Value |
|---|---|
| `Lead_Source` | Website |
| `Lead_Status` | Not Contacted |

## Notes

Company must be made optional first (CI-012, a `field` change to the existing Company
field), or every submission fails.
```

---

## A report CI covering variants

Three views of the same report that differ only by grouping: one CI (FD-031). A different report, like the conversion funnel, gets its own CI.

`CI-020-RPT-pipeline-report.md`:

```markdown
---
id: CI-020
title: Pipeline report
status: draft
ci_type: report
app: APP-CRM
module: Deals
requirements: [REQ-018]
stories: [US-015]
depends_on: [CI-016]
deploy_status: not_started
clickup_tasks: []
---

# Pipeline report

Summary report on Deals, open deals only (Stage is not Closed Won or Closed Lost).

**Columns:** Deal Name, Contact, Sales Designer, Stage, Amount, Probability, Expected
Revenue, Closing Date, Lead Source.

**Summaries:** count, sum of Amount and sum of Expected Revenue, per group.

## Variants

| Variant | Grouped by | Filter |
|---|---|---|
| Pipeline by stage | Stage | none |
| Pipeline by source | Lead Source | none |
| Pipeline by designer | Sales Designer | none |

All three get a Closing Date range filter at run time.
```

---

## An inventory template

`CI-021-ITPL-quote-template.md`:

```markdown
---
id: CI-021
title: Quote template
status: draft
ci_type: inventory_template
app: APP-CRM
module: Quotes
requirements: [REQ-011]
stories: [US-010]
decisions: [DD-002]
deploy_status: not_started
clickup_tasks: []
---

# Quote template

Inventory template for Quotes, set as the default. Northshore logo and address in the
header; homeowner name and site address; line items with product, description,
quantity, unit price and line total; discount as its own line; design fee credit; HST;
total; 30% deposit amount; terms and 30-day validity in the footer.
```
