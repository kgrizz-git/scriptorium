#!/usr/bin/env python3
"""Generate a synthetic Scriptorium book package into gitignored tmp/.

Produces a deterministic, schema-valid book fixture: meta.json plus minimal
valid PNGs for each page (stdlib-only — hand-rolled via zlib + struct). No
pip dependencies. Re-running with the same arguments yields byte-identical
output, so fixtures are reproducible and no large binaries need to live in git.

Empty annotations use the canonical form `[]` (see docs/book-format.md).

Usage:
    python3 scripts/generate-fixture-book.py
    python3 scripts/generate-fixture-book.py --pages 8 --seed 42
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
import zlib
from pathlib import Path

FORMAT_VERSION = 1
DEFAULT_PAGES = 12
DEFAULT_SEED = 20260824
FIXTURES_ROOT = Path("tmp/fixtures")
PAGE_WIDTH = 800
PAGE_HEIGHT = 1100
BOOK_ID_RE = re.compile(
    r"^(?!(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.[a-z0-9._-]*)?$)(?!.*\.$)[a-z0-9][a-z0-9._-]{0,63}$"
)
# Must match docs/book-format.schema.json properties.id.pattern (see tests).


def _crc32(data: bytes) -> int:
    return zlib.crc32(data) & 0xFFFFFFFF


def _png_chunk(tag: bytes, data: bytes) -> bytes:
    length = struct.pack(">I", len(data))
    crc = struct.pack(">I", _crc32(tag + data))
    return length + tag + data + crc


def make_png(width: int, height: int, seed_byte: int) -> bytes:
    """Return bytes of a minimal 8-bit RGB PNG with a deterministic gradient."""
    if width < 1 or height < 1:
        raise ValueError(f"PNG dimensions must be >= 1, got {width}x{height}")
    header = b"\x89PNG\r\n\x1a\n"
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)  # 8-bit, color_type=2 (RGB)
    ihdr = _png_chunk(b"IHDR", ihdr_data)

    # Raw image data: each row prefixed with filter byte 0 (None).
    raw = bytearray()
    for y in range(height):
        r = (seed_byte + y) & 0xFF
        g = (seed_byte * 2 + y) & 0xFF
        b = (seed_byte * 3 + y) & 0xFF
        raw.append(0)
        pixel = bytes([r, g, b])
        raw.extend(pixel * width)
    idat = _png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    iend = _png_chunk(b"IEND", b"")

    return header + ihdr + idat + iend


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_book_package(out_dir: Path, title: str, page_count: int, seed: int) -> dict:
    """Generate the book directory and return the meta.json dict."""
    if page_count < 1:
        raise ValueError(f"--pages must be >= 1, got {page_count}")
    if not BOOK_ID_RE.fullmatch(out_dir.name):
        raise ValueError(
            f"output directory name {out_dir.name!r} must match book id slug {BOOK_ID_RE.pattern}"
        )

    pages_dir = out_dir / "pages"
    if pages_dir.exists():
        for old_page in pages_dir.glob("*.png"):
            old_page.unlink()
    pages_dir.mkdir(parents=True, exist_ok=True)

    created = "2026-08-24T00:00:00Z"
    updated = "2026-08-24T00:00:00Z"

    pages = []
    for index in range(page_count):
        png = make_png(PAGE_WIDTH, PAGE_HEIGHT, seed + index)
        file_path = pages_dir / f"{index:03d}.png"
        file_path.write_bytes(png)

        pages.append(
            {
                "index": index,
                "file": f"pages/{index:03d}.png",
                "width": PAGE_WIDTH,
                "height": PAGE_HEIGHT,
                "byteSize": len(png),
                "sha256": sha256_hex(png),
                **({"pageLabel": "Cover"} if index == 0 else {}),
                "storage": "copied",
            }
        )

    meta = {
        "formatVersion": FORMAT_VERSION,
        "id": out_dir.name,
        "title": title,
        "createdAt": created,
        "updatedAt": updated,
        "renderMode": "scan",
        "lastReadPage": 0,
        "rights": "",
        "attribution": "",
        "pages": pages,
    }

    (out_dir / "meta.json").write_bytes((json.dumps(meta, indent=2) + "\n").encode("utf-8"))
    # Canonical empty annotations form is [] ({} tolerated on read, never written).
    (out_dir / "annotations.json").write_bytes(b"[]\n")

    return meta


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--pages",
        type=int,
        default=DEFAULT_PAGES,
        help="Number of pages (must be >= 1)",
    )
    parser.add_argument(
        "--out", type=Path, default=None, help="Output directory (default: tmp/fixtures/<id>)"
    )
    parser.add_argument("--title", type=str, default="Fixture Book", help="Book title")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Determinism seed")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.pages < 1:
        print(f"error: --pages must be >= 1, got {args.pages}", file=sys.stderr)
        return 2

    out_dir = args.out or FIXTURES_ROOT / "fixture-book"
    out_dir.mkdir(parents=True, exist_ok=True)

    meta = build_book_package(out_dir, args.title, args.pages, args.seed)

    print(f"Generated book '{meta['id']}' ({args.pages} pages) → {out_dir}")
    print(f"  formatVersion: {meta['formatVersion']}")
    print(f"  total bytes: {sum(p['byteSize'] for p in meta['pages'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
