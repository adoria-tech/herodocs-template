# Example UATs

Reference examples for the UAT skill, from the Northshore sample. Each is one scenario a client can run alone: specific setup, numbered steps using the labels they see, and a result that makes pass or fail obvious.

---

## Main path for a story

`UAT-001-referrer-fields-appear-for-referrals.md`:

```markdown
---
id: UAT-001
title: Referrer fields appear and save when the lead source is Referral
status: draft
module: Leads
stories: [US-001]
performed_by: Office Admin
---

# Referrer fields appear and save when the lead source is Referral

## Preconditions

- You're logged in as an Office Admin.
- A contact named Pat Partner exists in Contacts.

## Steps

1. Go to Leads and click **Create Lead**.
2. Enter First Name **Test**, Last Name **Referral**, and Phone **705-555-0101**.
3. Set **Lead Source** to **Referral**.
4. In the fields that appear, set **Referrer Type** to **Pool Builder**.
5. In **Referral Contact**, search for and select **Pat Partner**.
6. Click **Save**.

## Expected result

Referrer Type and Referral Contact appear as soon as Lead Source is set to Referral. After
saving, the lead shows Referrer Type **Pool Builder** and Referral Contact **Pat Partner**.

## Notes

Covers the referrer fields (CI-001, CI-002) and the layout rule that shows them (CI-007).
```

---

## An exception the design defines

The layout rule (CI-007) has two sides, so the other side gets its own test.

`UAT-002-referrer-fields-hidden-for-other-sources.md`:

```markdown
---
id: UAT-002
title: Referrer fields stay hidden for other lead sources
status: draft
module: Leads
stories: [US-001]
performed_by: Office Admin
---

# Referrer fields stay hidden for other lead sources

## Preconditions

- You're logged in as an Office Admin.

## Steps

1. Go to Leads and click **Create Lead**.
2. Enter First Name **Test**, Last Name **Website**, and Phone **705-555-0102**.
3. Set **Lead Source** to **Website**.
4. Look for the Referrer Type and Referral Contact fields.
5. Change **Lead Source** to **Referral**, then back to **Website**.

## Expected result

Referrer Type and Referral Contact are not shown while Lead Source is Website. They
appear when it's changed to Referral, and disappear again when it's changed back.
```

---

## System behavior, linked to the requirement

No user triggers the escalation, so there's no story. The test links to the requirement and is run by the role who sees the result.

`UAT-005-unreached-lead-moves-to-shared-queue.md`:

```markdown
---
id: UAT-005
title: An uncontacted lead moves to the shared queue after one business day
status: draft
module: Leads
requirements: [REQ-004]
performed_by: Owner
tags: [open-questions]
---

# An uncontacted lead moves to the shared queue after one business day

## Preconditions

- You're logged in as the Owner.
- A lead named Test Unreached was created more than one business day ago, is assigned to
  a Sales Designer, and still has Lead Status **Not Contacted**.

## Steps

1. Go to Leads and open the **Unreached Leads** view.
2. Find **Test Unreached**.
3. Open the lead and check **Lead Owner**.
4. Check your notifications.

## Expected result

Test Unreached appears in the Unreached Leads view, its Lead Owner is the Shared Queue,
and you received a notification that it was escalated.

## Notes

Tests the escalation rule (CI-015). Rests on the working assumption for SRC-002-Q4 that
escalated leads go to a shared queue the Owner watches. The scheduled rule runs hourly,
so allow up to an hour after the lead passes one business day.
```

---

## A no-build story still gets a test

The client confirms standard behavior does what they expect.

`UAT-006-designer-sees-own-leads.md`:

```markdown
---
id: UAT-006
title: Sales Designer sees only their own leads in My Leads
status: draft
module: Leads
stories: [US-007]
performed_by: Sales Designer
---

# Sales Designer sees only their own leads in My Leads

## Preconditions

- You're logged in as a Sales Designer.
- At least one lead is assigned to you, and at least one is assigned to another Sales
  Designer.

## Steps

1. Go to Leads.
2. Choose the **My Leads** view.

## Expected result

The list shows the leads assigned to you, and none of the leads assigned to anyone else.
```
