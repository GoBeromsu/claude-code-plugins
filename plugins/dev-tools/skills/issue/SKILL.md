---
name: issue
description: "Create well-structured GitHub issues following best practices for bug reports, feature requests, documentation gaps, performance, security, and refactoring tasks. Infers issue type from context — no need to specify explicitly. Use when the user invokes /issue, says '이슈 등록해줘', '이슈 만들어줘', '버그 리포트 남겨줘', 'GitHub 이슈 올려줘', '버그 신고해줘', '이 버그 GitHub에 올려줘', 'feature request 만들어줘', '버그 제보할게', '이슈 트래킹해줘', 'PR 연계 이슈 만들어줘', or otherwise wants to file a GitHub issue in the current repository. NOT for PR descriptions — create those directly. NOT for internal task tracking outside GitHub."
---

# Issue Skill

Create and file GitHub issues via `gh` CLI using structured templates.

## Workflow

1. **Identify issue type** from user input:
   - Bug → crash, error, unexpected behavior, 안 됨, 깨짐
   - Feature → 추가, 개선, 지원, "would be nice"
   - Docs → 문서, README, 설명 없음
   - Performance → 느림, 메모리, 용량
   - Security → vulnerability, CVE, 보안, 취약점, injection, XSS
   - Refactor → 코드 정리, tech debt, 리팩터

2. **Read `references/templates.md`** for the identified issue type's template and label conventions.

3. **Gather missing info** — ask only for fields you cannot infer from context. Only ask questions if genuinely ambiguous — max 1-2 questions total. Infer from:
   - Current repo name / language / stack (via `git remote -v`, `package.json`, etc.)
   - Files recently discussed or edited in conversation
   - Error messages already shared
   - For bug reports: always infer the environment from `git remote -v` and `package.json` — never ask the user what repo they're in
   - For feature requests: infer priority from the user's tone (urgent language = high priority)

4. **Draft the issue**:
   - Write a specific, scannable title (see Title Conventions in templates.md)
   - Fill the template body; omit empty optional sections
   - Pick appropriate labels from the Labels Reference in templates.md

5. **Confirm** — show the user the full title + body + labels before filing. Ask for approval.

6. **File** using `gh issue create`. Use `--body-file` with a temp file to avoid shell quoting issues with multi-line bodies:

```bash
# Write body to a temp file first
tmp=$(mktemp)
cat > "$tmp" << 'BODY'
<issue body here>
BODY

gh issue create \
  --title "<title>" \
  --body-file "$tmp" \
  --label "<label1>,<label2>"

rm "$tmp"
```

If a label doesn't exist in the repo, create it first or omit it and note it to the user.
If `gh issue create` fails for reasons other than auth (e.g., insufficient permissions, repo not found), report the error message and ask the user to verify the repo and their access level.

## Key Rules

- **One question at a time** when gathering info — ask sequentially, never all at once. Cap at 2 questions total across the entire interaction.
- **Never file without user confirmation** — always show the full draft first.
- If `gh` is not authenticated, instruct the user to run `gh auth login` first.
- If no remote repo is detected, ask the user which repo to file against.

## Quick Filing (no confirmation)

If the user says "빠르게 이슈 올려줘" or "just file it", skip the confirmation step and file immediately with best-guess values. Note the issue URL after filing.

## Templates & Labels

All templates (Bug, Feature, Docs, Performance, Security, Refactor) and label definitions are in `references/templates.md`. Read it at step 2.
