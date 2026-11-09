#!/usr/bin/env python3
"""
Validate every HeroDocs record in this repo.

Checks each record's frontmatter against its JSON Schema, then checks
cross-references: links point to real records of the right type, modules
have ERD files, roles, areas and apps exist in project.yaml, and file names match IDs.
Also warns if index.yaml or BUILD-PLAN.md is missing or out of date.

Run from the repo root:  python3 scripts/validate.py
In VS Code:              Cmd+Shift+B (rebuilds the index first)
Exit code is 1 if there are errors, 0 otherwise (warnings don't fail).
"""
import datetime
import json
import sys
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError:
    print("Missing libraries. Run:  pip3 install -r requirements.txt")
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent

# folder -> (schema name, ID prefix)
TYPES = {
    "sources": ("source", "SRC"),
    "requirements": ("requirement", "REQ"),
    "decisions": ("decision", "DD"),
    "erd": ("erd", "ENT"),
    "cis": ("ci", "CI"),
    "ci-groups": ("ci_group", "CG"),
    "stories": ("story", "US"),
    "uat": ("uat", "UAT"),
    "training": ("training", "TRN"),
    "docs": ("documentation", "DOC"),
}

# ci_type -> short code expected in CI file names (CI-012-FLD-project-type.md)
CI_CODES = {
    "module": "MOD", "field": "FLD", "layout": "LAY", "layout_rule": "LRL",
    "validation_rule": "VRL", "workflow_rule": "WFR", "blueprint": "BLU",
    "function": "FNC", "widget": "WDG", "web_form": "WEB", "report": "RPT",
    "dashboard": "DSH", "email_template": "ETPL", "mail_merge_template": "MTPL",
    "inventory_template": "ITPL", "integration": "INT", "other": "OTH",
}

# link field -> ID prefix it must point to
LINKS = {
    "sources": "SRC", "requirements": "REQ", "decisions": "DD",
    "depends_on": "CI", "stories": "US", "training": "TRN", "supersedes": "DD",
    "group": "CG",
}

# Text that only appears in the files under templates/. Finding it in a record
# means a template was copied but not filled in.
TEMPLATE_TEXT = [
    "Plain-language description of what the system must do.",
    "Context from the source, if useful.",
    "Short summary of the source.",
    "The problem or question we needed to answer.",
    "Each option with its trade-offs.",
    "What we chose and why.",
    "What this commits us to or rules out.",
    "What this module is for.",
    "Accounts ||--o{ Leads : has",
    "What to build, with the specific settings",
    "What this group covers and why",
    "As a **role**, I want to **do something**",
    "Optional detail that doesn't fit the sentence.",
    "Data or setup required before the test",
    "First step",
    "Second step",
    "What should happen.",
    "What this training covers.",
    "The documentation content.",
]

problems = []


def report(path, severity, message, line=1):
    rel = path.relative_to(ROOT) if isinstance(path, Path) else path
    problems.append((str(rel), line, severity, message))


def normalize(value):
    """Make YAML values schema-friendly: dates become strings, empty values are dropped."""
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in value.items() if v is not None and v != ""}
    if isinstance(value, list):
        return [normalize(v) for v in value]
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    return value


def read_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if "\t" in text.split("\n---", 1)[0]:
        report(path, "error", "Tab character in frontmatter. YAML needs spaces.")
        return None
    if not text.startswith("---\n"):
        report(path, "error", "File must start with a --- line (frontmatter).")
        return None
    end = text.find("\n---", 4)
    if end == -1:
        report(path, "error", "Frontmatter has no closing --- line.")
        return None
    try:
        data = yaml.safe_load(text[4:end])
    except yaml.YAMLError as e:
        line = getattr(getattr(e, "problem_mark", None), "line", 0) + 2
        report(path, "error", f"YAML syntax error: {getattr(e, 'problem', e)}", line)
        return None
    if not isinstance(data, dict):
        report(path, "error", "Frontmatter is empty or not a set of key: value pairs.")
        return None
    body = text[end + 4:]
    has_content = any(
        line.strip() and not line.lstrip().startswith("#")
        for line in body.splitlines()
    )
    if not has_content:
        report(path, "warning", "Body has no description, only headings or nothing at all.")
    leftovers = [t for t in TEMPLATE_TEXT if t in body]
    if any(line.strip() == "# Title" for line in body.splitlines()):
        leftovers.insert(0, "# Title")
    if leftovers:
        report(path, "warning", f"Leftover template text: '{leftovers[0]}'" + (f" (+{len(leftovers) - 1} more)" if len(leftovers) > 1 else ""))
    return normalize(data)


def load_schema(name):
    with open(ROOT / "schemas" / f"{name}.schema.json", encoding="utf-8") as f:
        return Draft202012Validator(json.load(f))


def schema_errors(validator, data, path):
    for err in sorted(validator.iter_errors(data), key=lambda e: [str(p) for p in e.absolute_path]):
        where = ".".join(str(p) for p in err.absolute_path)
        message = err.message
        if err.validator == "not" and err.instance == "Everyone":
            message = "Everyone is built in, don't list it in roles"
        elif err.validator == "anyOf" and not where:
            message = "needs at least one link in stories or requirements"
        elif err.validator == "pattern":
            # Link fields get a clearer message from the cross-reference check
            if err.absolute_path and err.absolute_path[0] in LINKS:
                continue
            hint = err.schema.get("description")
            message = f"'{err.instance}' isn't in the right format" + (f" ({hint})" if hint else "")
        report(path, "error", f"{where + ': ' if where else ''}{message}")


def main():
    # project.yaml
    project_path = ROOT / "project.yaml"
    project = {}
    if not project_path.exists():
        report("project.yaml", "error", "project.yaml is missing.")
    else:
        try:
            project = normalize(yaml.safe_load(project_path.read_text(encoding="utf-8")) or {})
            schema_errors(load_schema("project"), project, project_path)
        except yaml.YAMLError as e:
            report(project_path, "error", f"YAML syntax error: {e}")
    apps = {a.get("id") for a in project.get("apps", []) if isinstance(a, dict)}
    roles = set(project.get("roles", []))
    areas = set(project.get("areas", []) or [])

    # Load every record
    records = {}  # id -> (path, data, prefix)
    for folder, (schema_name, prefix) in TYPES.items():
        folder_path = ROOT / folder
        if not folder_path.is_dir():
            continue
        validator = load_schema(schema_name)
        for path in sorted(folder_path.glob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            data = read_frontmatter(path)
            if data is None:
                continue
            schema_errors(validator, data, path)
            rid = data.get("id")
            if not isinstance(rid, str):
                continue
            if not rid.startswith(prefix + "-"):
                report(path, "error", f"ID {rid} doesn't belong in {folder}/ (expected {prefix}-###).")
            if not (path.stem == rid or path.stem.startswith(rid + "-")):
                report(path, "error", f"File name should start with its ID: {rid}-short-name.md")
            elif prefix == "CI" and isinstance(data.get("ci_type"), str):
                expected = CI_CODES.get(data["ci_type"])
                actual = path.stem[len(rid) + 1:].split("-", 1)[0]
                if expected and actual != expected:
                    report(path, "warning", f"File name should carry the type code: {rid}-{expected}-short-name.md (ci_type is {data['ci_type']}).")
            if rid in records:
                report(path, "error", f"Duplicate ID {rid}, also used in {records[rid][0].relative_to(ROOT)}")
                continue
            records[rid] = (path, data, prefix)

    modules = {d.get("module") for (_, d, p) in records.values() if p == "ENT"}
    ci_targets = {(d.get("module"), d.get("api_name")) for (_, d, p) in records.values() if p == "CI"}

    # Cross-reference checks
    for rid, (path, data, prefix) in records.items():
        for field, target in LINKS.items():
            value = data.get(field)
            if value is None:
                continue
            for ref in value if isinstance(value, list) else [value]:
                if not isinstance(ref, str):
                    continue
                if ref == rid:
                    report(path, "error", f"{field}: a record can't link to itself.")
                elif ref not in records:
                    report(path, "error", f"{field}: {ref} doesn't exist.")
                elif records[ref][2] != target:
                    report(path, "error", f"{field}: {ref} is not a {target} record.")

        if prefix == "CI":
            if not data.get("requirements") and not data.get("decisions"):
                report(path, "warning", "No requirements or decisions linked, so nothing explains why this CI exists.")
            if data.get("deploy_status") in ("built", "deployed"):
                for d in data.get("decisions", []) or []:
                    if d in records and records[d][1].get("status") == "proposed":
                        report(path, "warning", f"Marked {data['deploy_status']} but {d} is still proposed.")

        module = data.get("module")
        if prefix != "ENT" and isinstance(module, str) and module not in modules:
            if prefix == "REQ":
                # Requirements are often written before the data model exists.
                report(path, "warning", f"module: no ERD file for '{module}' yet.")
            else:
                report(path, "error", f"module: no ERD file for '{module}'. Add erd/ENT-###-{module.lower()}.md or fix the name.")

        area = data.get("area")
        if prefix == "REQ" and isinstance(area, str) and area not in areas:
            report(path, "error", f"area: '{area}' is not in the areas list in project.yaml.")

        for field in ("app",):
            if isinstance(data.get(field), str) and data[field] not in apps:
                report(path, "error", f"app: {data[field]} is not listed in project.yaml.")
        for app in data.get("apps", []) or []:
            if isinstance(app, str) and app not in apps:
                report(path, "error", f"apps: {app} is not listed in project.yaml.")

        for field in ("role", "performed_by"):
            if isinstance(data.get(field), str) and data[field] not in roles:
                report(path, "error", f"{field}: '{data[field]}' is not in the roles list in project.yaml.")

        audience = data.get("audience")
        if isinstance(audience, list):
            if "Everyone" in audience and len(audience) > 1:
                report(path, "error", "audience: use [Everyone] on its own, not mixed with roles.")
            for role in audience:
                if role != "Everyone" and role not in roles:
                    report(path, "error", f"audience: '{role}' is not in the roles list in project.yaml.")

        if prefix == "ENT":
            seen = set()
            for f in data.get("fields", []) or []:
                if not isinstance(f, dict):
                    continue
                name = f.get("api_name")
                if name in seen:
                    report(path, "error", f"fields: duplicate api_name '{name}'.")
                seen.add(name)
                if f.get("status") in ("pending", "flagged") and (data.get("module"), name) not in ci_targets:
                    report(path, "warning", f"fields.{name}: marked {f.get('status')} but no CI builds it (no CI with module {data.get('module')} and api_name {name}).")
                target = f.get("lookup_to")
                if isinstance(target, str) and target not in modules:
                    report(path, "warning", f"fields.{name}: lookup_to '{target}' has no ERD file yet.")

    # Index and build plan freshness
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from build_index import build, build_plan
        for name, fresh in (("index.yaml", build()), ("BUILD-PLAN.md", build_plan())):
            target = ROOT / name
            if not target.exists():
                if records:
                    report(name, "warning", f"{name} is missing. Rebuild with Cmd+Shift+B or: python3 scripts/build_index.py")
            elif target.read_text(encoding="utf-8") != fresh:
                report(name, "warning", f"{name} is out of date. Rebuild with Cmd+Shift+B or: python3 scripts/build_index.py")
    except Exception as e:  # never let the index check break validation
        report("index.yaml", "warning", f"Couldn't check index.yaml and BUILD-PLAN.md: {e}")

    # Output
    for rel, line, severity, message in sorted(problems):
        print(f"{rel}:{line}: {severity}: {message}")
    errors = sum(1 for p in problems if p[2] == "error")
    warnings = len(problems) - errors
    print(f"\n{len(records)} records checked: {errors} error(s), {warnings} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
