---
name: brain
version: 1.3.0
description: |
  Personal knowledge base for capturing and retrieving information about people,
  places, restaurants, games, tech, events, media, ideas, and organizations.
  Use when: user mentions a person, place, restaurant, landmark, game, device,
  event, book/show, idea, or company. Trigger phrases: "remember", "note that",
  "met this person", "visited", "played", "what do I know about", etc.
  Brain entries take precedence over daily logs for named entities.
setup: |
  This skill uses OpenClaw's built-in memory_search and memory_get tools for
  search and retrieval — no external dependencies required.

  Optional: For richer BM25 + vector + reranking search, enable the QMD backend:
    1. Install QMD CLI: bun install -g https://github.com/tobi/qmd
    2. Set memory.backend = "qmd" in openclaw.json
    3. Add brain/ to memory.qmd.paths in openclaw.json:
         paths: [{ name: "brain", path: "~/.openclaw/workspace/brain", pattern: "**/*.md" }]

  The skill degrades gracefully to OpenClaw's built-in search if QMD is not configured.
permissions:
  paths:
    - "~/.openclaw/workspace/brain/**"
  write: true
  attachments: true
---

# Brain Skill — 2nd Brain Knowledge Base

A personal knowledge management system for capturing and retrieving information about people, places, things, and ideas.

## When to Use This Skill

**Brain takes precedence over daily logs for named entities.**

Trigger this skill when:
- User asks you to remember someone, something, or somewhere
- User shares information about a person, place, game, tech, event, media, idea, or organization
- User expresses a preference about an entity ("I like X at Y restaurant" -> update Y's file)
- User asks about something that might be in the brain ("Who was that guy from...", "What did I think about...")
- User updates existing knowledge ("Actually, he's 27 now", "I finished that game")

**Keywords that trigger:** "remember", "note that", "met this person", "visited", "played", "watched", "read", "idea:", "what do I know about", "who is", "where was"

**Do NOT put brain-eligible content in daily logs.** If it's a named entity (person, place, restaurant, product, game, etc.), it belongs in `brain/`, not `memory/YYYY-MM-DD.md`. Daily logs are for session context and ephemeral notes only.

## Data Location

All brain data lives in: `~/.openclaw/workspace/brain/`

```
brain/
  people/       # Contacts, people you've met
  places/       # Restaurants, landmarks, venues
  games/        # Video games and interactions
  tech/         # Devices, products, specs, gotchas
  events/       # Conferences, meetups, gatherings
  media/        # Books, shows, films, podcasts
  ideas/        # Business ideas, concepts, thoughts
  orgs/         # Companies, communities, groups
```

## Search & Retrieval

Use `memory_search` for all brain lookups:
```
memory_search("person name")
memory_search("restaurant name")
memory_search("what do I know about X")
```

Use `memory_get` to read a specific brain file:
```
memory_get("brain/people/name.md")
```

## Operational Rules

### Creating a New Entry
1. Search first — `memory_search("<name or topic>")` to check existing
2. No match — Create new file in appropriate category folder
3. Possible clash — List matches, ask user to confirm

### Updating an Existing Entry
1. Find the file — `memory_search` or direct path
2. Surgical edit — Update only relevant section
3. Log the date — Add timestamp to Notes section
4. Update `last_updated` field

## Categories Reference

| Category | Folder | Use For |
|----------|--------|---------|
| People | `brain/people/` | Anyone user has met or wants to remember |
| Places | `brain/places/` | Restaurants, landmarks, venues, locations |
| Games | `brain/games/` | Video games — status, opinions, notes |
| Tech | `brain/tech/` | Devices, products, specs, quirks |
| Events | `brain/events/` | Conferences, meetups, gatherings |
| Media | `brain/media/` | Books, shows, films, podcasts |
| Ideas | `brain/ideas/` | Business ideas, concepts, random thoughts |
| Orgs | `brain/orgs/` | Companies, communities, groups |
