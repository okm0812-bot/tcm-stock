---
name: codex
description: >
  Independent code review skill using a second-opinion approach. Provides an 
  objective review from a fresh perspective. Use when user says "codex", 
  "second opinion", "independent review", or wants cross-validation of review results.
version: 2.0.0
author: Garry Tan (Original), gstack-openclaw-skills Team
tags: [review, second-opinion, independent, validation, code-quality]
---

# Codex - Independent Code Review

Independent review skill that provides a fresh, objective perspective on code.

## When to Use This Skill

Use this skill when the user says:

- "codex"
- "second opinion"
- "independent review"
- "cross-validate"
- After /review to get a second perspective

## How It Differs from /review

| Aspect | /review | /codex |
|--------|---------|--------|
| Perspective | Primary reviewer | Independent reviewer |
| Focus | Comprehensive | Fresh eyes |
| Bias | May have context bias | Starts fresh |
| Use case | Standard review | Validation / second opinion |

## Execution Workflow

### Step 1: Fresh Start

Approach the code as if seeing it for the first time:
- No assumptions about intent
- No context from previous reviews
- Pure code quality assessment

### Step 2: Independent Analysis

Review for:

1. **Clarity**: Is the code self-explanatory?
2. **Correctness**: Does it do what it claims?
3. **Completeness**: Are edge cases handled?
4. **Consistency**: Does it follow the codebase patterns?

### Step 3: Compare with Previous Review

If /review was already run:
- Confirm findings that overlap
- Highlight any new issues found
- Note any disagreements

### Step 4: Output

```markdown
## Independent Code Review (Codex)

### Fresh Perspective Assessment
[Overall impression from a fresh set of eyes]

### Confirmed Issues (from /review)
[Issues that this review also found]

### New Issues Found
[Issues not caught in previous review]

### Disagreements
[Areas where this review differs from /review]

### Overall Verdict
[APPROVE / REQUEST CHANGES / NEEDS DISCUSSION]
```

---

**Original**: gstack/codex by Garry Tan  
**Adaptation**: OpenClaw/WorkBuddy version  
**Version**: 2.0.0
