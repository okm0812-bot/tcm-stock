---
name: plan-eng-review
description: >
  Engineering manager perspective review skill. Evaluates technical architecture 
  and implementation approaches. Use when user says "engineering review", 
  "architecture review", "tech review", or needs technical planning feedback.
version: 2.0.0
author: Garry Tan (Original), gstack-openclaw-skills Team
tags: [planning, engineering, architecture, technical, review]
---

# Plan Engineering Review - Engineering Architecture Review

Technical planning skill from an engineering manager perspective.

## When to Use This Skill

Use this skill when the user says:

- "engineering review"
- "architecture review"
- "tech review"
- "is this the right approach?"
- Evaluating technical architecture and implementation

## Engineering Review Framework

### 1. Architecture Assessment

- Is the architecture appropriate for the scale?
- Are there simpler alternatives?
- Does it follow established patterns in the codebase?

### 2. Technical Risks

- What could go wrong technically?
- Are there known failure modes?
- What's the blast radius if this fails?

### 3. Scalability

- Will this work at 10x current load?
- What are the bottlenecks?
- How does it degrade gracefully?

### 4. Maintainability

- Will future engineers understand this?
- Is it testable?
- Does it follow SOLID principles?

### 5. Dependencies

- What external dependencies are introduced?
- Are there better alternatives?
- What's the upgrade/migration path?

### 6. Implementation Estimate

- Complexity: Low / Medium / High
- Time estimate: [X days/weeks]
- Team size needed: [X engineers]

## Output Format

```markdown
## Engineering Review

### Architecture Assessment
[Evaluation of the proposed architecture]

### Technical Risks
1. [Risk 1] - Mitigation: [...]
2. [Risk 2] - Mitigation: [...]

### Recommended Approach
[Specific technical recommendation]

### Alternative Approaches
[Other options considered]

### Implementation Plan
- Phase 1: [...]
- Phase 2: [...]

### Estimate
- Complexity: [Low/Medium/High]
- Time: [X weeks]
```

---

**Original**: gstack/plan-eng-review by Garry Tan  
**Adaptation**: OpenClaw/WorkBuddy version  
**Version**: 2.0.0
