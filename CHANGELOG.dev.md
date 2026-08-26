# Developer Changelog

Internal / developer-facing changes that do not belong in the public
[`CHANGELOG.md`](CHANGELOG.md). See [`policies/changelog-conventions.md`](policies/changelog-conventions.md).

## [Unreleased]

### Added
- Fixture-generator unit tests (`tests/test_generate_fixture_book.py`); Rust round-trip test that deserializes generator `meta.json` into `BookMeta`.
- `BookMeta::validate` / `PageEntry::validate` for `lastReadPage` bounds, path safety, and non-zero dimensions.
- CI jobs: `Rust (src-tauri)` (cargo fmt/clippy `-D warnings`/test/check, with cargo cache), `Type check (TypeScript)` (pnpm + tsc), `Audit (advisory)` (pnpm audit + cargo audit, continue-on-error).
- `src-tauri/` scaffold (Tauri 2, Vite 7, React 19, TypeScript 5.8); pnpm v11 build-script approval via `pnpm-workspace.yaml`; Node 24 pinned (`engines` / `.nvmrc`).
- `scripts/generate-fixture-book.py` — stdlib-only deterministic fixture generator (real PNGs, schema-valid meta.json); `tests/fixtures/README.md`.
- Rust types in `src-tauri/src/book_format.rs` + schema-bind tests (jsonschema 0.51.0); `cargo fmt` clean.

### Changed
- CI: install Tauri Linux system deps in `Rust (src-tauri)`; point `cargo audit` at `src-tauri/`; fix plan archive relative links broken by M0 move; pin Rust via `rust-toolchain.toml` (`1.96.0`); install `jsonschema` in the pytest job so schema conformance cannot silently skip (**S1**).
- Book schema / Rust validate: `id` slug pattern (safe dirname) (**S5**); reject `byteSize: 0` (**S2**); enforce `pages[i].index == i` (**S3**); RFC 3339 `createdAt`/`updatedAt` (**S4**); `deny_unknown_fields` on `BookMeta`/`PageEntry` (**S6/SEC5**); reject `.` / `..` path segments; reject Windows-reserved device names + trailing periods on `id` and page path components; reject case-insensitive page-path collisions; `title`/`rights`/`attribution` max lengths + `pages` `maxItems: 100000`; table-driven negative path/index tests; slug lockstep tests (Rust + Python vs schema); structural validate accepts wrong-but-valid-shape `sha256` (documents M1 checksum gap); integer fields capped at Rust `u32`/`u64` maxima; `width`/`height` `minimum: 1`.
- Fixture generator: wipe and recreate `pages/` on regenerate (clears non-PNG orphans too); write `meta.json`/`annotations.json` as UTF-8 LF bytes for cross-platform determinism; CLI validates book-id dirname before mkdir.
- Documented page `file` schema-pattern invariants in `docs/book-format.md`.
- LongCat review follow-ups tracked: **LC-M2** (`cargo build` in CI), **LC-M3**/A13 CSP, **LC-L3**/L4 coverage+audit → M1 plan / M0.5 icebox.
- `annotations.json` empty form canonicalized to `[]` (`{}` back-compat only).
- Removed unused Tauri `greet` command; Cargo.toml `authors` set to `kgrizz-git`.
- Doc freshness: bumped Last reviewed on AGENTS/README/`to_do`/NAVIGATION; README covers fixture generator + book format.
- `.gitignore`: dropped `Cargo.lock` ignore (lockfile tracked); anchored `Icon?` to repo root (`/Icon?`) to stop swallowing `src-tauri/icons/` on case-insensitive macOS; added `src-tauri/gen/schemas/` and `.cargo-target/`.
- `docs/ci-and-hooks.md`: added Rust, TS typecheck, and audit to the recommendation table and required-checks list.
- M0 plan archived to [`plans/archive/completed/2026-08-23-m0-tauri-foundation.md`](plans/archive/completed/2026-08-23-m0-tauri-foundation.md); `to_do.md` updated to remove M0 from Next Up and Active.
- `to_do.md` is now strictly actionable: completed work is removed rather than retained in a `Recently done` section, and every meaningful completion is logged once.
- Semgrep (`security.yml`) scans the whole repo. Path skips are in `.semgrepignore` (`scaffolds/`, `ci/examples/`, scratch dirs). Live `.github/` workflows are included and SHA-pinned; Dependabot has an explicit 7-day `cooldown` so Semgrep's Dependabot rule passes.
- Changelog routing: user-visible security → `CHANGELOG.md`; CI/SAST harness → `CHANGELOG.dev.md`; operational maintenance only → `MAINTENANCE.md` (no double-logging). Aligned `templates/maintenance-log.md` with the same tree.

## [0.1.2] - 2026-08-23

### Added
- `.github/workflows/ci.yml` (policy, ruff+complexity, basedpyright, pytest+coverage report, gitleaks).
- `.github/workflows/security.yml` (Semgrep on PR; TruffleHog weekly advisory).
- Pre-push hook: `basedpyright` (`stages: [pre-push]`); `default_stages: [pre-commit]`.
- Roadmap M0.5 + `to_do.md` sections for post-Tauri CI/hooks follow-ups.
- `docs/ci-and-hooks.md`, `pyproject.toml`, `pyrightconfig.json`, `tmp/README.md`.

### Changed
- Ruff complexity rules aligned with `policies/file-size-and-counts.md`.
- Removed `template-checks.yml` (superseded by `ci.yml`).
- Formatted four legacy Python scripts for `ruff format --check`.
- M0 / pre-M1 spike / M1 plans tightened after ox-alpha review: copy collisions + orphan temps +
  checksum re-verify; natural-sort tie-break; named perf machine/corpus/fps; `lastReadPage` by
  book id; spike candidate shortlist; roadmap schema synced to M0; Rust required-check name in
  `docs/ci-and-hooks.md`.
- Backlog system: `to_do.md` **Next Up** / **Active** / **Icebox** sections; policy + agent
  guidance; advisory `check_todo_plan_sync.py` hook (CI + optional pre-commit).

## [0.1.1] - 2026-08-23

### Added
- `inventory/virtual-books-flipbook.md` and source-repo links for flipbook/IIIF/OCR candidates.

### Changed
- Removed unused domain-specific data-gate documentation, prompts, policies, hooks, and CI
  examples from the harness. Data classification is public/internal/confidential with standard
  secret hygiene (gitleaks).
- Project profile written (Tauri-first, hub-and-spoke, cultural-heritage page imagery).

## [0.1.0] - 2026-08-23

### Added
- New project cut from `project-seed-template` at template version **0.4.4**. Fresh
  git history; private `origin` → `kgrizz-git/scriptorium`. Template changelog history
  remains in the seed repo, not carried forward here.
