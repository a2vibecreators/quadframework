# QUAD Claude Code Configuration

This folder contains Claude Code configuration for QUAD Framework development.

---

## Quick Start

**Initialize session:** Type `/quad-init` in Claude Code

---

## Folder Structure

```
.claude/
├── commands/                    ← Slash commands
│   └── quad-init.md            ← /quad-init
├── rules/                       ← Session rules and context
│   ├── AGENT_RULES.md          ← 10 core rules
│   ├── SESSION_HISTORY.md      ← Previous session context
│   ├── CONTEXT_FILES.md        ← Key files reference
│   └── DATABASE_CHANGELOG.md   ← Schema changes
├── settings.json               ← Team settings (in git)
├── settings.local.json         ← Personal settings (gitignored)
├── config.json                 ← Agent config
└── README.md                   ← This file
```

---

## Reading Order

| Step | File | Purpose |
|------|------|---------|
| 1 | [../CLAUDE.md](../CLAUDE.md) | Project architecture, tech stack |
| 2 | [rules/AGENT_RULES.md](rules/AGENT_RULES.md) | 10 core rules |
| 3 | [rules/SESSION_HISTORY.md](rules/SESSION_HISTORY.md) | Previous sessions |
| 4 | [rules/CONTEXT_FILES.md](rules/CONTEXT_FILES.md) | Key files reference |

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/quad-init` | Initialize QUAD development session |

---

## Session Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    SESSION LIFECYCLE                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. SESSION START                                           │
│     └── Type /quad-init                                     │
│                                                             │
│  2. DURING SESSION                                          │
│     └── Follow rules, use TodoWrite, track progress         │
│                                                             │
│  3. SESSION END                                             │
│     └── Update SESSION_HISTORY.md with outcomes             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Relationship to CLAUDE.md

| File | Purpose | Location |
|------|---------|----------|
| [CLAUDE.md](../CLAUDE.md) | Project documentation | Root |
| `.claude/` | Claude Code configuration | This folder |

**CLAUDE.md is the source of truth** for project info.

---

**Version:** 1.0
**Created:** January 4, 2026
