# Developer Changelog

Internal / developer-facing changes that do not belong in the public
[`CHANGELOG.md`](CHANGELOG.md). See [`policies/changelog-conventions.md`](policies/changelog-conventions.md).

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
