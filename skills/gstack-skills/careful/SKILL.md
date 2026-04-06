---
name: careful
description: >
  Safety guardrails skill. Adds warnings and confirmation steps before dangerous operations.
  Use when about to perform delete operations, file overwrites, dangerous commands, 
  or any irreversible action. Automatically activates for risky operations.
version: 2.0.0
author: Garry Tan (Original), gstack-openclaw-skills Team
tags: [safety, careful, dangerous, confirmation, guardrails]
---

# Careful - Dangerous Operation Safety Guardrails

Safety skill that adds confirmation steps before dangerous operations.

## When to Use This Skill

Use this skill when:

- About to delete files or data
- Overwriting important files
- Running dangerous commands (rm -rf, DROP TABLE, etc.)
- Making irreversible changes
- User says "careful", "be careful", "double-check this"

## Dangerous Operations Checklist

Before executing any of these, STOP and confirm:

### File Operations
- `rm -rf` or equivalent
- Overwriting files without backup
- Deleting directories
- Clearing databases

### Database Operations
- `DROP TABLE`
- `DELETE FROM` without WHERE clause
- `TRUNCATE`
- Schema migrations in production

### Git Operations
- `git push --force`
- `git reset --hard`
- Deleting branches with unmerged work
- Rewriting history on shared branches

### System Operations
- Changing permissions (chmod 777)
- Modifying system files
- Stopping production services

## Confirmation Protocol

For any dangerous operation:

1. **STOP**: Don't execute immediately
2. **DESCRIBE**: Explain exactly what will happen
3. **WARN**: List what could go wrong
4. **BACKUP**: Suggest backup if applicable
5. **CONFIRM**: Ask user to explicitly confirm

```
⚠️ DANGEROUS OPERATION DETECTED

Action: [What you're about to do]
Risk: [What could go wrong]
Irreversible: [Yes/No]

Backup recommendation: [How to backup first]

Type "yes" to confirm, or "no" to cancel.
```

## Auto-Activation

This skill automatically activates when detecting:
- Commands containing: `rm`, `delete`, `drop`, `truncate`, `force`, `hard`
- File operations on critical paths
- Production environment operations

---

**Original**: gstack/careful by Garry Tan  
**Adaptation**: OpenClaw/WorkBuddy version  
**Version**: 2.0.0
