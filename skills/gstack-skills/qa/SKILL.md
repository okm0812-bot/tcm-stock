---
name: qa
description: >
  QA engineer skill. Systematically tests application, finds bugs, and fixes them.
  Use when user says "run QA", "test this", "check bugs", "find issues", or code needs verification.
version: 2.0.0
author: Garry Tan (Original), gstack-openclaw-skills Team
tags: [qa, testing, bugs, quality, verification]
---

# QA - Quality Assurance Engineer

Systematic QA testing skill that finds and fixes bugs.

## When to Use This Skill

Use this skill when the user says:

- "run QA"
- "test this"
- "check bugs"
- "find issues"
- "QA the feature"
- Code changes need verification before shipping

## Execution Workflow

### Step 1: Understand What to Test

- Review recent changes (git diff)
- Identify affected features
- List test scenarios

### Step 2: Systematic Testing

Test in order:

1. **Happy Path**: Does the main flow work?
2. **Edge Cases**: Empty inputs, boundary values, null handling
3. **Error Cases**: Invalid inputs, network failures, permission errors
4. **Integration**: Does it work with other parts of the system?

### Step 3: Bug Triage

For each bug found:

- **Severity**: Critical / High / Medium / Low
- **Reproducibility**: Always / Sometimes / Rarely
- **Impact**: Who is affected?

### Step 4: Fix Bugs

Following the Boil the Lake principle — don't just report, fix:

1. Identify root cause
2. Implement fix
3. Verify fix works
4. Check for regressions

### Step 5: Report

```markdown
## QA Report

### Tests Run: X
### Bugs Found: X
### Bugs Fixed: X
### Status: PASS / FAIL

### Critical Issues
- [Issue description + fix applied]

### Remaining Issues
- [Issue description + recommended action]
```

## Boil the Lake Principle

> "Don't be half-invested, boil the whole lake"

QA isn't done until bugs are fixed, not just reported.

---

**Original**: gstack/qa by Garry Tan  
**Adaptation**: OpenClaw/WorkBuddy version  
**Version**: 2.0.0
