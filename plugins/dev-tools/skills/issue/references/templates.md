# GitHub Issue Templates — Best Practices

## Table of Contents
1. [Bug Report](#bug-report)
2. [Feature Request](#feature-request)
3. [Documentation](#documentation)
4. [Performance](#performance)
5. [Security](#security)
6. [Refactor / Tech Debt](#refactor--tech-debt)
7. [Labels Reference](#labels-reference)

---

## Bug Report

**When to use**: Unexpected behavior, crashes, errors, wrong output.

```markdown
## Summary
<!-- One-sentence description of the bug -->

## Steps to Reproduce
1.
2.
3.

## Expected Behavior
<!-- What should happen -->

## Actual Behavior
<!-- What actually happens -->

## Environment
- OS:
- Version/Commit:
- Relevant config:

## Additional Context
<!-- Screenshots, logs, error messages -->
```

**Labels**: `bug`, optionally `regression` / `critical` / `good first issue`
**Assignee**: Leave blank unless obvious owner
**Milestone**: Set if it blocks a release

---

## Feature Request

**When to use**: New capability, UX improvement, user-visible enhancement.

```markdown
## Problem / Motivation
<!-- What pain point does this solve? Who is affected? -->

## Proposed Solution
<!-- Describe the desired behavior or UI change -->

## Alternatives Considered
<!-- Other approaches you considered and why you rejected them -->

## Acceptance Criteria
- [ ]
- [ ]
- [ ]

## Additional Context
<!-- Mockups, related issues, prior art -->
```

**Labels**: `enhancement`
**Tip**: Frame around the user problem, not the implementation.

---

## Documentation

**When to use**: Missing docs, outdated content, unclear explanation.

```markdown
## What's Missing or Wrong
<!-- Which page/section/README, and what's the issue? -->

## Suggested Improvement
<!-- What should it say, or what topic should be added? -->

## Why This Matters
<!-- Who is confused and how does this block them? -->
```

**Labels**: `documentation`

---

## Performance

**When to use**: Latency, memory, CPU, bundle size regression.

```markdown
## Symptom
<!-- Describe the slowness / resource issue -->

## Measurement
<!-- Benchmark results, profiling data, before/after numbers -->

## Affected Scope
<!-- Which users, flows, or data sizes trigger this? -->

## Proposed Fix (optional)
<!-- If you have a hypothesis -->
```

**Labels**: `performance`

---

## Security

**When to use**: Vulnerability, CVE, injection, XSS, auth bypass, data exposure.

```markdown
## Summary
<!-- One-sentence description of the vulnerability -->

## Attack Vector
<!-- How could this be exploited? (e.g., unauthenticated HTTP request, malicious input) -->

## Impact
<!-- What is at risk? (data leak, privilege escalation, denial of service) -->

## Severity
<!-- Critical / High / Medium / Low — use CVSS if available -->

## Steps to Reproduce
1.
2.
3.

## Suggested Fix (optional)
<!-- If you have a mitigation or patch idea -->

## References
<!-- CVE IDs, advisories, related issues -->
```

**Labels**: `security`, optionally `critical`
**Note**: For private repos, consider using GitHub Security Advisories instead of public issues for critical vulnerabilities.

---

## Refactor / Tech Debt

**When to use**: Code quality, maintainability, internal cleanup (no user-visible change).

```markdown
## What Needs Refactoring
<!-- Which module/file/pattern, and why is it a problem? -->

## Goals
- [ ]
- [ ]

## Out of Scope
<!-- What this PR will NOT change -->

## Risk
<!-- What could break? -->
```

**Labels**: `refactor` or `tech-debt`

---

## Labels Reference

| Label | When |
|---|---|
| `bug` | Confirmed broken behavior |
| `enhancement` | New feature or improvement |
| `documentation` | Docs only |
| `performance` | Speed / memory issue |
| `refactor` | Internal cleanup |
| `tech-debt` | Known shortcuts to pay back |
| `security` | Vulnerability or security concern |
| `good first issue` | Beginner-friendly |
| `help wanted` | Needs external contribution |
| `critical` | Blocking users / production |
| `regression` | Was working before |
| `needs-repro` | Can't reproduce yet |
| `wontfix` | Intentional or out of scope |

---

## Title Conventions

Good titles are specific and scannable:

| Bad | Good |
|---|---|
| "Bug in app" | "App crashes on launch when no config file exists" |
| "Add feature" | "Add dark mode support via system preference detection" |
| "Fix docs" | "README missing setup instructions for Windows" |
| "Slow" | "Search takes >3s on queries with >1000 results" |

**Format**: `[Area] Action + detail` — e.g., `[Auth] Token refresh fails silently after 24h`
