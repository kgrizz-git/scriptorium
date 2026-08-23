# Plan: MVP scaffold (M0 + M1)

Last reviewed: 2026-08-23
Date: 2026-08-23
Author: bootstrap session
Status: approved
Linked issue/PR: n/a

## Goal

Ship a runnable **Tauri desktop app** that opens a folder of scanned pages and displays them as a
**virtual flipbook** using the **page images directly**. Establish the book package format and repo
harness so M2+ (OCR, text mode, library) can extend without rework.

Full roadmap: [`2026-08-23-product-roadmap.md`](2026-08-23-product-roadmap.md).

## Out of scope (this plan)

- OCR, search, text layer (M2)
- Rendered text / hybrid modes (M3–M4)
- Multi-book library UI (M5)
- Hotspot authoring (M6)
- Web/PWA deploy (M8)
- IIIF export

## Approach

**Image-first viewer** with schema hooks for OCR and `renderMode` later.

| Choice | Decision |
|---|---|
| Shell | Tauri 2 + Vite + TypeScript |
| UI framework | React (change to Svelte only if explicitly requested) |
| Page turn | StPageFlip via `page-flip` or `react-pageflip` |
| Ingest | Tauri FS: user picks folder → natural sort → book package under app data dir |
| Package | `meta.json` + `pages/*` + empty `ocr/` + `annotations.json` stub |

## Proposed file changes

```
src-tauri/           — Tauri 2 app, Rust commands (folder pick, book I/O)
src/                 — React UI: Library placeholder, Reader, ingest flow
package.json         — pnpm, Vite, React, page-flip
src-tauri/Cargo.toml — Tauri deps
docs/book-format.md  — book package schema v1
.envrc.example       — direnv: Node, pnpm, Rust
.github/workflows/   — ci.yml: lint, typecheck, cargo check
to_do.md             — backlog index (already exists)
```

## Phases & checklist

### Phase A — Repo harness (bootstrap P3–P7)

- [ ] GitHub hygiene: document standard tier in profile / README
- [ ] Root `.pre-commit-config.yaml` aligned with `hooks/`; `pre-commit install`
- [ ] CI workflow: frontend lint/typecheck + `cargo check`
- [ ] `.envrc.example` + `.python-version` if Python OCR tooling added later
- [ ] Agent tooling contract in `AGENTS.md`; `.agent-state/` in `.gitignore`

### Phase B — Tauri + Vite scaffold

- [ ] `pnpm create tauri-app` or equivalent manual scaffold (Tauri 2 + Vite + React + TS)
- [ ] Dev command documented in README (`pnpm tauri dev`)
- [ ] Minimal app shell: title bar, empty states

### Phase C — Book package v1

- [ ] Define `docs/book-format.md` (fields: `renderMode`, pages, future `ocr` paths)
- [ ] Rust: create book from image folder (copy or reference strategy TBD)
- [ ] Rust: load book metadata + page list
- [ ] Sample fixture book in `tests/fixtures/` (small synthetic pages, gitignored if large)

### Phase D — Scan viewer (M1)

- [ ] Reader route/view: StPageFlip bound to page image URLs/paths
- [ ] Prev/next, keyboard, basic responsive layout
- [ ] “Open folder…” → ingest → open reader
- [ ] “Open book…” → load existing package
- [ ] Save last-read page index in book `meta.json` or sidecar

## Verification

- [ ] `pnpm tauri dev` opens app; user can pick a folder of images and flip pages
- [ ] Book package reloads after restart with correct page order
- [ ] CI passes on PR
- [ ] `bash scripts/check-bootstrap.sh` findings resolved or documented

## Open questions

- [ ] Copy vs symlink scanned images into book package (default: copy for portability)
- [ ] React confirmed vs Svelte

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| StPageFlip + Tauri asset paths awkward | med | med | Use convertFileSrc; spike early |
| Large scans slow first load | med | med | Thumbnails in M7; lazy load in M1 if needed |
| OCR deferred but schema wrong | low | high | Reserve `ocr/` and `renderMode` in M0 schema |

## Completion steps

When M1 is done: set Status `complete`, move to `plans/archive/`, update CHANGELOG.md,
trim `to_do.md`, keep roadmap file active.
