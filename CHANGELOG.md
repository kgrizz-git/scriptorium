# Changelog

All notable **user-facing** changes are documented here.
Developer-only detail lives in [`CHANGELOG.dev.md`](CHANGELOG.dev.md).
See [`policies/changelog-conventions.md`](policies/changelog-conventions.md).

The format follows [Keep a Changelog](https://keepachangelog.com/), and this project
uses [Semantic Versioning](https://semver.org/).

## [0.1.1] - 2026-08-23

### Added
- Product roadmap (M0–M8): scan viewer, OCR-aware scans, text/hybrid modes, library,
  authoring/hotspots, polish, platform/interop — [`plans/2026-08-23-product-roadmap.md`](plans/2026-08-23-product-roadmap.md).
- Active MVP scaffold plan and root backlog [`to_do.md`](to_do.md).
- Domain inventory for virtual books / flipbooks / OCR / annotations
  (`inventory/virtual-books-flipbook.md`).

### Changed
- Harness trimmed to standard secret hygiene only; unused domain-specific data-gate
  prompts, policies, hooks, and CI examples removed. Project profile captured for
  Scriptorium (Tauri-first virtual book app).

## [0.1.0] - 2026-08-23

### Added
- Initialized **Scriptorium** from `kgrizz-git/project-seed-template` (harness baseline:
  prompts, policies, hooks, CI examples, inventories). Private GitHub remote created;
  full project bootstrap still pending.
