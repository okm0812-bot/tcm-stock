---
name: guard
description: >
  Full safety mode skill. Combines careful + freeze for maximum caution.
  Use when user says "guard", "maximum safety", "be very careful", or when 
  working in production environments or with critical data.
version: 2.0.0
author: Garry Tan (Original), gstack-openclaw-skills Team
tags: [safety, guard, careful, freeze, production, critical]
---

# Guard - Full Safety Mode

Maximum safety skill combining careful + freeze guardrails.

## When to Use This Skill

Use this skill when:

- Working in production environments
- Handling critical/sensitive data
- User says "guard", "maximum safety", "be very careful"
- High-stakes operations where mistakes are costly

## What Guard Does

Guard = /careful + /freeze combined:

1. **Careful mode**: Confirmation required for all dangerous operations
2. **Freeze mode**: File editing restricted to defined scope
3. **Audit log**: All actions logged for review
4. **Double confirmation**: Extra confirmation for irreversible actions

## Guard Protocol

When guard is active, before ANY action:

```
🛡️ GUARD MODE ACTIVE

Action: [What you're about to do]
Type: [Read / Write / Delete / Execute]
Risk Level: [Low / Medium / High / Critical]

[If High/Critical]:
⚠️ This action requires explicit confirmation.
Type "CONFIRM [action]" to proceed.
```

## Activation

```
/guard  # Activate full safety mode
/guard src/  # Activate with scope restriction
```

## Deactivation

```
/unguard  # Deactivate guard mode
```

## Guard Checklist

Before any significant action:

- [ ] Is this action reversible?
- [ ] Is there a backup?
- [ ] Is this in the correct environment?
- [ ] Has the user explicitly requested this?
- [ ] Are there any side effects?

## Use Cases

- **Production deployments**: Extra caution when deploying
- **Database migrations**: Protect against data loss
- **Security-sensitive code**: Extra review for auth/crypto code
- **Onboarding**: When learning a new codebase

---

**Original**: gstack/guard by Garry Tan  
**Adaptation**: OpenClaw/WorkBuddy version  
**Version**: 2.0.0
