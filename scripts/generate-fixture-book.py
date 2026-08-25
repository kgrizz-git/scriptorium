#!/usr/bin/env python3
"""Generate a synthetic Scriptorium book package into gitignored tmp/.

Produces a deterministic, schema-valid book fixture: meta.json plus minimal
valid PNGs for each page (stdlib-only — hand-rolled via zlib + struct). No
pip dependencies. Re-running with the same arguments yields byte-identical
output, so fixtures are reproducible and no large binaries need to live in git.

Usage:
    python3 scripts/generate-fixture-book.py
    python3 scripts/generate-fixture-book.py --pages 8 --seed 42
"""

import argparse
import hashlib
import json
import struct
import zlib
from pathlib import Path

FORMAT_VERSION = 1
DEFAULT_PAGES = 12
DEFAULT_SEED = 20260824
FIXTURES_ROOT = Path("tmp/fixtures")


def _crc32(data: bytes) -> int:
    return zlib.crc32(data) & 0xFFFFFFFF


def _png_chunk(tag: bytes, data: bytes) -> bytes:
    length = struct.pack(">I", len(data))
    crc = struct.pack(">I", _crc32(tag + data))
    return length + tag + data + crc


def make_png(width: int, height: int, seed_byte: int) -> bytes:
    """Return bytes of a minimal 8-bit RGB PNG with a deterministic gradient."""
    header = b"\x89PNG\r\n\x1a\n"
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)  # 8-bit, color_type=2 (RGB)
    ihdr = _png_chunk(b"IHDR", ihdr_data)

    # Raw image data: each row prefixed with filter byte 0 (None).
    row = bytes()
    for y in range(height):
        r = (seed_byte + y) & 0xFF
        g = (seed_byte * 2 + y) & 0xFF
        b = (seed_byte * 3 + y) & 0xFF
        row += b"\x00" + bytes([r, g, b]) * width
    idat = _png_chunk(b"IDAT", zlib.compress(row, 9))
    iend = _png_chunk(b"IEND", b"")

    return header + ihdr + idat + iend


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_book_package(out_dir: Path, title: str, page_count: int, seed: int) -> dict:
    """Generate the book directory and return the meta.json dict."""
    pages_dir = out_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    created = "2026-08-24T00:00:00Z"
    updated = "2026-08-24T00:00:00Z"

    pages = []
    for index in range(page_count):
        width = 800
        height = 1100
        png = make_png(width, height, seed + index)
        file_path = pages_dir / f"{index:03d}.png"
        file_path.write_bytes(png)

        pages.append(
            {
                "index": index,
                "file": f"pages/{index:03d}.png",
                "width": width,
                "height": height,
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

    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    (out_dir / "annotations.json").write_text("[]\n")

    return meta


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--pages", type=int, default=DEFAULT_PAGES, help="Number of pages")
    parser.add_argument(
        "--out", type=Path, default=None, help="Output directory (default: tmp/fixtures/<id>)"
    )
    parser.add_argument("--title", type=str, default="Fixture Book", help="Book title")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Determinism seed")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = args.out or FIXTURES_ROOT / "fixture-book"
    out_dir.mkdir(parents=True, exist_ok=True)

    meta = build_book_package(out_dir, args.title, args.pages, args.seed)

    print(f"Generated book '{meta['id']}' ({args.pages} pages) → {out_dir}")
    print(f"  formatVersion: {meta['formatVersion']}")
    print(f"  total bytes: {sum(p['byteSize'] for p in meta['pages'])}")


if __name__ == "__main__":
    main()
