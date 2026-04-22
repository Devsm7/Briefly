---
name: summary
description: Summarize the project for someone returning after a break — what it does, its structure, recent changes, open work, and what to focus on next.
allowed-tools: [Bash, Read, Grep, Glob]
---

# Project Summary

Give a full orientation for someone returning to this project after time away.

## Steps

1. **Project identity**
   - Read `README.md` (or any root-level docs) to get the project's purpose and tech stack
   - If no README, infer from `package.json`, `pyproject.toml`, `requirements.txt`, or similar

2. **Codebase structure**
   - Run `git ls-files | head -80` to get a feel for the file layout
   - Identify the main entry points, key directories, and any notable config files

3. **Recent activity**
   - Run `git log --oneline -20` to get the last 20 commits
   - Run `git log --since="30 days ago" --oneline` to scope to recent work
   - Note which areas of the codebase were touched most

4. **Current state**
   - Run `git status` to see any uncommitted changes
   - Run `git stash list` to check for stashed work
   - Run `git branch -a` to see open branches

5. **Open work / loose ends**
   - Search for `TODO`, `FIXME`, `HACK` comments: `grep -r "TODO\|FIXME\|HACK" --include="*.py" --include="*.ts" --include="*.tsx" --include="*.js" -l`
   - Note any empty or stub files

6. **Report** using this structure:

---

### Project Summary

**What it is:** one sentence on the project's purpose.

**Stack:** languages, frameworks, key dependencies.

**Structure:** 3–5 bullet points on major directories/modules and what they do.

**Recent changes (last 30 days):**
- bullet per meaningful commit or theme of work

**Current state:**
- Uncommitted changes / stashes / open branches worth noting

**Loose ends:**
- TODOs, stubs, or unfinished areas found in the code

**Where to pick up:** 1–2 sentences recommending the most logical next step based on recent activity and open work.

---

Keep it scannable. No padding. If a section has nothing to report, omit it.