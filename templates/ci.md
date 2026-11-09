---
id: CI-000
title: ""
status: draft        # draft | review | approved | declined
ci_type: field       # module | field | layout | layout_rule | validation_rule | workflow_rule | blueprint |
                     # function | widget | web_form | report | dashboard | email_template |
                     # mail_merge_template | inventory_template | integration | other
app: APP-CRM
module: ""           # must match an ERD file
api_name: ""         # for field CIs: the field's API name, matching its ERD entry
requirements: []
stories: []          # the user stories this CI helps deliver; leave empty for system behavior
decisions: []        # optional
depends_on: []       # other CIs that must exist first
group: ""            # optional, the CG-### this CI is built with
playbook: ""         # optional, the Hero playbook followed, e.g. quoting-transactional@3
deploy_status: not_started   # not_started | built | deployed
clickup_tasks: []    # optional; usually the task lives on the group
# origin: ""
# tags: []
---

# Title

What to build, with the specific settings (field type, values, rule criteria, etc.).
