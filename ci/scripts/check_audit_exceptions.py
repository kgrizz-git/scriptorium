#!/usr/bin/env python3
"""
check_audit_exceptions.py — enforce time-bound cargo-audit ignores.

cargo-audit accepts advisory IDs in advisories.ignore but does not interpret
expiration dates. This repo keeps machine-readable exceptions in
src-tauri/.cargo/audit-exceptions.toml and fails CI once an ignore has expired
(or when ignore lists drift from the exceptions file).

Inputs:
  --audit PATH       path to audit.toml (default: src-tauri/.cargo/audit.toml)
  --exceptions PATH  path to audit-exceptions.toml
                     (default: src-tauri/.cargo/audit-exceptions.toml)
  --root PATH        directory that audit/exception paths must stay under
                     (default: current working directory)
  --today YYYY-MM-DD override "today" for tests

Outputs:
  Prints a short status line per exception. Exit 0 when all ignores have a
  matching, unexpired exception; exit 1 on expiry or sync failure; exit 2 on
  usage / parse errors.

Requirements:
  Python 3.11+ (stdlib only).
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from datetime import date
from pathlib import Path
from typing import Any


DEFAULT_AUDIT = Path("src-tauri/.cargo/audit.toml")
DEFAULT_EXCEPTIONS = Path("src-tauri/.cargo/audit-exceptions.toml")
# Strict calendar date only — Python 3.11+ fromisoformat also accepts compact/week forms.
CANONICAL_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def resolve_under_root(path: Path, root: Path) -> Path:
    """Resolve path and require it stays under root (blocks CLI path escape)."""
    root_resolved = root.resolve()
    candidate = path if path.is_absolute() else root_resolved / path
    resolved = candidate.resolve()
    if not resolved.is_relative_to(root_resolved):
        raise ValueError(f"{path}: must stay under {root_resolved}")
    return resolved


def parse_canonical_date(value: str, *, label: str) -> date:
    """Parse YYYY-MM-DD only; reject compact and week-date ISO forms."""
    if not CANONICAL_DATE_RE.fullmatch(value):
        raise ValueError(f"{label} must be YYYY-MM-DD, got {value!r}")
    return date.fromisoformat(value)


def load_toml(path: Path) -> dict[str, Any]:
    """Parse a TOML file into a dict; raise ValueError with path context on failure."""
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as err:
        raise ValueError(f"{path}: invalid TOML: {err}") from err
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a TOML table at the root")
    return data


def parse_ignore_ids(path: Path) -> list[str]:
    """Return advisories.ignore as a list of non-empty strings from audit.toml."""
    data = load_toml(path)
    advisories = data.get("advisories")
    if advisories is None:
        return []
    if not isinstance(advisories, dict):
        raise ValueError(f"{path}: [advisories] must be a table")
    if "ignore" not in advisories:
        return []
    ignore = advisories["ignore"]
    if not isinstance(ignore, list):
        raise ValueError(f"{path}: advisories.ignore must be a list of strings")
    ids: list[str] = []
    for i, item in enumerate(ignore):
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                f"{path}: advisories.ignore[{i}] must be a non-empty string, got {item!r}"
            )
        ids.append(item.strip())
    return ids


def load_exceptions(path: Path) -> list[dict[str, str]]:
    """Load [[exceptions]] rows; each needs id, expires (YYYY-MM-DD), reason."""
    data = load_toml(path)
    rows = data.get("exceptions")
    if not isinstance(rows, list):
        raise ValueError(f"{path}: missing [[exceptions]] table array")
    out: list[dict[str, str]] = []
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"{path}: exceptions[{i}] must be a table")
        for key in ("id", "expires", "reason"):
            if key not in row or not isinstance(row[key], str) or not row[key].strip():
                raise ValueError(f"{path}: exceptions[{i}] missing string field '{key}'")
        out.append(
            {
                "id": row["id"].strip(),
                "expires": row["expires"].strip(),
                "reason": row["reason"].strip(),
            }
        )
    return out


def collect_problems(
    ignore_ids: list[str],
    exceptions: list[dict[str, str]],
    today: date,
    audit_label: Path,
    exceptions_label: Path,
) -> list[str]:
    """Return policy problems (sync drift, bad dates, expired ignores)."""
    by_id = {row["id"]: row for row in exceptions}
    if len(by_id) != len(exceptions):
        return ["duplicate exception ids"]

    problems: list[str] = []
    ignore_set = set(ignore_ids)
    exception_set = set(by_id)

    for missing in sorted(ignore_set - exception_set):
        problems.append(f"ignore {missing} has no row in {exceptions_label}")
    for orphan in sorted(exception_set - ignore_set):
        problems.append(f"exception {orphan} is not listed in {audit_label} ignore")

    for row in exceptions:
        try:
            expires = parse_canonical_date(row["expires"], label=f"{row['id']} expires")
        except ValueError as err:
            problems.append(str(err))
            continue
        if today > expires:
            problems.append(
                f"{row['id']} expired on {expires.isoformat()} — "
                f"remove ignore or extend with justification ({row['reason']})"
            )
        else:
            print(f"[audit-exceptions] ok {row['id']} until {expires.isoformat()}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(__doc__ or "").split("\n\n", 1)[0],
    )
    parser.add_argument("--audit", type=Path, default=DEFAULT_AUDIT)
    parser.add_argument("--exceptions", type=Path, default=DEFAULT_EXCEPTIONS)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="directory that --audit/--exceptions must stay under",
    )
    parser.add_argument("--today", type=str, default=None, help="YYYY-MM-DD override")
    args = parser.parse_args()

    try:
        today = parse_canonical_date(args.today, label="--today") if args.today else date.today()
        root = args.root.resolve()
        audit_path = resolve_under_root(args.audit, root)
        exceptions_path = resolve_under_root(args.exceptions, root)
    except ValueError as err:
        print(f"[audit-exceptions] ERROR: {err}", file=sys.stderr)
        return 2

    if not audit_path.is_file():
        print(f"[audit-exceptions] ERROR: missing {audit_path}", file=sys.stderr)
        return 2
    if not exceptions_path.is_file():
        print(f"[audit-exceptions] ERROR: missing {exceptions_path}", file=sys.stderr)
        return 2

    try:
        ignore_ids = parse_ignore_ids(audit_path)
        exceptions = load_exceptions(exceptions_path)
    except (OSError, ValueError) as err:
        print(f"[audit-exceptions] ERROR: {err}", file=sys.stderr)
        return 2

    problems = collect_problems(ignore_ids, exceptions, today, audit_path, exceptions_path)
    if problems:
        for problem in problems:
            print(f"[audit-exceptions] ERROR: {problem}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
