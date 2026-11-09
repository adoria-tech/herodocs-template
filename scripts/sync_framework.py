#!/usr/bin/env python3
"""
Sync this repo's framework files from herocrm/herodocs-template.

The template's framework.yaml lists every framework path. This script pulls those
paths from the template's latest version, removes framework files the template no
longer has, records the template version in .herodocs-version, rebuilds the index
and build plan, validates, and commits. Project files (records, project.yaml,
index.yaml, BUILD-PLAN.md) are never touched.

Run from the repo root, on main:   python3 scripts/sync_framework.py
Preview only:                      python3 scripts/sync_framework.py --dry-run
Also push the commit:              python3 scripts/sync_framework.py --push

It reads the TEMPLATE's manifest, not this repo's, so new framework paths added to
the template come across on the next sync. The script syncs scripts/ too, so it
updates itself. Change it only in the template.
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REMOTE = "template"
DEFAULT_URL = "https://github.com/herocrm/herodocs-template.git"
BRANCH = "main"
VERSION_FILE = ".herodocs-version"


def git(*args, check=True, capture=True):
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    if check and result.returncode != 0:
        print(f"git {' '.join(args)} failed:\n{(result.stderr or '').strip()}")
        sys.exit(1)
    return (result.stdout or "").strip()


def parse_manifest(text):
    """framework.yaml is a simple YAML list under `paths:`. Parsed without PyYAML so
    the sync can run even before requirements are installed."""
    paths, in_paths = [], False
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.strip() == "paths:":
            in_paths = True
            continue
        if in_paths:
            stripped = line.strip()
            if stripped.startswith("- "):
                paths.append(stripped[2:].strip().strip("'\""))
            elif not line.startswith(" "):
                in_paths = False
    return paths


def matches(path, manifest):
    return any(path.startswith(p) if p.endswith("/") else path == p for p in manifest)


def main():
    parser = argparse.ArgumentParser(description="Sync framework files from herodocs-template.")
    parser.add_argument("--dry-run", action="store_true", help="show what would change, change nothing")
    parser.add_argument("--push", action="store_true", help="push the sync commit")
    parser.add_argument("--allow-dirty", action="store_true", help="run even with uncommitted changes")
    parser.add_argument("--url", default=DEFAULT_URL, help="template repo URL")
    parser.add_argument("--allow-branch", action="store_true", help="run on a branch other than main")
    args = parser.parse_args()

    branch = git("branch", "--show-current")
    if branch != BRANCH and not args.allow_branch:
        print(f"You're on '{branch or 'a detached HEAD'}'. Framework syncs commit to {BRANCH}: "
              f"switch to {BRANCH} (git checkout {BRANCH}), sync, then merge {BRANCH} into your branch if needed.")
        return 1

    if not args.allow_dirty and git("status", "--porcelain", "--untracked-files=no"):
        print("This repo has uncommitted changes. Commit or discard them first, then sync.")
        return 1

    # 1. Link the template (once) and fetch its latest version.
    if subprocess.run(["git", "remote", "get-url", REMOTE], cwd=ROOT,
                      capture_output=True).returncode != 0:
        git("remote", "add", REMOTE, args.url)
        print(f"Linked the template as git remote '{REMOTE}'.")
    print("Fetching the template...")
    git("fetch", REMOTE, BRANCH)
    ref = f"{REMOTE}/{BRANCH}"
    sha = git("rev-parse", ref)
    subject = git("log", "-1", "--format=%s", ref)

    # 2. Read the template's manifest.
    manifest_text = git("show", f"{ref}:framework.yaml", check=False)
    manifest = parse_manifest(manifest_text)
    if not manifest:
        print("The template has no framework.yaml (or it lists no paths). Nothing synced.")
        return 1

    template_files = {f for f in git("ls-tree", "-r", "--name-only", ref).splitlines() if matches(f, manifest)}
    local_files = {f for f in git("ls-files").splitlines() if matches(f, manifest)}
    to_remove = sorted(local_files - template_files)

    previous = (ROOT / VERSION_FILE).read_text().split()[0] if (ROOT / VERSION_FILE).exists() else None
    if previous == sha and not to_remove:
        # Still pull, in case a framework file was edited locally, but say we're current.
        print(f"Already on template version {sha[:7]}; checking for local drift.")

    if args.dry_run:
        changed = git("diff", "--name-status", "HEAD", ref, "--", *sorted({
            p for p in manifest if p.endswith("/") or p in template_files}), check=False)
        print(f"\nTemplate version: {sha[:7]} ({subject})")
        print("Would update:\n" + (changed or "  nothing"))
        print("Would remove:\n" + ("\n".join(f"  {f}" for f in to_remove) or "  nothing"))
        return 0

    # 3. Pull every framework file from the template, and remove the ones it dropped.
    if template_files:
        git("checkout", ref, "--", *sorted(template_files))
    if to_remove:
        git("rm", "--quiet", "--", *to_remove)

    # 4. Record the template version.
    (ROOT / VERSION_FILE).write_text(f"{sha}\n{subject}\n")
    git("add", VERSION_FILE)

    # 5. Rebuild and validate with the freshly synced scripts.
    python = sys.executable
    subprocess.run([python, "scripts/build_index.py"], cwd=ROOT)
    git("add", "--", "index.yaml", "BUILD-PLAN.md", check=False)
    validation = subprocess.run([python, "scripts/validate.py"], cwd=ROOT)

    summary = git("diff", "--cached", "--stat")
    print("\nChanges from the sync:\n" + (summary or "  none"))
    if not summary:
        print(f"Already in sync with template version {sha[:7]}.")
        return 0

    if validation.returncode != 0:
        print("\nValidation found errors after the sync, so nothing was committed. The changes are "
              "staged. The new framework rules likely affect existing records: fix those (the "
              "herodocs-sync skill can help), then commit.")
        return 1

    git("commit", "--quiet", "-m", f"Sync framework to herodocs-template {sha[:7]}", "-m", subject)
    print(f"\nCommitted: framework synced to template version {sha[:7]}.")
    if args.push:
        git("push", capture=False)
        print("Pushed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
