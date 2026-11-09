---
id: ENT-000
title: ""            # module display name
app: APP-CRM
module: ""           # Zoho API name of the module
module_kind: standard   # standard | custom
status: exists       # pending | exists | flagged | removed
# origin: ""
# tags: []

fields:
  - api_name: ""
    label: ""
    type: text       # text | textarea | number | decimal | currency | date | datetime |
                     # email | phone | url | picklist | multiselect | checkbox | lookup |
                     # user | formula | autonumber | subform | other
    standard: true
    required: false  # optional
    status: exists   # pending | exists | flagged | removed
    # values: []     # required for picklist and multiselect
    # lookup_to: ""  # required for lookup, the target module
    # notes: ""
---

# Title

What this module is for.

## Relationships

```mermaid
erDiagram
    Accounts ||--o{ Leads : has
```
