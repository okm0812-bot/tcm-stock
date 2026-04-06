---
name: review
description: >
  Pre-merge code review tool. Analyzes SQL security, LLM trust boundaries, race conditions, 
  and structural issues. Automatically reviews git diff, identifies bugs, and provides fixes.
  Use when user says "review this PR", "code review", "pre-landing review", "check my diff", 
  or code is about to be merged.
version: 2.0.0
author: Garry Tan (Original), gstack-openclaw-skills Team
tags: [code, review, security, quality, git, pre-merge]
---

# Review - Pre-Merge Code Review Tool

Pre-merge PR review tool that analyzes code diffs and provides actionable feedback.

## When to Use This Skill

Use this skill when the user says:

- "review this PR"
- "code review"
- "pre-landing review"
- "check my diff"
- "review the current branch"
- "review my changes"
- Code is about to be merged

## Execution Workflow

### Step 1: Get the Diff

```bash
git diff origin/main...HEAD
```

### Step 2: Two-Phase Review

#### Phase 1: Critical Issues (Must Fix)

1. **SQL Security** - Check for SQL injection vulnerabilities
2. **Race Conditions** - Identify concurrent access issues
3. **LLM Trust Boundaries** - Check for prompt injection risks
4. **Authentication/Authorization** - Check permission checks

#### Phase 2: Informational Issues (Should Fix)

1. **Magic Numbers** - Identify hardcoded values
2. **Dead Code** - Find unused variables/functions
3. **Test Coverage** - Check for missing tests
4. **Performance Issues** - Identify N+1 queries

### Step 3: Provide Fixes

For issues found, categorize and provide fixes:

- **AUTO-FIX**: Automatically fix mechanical issues
- **ASK**: Require user confirmation for complex changes

### Step 4: Generate Review Status

- **DONE**: Review complete, code can merge
- **BLOCKED**: Cannot proceed, blocking issues exist

## Boil the Lake Principle

> "Don't be half-invested, boil the whole lake"

- Don't just report bugs, fix them
- A review isn't done until issues are addressed

---

**Original**: gstack/review by Garry Tan  
**Adaptation**: OpenClaw/WorkBuddy version  
**Version**: 2.0.0
