#!/usr/bin/env python3
"""
check_todo_plan_sync.py — advisory sync between to_do.md and plans/

Warns when Next Up / Active sections drift from active plan files. See
policies/plans-and-todos.md.

Usage:
  python hooks/scripts/check_todo_plan_sync.py [to_do.md]

Environment:
  POLICY_NEXT_UP_MIN        (default 3)
  POLICY_NEXT_UP_MAX        (default 5)
  POLICY_ICEBOX_SOFT_CAP    (default 20)
  POLICY_REPO_ROOT          (default .)
  POLICY_WARN_AS_ERROR      (set to 1 to treat warnings as errors)
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

NEXT_UP_MIN = int(os.getenv("POLICY_NEXT_UP_MIN", "3"))
NEXT_UP_MAX = int(os.getenv("POLICY_NEXT_UP_MAX", "5"))
ICEBOX_SOFT_CAP = int(os.getenv("POLICY_ICEBOX_SOFT_CAP", "20"))
WARN_AS_ERROR = os.getenv("POLICY_WARN_AS_ERROR", "0") == "1"

ACTIVE_PLAN_SKIP = {"README.md", "orchestration-state.md"}
ARCHIVE_PREFIXES = ("plans/archive/", "plans/deferred/")
PLAN_LINK_RE = re.compile(r"plans/[^\s`)>\]]+\.md")
STATUS_RE = re.compile(r"^Status:\s*(\S+)", re.MULTILINE | re.IGNORECASE)
SECTION_RE = re.compile(
    r"^## (?P<title>[^\n]+)\n(?P<body>.*?)(?=^## |\Z)",
    re.MULTILINE | re.DOTALL,
)
NEXT_UP_ENTRY_RE = re.compile(r"^\s*(?:\d+\.|[-*])\s+.+", re.MULTILINE)


def extract_section(text: str, title_prefix: str) -> str:
    """Return body of the first ## heading whose title starts with title_prefix."""
    for match in SECTION_RE.finditer(text):
        title = match.group("title").strip()
        if title.lower().startswith(title_prefix.lower()):
            return match.group("body")
    return ""


def plan_links(text: str) -> set[str]:
    """Normalize plan paths referenced in markdown."""
    found: set[str] = set()
    for raw in PLAN_LINK_RE.findall(text):
        path = raw.split("#", 1)[0]
        if not path.startswith("plans/"):
            path = f"plans/{path.lstrip('/')}"
        found.add(path)
    return found


def count_next_up_entries(section_body: str) -> int:
    return len(NEXT_UP_ENTRY_RE.findall(section_body))


def active_plan_paths(repo_root: Path) -> list[Path]:
    plans_dir = repo_root / "plans"
    if not plans_dir.is_dir():
        return []
    paths: list[Path] = []
    for plan_file in sorted(plans_dir.glob("*.md")):
        if plan_file.name in ACTIVE_PLAN_SKIP:
            continue
        paths.append(plan_file)
    return paths


def rel_plan_path(repo_root: Path, plan_file: Path) -> str:
    return plan_file.relative_to(repo_root).as_posix()


def is_archived_or_deferred(path: str) -> bool:
    normalized = path.replace("\\", "/")
    return any(normalized.startswith(prefix) for prefix in ARCHIVE_PREFIXES)


def broken_link_errors(repo_root: Path, todo_path: Path, links: set[str]) -> list[str]:
    """Return errors for links in the backlog that do not resolve to files."""
    errors: list[str] = []
    for link in sorted(links):
        target = repo_root / link
        if not target.is_file():
            errors.append(f"{todo_path}: link target missing: {link}")
    return errors


def next_up_warnings(repo_root: Path, todo_path: Path, next_up_body: str) -> list[str]:
    """Return warnings for the size and shape of the Next Up queue."""
    warnings: list[str] = []

    if next_up_body.strip():
        count = count_next_up_entries(next_up_body)
        if count < NEXT_UP_MIN:
            warnings.append(
                f"{todo_path}: Next Up has {count} entries (target {NEXT_UP_MIN}–{NEXT_UP_MAX})"
            )
        elif count > NEXT_UP_MAX:
            warnings.append(
                f"{todo_path}: Next Up has {count} entries (target {NEXT_UP_MIN}–{NEXT_UP_MAX})"
            )
    else:
        active_plans = active_plan_paths(repo_root)
        if active_plans:
            warnings.append(f"{todo_path}: missing ## Next Up section while active plans exist")

    for line in next_up_body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not re.match(r"^\d+\.|[-*]", stripped):
            continue
        if "plans/" not in stripped and "unplanned" not in stripped.lower():
            warnings.append(
                f"{todo_path}: Next Up entry without plan link (add plans/… or label unplanned): "
                f"{stripped[:80]}"
            )
    return warnings


def active_plan_warnings(repo_root: Path, todo_path: Path, links: set[str]) -> list[str]:
    """Return warnings for active plan files missing from the backlog."""
    warnings: list[str] = []

    for plan_file in active_plan_paths(repo_root):
        rel = rel_plan_path(repo_root, plan_file)
        if rel not in links:
            warnings.append(f"{todo_path}: active plan not linked: {rel}")
    return warnings


def queue_warnings(todo_path: Path, next_up_body: str, active_body: str) -> list[str]:
    """Return warnings for archived or deferred plans in active queues."""
    warnings: list[str] = []

    queue_links = plan_links(next_up_body) | plan_links(active_body)
    for link in sorted(queue_links):
        if is_archived_or_deferred(link):
            warnings.append(
                f"{todo_path}: archived/deferred plan linked from Next Up or Active: {link}"
            )
    return warnings


def icebox_warnings(todo_path: Path, icebox_body: str) -> list[str]:
    """Return warnings when the Icebox exceeds its advisory capacity."""
    warnings: list[str] = []

    if icebox_body.strip():
        icebox_count = len(NEXT_UP_ENTRY_RE.findall(icebox_body))
        if icebox_count > ICEBOX_SOFT_CAP:
            warnings.append(
                f"{todo_path}: Icebox has {icebox_count} entries "
                f"(soft cap {ICEBOX_SOFT_CAP}); promote to plans/deferred/"
            )
    return warnings


def check(repo_root: Path, todo_path: Path) -> tuple[list[str], list[str]]:
    """Check that the backlog's active queues match the plan directory."""
    if not todo_path.is_file():
        return [], [f"{todo_path}: backlog file missing (skip sync)"]

    text = todo_path.read_text(encoding="utf-8", errors="ignore")
    all_links = plan_links(text)
    next_up_body = extract_section(text, "Next Up")
    active_body = extract_section(text, "Active plans")
    icebox_body = extract_section(text, "Icebox")

    errors = broken_link_errors(repo_root, todo_path, all_links)
    warnings = next_up_warnings(repo_root, todo_path, next_up_body)
    warnings.extend(active_plan_warnings(repo_root, todo_path, all_links))
    warnings.extend(queue_warnings(todo_path, next_up_body, active_body))
    warnings.extend(icebox_warnings(todo_path, icebox_body))

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Check to_do.md ↔ plans/ sync (advisory).")
    parser.add_argument(
        "todo_file",
        nargs="?",
        default="to_do.md",
        help="Path to living backlog (default: to_do.md)",
    )
    parser.add_argument(
        "--repo-root",
        default=os.getenv("POLICY_REPO_ROOT", "."),
        help="Repository root (default: cwd or POLICY_REPO_ROOT)",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    todo_path = Path(args.todo_file)
    if not todo_path.is_absolute():
        todo_path = (repo_root / todo_path).resolve()

    errors, warnings = check(repo_root, todo_path)

    for warning in warnings:
        print(f"[todo-plan-sync] WARN  {warning}", file=sys.stderr)
    for error in errors:
        print(f"[todo-plan-sync] ERROR {error}", file=sys.stderr)

    if errors:
        return 1
    if WARN_AS_ERROR and warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
