# Policy: GitHub Repository Hygiene & Secret Gates

Last reviewed: 2026-08-23
Enforced by: GitHub rulesets/branch protection, hooks, CI, and selected GitHub Apps.

## Purpose

Set a small, enforceable GitHub baseline before a repository receives real work. Scale it
to the data it may contain: a public utility needs less process than a confidential
business repo, but neither should accept direct pushes, red CI, credentials, customer
exports, or machine-specific paths by accident.

This policy complements [`security-baseline.md`](security-baseline.md). It does **not** make
a project compliance-certified. Obtain the organization's privacy, security, legal, and
compliance decisions before committing customer data or sending repository contents to a
third-party service.

## 1. Classify before configuring

Capture the intended data classification in `.context/project-profile.md` and choose a tier.
If the answer is unknown, use the more protective tier until it is resolved.

| Tier | Use when | Minimum decision |
|---|---|---|
| Public | Open-source code and public/synthetic test data only | State that production credentials, customer exports, and internal-only material are prohibited. |
| Internal | Team code, internal designs, or non-public documentation | State what may enter the repo; prohibit real credentials and production exports unless an approved handling design exists. |
| Confidential | Customer data, credentials, business-confidential designs, or financial records | Treat real customer/credential data as prohibited unless an approved data-handling design says otherwise; document who owns exceptions and how leaks are contained. |

**Data rule:** source control is not a data store. Do not commit production dumps, support
tickets, screenshots with secrets, chat transcripts, database backups, or unreviewed exports.
Use deterministic synthetic fixtures and document their provenance.

For confidential repositories, also document: permitted data classes, where scans run, who
can read workflow logs/artifacts, retention periods, encryption and key ownership, approved
subprocessors, and a breach/escalation contact. Do not upload candidate sensitive content to a
third-party scanner without an approved data-processing arrangement.

## 2. Protect the default branch

Prefer a named **repository ruleset** targeting the default branch (use legacy branch
protection only where rulesets are unavailable). Start in evaluate mode if the repository is
already busy, fix failures, then make it active. GitHub rulesets can require PRs, status
checks, reviews, deployments, signed commits, and code-scanning results; push rulesets can
restrict paths, extensions, path length, and file size. They do not inspect a file's content
for secrets. See GitHub's [available ruleset rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
and [push-ruleset limits](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository).

| Control | Public / internal | Confidential |
|---|---|---|
| Pull requests | Require PRs; block direct pushes to the default branch | Same; allow bypass only to a small, named break-glass group. |
| Reviews | 1 approval; dismiss stale approvals; require resolved conversations | 2 approvals or 1 + required CODEOWNER; require approval of the latest push for high-risk paths. |
| Checks | Require the fast CI, tests, secret scan, and policy gate; require branches up to date or use merge queue | Same, plus required SAST/code scanning when the project warrants it. |
| History | Block force pushes and deletions; restrict pushes | Also consider signed commits and linear history where the team can support them. |
| Deployment | Optional staging deployment gate | Require an approved staging/control environment when a deployable service warrants it. |
| Exceptions | Keep the bypass list narrow and review it periodically | Record who bypassed, why, approval, remediation, and whether an incident review is required. |

Use stable, specific required-check names (for example, `ci / test`, `ci / policy`,
`security / secret scan`) and remove obsolete checks when a workflow is renamed. A required
status check only protects a branch if the matching workflow actually runs for that PR.
Protect workflow, policy, dependency, and deployment files with `CODEOWNERS` so the people
responsible for the controls review their changes.

For active repositories with frequent merges, a merge queue can replace repeatedly rebasing
PRs just to satisfy “up to date”; GitHub documents it as an alternative to that requirement
for protected branches. [Branch-protection settings](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
also support the same core PR, status-check, review, and conversation controls.

## 3. Enable GitHub's built-in security floor

Enable only features available to the repository's plan and data classification, then verify
alerts are owned and triaged.

1. Enable the dependency graph, Dependabot alerts, security updates, and version-update PRs.
2. Enable secret scanning and push protection where available. Push protection blocks many
   credentials *before* they reach the repository; configure custom secret patterns only for
   high-confidence, organization-specific secrets. It is not a substitute for local gitleaks.
   [GitHub push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection)
   explains its bypass and custom-pattern behavior.
3. Enable CodeQL code scanning. Default setup is a sensible low-maintenance start for eligible
   repositories; use the advanced workflow when the build, query suite, paths, or language
   matrix need deliberate control. [CodeQL setup types](https://docs.github.com/en/code-security/concepts/code-scanning/setup-types)
   describes the trade-off. Require the resulting scan through the ruleset only after it is
   reliable and findings have an owner.
4. Add `CODEOWNERS`, issue/PR templates, a security contact or `SECURITY.md`, and a clear
   vulnerability-reporting route. Keep repository visibility, collaborators, teams, deploy
   keys, environment secrets, and GitHub App permissions least-privileged.
5. Pin third-party Actions to reviewed full commit SHAs where the project risk warrants it;
   grant each workflow only the permissions it needs (normally `contents: read`), and keep
   workflow artifact/log retention appropriate for the data classification.

## 4. Hooks and CI: block secrets and path leaks before they spread

Local hooks make feedback fast; CI makes the control unavoidable. Run the same checker in
both places and make the CI job a required check when the project needs it. Keep finding output
minimal: report a path, line number, rule ID, and remediation—not the secret itself.

| Risk | Local hook | Required CI job | Notes |
|---|---|---|---|
| Credentials | gitleaks + `detect-private-key` | gitleaks and scheduled history scan | Already included in [`hooks/.pre-commit-config.yaml`](../hooks/.pre-commit-config.yaml). See [`inventory/security-quality.md`](../inventory/security-quality.md). |
| Absolute local paths | Optional staged-diff rule | Re-run against the PR diff when justified | Detect Unix home paths, Windows drive paths, and `file://` URLs; allow only documented portable examples. Prefer project-relative paths, env vars, or config values. |
| Large binaries / exports | Filename, extension, size, and allowlist rule | Re-run when justified | A ruleset can block risky paths/extensions/sizes; content inspection needs a hook or CI scanner. |

Do not enable a broad content regex as a hard gate without measuring it against representative
fixtures. Start advisory rules in report-only mode, define a false-positive process, and promote
only high-confidence rules to blocking.

Per-commit and per-PR gates only see the current diff. For confidential repositories, also
schedule a periodic **repo-wide credential history scan** (for example TruffleHog against a
local checkout). GitHub-native scanning covers credentials, not every business-confidential
string. Run history scans offline and treat findings as triage for human review. See
[`prompts/maintenance-loop.md`](../prompts/maintenance-loop.md).

### Recommended implementation contract

Before wiring optional path or export checks, write a small project-owned configuration that names:

- prohibited file paths/extensions and size caps;
- allowed fixture directories and why they are safe;
- absolute-path patterns, portable replacements, and narrowly scoped examples;
- exception owner, expiry, and review record; and
- the CI job name that branch rules require.

Redact matches from logs, exit non-zero for blocking rules, and have tests proving synthetic
representative samples are caught. A pre-commit hook is a convenience; a required PR check is
the merge control.

## 5. GitHub Apps and outside services

Treat every App as a data processor with code and metadata access. Install the smallest
useful set, scope it to selected repositories, give it minimum permissions, review its
retention/training/subprocessor terms, and periodically remove unused Apps. See the curated
options in [`inventory/github-apps.md`](../inventory/github-apps.md).

- **Start small:** Dependabot plus GitHub-native scanning is enough for many public/internal repos.
- **Add review quality deliberately:** CodeRabbit, DeepSource, or similar can improve review,
  but their PR/code access must be acceptable for the classification.
- **Add unified security only when owned:** Snyk or Aikido can centralize SCA/SAST/container
  posture, but designate a team to triage and remediate findings before making their checks
  required.
- **For confidential work:** prefer approved internal runners over sending source or credentials
  to a convenience SaaS. Verify the service agreement and organizational policy first.

## 6. Rollout and recurring verification

1. Inventory current branches, collaborators, Apps, workflows, secrets, environments, and
   data-bearing files before enabling gates.
2. Configure the default-branch ruleset in evaluate/advisory mode where possible; establish
   the required check names and fix noisy checks.
3. Install hooks, make CI required, enable GitHub's built-in scans, and test a deliberately
   synthetic blocked example in a throwaway branch.
4. Turn the ruleset active. Document break-glass access and make bypasses auditable.
5. At least quarterly—and after a domain, team, or data-classification change—review ruleset
   bypasses, failed/renamed checks, CODEOWNERS, App access, alert backlog, false positives,
   and workflow permissions/retention.

If credentials or customer exports reach the remote despite these gates: stop sharing them,
revoke/rotate any secrets, restrict access, follow the organization's incident process, and
only then plan history remediation. Rewriting Git history does not remove clones, caches, logs,
artifacts, or third-party copies.
