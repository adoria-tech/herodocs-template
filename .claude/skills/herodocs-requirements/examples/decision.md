# Example: Design Decision

A decision written by this skill, where guidance overrides a client document's suggestion. It's `decided` because a `guidance` source settles it, so `decided_on` is that source's date. A choice the user confirmed while steering the outline would also be `decided`, dated from the approval. A choice with neither would be `proposed`, with the same structure.

---

```markdown
---
id: DD-002
title: Build quoting in CRM Quotes, not Creator
status: decided
decided_on: 2026-10-24
requirements: [REQ-011, REQ-012, REQ-013]
---

# Build quoting in CRM Quotes, not Creator

## Context

Northshore needs itemized, versioned quotes with e-signature and a deposit line
(REQ-011 to REQ-013). The client's scenario document suggests building quoting in
Zoho Creator (SRC-001). Where quotes live affects pipeline reporting and how much
syncing the system needs.

## Options Considered

**Zoho Creator** (suggested in SRC-001). Fully custom layout and logic. But quotes
would live apart from Deals, so pipeline value and conversion reports would need a
sync between two apps, for a team of five.

**Zoho CRM Quotes.** Native line items, tied directly to the Deal, with standard
quote templates. Versioning has to be handled as separate Quotes on the same Deal.

## Decision

CRM Quotes, as directed in Hero's guidance (SRC-003, 2026-10-24): keeping quotes on
the Deal keeps Mark's pipeline and funnel reports simple and avoids a sync. Revisions
are separate Quotes linked to the same Deal. Zoho Sign handles e-signature, since
Northshore is on Zoho One.

## Consequences

No Creator app for phase 1. Quote layout is limited to what CRM quote templates
support. A custom versioning module is ruled out unless revision volume grows.
```
