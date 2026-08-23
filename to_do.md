# Scriptorium backlog

Last reviewed: 2026-08-23

Prioritized index. **Active work:** [`plans/2026-08-23-mvp-scaffold.md`](plans/2026-08-23-mvp-scaffold.md).
**Full roadmap:** [`plans/2026-08-23-product-roadmap.md`](plans/2026-08-23-product-roadmap.md).

## Now (M0 + M1)

- [ ] Bootstrap harness: pre-commit, CI, `.envrc.example`, agent contract — see [mvp-scaffold Phase A](plans/2026-08-23-mvp-scaffold.md#phase-a--repo-harness-bootstrap-p3p7)
- [ ] Tauri 2 + Vite + React + TS scaffold — [Phase B](plans/2026-08-23-mvp-scaffold.md#phase-b--tauri--vite-scaffold)
- [ ] Book package v1 (`meta.json`, `pages/`, schema hooks for OCR) — [Phase C](plans/2026-08-23-mvp-scaffold.md#phase-c--book-package-v1)
- [ ] Folder ingest + StPageFlip scan viewer — [Phase D](plans/2026-08-23-mvp-scaffold.md#phase-d--scan-viewer-m1)

## Next (M2 — OCR on scans)

- [ ] OCR pipeline + per-page bbox JSON
- [ ] Search across book; jump to hits
- [ ] Select/copy via aligned text layer on scan view
- [ ] Background OCR job + progress UI

## Later (see roadmap)

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
