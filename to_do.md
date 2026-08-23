# Scriptorium backlog

Last reviewed: 2026-08-23

**Active plans (in order):**
1. [`plans/2026-08-23-m0-tauri-foundation.md`](plans/2026-08-23-m0-tauri-foundation.md) — Tauri shell + book schema
2. [`plans/2026-08-23-m1-scan-viewer.md`](plans/2026-08-23-m1-scan-viewer.md) — first product milestone (scan flipbook)

**Roadmap:** [`plans/2026-08-23-product-roadmap.md`](plans/2026-08-23-product-roadmap.md) ·
**CI/hooks:** [`docs/ci-and-hooks.md`](docs/ci-and-hooks.md)

## Now

- [ ] Address M0/M1 plan-review top 5 (esp. pre-M1 flipbook spike ADR); review notes live under gitignored `tmp/` — do not link from tracked docs
- [ ] Revise M0/M1 plans per review; then execute M0 → M1
- [x] Plan folder layout: `deferred/`, `archive/completed/`, `archive/superseded/` + AGENTS/policy

## Next after Tauri lands (M0.5 — harness follow-ups)

See [roadmap M0.5](plans/2026-08-23-product-roadmap.md#m05--harness-follow-ups-after-tauri-scaffold--when-app-code-exists).

- [ ] CI + pre-push: TypeScript lint + `tsc --noEmit`
- [ ] CI + hooks: `cargo fmt` / `clippy` / `test` / `check`
- [ ] Vitest (+ coverage); raise app coverage gate
- [ ] Rust test coverage when useful
- [ ] Raise Python harness `fail_under` once scripts have in-process tests
- [ ] Optional CodeQL; Dependabot for npm/cargo/Actions
- [ ] GitHub required checks for CI + Semgrep jobs

## Next product (M2 — OCR on scans)

- [ ] OCR pipeline + per-page bbox JSON
- [ ] Search; select/copy via text layer on scans
- [ ] Background OCR + progress UI

## Later (product)

| Milestone | Summary |
|---|---|
| **M3** | Rendered text mode |
| **M4** | Hybrid mode + toggle |
| **M5** | Multi-book library |
| **M6** | Authoring + hotspot lore popups |
| **M7** | Figure extraction, deep-zoom, polish |
| **M8** | Web/PWA, IIIF, optional CMS, advanced OCR |

## Decisions pending

- [ ] React vs Svelte (default: React in M0 plan)
- [ ] Library root: app-data vs user-picked (spike in M1 Phase 0)
- [ ] OCR runtime (decide at M2)

## Recently done

- [x] CI/hooks baseline + pre-push basedpyright + `tmp/`
- [x] Product roadmap; split M0/M1 plans from combined mvp-scaffold
