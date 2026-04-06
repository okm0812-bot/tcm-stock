---
name: plan-design-review
description: >
  Designer perspective review skill. Evaluates UX, design quality, and user experience.
  Use when user says "design review", "UX review", "check the design", or needs 
  design feedback on features or interfaces.
version: 2.0.0
author: Garry Tan (Original), gstack-openclaw-skills Team
tags: [design, ux, ui, review, user-experience]
---

# Plan Design Review - Designer Perspective Review

Design review skill from a UX/product designer perspective.

## When to Use This Skill

Use this skill when the user says:

- "design review"
- "UX review"
- "check the design"
- "is this good UX?"
- Evaluating user experience and interface design

## Design Review Framework

### 1. User Journey

- Is the flow intuitive?
- Where will users get confused?
- What's the happy path? Is it obvious?

### 2. Consistency

- Does it match the existing design system?
- Are patterns consistent with the rest of the app?
- Typography, spacing, colors — are they on-brand?

### 3. Accessibility

- Is it keyboard navigable?
- Does it work with screen readers?
- Is color contrast sufficient (WCAG AA)?
- Are touch targets large enough (44px minimum)?

### 4. Error States

- What happens when things go wrong?
- Are error messages helpful?
- Is there a recovery path?

### 5. Empty States

- What does the user see with no data?
- Is there a clear call to action?

### 6. Mobile/Responsive

- Does it work on mobile?
- Are touch interactions considered?

## Output Format

```markdown
## Design Review

### UX Assessment
[Overall user experience evaluation]

### Issues Found
1. [Issue] - Severity: [High/Medium/Low]
   Recommendation: [...]

### Accessibility Concerns
[List of accessibility issues]

### Recommendations
[Specific design improvements]

### Approved / Needs Revision
```

---

**Original**: gstack/plan-design-review by Garry Tan  
**Adaptation**: OpenClaw/WorkBuddy version  
**Version**: 2.0.0
