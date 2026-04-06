---
name: design-review
description: >
  Design audit and fix skill. Reviews UI/UX implementation against design specs 
  and fixes issues. Use when user says "design review", "audit the UI", 
  "check design implementation", or UI needs to be verified against designs.
version: 2.0.0
author: Garry Tan (Original), gstack-openclaw-skills Team
tags: [design, review, audit, ui, ux, implementation]
---

# Design Review - Design Audit and Fixes

Design audit skill that reviews UI implementation and fixes design issues.

## When to Use This Skill

Use this skill when the user says:

- "design review"
- "audit the UI"
- "check design implementation"
- "does this match the design?"
- UI needs verification against design specs

## Design Review Checklist

### Visual Consistency
- [ ] Colors match design tokens
- [ ] Typography follows the scale
- [ ] Spacing uses the grid system
- [ ] Icons are consistent style/size

### Component Accuracy
- [ ] Buttons match design specs
- [ ] Forms are correctly styled
- [ ] Cards/containers have correct padding
- [ ] Navigation matches design

### Responsive Design
- [ ] Mobile layout is correct
- [ ] Tablet breakpoints work
- [ ] Desktop layout is correct
- [ ] No overflow/clipping issues

### Interaction States
- [ ] Hover states are implemented
- [ ] Focus states are visible
- [ ] Active/pressed states work
- [ ] Disabled states are correct

### Accessibility
- [ ] Color contrast passes WCAG AA
- [ ] Focus indicators are visible
- [ ] Text is readable at all sizes

## Output Format

```markdown
## Design Review Report

### Overall Assessment
[Pass / Needs Work / Fail]

### Issues Found

#### Critical (Must Fix)
- [Issue]: [File/Component] - [Description]

#### Minor (Should Fix)
- [Issue]: [File/Component] - [Description]

### Auto-Fixes Applied
- [Fix 1]
- [Fix 2]

### Remaining Manual Work
- [Item 1]
```

---

**Original**: gstack/design-review by Garry Tan  
**Adaptation**: OpenClaw/WorkBuddy version  
**Version**: 2.0.0
