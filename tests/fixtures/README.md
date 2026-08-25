# Test fixtures

Large scan corpora and binary fixtures do **not** live in git. Instead, scripts
in `scripts/` regenerate them on demand into gitignored `tmp/`.

## Fixture book

`../scripts/generate-fixture-book.py` produces a deterministic, schema-valid
Scriporium book package under `tmp/fixtures/fixture-book/`:

```
tmp/fixtures/fixture-book/
├── meta.json
├── annotations.json
└── pages/
    ├── 000.png
    ├── 001.png
    └── ...
```

It is stdlib-only (no pip deps) and hand-rolls minimal valid PNGs, so it runs
anywhere Python 3 is available.

### Usage

```sh
python3 scripts/generate-fixture-book.py                  # default 12-page book
python3 scripts/generate-fixture-book.py --pages 8        # fewer pages
python3 scripts/generate-fixture-book.py --seed 42 --title "My Book"
python3 scripts/generate-fixture-book.py --out tmp/fixtures/custom-book
```

### Determinism

The generator is fully deterministic: the same `--pages`, `--seed`, and `--title`
arguments produce byte-identical output across runs. The default seed is fixed,
so plain invocations regenerate the same fixture every time. This keeps tests
reproducible and means no large binaries need to be committed.

### Schema

The generated `meta.json` conforms to formatVersion 1 of the book package spec
(see [`docs/book-format.md`](../../docs/book-format.md)): real `sha256` and
`byteSize` are computed from the written PNGs, and page 0 carries an optional
`pageLabel` to exercise that field.
