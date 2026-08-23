# Plan: M1 — Scan viewer (first product milestone)

Last reviewed: 2026-08-23
Date: 2026-08-23
Author: bootstrap session
Status: draft
Linked issue/PR: n/a
Depends on: [`2026-08-23-m0-tauri-foundation.md`](2026-08-23-m0-tauri-foundation.md) complete
Follows: product roadmap M1

## Goal

Deliver the **first usable product slice**: a librarian/curator can **open a folder of scanned page
images**, Scriptorium builds a **book package**, and the visitor (or same user) can **flip through
faithful page images** in a virtual book. UX priorities: reliability and correctness over polish.

## Out of scope

- OCR, search, select/copy text layer (M2)
- Rendered text / hybrid modes (M3–M4)
- Multi-book library UI beyond “open another book” (M5)
- Hotspot authoring / lore popups (M6)
- Deep-zoom, figure extraction, heavy texture art (M7)
- Web/PWA / IIIF (M8)
- Full M0.5 quality matrix unless already cheap from M0

## Approach

**Image-first reader.** Pages are the scan files themselves (JPEG/PNG/WebP), displayed via
**StPageFlip** (`page-flip` / `react-pageflip`). Ingest uses Tauri dialog + filesystem APIs:
natural-sort image files → **copy** into a book package (portable default) under a known library
root (app data or user-chosen — decide in Phase 0 spike). Schema from M0 `docs/book-format.md`.

Spike **early**: `convertFileSrc` (or asset protocol) so flipbook can load local page paths inside
the webview.

### Alternatives considered

| Option | Why not chosen for M1 |
|---|---|
| PDF-only ingest | User model is folder-of-scans; PDF can be M7+ |
| Symlink pages into package | Breaks when source folder moves; copy is safer default |
| IIIF / OpenSeadragon as primary UI | Wrong metaphor for “book”; optional later for inspect |
| Full library shelf UI | YAGNI; open folder + reopen package is enough |

## Acceptance criteria (done when)

1. User runs the desktop app and chooses **Open folder…**
2. App creates a book package conforming to `docs/book-format.md` with ordered pages
3. Flipbook shows **scan images** (not placeholder HTML) with turn animation
4. Keyboard and on-screen next/prev work; last-read page persists across relaunch
5. User can **Open book…** pointing at an existing package directory
6. Corrupt/empty folder fails with a clear error (no crash)

## Proposed file changes

```
src-tauri/src/book/          — create_book_from_folder, load_book, save_progress
src-tauri/src/lib.rs / commands — #[tauri::command] wrappers + error types
src/features/reader/         — FlipbookView (StPageFlip), page URL resolution
src/features/home/           — Open folder / Open book actions
src/lib/bookTypes.ts         — TS types mirroring meta.json
docs/book-format.md          — amend if I/O reveals gaps (keep versioned)
tests/                       — Rust unit tests for sort/package; optional TS smoke
README.md                    — “Try it” with fixture folder instructions
```

## Phases & checklist

### Phase 0 — Path & package spike (time-box ≤ half day)

- [ ] Confirm library root: app-data `books/` vs user-picked parent folder
- [ ] Prove one local image loads in webview via Tauri asset/convertFileSrc
- [ ] Prove StPageFlip renders ≥2 images in Tauri webview
- [ ] Record spike notes in `.context/` (gitignored) or short ADR if decisions stick

### Phase 1 — Book I/O (Rust)

- [ ] Natural sort of image extensions (`.jpg`, `.jpeg`, `.png`, `.webp`; case-insensitive)
- [ ] `create_book_from_folder(src, dest)` → copy pages, write `meta.json`, stub `ocr/`,
      empty `annotations.json`
- [ ] `load_book(path)` → validate schema, return metadata + ordered page paths
- [ ] `set_last_read_page(path, index)` / read on load
- [ ] Unit tests: sort order, reject empty folder, reject unsupported-only folder

### Phase 2 — Commands + UI wiring

- [ ] Tauri commands + permissions (dialog, fs scope for library root)
- [ ] Home: Open folder → progress/status → navigate to reader
- [ ] Home: Open book → validate → reader
- [ ] Error toasts/dialogs for user-visible failures

### Phase 3 — Flipbook reader

- [ ] StPageFlip bound to page list (cover mode if trivial; else soft pages)
- [ ] Next/prev controls + Left/Right (or space) keyboard
- [ ] Persist page index on flip (debounce writes)
- [ ] Basic empty/loading states; no “library grid” yet

### Phase 4 — Docs & handoff

- [ ] README: how to run + how to test with a local scan folder
- [ ] Changelog 0.2.0 (or 0.1.x) user-facing notes
- [ ] Update `to_do.md` / roadmap M1 checkboxes; archive this plan when verified

## Verification

- [ ] Manual: folder with 4–10 mixed-case numbered images → correct order in flipbook
- [ ] Manual: relaunch → opens at last page
- [ ] Manual: open existing package without re-ingest
- [ ] `cargo test` for book module; CI still green
- [ ] No secrets or absolute user home paths committed in fixtures

## Open questions

- [ ] Max pages soft-warn in M1? (defer hard limits; note large-book risk)
- [ ] HEIC support? (defer; document unsupported)
- [ ] Single-page vs spread on wide screens (StPageFlip defaults OK for M1)

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| StPageFlip + Tauri file URLs fail | med | high | Phase 0 spike; fallback `<img>` strip if blocked |
| Huge scans OOM / slow open | med | med | Document; lazy-load later (M7); copy progress UI |
| Schema drift TS vs Rust | med | med | Single `docs/book-format.md`; generate or hand-sync types |
| Scope creep into OCR/hotspots | high | med | Out-of-scope list; reject in review |

## Completion steps

1. Status → `complete`; move to `plans/archive/completed/`
2. `CHANGELOG.md` user-facing; bump `VERSION` to **0.2.0**
3. Roadmap M1 items `[x]`; `to_do.md` prune
4. Kick M0.5 harness follow-ups if not already done during M0/M1

## Related

- Prerequisite: [`2026-08-23-m0-tauri-foundation.md`](2026-08-23-m0-tauri-foundation.md)
- Roadmap: [`2026-08-23-product-roadmap.md`](2026-08-23-product-roadmap.md)
- Domain menu: [`inventory/virtual-books-flipbook.md`](../inventory/virtual-books-flipbook.md)
- Profile: `.context/project-profile.md`
