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


DEFAULT_AUDIT = Path("src-tauri/.cargo/audit.toml")
DEFAULT_EXCEPTIONS = Path("src-tauri/.cargo/audit-exceptions.toml")
IGNORE_RE = re.compile(r"^\s*ignore\s*=\s*\[(.*?)\]", re.MULTILINE | re.DOTALL)
ID_RE = re.compile(r'"([^"]+)"')


def parse_ignore_ids(audit_text: str) -> list[str]:
    """Extract advisory IDs from the advisories.ignore list in audit.toml."""
    match = IGNORE_RE.search(audit_text)
    if not match:
        return []
    return ID_RE.findall(match.group(1))


def load_exceptions(path: Path) -> list[dict[str, str]]:
    """Load [[exceptions]] rows; each needs id, expires (YYYY-MM-DD), reason."""
    data = tomllib.loads(path.read_text(encoding="utf-8"))
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


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(__doc__ or "").split("\n\n", 1)[0],
    )
    parser.add_argument("--audit", type=Path, default=DEFAULT_AUDIT)
    parser.add_argument("--exceptions", type=Path, default=DEFAULT_EXCEPTIONS)
    parser.add_argument("--today", type=str, default=None, help="YYYY-MM-DD override")
    args = parser.parse_args()

    try:
        today = date.fromisoformat(args.today) if args.today else date.today()
    except ValueError as err:
        print(f"[audit-exceptions] ERROR: bad --today: {err}", file=sys.stderr)
        return 2

    if not args.audit.is_file():
        print(f"[audit-exceptions] ERROR: missing {args.audit}", file=sys.stderr)
        return 2
    if not args.exceptions.is_file():
        print(f"[audit-exceptions] ERROR: missing {args.exceptions}", file=sys.stderr)
        return 2

    try:
        ignore_ids = parse_ignore_ids(args.audit.read_text(encoding="utf-8"))
        exceptions = load_exceptions(args.exceptions)
    except (OSError, ValueError, tomllib.TOMLDecodeError) as err:
        print(f"[audit-exceptions] ERROR: {err}", file=sys.stderr)
        return 2

    by_id = {row["id"]: row for row in exceptions}
    if len(by_id) != len(exceptions):
        print("[audit-exceptions] ERROR: duplicate exception ids", file=sys.stderr)
        return 1

    problems: list[str] = []
    ignore_set = set(ignore_ids)
    exception_set = set(by_id)

    for missing in sorted(ignore_set - exception_set):
        problems.append(f"ignore {missing} has no row in {args.exceptions}")
    for orphan in sorted(exception_set - ignore_set):
        problems.append(f"exception {orphan} is not listed in {args.audit} ignore")

    for row in exceptions:
        try:
            expires = date.fromisoformat(row["expires"])
        except ValueError:
            problems.append(f"{row['id']}: bad expires date {row['expires']!r}")
            continue
        if today > expires:
            problems.append(
                f"{row['id']} expired on {expires.isoformat()} — "
                f"remove ignore or extend with justification ({row['reason']})"
            )
        else:
            print(f"[audit-exceptions] ok {row['id']} until {expires.isoformat()}")

    if problems:
        for problem in problems:
            print(f"[audit-exceptions] ERROR: {problem}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
