# Example: solution outline

What Phase 2 shows the user, in chat, for Northshore. After approval it's saved as a `guidance` source and its areas go into `project.yaml`.

---

# Solution outline: Northshore Outdoor Living

## Capability areas

1. **Lead intake**: capturing every lead from the website, social ads and referrals, with its source.
2. **Referral tracking**: who referred each lead, and partner thank-yous.
3. **Lead nurture**: the three-email sequence and its stop conditions.
4. **Sales pipeline**: from qualified lead through site visit, quote and close.
5. **Quoting**: itemized, versioned quotes with e-signature and deposit.
6. **Handoff to operations**: telling Dan when a job is sold.
7. **Reporting**: pipeline, lead sources and conversion funnel for Mark.

## Process

1. A lead arrives from the website, an ad, or a referral, and lands in one place with its source.
2. The assigned Sales Designer gets it; the nurture sequence starts (referrals get a call first).
3. Priya or the designer qualifies it within one business day; qualified leads become opportunities.
4. Site visit booked, then completed, with a reminder email 24 hours before.
5. Itemized quote sent within five business days; revisions become new versions.
6. Homeowner signs and pays the 30% deposit; Priya confirms it cleared; deal is won.
7. Dan gets the sold-job notice with everything he needs to order materials.

## Approach by area

| Area | Recommended | Alternatives | Basis |
|---|---|---|---|
| Lead intake | Zoho CRM, Leads module | Contacts with a contact type | SRC-001, SRC-002. Leads vs Contacts is still open; see Decisions needed. |
| Referral tracking | Zoho CRM | | SRC-001, SRC-002 |
| Lead nurture | Zoho CRM cadences | Zoho Campaigns | Cadences keep emails coming from the assigned designer, which SRC-001 asks for. |
| Sales pipeline | Zoho CRM, Deals | | SRC-001 |
| Quoting | Zoho CRM, Quotes, with Zoho Sign | Zoho Creator (suggested in SRC-001) | **Decided by guidance SRC-003**: quotes stay tied to deals for reporting; no sync for a team of five. |
| Handoff to operations | Zoho CRM email notification | | SRC-001 |
| Reporting | Zoho CRM reports and dashboards | Zoho Analytics | The funnel needs stage history; CRM may be enough. See Decisions needed. |

## Decisions needed

1. Leads module, or Contacts with a contact type, for incoming leads?
2. Can the conversion funnel be built in CRM reports, or does it need Zoho Analytics?

## Scope

- **In:** everything above.
- **Deferred to a later phase:** crew scheduling, materials ordering (SRC-003).
- **Out:** accounting, payments processing beyond recording the deposit.

## Conflicts between sources

- **Deposit before won (SRC-001 vs SRC-002):** the scenario requires the deposit to clear before a deal is won; Mark hinted repeat clients might be an exception. Suggest keeping the rule and asking Mark (SRC-001-Q8).
