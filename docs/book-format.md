# Scriptorium book package format

Last reviewed: 2026-08-25

Normative spec for a Scriptorium **book package** (formatVersion 1). A package is a
self-contained directory that the app can open, verify, and re-locate on disk without
dangling references. The locked decisions here come from the
[M0 foundation plan](../plans/archive/completed/2026-08-23-m0-tauri-foundation.md); this doc is the
human-readable source of truth. Field *types* are normative in
[`book-format.schema.json`](book-format.schema.json) — when the two disagree, the schema
wins on types, this doc wins on rules and intent.

## Package layout

```
<book-id>/
├── meta.json          # required — see fields below
├── pages/             # required — page images, relative paths stored in meta.json
├── ocr/               # reserved — may be empty; text layer lands here in M2+
└── annotations.json   # reserved — empty form is `[]` (canonical); `{}` tolerated on read, never written
```

**Portability:** everything inside the package is addressed with **relative paths**.
`meta.json` MUST NOT contain absolute paths (no home directory, no root-anchored source
path). Page `file` values MUST be package-relative, use forward slashes only, and MUST NOT
contain `..` segments or null bytes (enforced in the schema and in Rust
`BookMeta::validate`). A package directory can be moved or copied to another machine and
still load.

## meta.json fields (formatVersion 1)

| Field | Type | Required | Notes |
|---|---|---|---|
| `formatVersion` | number | yes | `1` for this spec |
| `id` | string | yes | stable book identifier **and** package directory name; slug `^[a-z0-9][a-z0-9._-]{0,63}$` |
| `title` | string | yes | display title |
| `createdAt` | string | yes | RFC 3339 / ISO 8601 date-time (enforced in schema + `BookMeta::validate`) |
| `updatedAt` | string | yes | RFC 3339 / ISO 8601 date-time (enforced in schema + `BookMeta::validate`) |
| `renderMode` | string | yes | `"scan"` default; `"text"` / `"hybrid"` reserved |
| `lastReadPage` | number | yes | 0-based index; loader MUST clamp or reject when `>= pages.length` |
| `rights` | string | yes | may be empty |
| `attribution` | string | yes | may be empty |
| `pages[]` | array | yes | one entry per page, in order (`minItems: 1`) |

`pages[]` item:

| Field | Type | Required | Notes |
|---|---|---|---|
| `index` | number | yes | 0-based position; MUST equal array position (`pages[i].index == i`) |
| `file` | string | yes | relative path under the package (no `..`, no absolutes) |
| `width` | number | yes | image width in px (`minimum: 1`) |
| `height` | number | yes | image height in px (`minimum: 1`) |
| `byteSize` | number | yes | bytes on disk (`exclusiveMinimum: 0`) |
| `sha256` | string | yes | hex digest of the page file |
| `pageLabel` | string | no | optional human label |
| `storage` | string | no | `"copied"` default; `"referenced"` reserved, not implemented in M1 |

## Evolution rule

While `formatVersion` is `1`, changes to `meta.json` MUST be **additive only** — add
fields, don't rename or remove them, don't change the meaning of existing fields. A
breaking change requires bumping `formatVersion` and a migration note describing how to
upgrade a v1 package to the new version.

## Loader validation

After JSON Schema validation, loaders MUST run the Rust `BookMeta::validate` checks (or
an equivalent):

| Check | Behavior |
|---|---|
| `id` | MUST match slug `^[a-z0-9][a-z0-9._-]{0,63}$` (safe as a library directory name). |
| `createdAt` / `updatedAt` | MUST parse as RFC 3339 date-time. |
| `lastReadPage` | MUST be `< pages.length`. Prefer reject (`LastReadPageOutOfRange`); UI may clamp to `pages.length - 1` if recovering a corrupt bookmark. |
| `pages[].index` | MUST equal array position (`pages[i].index == i`); reject duplicates / gaps / out-of-order. |
| `pages[].file` | Reject absolute paths, `..` segments, backslashes, null bytes, empty segments. |
| `pages[].width` / `height` | Reject values `< 1` (degenerate images). |
| `pages[].byteSize` | Reject `0` (empty page files). |

## Ingest rules

Each ingest copies source page images into a new package under the library root
(`<app-data>/books/`). The rules below are load-bearing; the error names are what the
ingest pipeline returns on failure.

| Rule | Behavior on violation | Error |
|---|---|---|
| **Storage default** | Copy page bytes into `pages/`. Symlinks are rejected. `storage: "referenced"` is reserved and NOT implemented in M1. | — |
| **Source collisions** | If two source files map to the same destination stem, including case-insensitive match on APFS/NTFS (e.g. `1.jpg` + `1.JPG`), ingest fails — never silently overwrite. | `DuplicatePageStem` |
| **Atomic write** | Write to a temp dir under the destination parent → validate → rename into place. If a destination book id already exists, ingest fails. | `DestinationExists` |
| **Orphan cleanup** | On startup and before ingest, delete orphaned `*.scriptorium-tmp` / `.ingest-tmp-*` dirs under the library root older than 1 hour (or any left from a previous crashed run). | — |
| **Checksums** | Compute `sha256` at ingest and store it in `meta.json`. `load_book` re-verifies the sha256 of each page file; drift is a hard failure. Skip re-verify only behind an explicit future flag — not in M1. | `ChecksumMismatch` |
| **Free space** | Pre-flight check: refuse the copy if free space is less than `estimated_bytes × 1.1 + 50 MB` headroom. | — |

## Provenance and privacy

`meta.json` MUST NOT store an absolute `sourcePath`. The package is self-contained and
portable; binding it to a specific source location breaks that.

EXIF / XMP metadata embedded in source images is copied **bytes-as-is** in M1. Stripping
or policy (GPS removal, etc.) is deferred but documented here so a future ingest path can
add it without a schema change.
