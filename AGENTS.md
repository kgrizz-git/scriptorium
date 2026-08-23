# AGENTS.md

Last reviewed: 2026-08-23

Single source of truth for AI coding agents working in this repository. Other agent
entrypoints (`CLAUDE.md`, `GEMINI.md`, `QWEN.md`, `.github/copilot-instructions.md`,
`.cursor/rules/`, `.windsurf/rules/`) are thin pointers back to this file.

> **Scriptorium** — project repo initialized from `project-seed-template`. Until
> bootstrap finishes, treat harness assets (prompts, policies, hooks, CI guidance,
> templates, inventories) as the working surface. Keep additions small, durable, and
> discoverable. Prefer [`prompts/bootstrap-project.md`](prompts/bootstrap-project.md)
> before inventing a large application scaffold.

## Read this first (thin entry → deep docs)

**Quick navigation:** See [`docs/NAVIGATION.md`](docs/NAVIGATION.md) for a role-based guide to finding documentation.

Do not load everything. Start here, then open only what the task needs.

| If you are… | Read |
|---|---|
| Starting a new project from this template | [`prompts/bootstrap-project.md`](prompts/bootstrap-project.md) (+ tick-list [`prompts/bootstrap-checklist.md`](prompts/bootstrap-checklist.md), decision cards [`prompts/bootstrap/`](prompts/bootstrap/)) |
| Resuming or auditing a bootstrap | `.context/bootstrap-state.md` (from [`templates/bootstrap-state.md`](templates/bootstrap-state.md)), then `bash scripts/check-bootstrap.sh` |
| Starting a work session on an existing project | [`prompts/new-agent-session.md`](prompts/new-agent-session.md) |
| Moving work between agents or IDEs | [`templates/handoff.md`](templates/handoff.md) → `.context/handoff.md` |
| Choosing code-intelligence / MCP tooling | [`inventory/agent-tooling-efficiency.md`](inventory/agent-tooling-efficiency.md), [`policies/agent-tooling-contract.md`](policies/agent-tooling-contract.md) |
| Capturing what kind of project this is | [`prompts/project-init-profile.md`](prompts/project-init-profile.md) |
| Running periodic repo health checks | [`prompts/maintenance-loop.md`](prompts/maintenance-loop.md) |
| Looking for a tool / library / service | [`inventory/README.md`](inventory/README.md) (a menu, not a checklist) |
| Adding/enforcing repo rules | [`policies/README.md`](policies/README.md) |
| Wiring local checks | [`hooks/README.md`](hooks/README.md) |
| Setting up CI | [`ci/README.md`](ci/README.md) |
| Working with PII, PHI, medical/FHIR/HL7/DICOM, or regulated data | [`prompts/strict-phi-agent-guidance.md`](prompts/strict-phi-agent-guidance.md) **before editing or configuring tools** |
| Making sure code doesn't leak sensitive data at runtime (logs, temp files, caches, test/CI output, telemetry) | [`prompts/sensitive-data-leak-prevention.md`](prompts/sensitive-data-leak-prevention.md) |
| Checking Actions minutes / storage | [`ci/scripts/check_gha_usage.py`](ci/scripts/check_gha_usage.py), [`policies/github-actions-usage.md`](policies/github-actions-usage.md) |
| Checking open PRs after push / daily | [`ci/scripts/check_open_prs.py`](ci/scripts/check_open_prs.py), [`policies/commits-and-branches.md`](policies/commits-and-branches.md) |
| Writing a plan / design / review | [`templates/`](templates/) and [`prompts/`](prompts/) |
| Installing skills or subagents | [`inventory/catalog-skills-agents.md`](inventory/catalog-skills-agents.md) |
| Choosing an orchestration approach | [`inventory/harness-engineering.md`](inventory/harness-engineering.md) |

## Operating principles

1. **Menu, not mandate.** Inventories list options; choose the minimal useful set per project.
2. **Thin entry, deep docs.** Keep this file short; push detail into linked docs.
3. **Interview before scaffolding.** Ask the user goals/constraints before writing many files.
4. **Verify, don't guess.** Prefer running tools and reading files over assuming.
5. **Policy as code where it pays.** Encode durable rules as checks with clear remediation.
6. **Temporary stays temporary.** Put scratch plans/research in `.context/` (gitignored).
7. **Protect remotes.** Push only to this project's `origin` (`kgrizz-git/scriptorium`),
   never to `project-seed-template`.
8. **Clean up after completion.** Remove completed TODOs, log completions appropriately,
   archive completed plans, and clean scratch files. See [`policies/plans-and-todos.md`](policies/plans-and-todos.md)
   and [`prompts/cleanup-completed-work.md`](prompts/cleanup-completed-work.md).
9. **Recommendations stand on their own.** A reader without access to any external source
   should still be able to act on what a file says. Referencing private or personal repos is
   encouraged — cite them by `repo → path` and mark them private; an agent that *does* have
   access should go read them. Just don't let the advice become unusable without them.
10. **Progress is written down, not remembered.** Multi-phase work records state in `.context/`
    as it goes. A session that ends mid-task leaves a `Next action`, not a gap.

## Repo map

- `prompts/` — reusable prompts (bootstrap, refactor, docs audit, subagent workflow, reviews).
- `prompts/bootstrap/` — per-topic decision cards (ask → branch → produce → done when) for the
  bootstrap phases that have a real branch.
- `templates/` — fill-in artifacts (briefs, plans, designs, ADRs, runbooks, releases, reviews, assessments).
- `policies/` — durable repo rules (file size/counts, plans/todos, changelogs, doc freshness, commits, security).
- `hooks/` — pre-commit config + policy-check scripts (file size, TODO limits, secrets, lint).
- `ci/` — CI selection guidance and example workflows.
- `inventory/` — curated indexes of tools, skills, MCP servers, references (install-on-demand).
- `docs/` — navigation helpers and quick-reference guides.
- `scripts/` — automation scripts (setup, health check, environment validation).
- `plans/` — (when adopted) active implementation plans; archive completed ones under `plans/archive/`.
- `hooks/scripts/check_sensitive_data.py` — opt-in strict medical-data gate; scans every tracked file and requires exact human approval for opaque files.
- `hooks/scripts/check_gitignore_protected.py`, `check_forbidden_paths.py`, `check_scan_contract.py` — opt-in structural sensitive-data gates (see `policies/sensitive-data-scan-gates.md`).
- `inventory/medical-data-security.md` — strict guard setup and medical-data scanner menu.
- `.cursor/`, `.windsurf/` — editor rule sets (CodeGuard security rules).
- `.devin/` — Devin CLI configuration and project-specific skills.
- `.context/` — scratch only; never required reading, never committed.

## Conventions (changelog, plans, sizes)

| Topic | Where documented |
|---|---|
| Public vs developer changelogs + SemVer | [`policies/changelog-conventions.md`](policies/changelog-conventions.md) |
| Plans lifecycle, marking done, archiving, `to_do` caps | [`policies/plans-and-todos.md`](policies/plans-and-todos.md) |
| Source/doc line caps (soft **600** / hard **1000**) | [`policies/file-size-and-counts.md`](policies/file-size-and-counts.md) |
| Secret scanning + lint hooks | [`hooks/README.md`](hooks/README.md), [`policies/security-baseline.md`](policies/security-baseline.md) |
| GitHub Actions minutes/storage (estimate before expanding CI) | [`policies/github-actions-usage.md`](policies/github-actions-usage.md), [`ci/scripts/check_gha_usage.py`](ci/scripts/check_gha_usage.py) |
| Open PRs after push (advisory, not a hook) | [`policies/commits-and-branches.md`](policies/commits-and-branches.md), [`ci/scripts/check_open_prs.py`](ci/scripts/check_open_prs.py) |
| Strict PII/PHI controls, approval inventory, and agent behavior | [`prompts/strict-phi-agent-guidance.md`](prompts/strict-phi-agent-guidance.md), [`inventory/medical-data-security.md`](inventory/medical-data-security.md) |
| Runtime/dev leak prevention (redaction, temp files, caches, telemetry, easy clearance) | [`prompts/sensitive-data-leak-prevention.md`](prompts/sensitive-data-leak-prevention.md) (how), [`policies/sensitive-data-runtime-leaks.md`](policies/sensitive-data-runtime-leaks.md) (rule + tiers) |
| Structural sensitive-data gates (protected `.gitignore`, forbidden tracked paths, heavy-scanner contract/ledger) | [`policies/sensitive-data-scan-gates.md`](policies/sensitive-data-scan-gates.md) |
| Setup, health check, environment validation | [`scripts/setup.sh`](scripts/setup.sh), [`scripts/health-check.sh`](scripts/health-check.sh), [`scripts/validate-env.sh`](scripts/validate-env.sh) |
| Bootstrap completeness (evidence, not claims) | [`scripts/check-bootstrap.sh`](scripts/check-bootstrap.sh) |
| Agent tooling: one tool per role, `.agent-state/` untracked, smoke tests | [`policies/agent-tooling-contract.md`](policies/agent-tooling-contract.md) (rule), [`inventory/agent-tooling-efficiency.md`](inventory/agent-tooling-efficiency.md) (menu) |
| Tool-catalog staleness (dead links, renamed projects) | [`ci/scripts/check_doc_links.py`](ci/scripts/check_doc_links.py), [`policies/doc-freshness.md`](policies/doc-freshness.md) |

**Notes_and_Ideas vs this template:** personal research dumps, private key dashboards, and
exploratory idea notes belong in a Notes_and_Ideas (or similar) repo. Index only durable,
reusable menus and conventions here.

## Agent compatibility

This file follows the [AGENTS.md](https://agents.md) convention and is read (directly or via
a thin pointer) by Claude Code, OpenAI Codex/GPT, Cursor, Gemini/Antigravity, Qwen, DeepSeek,
MiniMax, opencode, Windsurf, and GitHub Copilot. When adding tool-specific behavior, keep the
durable rule here and let the per-tool file point to it.
