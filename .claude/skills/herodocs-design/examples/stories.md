# Example User Stories

Reference examples for the design skill, from the Northshore sample. Stories describe what a person does, in business language a client can approve. Each is one role and one piece of functionality; edge cases go to UAT.

---

## A story delivered by built CIs

`US-001-admin-records-referrer.md`:

```markdown
---
id: US-001
title: Office Admin records who referred a lead
status: draft
role: Office Admin
module: Leads
requirements: [REQ-003]
---

As an **Office Admin**, I want to **record who referred a new lead, and what kind of
referrer they are**, so that **Mark can see which partners send us work and thank them**.

## Notes

The referrer details only appear when the lead's source is Referral, so they don't
clutter every other lead.
```

The CIs that deliver it link back with `stories: [US-001]`: the Referrer Type and Referral Contact fields, and the layout rule that shows them. In `BUILD-PLAN.md`, each of those CIs reads `(delivers US-001)`.

---

## A story for a different role on the same requirement

`US-002-designer-sees-referrer.md`:

```markdown
---
id: US-002
title: Sales Designer sees who referred a deal
status: draft
role: Sales Designer
module: Deals
requirements: [REQ-003]
---

As a **Sales Designer**, I want to **see who referred a deal when I open it**, so that
**I can mention the referrer when I first talk to the homeowner**.

## Notes

The referrer carries over from the lead when it's converted, so nobody re-enters it.
```

Delivered by the referrer fields on Deals, the Deals layout rule, and the lead conversion mapping.

---

## A no-build story

Standard Zoho already does this, but the client should still see it as part of the experience.

`US-007-designer-sees-my-leads.md`:

```markdown
---
id: US-007
title: Sales Designer sees the leads assigned to them
status: draft
role: Sales Designer
module: Leads
requirements: [REQ-004]
tags: [no-build]
---

As a **Sales Designer**, I want to **see the leads assigned to me in one list**, so that
**I know who to contact today**.

## Notes

Delivered by Zoho CRM's standard My Leads view. Nothing to build.
```

---

## System behavior gets no story

"Unreached leads move to the shared queue after one business day" has no user action, so there's no story for it. Its workflow rule CI links only to the requirement, and its UAT tests the requirement directly.
