---
name: investigate
description: >
  Debugging expert skill for systematic root cause analysis. Use when user says 
  "debug this", "investigate", "root cause", "why is this broken", or needs 
  systematic troubleshooting of complex issues.
version: 2.0.0
author: Garry Tan (Original), gstack-openclaw-skills Team
tags: [debug, investigate, root-cause, troubleshooting]
---

# Investigate - Systematic Root Cause Analysis

Debugging expert skill for finding root causes of complex issues.

## When to Use This Skill

Use this skill when the user says:

- "debug this"
- "investigate"
- "root cause"
- "why is this broken"
- "something is wrong with..."
- Complex troubleshooting needed

## Execution Workflow

### Step 1: Gather Information

Before investigating, collect:

- Error messages (exact text)
- Stack traces
- When did it start?
- What changed recently?
- Is it reproducible? Always/sometimes?
- Environment (dev/staging/prod)?

### Step 2: Form Hypotheses

List possible causes ranked by likelihood:

1. Most likely cause
2. Second most likely
3. Less likely but possible

### Step 3: Systematic Investigation

For each hypothesis:

```
Hypothesis: [What might be wrong]
Test: [How to verify]
Result: [What you found]
Conclusion: [Confirmed / Ruled out]
```

### Step 4: Isolate the Issue

- Narrow down to smallest reproducible case
- Binary search through code/commits
- Check logs at each layer

### Step 5: Root Cause Report

```markdown
## Investigation Report

### Issue
[Description of the problem]

### Root Cause
[The actual cause]

### Evidence
[What confirmed this is the root cause]

### Fix
[How to fix it]

### Prevention
[How to prevent this in the future]

### Timeline
[When it was introduced, when discovered]
```

## Investigation Techniques

- **Binary search**: Narrow down by halving the search space
- **Rubber duck**: Explain the problem step by step
- **Diff analysis**: What changed between working and broken?
- **Log analysis**: Follow the execution path through logs
- **Minimal reproduction**: Create smallest failing test case

---

**Original**: gstack/investigate by Garry Tan  
**Adaptation**: OpenClaw/WorkBuddy version  
**Version**: 2.0.0
