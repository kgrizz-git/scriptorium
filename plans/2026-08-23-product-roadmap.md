# Plan: Scriptorium product roadmap

Last reviewed: 2026-08-23
Date: 2026-08-23
Author: bootstrap session
Status: approved
Linked issue/PR: n/a

## Goal

Single source of truth for **all** planned product phases and features. Immediate work lives in
[`2026-08-23-mvp-scaffold.md`](2026-08-23-mvp-scaffold.md). Later milestones stay here and in
[`to_do.md`](../to_do.md) until promoted to an active plan.

## Rendering model (long-term)

Three layers, not a single rendering choice:

| Layer | Role |
|---|---|
| **Page images** | Canonical visual record (scanned JPEG/PNG/WebP). Always retained. |
| **OCR + geometry** | Per-page text with word/line bounding boxes (JSON, hOCR, or ALTO). Powers search, select, copy on scans. |
| **Annotations** | Hotspots, lore popups, curator enrichment (W3C Web Annotation–friendly JSON). |

**Reader modes** (book-level `renderMode`, extensible):

| Mode | User sees | When |
|---|---|---|
| `scan` | Flipbook over page images (default MVP) | Authentic book feel |
| `scan+ocr` | Same images + invisible/selectable text layer + search | After M2 |
| `text` | Reflowed or fixed-layout rendered text | M3 — cleaner reading, copy, enrichment |
| `hybrid` | Toggle or split: scan + text side-by-side or overlaid | M4 |

## Milestones

### M0 — Harness & scaffold (in progress)

**Active plan:** [`2026-08-23-mvp-scaffold.md`](2026-08-23-mvp-scaffold.md)

- [ ] Complete bootstrap P3–P7 (hooks, CI, env, agent contract)
- [ ] Tauri 2 + Vite + TypeScript UI shell (React default unless changed)
- [ ] Book package format v1 on disk (`meta.json`, `pages/`, schema reserves `renderMode`, `ocr/`)
- [ ] Minimal docs: README run instructions

### M1 — Scan viewer (MVP core)

**Target:** one book from a folder of scans; page-turn; faithful page images.

- [ ] Tauri command: pick folder → natural sort → copy/link into book package
- [ ] StPageFlip (or `react-pageflip`) viewer over page images
- [ ] Paper/book chrome (texture, spread, cover — iterate on UX)
- [ ] Persist last-read page per book
- [ ] Open existing book package from disk

**Out of scope for M1:** library, authoring UI, OCR, hotspots, web deploy.

### M2 — OCR-aware scans (text under the image)

**Target:** app is “aware” of text while still showing scans; search, select, copy.

- [ ] OCR pipeline (evaluate: Tesseract via Rust sidecar vs batch CLI vs tesseract.js)
- [ ] Store per-page OCR: plain text + word/line `bbox` JSON
- [ ] Full-text search UI; jump to page/highlight hit
- [ ] Transparent text layer aligned to scan (select + copy)
- [ ] Background OCR job with progress (re-run when pages change)
- [ ] Book metadata: `ocrStatus`, `ocrEngine`, `ocrGeneratedAt`

### M3 — Rendered text mode

**Target:** optional clean text reading view for enrichment and accessibility.

- [ ] `renderMode: text` reader (fixed-layout first; reflow later if needed)
- [ ] Preserve links to page numbers / scan view for “show original”
- [ ] Curator-friendly editing surface for lore tied to text spans (prep for M5)
- [ ] Export/copy plain text per page or whole book

### M4 — Hybrid & mode switching

- [ ] In-app toggle: scan | text | hybrid (split or overlay)
- [ ] Remember user preference per book or globally
- [ ] Sync selection between text and scan when geometry allows

### M5 — Library & multi-book

- [ ] Library home: grid/list of books (cover thumbnail, title, progress)
- [ ] Create / import / remove books
- [ ] Standalone book bundles (portable folder or `.scriptorium` archive)
- [ ] Optional shelves/collections tags in `meta.json`

### M6 — Authoring & hotspots

**Audience:** librarians and gallery directors.

- [ ] Author mode: draw region on page (`xywh` or polygon)
- [ ] Attach lore popup content (markdown/HTML, images, links)
- [ ] Long-press on touch / click on desktop → popup
- [ ] Import/export annotations JSON (interchange with IIIF-style bodies later)

### M7 — Polish & extraction

- [ ] Figure/image extraction from page regions (crop to assets)
- [ ] Deep-zoom inspect on a page or region (OpenSeadragon-style panel)
- [ ] Enhanced paper texture, lighting, hard covers (StPageFlip hard pages)
- [ ] Performance: lazy load pages, thumbnail strip, large book handling

### M8 — Platform & interop (later)

- [ ] PWA or static web build of reader (read-only first)
- [ ] IIIF Presentation export/import (optional GLAM interop)
- [ ] Hosted multi-user CMS / sync (only if product needs it)
- [ ] Optional vector semantic search over OCR (separate from page-image fidelity)
- [ ] OCR engine upgrade path (e.g. PaddleOCR) if Tesseract quality insufficient

## Book package schema (evolving)

Documented in code when scaffold lands; roadmap fields:

```json
{
  "id": "uuid",
  "title": "string",
  "renderMode": "scan",
  "defaultView": "scan",
  "pages": [{ "index": 1, "image": "pages/001.jpg", "ocr": "ocr/001.json" }],
  "annotations": "annotations.json",
  "createdAt": "ISO-8601",
  "updatedAt": "ISO-8601"
}
```

## Open questions (roadmap)

- [ ] React vs Svelte for Vite UI (default React at scaffold)
- [ ] OCR runtime: in-app Rust/Tesseract vs external batch vs WASM
- [ ] Fixed-layout text vs reflow for M3 (likely fixed-layout first for scanned books)

## Related docs

- [`.context/project-profile.md`](../.context/project-profile.md) — stack and constraints
- [`inventory/virtual-books-flipbook.md`](../inventory/virtual-books-flipbook.md) — library menu
- [`to_do.md`](../to_do.md) — prioritized backlog index
