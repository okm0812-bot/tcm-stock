---
name: ship
description: >
  Release engineer skill. Automates the full release workflow: merge base branch, 
  run tests, version management, create PR. Use when user says "ship", "deploy", 
  "push to main", "create PR", or is ready to release.
version: 2.0.0
author: Garry Tan (Original), gstack-openclaw-skills Team
tags: [ship, deploy, release, git, pr, ci-cd]
---

# Ship - Automated Release Workflow

Automated release engineer skill for shipping code to production.

## When to Use This Skill

Use this skill when the user says:

- "ship"
- "deploy"
- "push to main"
- "create PR"
- "release this"
- Code has passed review and QA and is ready to ship

## Prerequisites

Before shipping, ensure:
- [ ] /review has been run and issues addressed
- [ ] /qa has been run and bugs fixed
- [ ] Tests are passing
- [ ] No uncommitted changes

## Execution Workflow

### Step 1: Pre-Ship Checklist

```bash
# Verify clean state
git status

# Run tests
npm test  # or pytest, go test, etc.

# Check for uncommitted changes
git diff
```

### Step 2: Sync with Base Branch

```bash
# Fetch latest
git fetch origin

# Merge or rebase base branch
git merge origin/main
# or
git rebase origin/main
```

### Step 3: Version Management

Determine version bump:
- **Patch** (1.0.x): Bug fixes
- **Minor** (1.x.0): New features, backward compatible
- **Major** (x.0.0): Breaking changes

Update version in relevant files (package.json, pyproject.toml, etc.)

### Step 4: Create PR

```bash
# Push branch
git push origin HEAD

# Create PR (via gh CLI or manual)
gh pr create --title "[Feature] Description" --body "..."
```

### Step 5: Ship Report

```markdown
## Ship Report

### Branch: feature/xxx → main
### Version: 1.2.3 → 1.3.0
### PR: #123

### Changes Shipped
- [Change 1]
- [Change 2]

### Tests: ✅ All passing
### Status: 🚀 Shipped
```

## Safety Checks

- Never ship directly to main without PR (unless explicitly requested)
- Always run tests before shipping
- Document breaking changes

---

**Original**: gstack/ship by Garry Tan  
**Adaptation**: OpenClaw/WorkBuddy version  
**Version**: 2.0.0
