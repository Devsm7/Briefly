---
name: review-code
description: Review staged or recent code changes for bugs, security issues, and quality. Use when the user asks to review code, check changes, or audit recent edits.
allowed-tools: [Bash, Read, Grep, Glob]
---

# Code Review

Review the current code changes and provide actionable feedback.

## Steps

1. **Get the diff**
   - Run `git diff HEAD` to see unstaged changes
   - Run `git diff --cached` to see staged changes
   - If no changes, run `git diff HEAD~1` to review the last commit

2. **Analyze each changed file** for:
   - **Bugs**: logic errors, off-by-one, null/undefined access, unhandled promise rejections
   - **Security**: hardcoded secrets, SQL injection, XSS, unsafe eval, exposed API keys
   - **Quality**: dead code, duplicate logic, overly complex conditions, missing error handling at system boundaries
   - **Consistency**: naming conventions, code style relative to surrounding code

3. **Read surrounding context** for any file where something looks suspicious — use Read to check the full function or class before flagging an issue.

4. **Report findings** grouped by severity:

---

### Code Review

**[file:line]** — description of issue and why it matters

Severity: `high` | `medium` | `low`

---

Only report real issues. Skip:
- Pre-existing problems not introduced in these changes
- Style nitpicks unless they break consistency
- Things a linter or type checker would catch
- Speculative issues with no evidence in the code
