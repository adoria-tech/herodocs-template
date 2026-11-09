# Example: requirements

Four requirements from the Northshore sample, sized and written the way this skill should write them (see "Sizing requirements" in SKILL.md). Note:

- website capture and social ad capture are separate requirements, because one is a form and the other an integration
- the pipeline report is one requirement holding everything about that report, including its filters, with a minor nice-to-have marked `(optional)`
- the last one has no module yet and an open question carried as a labeled working assumption

---

```markdown
---
id: REQ-001
title: Website quote requests are captured with their source and project details
status: draft
priority: must
area: Lead intake
module: Leads
sources: [SRC-001, SRC-002, SRC-004]
---

# Website quote requests are captured with their source and project details

Every quote request from the website lands in one place as a new lead, with its
source recorded as the website without anyone typing it in. The lead keeps everything
the homeowner provided:

- name, email, phone and address
- the type of project (deck, pergola, patio or a combination)
- approximate size, budget range and timeline
- how they heard about Northshore
- any photos of the space

The Sales Designer making first contact can see all of this without asking the
homeowner to repeat it.

## Notes

Mark: "I have no idea if the pool guys have sent us two jobs or twenty." Budget and
timeline are often blank or vague, so they can't be required on the form.
```

```markdown
---
id: REQ-002
title: Social ad leads are captured with their source and campaign
status: draft
priority: must
area: Lead intake
module: Leads
sources: [SRC-001, SRC-004]
---

# Social ad leads are captured with their source and campaign

Leads from Northshore's Facebook and Instagram lead ads arrive in the same place as
every other lead, without anyone re-entering them. Each keeps the homeowner's details
from the ad form, its source as social ads, and the name of the campaign it came from,
so Mark can compare ad spend to results campaign by campaign.

## Notes

Capture method is DD-002 (native lead ads integration recommended).
```

```markdown
---
id: REQ-015
title: Pipeline report for the Owner
status: draft
priority: must
area: Reporting
module: Deals
sources: [SRC-001, SRC-004]
---

# Pipeline report for the Owner

Mark can see every open opportunity at a glance, to forecast the season and spot
stalled deals:

- open opportunities grouped by stage, with the count and total value in each
- weighted value by stage, using each stage's probability
- filterable by lead source and date range
- filterable by Sales Designer (optional)

## Notes

Stage probabilities come from REQ-007. Mark reviews this weekly on Monday mornings
(SRC-001).
```

```markdown
---
id: REQ-004
title: Every lead is assigned and gets a first personal response within one business day
status: draft
priority: must
area: Lead intake
sources: [SRC-001, SRC-002, SRC-004]
tags: [open-questions]
---

# Every lead is assigned and gets a first personal response within one business day

Every new lead has a Sales Designer assigned from the moment it arrives, and gets a
first personal response within one business day. When a lead hasn't been reached by
then, a named person is responsible for following up, so no lead sits untouched in
peak season.

## Open questions

- **SRC-002-Q4:** Who owns follow-up when a lead isn't reached on the first day?
  Working assumption: the assigned Sales Designer, since they own the lead from
  assignment (SRC-001). Confirm with Mark.
- Depends on DD-001 (Leads module or Contacts with a contact type) for where this lives.

## Notes

Mark: "Leads slip through the cracks in peak season." The one-business-day target is
stated in SRC-001 and repeated by Mark on the kickoff call.
```
