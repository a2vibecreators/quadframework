---
description: Initialize QUAD development session
allowed-tools: Read
---

# QUAD Agent Initialization

You are the QUAD Framework AI Agent. Initialize by following these steps:

## STEP 1: READ CONTEXT FILES (in this order)

1. Read `CLAUDE.md` - Project architecture, deployment, tech stack
2. Read `.claude/rules/AGENT_RULES.md` - Learn the 10 core rules
3. Read `.claude/rules/SESSION_HISTORY.md` - Know what happened in previous sessions
4. Read `.claude/rules/CONTEXT_FILES.md` - Quick reference to key files

## STEP 2: GREET USER WITH CONTEXT

After reading the files above, greet me with:
```
QUAD Agent Initialized

Last Session: [Date and main topics from SESSION_HISTORY.md]
Key Decisions: [1-2 most recent decisions]
Current Focus: [What was being worked on]
Tech Stack: Next.js 15 + Java Spring Boot + PostgreSQL

What would you like to work on today, macha?
```

## STEP 3: DURING SESSION - FOLLOW RULES

**Critical Rules (from AGENT_RULES.md):**
- 7-day context window - compress older sessions
- Always check context files first before starting work
- Update SESSION_HISTORY.md after major milestones
- Use TodoWrite for multi-step tasks
- Database tables use QUAD_ prefix
- Ask before production deployment
- Use conventional commits (feat:, fix:, docs:, chore:)

**Tech Stack Reminders:**
- Frontend: Next.js 15 (App Router) + TypeScript + Tailwind
- Backend: Java Spring Boot 3.2.1 + Maven
- Database: PostgreSQL with Prisma ORM (quad-web) + JPA (quad-services)
- Secrets: Vaultwarden (vault.a2vibes.tech)

**Deployment:**
- DEV: https://dev.quadframe.work (port 14001)
- QA: https://qa.quadframe.work (port 15001)
- Deploy: `./deploy-studio.sh dev|qa|all`

Now initialize and greet me.
