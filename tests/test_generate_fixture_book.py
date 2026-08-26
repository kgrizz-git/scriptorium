#!/usr/bin/env python3
"""Tests for scripts/generate-fixture-book.py.

Covers PNG layout, SHA-256, schema conformance, determinism, and --pages 0 rejection.
Stdlib unittest only (no pytest required for local runs).

Run:
  python3 -m unittest tests.test_generate_fixture_book -v
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]


def _load_generator() -> ModuleType:
    """Load the hyphenated script as a module."""
    path = ROOT / "scripts" / "generate-fixture-book.py"
    spec = importlib.util.spec_from_file_location("generate_fixture_book", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gen = _load_generator()


def _parse_png_ihdr(png: bytes) -> tuple[int, int, int, int]:
    assert png[:8] == b"\x89PNG\r\n\x1a\n", "missing PNG signature"
    length = struct.unpack(">I", png[8:12])[0]
    assert png[12:16] == b"IHDR"
    assert length == 13
    width, height, bit_depth, color_type = struct.unpack(">IIBB", png[16:26])
    return width, height, bit_depth, color_type


def _idat_raw_size(png: bytes) -> int:
    """Decompress concatenated IDAT payloads and return raw byte length."""
    offset = 8
    compressed = b""
    while offset < len(png):
        length = struct.unpack(">I", png[offset : offset + 4])[0]
        tag = png[offset + 4 : offset + 8]
        data = png[offset + 8 : offset + 8 + length]
        offset += 12 + length
        if tag == b"IDAT":
            compressed += data
        elif tag == b"IEND":
            break
    return len(zlib.decompress(compressed))


class MakePngTests(unittest.TestCase):
    def test_png_header_and_ihdr(self) -> None:
        png = gen.make_png(4, 3, seed_byte=9)
        width, height, bit_depth, color_type = _parse_png_ihdr(png)
        self.assertEqual((width, height), (4, 3))
        self.assertEqual(bit_depth, 8)
        self.assertEqual(color_type, 2)  # RGB

    def test_idat_decompresses_to_expected_size(self) -> None:
        width, height = 5, 7
        png = gen.make_png(width, height, seed_byte=1)
        # filter byte + 3 bytes/pixel per row
        expected = height * (1 + width * 3)
        self.assertEqual(_idat_raw_size(png), expected)

    def test_make_png_rejects_zero_dimension(self) -> None:
        with self.assertRaises(ValueError):
            gen.make_png(0, 10, seed_byte=1)


class FixtureBookTests(unittest.TestCase):
    def test_meta_validates_against_schema(self) -> None:
        try:
            import jsonschema
        except ImportError as exc:  # pragma: no cover - CI installs jsonschema
            self.fail(
                "jsonschema is required for schema conformance tests; "
                "install with `pip install jsonschema` or `pip install '.[test]'` "
                f"(import failed: {exc})"
            )

        schema = json.loads((ROOT / "docs" / "book-format.schema.json").read_text())
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "schema-book"
            meta = gen.build_book_package(out, "Schema Book", page_count=2, seed=3)
            format_checker = jsonschema.FormatChecker()
            self.assertIn(
                "date-time",
                format_checker.checkers,
                "date-time format checking requires rfc3339-validator "
                "(pip install rfc3339-validator or pip install '.[test]')",
            )
            jsonschema.validate(meta, schema, format_checker=format_checker)
            invalid_meta = dict(meta, createdAt="not-a-timestamp")
            with self.assertRaises(jsonschema.ValidationError):
                jsonschema.validate(
                    invalid_meta,
                    schema,
                    format_checker=format_checker,
                )
            self.assertEqual((out / "annotations.json").read_text(), "[]\n")

    def test_determinism_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            a = root / "run1" / "same-book"
            b = root / "run2" / "same-book"
            gen.build_book_package(a, "Same", page_count=3, seed=42)
            gen.build_book_package(b, "Same", page_count=3, seed=42)
            for rel in ("meta.json", "annotations.json", "pages/000.png", "pages/001.png"):
                self.assertEqual(
                    (a / rel).read_bytes(),
                    (b / rel).read_bytes(),
                    f"{rel} must be byte-identical across runs",
                )

    def test_sha256_matches_file_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "hash-book"
            meta = gen.build_book_package(out, "Hash", page_count=1, seed=1)
            page = meta["pages"][0]
            data = (out / page["file"]).read_bytes()
            self.assertEqual(page["sha256"], hashlib.sha256(data).hexdigest())
            self.assertEqual(page["byteSize"], len(data))

    def test_pages_zero_rejected_by_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "empty"
            code = gen.main(["--pages", "0", "--out", str(out)])
            self.assertEqual(code, 2)
            self.assertFalse((out / "meta.json").exists())

    def test_build_rejects_zero_pages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                gen.build_book_package(Path(tmp) / "x", "x", page_count=0, seed=1)

    def test_book_id_pattern_matches_schema(self) -> None:
        schema = json.loads((ROOT / "docs" / "book-format.schema.json").read_text())
        pattern = schema["properties"]["id"]["pattern"]
        self.assertEqual(
            gen.BOOK_ID_RE.pattern,
            pattern,
            "Python BOOK_ID_RE must match docs/book-format.schema.json",
        )

    def test_regenerate_fewer_pages_clears_orphans(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "regen-book"
            gen.build_book_package(out, "Regen", page_count=3, seed=1)
            self.assertTrue((out / "pages" / "002.png").exists())
            gen.build_book_package(out, "Regen", page_count=1, seed=1)
            self.assertTrue((out / "pages" / "000.png").exists())
            self.assertFalse((out / "pages" / "001.png").exists())
            self.assertFalse((out / "pages" / "002.png").exists())
            meta = json.loads((out / "meta.json").read_text(encoding="utf-8"))
            self.assertEqual(len(meta["pages"]), 1)

    def test_meta_and_annotations_use_lf_newlines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "lf-book"
            gen.build_book_package(out, "LF", page_count=1, seed=1)
            meta_bytes = (out / "meta.json").read_bytes()
            ann_bytes = (out / "annotations.json").read_bytes()
            self.assertNotIn(b"\r", meta_bytes)
            self.assertNotIn(b"\r", ann_bytes)
            self.assertTrue(meta_bytes.endswith(b"\n"))
            self.assertEqual(ann_bytes, b"[]\n")


if __name__ == "__main__":
    unittest.main()
