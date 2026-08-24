# Policy: Changelog Conventions (Public + Developer)

Last reviewed: 2026-08-24
Enforced by: convention + release hygiene (orchestrator / humans). See also
[`VERSION`](../VERSION) and root [`CHANGELOG.md`](../CHANGELOG.md).

## Why

Users and operators need a short, trustworthy story of what changed. Developers and
agents need a fuller record (tests, CI, refactors, inventory) that would clutter a
public release note. Split audiences so neither document lies by omission or noise.

## Dual-track model (recommended)

| Track | File (default) | Audience | Contents |
|---|---|---|---|
| **Public / user-facing** | `CHANGELOG.md` | Users, operators, release notes | User-visible features, fixes, breaking changes, migrations |
| **Developer / internal** | `CHANGELOG.dev.md` (optional) | Maintainers, agents | Tests added, CI/hooks, inventory, docs-only, refactors with no user impact |

If the project is template-only or early and has no external users, a single
`CHANGELOG.md` is fine — keep entries honest about impact, and promote to dual-track
when you ship to others.

### What goes where

**Public `CHANGELOG.md`**

- Added / Changed / Deprecated / Removed / Fixed / Security that affect callers or UX
- Breaking changes and migration notes
- Dependency upgrades that change runtime behavior or security posture

**Developer `CHANGELOG.dev.md`** (or a `### Internal` subsection if you keep one file)

- New or expanded tests, fixtures, coverage gates
- CI workflow / pre-commit / policy-hook changes (including SAST/secret-scan tooling)
- Inventory and prompt/template updates with no product behavior change
- Pure refactors, renames, doc freshness, agent stub files

**Security and maintenance (pick one destination; never both)**

| Kind of work | Log in |
|---|---|
| User-visible security fix or posture change (affects callers, UX, or shipped product) | Public `CHANGELOG.md` under `### Security` (or Fixed/Changed as appropriate) |
| Harness/CI security tooling with no product behavior change | `CHANGELOG.dev.md` |
| Operational maintenance (infra upkeep, non-release secret/cert rotation, recurring ops hygiene) | `MAINTENANCE.md` (create if needed) |

Never put secrets, tokens, or private URLs in either changelog or `MAINTENANCE.md`.

## SemVer impact

Use an `## [Unreleased]` section at the top of each applicable changelog for work that has
landed but is not released. When cutting a release, move those bullets into a dated version
section and bump [`VERSION`](../VERSION) in the same change. Do not bump the version merely for
an ordinary commit.

Choose the release bump from the public impact:

| Bump | When |
|---|---|
| **MAJOR** | Breaking public API / CLI / config / data format |
| **MINOR** | Backward-compatible user-visible feature or capability |
| **PATCH** | Bugfix, security patch, or docs/tooling that does not change product behavior |

Developer-only changes that do not alter product behavior are usually **PATCH** (or
unchanged version if you only commit inventory mid-cycle — prefer PATCH when releasing).

## Entry format

Follow [Keep a Changelog](https://keepachangelog.com/). Example public entry:

```markdown
## [1.2.0] - 2026-07-09

### Added
- Export reports as CSV from the dashboard.

### Fixed
- Login redirect loop on expired sessions.
```

Example developer entry:

```markdown
## [1.2.0] - 2026-07-09

### Added
- Pre-commit hook `check-todo-limits` (soft gate at 150 lines).
- CI: Semgrep OWASP ruleset on PRs.

### Changed
- Inventory: Graphify + NetworkX under knowledge-graph-code-mapping.
```

## Agent rules

1. Log every meaningful completion exactly once. Skip changelog or maintenance entries only for
   truly trivial edits, such as a typo or formatting-only change.
2. When product behavior changes (including user-visible security fixes), update the **public**
   changelog under `Unreleased`; bump `VERSION` when that work is released.
3. When only harness/inventory/tests/CI change, update **developer** changelog (or
   Internal section); use `Unreleased` until you cut a release, then bump PATCH if appropriate.
4. Use `MAINTENANCE.md` only for operational maintenance (infra upkeep, non-release rotations,
   recurring ops hygiene). Do **not** route user-visible security patches or CI/SAST harness
   work there — those belong in `CHANGELOG.md` or `CHANGELOG.dev.md` per the table above.
   Never log the same completion in both a changelog and `MAINTENANCE.md`.
5. Do not invent user-facing bullets for internal work.
6. Link PRs/issues when helpful; keep bullets scannable (one idea each).
