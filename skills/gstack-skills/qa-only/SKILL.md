---
name: qa-only
description: >
  QA reporter skill. Tests application and reports bugs WITHOUT fixing them.
  Use when user says "qa-only", "just report bugs", "find issues but don't fix", 
  or wants a pure bug report without automatic fixes.
version: 2.0.0
author: Garry Tan (Original), gstack-openclaw-skills Team
tags: [qa, testing, bugs, reporting]
---

# QA-Only - Bug Reporter

QA reporting skill that finds bugs and reports them without automatic fixes.

## When to Use This Skill

Use this skill when the user says:

- "qa-only"
- "just report bugs"
- "find issues but don't fix"
- "I want a bug report"
- User wants to review bugs before deciding on fixes

## Difference from /qa

| Feature | /qa | /qa-only |
|---------|-----|----------|
| Find bugs | ✅ | ✅ |
| Fix bugs | ✅ Auto-fix | ❌ Report only |
| Output | Fixed code + report | Report only |

## Execution Workflow

### Step 1: Test Systematically

Same testing approach as /qa:
1. Happy path testing
2. Edge case testing
3. Error case testing
4. Integration testing

### Step 2: Document All Issues

For each issue found:

```markdown
### Bug: [Title]
**Severity**: Critical / High / Medium / Low
**File**: [path:line]
**Description**: [What's wrong]
**Steps to Reproduce**:
1. [Step 1]
2. [Step 2]
**Expected**: [What should happen]
**Actual**: [What actually happens]
**Suggested Fix**: [How to fix it]
```

### Step 3: Prioritized Report

```markdown
## QA Report (Report Only)

### Summary
- Tests Run: X
- Bugs Found: X
- Critical: X | High: X | Medium: X | Low: X

### Critical Bugs (Fix Immediately)
[List]

### High Priority Bugs
[List]

### Medium/Low Priority
[List]

### Recommended Next Steps
Use /qa to automatically fix these issues, or address manually.
```

---

**Original**: gstack/qa-only by Garry Tan  
**Adaptation**: OpenClaw/WorkBuddy version  
**Version**: 2.0.0
