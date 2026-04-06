---
name: freeze
description: >
  File editing scope lock skill. Restricts which files can be edited to prevent 
  unintended changes. Use when user says "freeze", "lock files", "only edit X", 
  or wants to restrict changes to specific directories/files.
version: 2.0.0
author: Garry Tan (Original), gstack-openclaw-skills Team
tags: [safety, freeze, lock, scope, files]
---

# Freeze - File Editing Scope Lock

Skill that restricts file editing to a defined scope.

## When to Use This Skill

Use this skill when:

- User says "freeze", "lock files", "only edit X"
- Want to restrict changes to specific directories
- Working on a focused task and don't want scope creep
- Need to protect certain files from modification

## How It Works

When freeze is active:

1. Define the allowed scope (files/directories)
2. Before any file edit, check if it's in scope
3. If out of scope: STOP and ask for confirmation
4. Log all attempted out-of-scope edits

## Activation

```
/freeze src/components/  # Only allow edits in this directory
/freeze src/api/routes.py  # Only allow edits to this file
/freeze src/ tests/  # Allow edits in multiple locations
```

## Freeze Protocol

When a file edit is requested:

1. Check if file is in allowed scope
2. If YES: Proceed normally
3. If NO:
   ```
   🔒 FREEZE ACTIVE
   
   Attempted edit: [file path]
   Allowed scope: [defined scope]
   
   This file is outside the frozen scope.
   Confirm to override freeze, or cancel.
   ```

## Unfreeze

```
/unfreeze  # Remove all restrictions
```

## Use Cases

- **Focused refactoring**: Only touch the module being refactored
- **Bug fix**: Only edit the file with the bug
- **Review mode**: Prevent accidental edits while reviewing

---

**Original**: gstack/freeze by Garry Tan  
**Adaptation**: OpenClaw/WorkBuddy version  
**Version**: 2.0.0
