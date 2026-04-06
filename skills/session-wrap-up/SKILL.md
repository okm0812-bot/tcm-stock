---
name: session-wrap-up
version: 1.0.0
description: End-of-session automation that commits unpushed work, extracts learnings, detects patterns, and persists rules.
---

# Session Wrap-Up

## When to Run

- **On-demand**: User says "wrap up" or "session wrap-up"
- **Automatic**: End of significant work session (optional)

## What It Does (4 Phases)

### Phase 1: Ship It
- Check for unstaged/uncommitted files in workspace
- Commit with auto-generated message

### Phase 2: Extract Learnings
- Scan session conversation for key decisions
- Pull from recent memory file entries
- Identify what worked / what didn't

### Phase 3: Pattern Detect
- Analyze extracted learnings
- Find repeated mistakes or requests
- Identify automation opportunities

### Phase 4: Persist & Evolve
- Write learnings to memory/YYYY-MM-DD.md
- Update MEMORY.md if new patterns found

## Output

- Commit confirmation
- Learnings summary (1-3 bullets)
- Patterns detected (if any)
- Files updated (if any)
