# Scriptorium

Last reviewed: 2026-08-23

Tauri-first app for assembling scanned page folders into textured virtual books
(page-turn reading, faithful page images, curator hotspots with lore popups) and
browsing a multi-book library. Built for librarians and gallery directors (authors)
and visitors/students (readers).

Bootstrapped from [`kgrizz-git/project-seed-template`](https://github.com/kgrizz-git/project-seed-template).
Private for now; public soon. Profile: `.context/project-profile.md` (local).

**Agent sessions:** [`prompts/new-agent-session.md`](prompts/new-agent-session.md).
**Roadmap:** [`plans/2026-08-23-product-roadmap.md`](plans/2026-08-23-product-roadmap.md) · **Backlog:** [`to_do.md`](to_do.md).
**CI & hooks:** [`docs/ci-and-hooks.md`](docs/ci-and-hooks.md).
**Domain menu:** [`inventory/virtual-books-flipbook.md`](inventory/virtual-books-flipbook.md).

---

## What's here and why

| Directory | What it is |
|---|---|
| [`prompts/`](prompts/) | Reusable agent prompts: bootstrap, session-start, maintenance, reviews, audits |
| [`templates/`](templates/) | Fill-in artifacts: briefs, plans, designs, ADRs, runbooks, release checklists, reviews, assessments |
| [`policies/`](policies/) | Durable repo rules: file size, plans/todos, changelogs, doc freshness, commits, security, GC |
| [`hooks/`](hooks/) | Pre-commit config + policy scripts (file size, TODO limits, secrets, lint) |
| [`ci/`](ci/) | CI selection guidance and example GitHub Actions workflows |
| [`inventory/`](inventory/) | Curated menus of tools, skills, platforms, libraries, and references — load what you need |
| [`plans/`](plans/) | Product roadmap, active MVP plan, archived completed plans |

Full contents: see [`inventory/README.md`](inventory/README.md) and [`AGENTS.md`](AGENTS.md).

Changelogs: [`CHANGELOG.md`](CHANGELOG.md) / [`CHANGELOG.dev.md`](CHANGELOG.dev.md).
GitHub hygiene: [`policies/github-repository-hygiene.md`](policies/github-repository-hygiene.md).
