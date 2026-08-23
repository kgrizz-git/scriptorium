# Scriptorium

Last reviewed: 2026-08-23

Private project repository. Bootstrapped from
[`kgrizz-git/project-seed-template`](https://github.com/kgrizz-git/project-seed-template)
(harness: policies, hooks, CI examples, templates, and curated inventories).

**Next:** run [`prompts/bootstrap-project.md`](prompts/bootstrap-project.md) to interview,
capture a project profile, and scaffold what this repo needs.

**Returning sessions:** run [`prompts/new-agent-session.md`](prompts/new-agent-session.md).

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
| [`plans/`](plans/) | Optional active plans + archive convention (see policies) |

Full contents: see [`inventory/README.md`](inventory/README.md) for the tool/skill menu and [`AGENTS.md`](AGENTS.md) for agent navigation.

Changelogs: user-facing [`CHANGELOG.md`](CHANGELOG.md); developer/internal [`CHANGELOG.dev.md`](CHANGELOG.dev.md) — see [`policies/changelog-conventions.md`](policies/changelog-conventions.md).

GitHub setup and sensitive-data controls: [`policies/github-repository-hygiene.md`](policies/github-repository-hygiene.md).
