---
name: document-release
description: >
  Technical writer skill for updating documentation after releases. Use when user 
  says "document release", "update docs", "write release notes", or documentation 
  needs to be updated after code changes.
version: 2.0.0
author: Garry Tan (Original), gstack-openclaw-skills Team
tags: [documentation, release-notes, technical-writing, docs]
---

# Document Release - Technical Writer

Technical writing skill for updating documentation after releases.

## When to Use This Skill

Use this skill when the user says:

- "document release"
- "update docs"
- "write release notes"
- "update changelog"
- After shipping code that needs documentation

## Documentation Checklist

After a release, update:

- [ ] CHANGELOG.md
- [ ] README.md (if APIs changed)
- [ ] API documentation
- [ ] Migration guide (if breaking changes)
- [ ] User-facing docs

## Release Notes Template

```markdown
## [Version] - [Date]

### New Features
- **[Feature Name]**: [Description of what it does and why it's useful]

### Bug Fixes
- Fixed [issue description] ([#issue-number])

### Breaking Changes
- **[Change]**: [What changed and how to migrate]

### Deprecations
- [Feature] is deprecated. Use [alternative] instead.

### Performance Improvements
- [Improvement description]
```

## CHANGELOG Format

Follow Keep a Changelog (keepachangelog.com):

```markdown
# Changelog

## [Unreleased]

## [1.2.0] - 2024-01-15
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
```

## API Documentation

For API changes, document:

- Endpoint URL
- Method (GET/POST/PUT/DELETE)
- Request parameters
- Response format
- Example request/response
- Error codes

---

**Original**: gstack/document-release by Garry Tan  
**Adaptation**: OpenClaw/WorkBuddy version  
**Version**: 2.0.0
