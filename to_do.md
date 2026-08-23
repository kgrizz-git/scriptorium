# Scriptorium backlog

Last reviewed: 2026-08-23

Prioritized index. **Active work:** [`plans/2026-08-23-mvp-scaffold.md`](plans/2026-08-23-mvp-scaffold.md).
**Full roadmap:** [`plans/2026-08-23-product-roadmap.md`](plans/2026-08-23-product-roadmap.md).
**CI/hooks guide:** [`docs/ci-and-hooks.md`](docs/ci-and-hooks.md).

## Now (M0 + M1)

- [x] Bootstrap CI + hooks (policy, lint, complexity, gitleaks, Semgrep) — [`docs/ci-and-hooks.md`](docs/ci-and-hooks.md)
- [x] Pre-push typecheck (`basedpyright`) — install with `pre-commit install --hook-type pre-commit --hook-type pre-push`
- [ ] Finish M0 harness leftovers: `.envrc.example`, agent tooling contract in `AGENTS.md`
- [ ] Tauri 2 + Vite + React + TS scaffold — [Phase B](plans/2026-08-23-mvp-scaffold.md#phase-b--tauri--vite-scaffold)
- [ ] Book package v1 (`meta.json`, `pages/`, schema hooks for OCR) — [Phase C](plans/2026-08-23-mvp-scaffold.md#phase-c--book-package-v1)
- [ ] Folder ingest + StPageFlip scan viewer — [Phase D](plans/2026-08-23-mvp-scaffold.md#phase-d--scan-viewer-m1)

## Next after Tauri lands (M0.5 — harness follow-ups)

Do these when app source exists; details in [roadmap M0.5](plans/2026-08-23-product-roadmap.md#m05--harness-follow-ups-after-tauri-scaffold--when-app-code-exists).

- [ ] CI + pre-push: TypeScript lint + `tsc --noEmit`
- [ ] CI + hooks: `cargo fmt` / `clippy` / `test` / `check`
- [ ] Vitest (+ coverage); raise app coverage gate
- [ ] Rust test coverage when useful
- [ ] Raise Python harness `fail_under` once scripts have in-process tests
- [ ] Optional CodeQL; Dependabot for npm/cargo/Actions
- [ ] GitHub required checks for CI + Semgrep jobs

## Next product (M2 — OCR on scans)

- [ ] OCR pipeline + per-page bbox JSON
- [ ] Search across book; jump to hits
- [ ] Select/copy via aligned text layer on scan view
- [ ] Background OCR job + progress UI

## Later (product — see roadmap)

| Milestone | Summary |
|---|---|
| **M3** | Rendered **text mode** (clean typography, copy, enrichment) |
| **M4** | **Hybrid** mode + scan/text toggle |
| **M5** | **Library** — multiple books, browse, portable bundles |
| **M6** | **Authoring** — region hotspots, lore popups, long-press |
| **M7** | Figure extraction, deep-zoom, texture polish, perf |
| **M8** | Web/PWA, IIIF interop, optional hosted CMS, advanced OCR |

## Decisions pending

- [ ] React vs Svelte (default: React)
- [ ] OCR runtime: Rust/Tesseract vs batch CLI vs WASM (decide during M2)

## Recently done

- [x] P0/P1 discovery + project profile (2026-08-23)
- [x] Product roadmap + backlog recorded (2026-08-23)
- [x] CI/hooks baseline + `tmp/` (2026-08-23)
- [x] Pre-push basedpyright (2026-08-23)
