# Claude Code Architecture: Commands, Skills, and Subagents

**Version:** 1.0
**Last Updated:** January 4, 2026
**Author:** Suman Addanki

---

## Table of Contents

1. [Critical Understanding: Claude Code vs Claude API](#critical-understanding)
2. [The Three Mechanisms](#the-three-mechanisms)
3. [Slash Commands Deep Dive](#slash-commands-deep-dive)
4. [Skills Deep Dive](#skills-deep-dive)
5. [Subagents Deep Dive](#subagents-deep-dive)
6. [Main Agent vs Subagents](#main-agent-vs-subagents)
7. [Memory and Session History](#memory-and-session-history)
8. [Multi-Model Strategy](#multi-model-strategy)
9. [How QUAD Platform Will Work](#how-quad-platform-will-work)
10. [FAQ](#faq)

---

## Critical Understanding

### Claude Code vs Claude API - VERY IMPORTANT

```
┌─────────────────────────────────────────────────────────────────────┐
│                    TWO DIFFERENT THINGS                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  CLAUDE CODE (VS Code Extension)                                   │
│  ├── Has: Commands, Skills, Subagents                              │
│  ├── Runs in: VS Code IDE                                          │
│  ├── Features: Auto-triggers, file watching, IDE integration       │
│  └── Magic: Skills auto-invoke based on context                    │
│                                                                     │
│  CLAUDE API (HTTP Calls)                                           │
│  ├── Has: NONE of the above                                        │
│  ├── Runs in: Your backend server                                  │
│  ├── Features: Just sends messages, gets responses                 │
│  └── Magic: NONE - you must implement everything yourself          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Key Insight:**

When QUAD Platform makes HTTP API calls to Claude (Anthropic API), there are NO:
- Slash commands
- Skills
- Subagents
- Auto-triggers

These are **Claude Code (VS Code extension) features ONLY**.

QUAD Platform must **implement its own** skill/agent routing system.

---

## The Three Mechanisms

| Mechanism | Invocation | Complexity | Use Case |
|-----------|------------|------------|----------|
| **Slash Commands** | Manual (`/command`) | Low | Frequent typed actions |
| **Skills** | Auto (Claude decides) | Medium | Teaching Claude capabilities |
| **Subagents** | Manual or delegated | High | Specialized AI personas |

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MECHANISM COMPARISON                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  SLASH COMMANDS                                                    │
│  ┌──────────────────┐                                              │
│  │ User types /cmd  │ ──→ Executes prompt ──→ Response             │
│  └──────────────────┘                                              │
│  Simple, manual, same conversation context                         │
│                                                                     │
│  SKILLS                                                            │
│  ┌──────────────────┐                                              │
│  │ Claude sees      │                                              │
│  │ relevant context │ ──→ Auto-loads skill ──→ Enhanced response   │
│  └──────────────────┘                                              │
│  Automatic, context-aware, same conversation                       │
│                                                                     │
│  SUBAGENTS                                                         │
│  ┌──────────────────┐     ┌──────────────────┐                     │
│  │ Main Agent       │ ──→ │ Subagent         │ ──→ Result back     │
│  │ (delegates task) │     │ (own context)    │                     │
│  └──────────────────┘     └──────────────────┘                     │
│  Separate context, own memory, can use different model             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Slash Commands Deep Dive

### What They Are

A slash command is a shortcut that expands into a prompt template.

### File Structure

```
.claude/commands/
├── deploy.md           → /deploy
├── review.md           → /review
└── frontend/
    └── test.md         → /frontend:test
```

### Example: Deploy Command

**File:** `.claude/commands/deploy.md`

```markdown
---
description: Deploy to specified environment
argument-hint: [dev|qa|prod]
allowed-tools: Bash
---

Deploy the application to $1 environment:

1. Run tests first
2. Build the application
3. Deploy using ./deploy-studio.sh $1
4. Verify deployment succeeded
```

**Usage:**
```
User: /deploy dev
Claude: [Executes the prompt with $1 = "dev"]
```

### Can Subagents Use Slash Commands?

**No.** Slash commands are user-invoked only. However, a subagent CAN be instructed to perform the same actions described in a command.

---

## Skills Deep Dive

### What They Are

Skills teach Claude HOW to do something, with reference materials. Claude auto-decides when to use them.

### File Structure

```
.claude/skills/
└── code-review/
    ├── SKILL.md           ← Main definition (required)
    ├── CHECKLIST.md       ← Reference file
    ├── examples/
    │   ├── good-review.md ← Example of good output
    │   └── bad-review.md  ← Example of bad output
    └── templates/
        └── review-format.md
```

### SKILL.md Anatomy

```markdown
---
name: code-review
description: Review code for quality, security, and best practices
triggers:                              ← WHEN to auto-invoke
  - "review this code"
  - "check for bugs"
  - "code review"
allowed-tools: Read, Grep, Glob
---

# Code Review Skill

When reviewing code, follow these steps:

1. Read CHECKLIST.md for review criteria
2. Check examples/good-review.md for format
3. Look for:
   - Security vulnerabilities
   - Performance issues
   - Code style violations
   - Missing tests
```

### When Are Skills Auto-Invoked?

**Trigger Conditions:**

1. **Keyword triggers** - User says "review this code" (matches triggers list)
2. **Context triggers** - Claude detects relevant situation
3. **File triggers** - User opens specific file types

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SKILL AUTO-INVOCATION FLOW                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. User says: "Can you review this function?"                     │
│                        │                                           │
│                        ▼                                           │
│  2. Claude Code checks: Does this match any skill triggers?        │
│     - "review" matches code-review skill triggers                  │
│                        │                                           │
│                        ▼                                           │
│  3. Claude Code loads: code-review/SKILL.md + reference files      │
│                        │                                           │
│                        ▼                                           │
│  4. Claude responds: Using skill knowledge + checklist + examples  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Skill vs Agent: What's the Difference?

| Aspect | Skill | Subagent |
|--------|-------|----------|
| **Context** | Same conversation | Separate conversation |
| **Memory** | Shared with main | Own memory |
| **Invocation** | Auto (Claude decides) | Manual or delegated |
| **Model** | Same model | Can be different |
| **Purpose** | Enhance main agent | Delegate specialized task |

**Code Review Skill** = Main Claude gets better at reviewing (same conversation)
**Code Review Agent** = Separate Claude instance that ONLY does reviews (isolated)

### More Skill Examples

#### 1. Security Audit Skill

```
.claude/skills/security-audit/
├── SKILL.md
├── OWASP_TOP_10.md
├── common-vulnerabilities.md
└── secure-patterns/
    ├── auth.md
    └── input-validation.md
```

**SKILL.md:**
```markdown
---
name: security-audit
description: Audit code for security vulnerabilities
triggers:
  - "security review"
  - "check for vulnerabilities"
  - "audit security"
allowed-tools: Read, Grep
---

# Security Audit Skill

Check against OWASP_TOP_10.md criteria.
Reference common-vulnerabilities.md for patterns.
Suggest fixes from secure-patterns/ folder.
```

#### 2. Database Migration Skill

```
.claude/skills/db-migration/
├── SKILL.md
├── migration-checklist.md
├── rollback-template.sql
└── examples/
    └── safe-migration.sql
```

**SKILL.md:**
```markdown
---
name: db-migration
description: Create safe database migrations
triggers:
  - "create migration"
  - "alter table"
  - "add column"
allowed-tools: Read, Write, Bash
---

# Database Migration Skill

1. Check migration-checklist.md before ANY schema change
2. Always create rollback script (see rollback-template.sql)
3. Follow examples/safe-migration.sql patterns
```

#### 3. Test Generation Skill

```
.claude/skills/test-generation/
├── SKILL.md
├── test-patterns.md
├── coverage-requirements.md
└── examples/
    ├── unit-test.java
    └── integration-test.java
```

---

## Subagents Deep Dive

### What They Are

Subagents are **separate Claude instances** with their own:
- Context/memory
- Rules
- Allowed tools
- (Optionally) Different AI model

### File Structure

```
.claude/agents/
└── security-specialist/
    └── AGENT.md
```

### AGENT.md Anatomy

```markdown
---
name: security-specialist
description: Security-focused code analysis
model: claude-opus-4-5-20251101        ← Can specify model
allowed-tools: Read, Grep, Glob
skills: security-audit                  ← Can use skills
---

# Security Specialist Agent

You are a SECURITY EXPERT. Your ONLY focus is:
- OWASP Top 10 vulnerabilities
- Authentication/authorization flaws
- Injection attacks
- Data exposure

DO NOT comment on:
- Code style
- Performance (unless security-related)
- Architecture decisions
```

### What Happens When `/agents security-specialist` is Called?

```
┌─────────────────────────────────────────────────────────────────────┐
│            /agents security-specialist EXECUTION FLOW               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. User types: /agents security-specialist                        │
│                        │                                           │
│                        ▼                                           │
│  2. Claude Code reads: .claude/agents/security-specialist/AGENT.md │
│                        │                                           │
│                        ▼                                           │
│  3. NEW Claude instance created with:                              │
│     - System prompt from AGENT.md                                  │
│     - Model: claude-opus-4-5-20251101 (from config)                │
│     - Tools: Read, Grep, Glob only                                 │
│     - Skills: security-audit loaded                                │
│                        │                                           │
│                        ▼                                           │
│  4. Subagent runs in ISOLATION:                                    │
│     - Cannot see main conversation                                 │
│     - Has own memory/context                                       │
│     - Focused only on security                                     │
│                        │                                           │
│                        ▼                                           │
│  5. Result returned to main conversation                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Subagent Memory

**Each subagent has its OWN session/memory:**

```
Main Agent (root)
├── Memory: Full conversation history
├── Context: Everything discussed
│
├── Subagent: security-specialist
│   ├── Memory: Only security-related tasks
│   └── Context: Isolated from main
│
└── Subagent: code-reviewer
    ├── Memory: Only code review tasks
    └── Context: Isolated from main
```

**There is NO global session history for subagents.** Each is independent.

---

## Main Agent vs Subagents

### The "Root" or "Main" Agent

When you open Claude Code in VS Code, you're talking to the **main agent**.

**How to configure the main agent:**

1. **CLAUDE.md** - Project instructions (loaded automatically)
2. **~/.claude/CLAUDE.md** - Personal instructions (loaded automatically)
3. **.claude/settings.json** - Allowed tools, behaviors

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MAIN AGENT CONFIGURATION                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  CLAUDE.md (root of project)                                       │
│  ├── Project overview                                              │
│  ├── Tech stack                                                    │
│  ├── Coding standards                                              │
│  └── Rules for THIS project                                        │
│                                                                     │
│  ~/.claude/CLAUDE.md (your home folder)                            │
│  ├── Your personal preferences                                     │
│  ├── Cross-project rules                                           │
│  └── Your coding style                                             │
│                                                                     │
│  .claude/settings.json                                             │
│  ├── Allowed tools                                                 │
│  ├── Denied tools                                                  │
│  └── Behavior settings                                             │
│                                                                     │
│  RESULT: Main agent = CLAUDE.md + ~/.claude/CLAUDE.md + settings   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Giving Rules to Main Agent vs Subagent

| What | Main Agent | Subagent |
|------|------------|----------|
| **Rules location** | CLAUDE.md | AGENT.md |
| **Session history** | Automatic (in conversation) | Separate per subagent |
| **Model** | Default (settings) | Can override in AGENT.md |
| **Tools** | settings.json | AGENT.md `allowed-tools` |

---

## Memory and Session History

### Main Agent Memory

The main agent's "memory" IS the conversation. Claude Code doesn't persist sessions by default.

**To persist session history:**
- Use `.claude/commands/` to load context files
- Use CLAUDE.md to store key decisions
- Use our custom SESSION_HISTORY.md approach

### Subagent Memory

**Subagents do NOT persist memory between invocations.**

Each time you call `/agents security-specialist`, it starts fresh.

**To give subagents "memory":**

```markdown
---
name: security-specialist
description: Security analysis with memory
---

# Security Specialist

Before analyzing, read these files for context:
- .claude/agents/security-specialist/HISTORY.md
- .claude/agents/security-specialist/KNOWN_ISSUES.md

After analyzing, append findings to HISTORY.md.
```

---

## Multi-Model Strategy

### Different Models for Different Tasks

```markdown
---
name: story-writer
model: gemini-pro                    ← Cheaper model for content
allowed-tools: Read, Write
---

# Story Writer Agent

Write user stories. You're good at creative content.
```

```markdown
---
name: code-implementer
model: claude-opus-4-5-20251101     ← Best model for code
allowed-tools: Read, Write, Edit, Bash
---

# Code Implementer Agent

Implement the code based on the story provided.
```

### QUAD's Planned Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    QUAD MULTI-MODEL PIPELINE                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. STORY CREATION (Gemini - cheap)                                │
│     └── story-agent (gemini-pro)                                   │
│         └── Creates user story from requirements                   │
│                        │                                           │
│                        ▼                                           │
│  2. ARCHITECTURE (Claude Sonnet - balanced)                        │
│     └── architect-agent (claude-sonnet)                            │
│         └── Designs implementation approach                        │
│                        │                                           │
│                        ▼                                           │
│  3. CODE IMPLEMENTATION (Claude Opus - best)                       │
│     └── developer-agent (claude-opus)                              │
│         └── Writes actual code                                     │
│                        │                                           │
│                        ▼                                           │
│  4. CODE REVIEW (Claude Sonnet - balanced)                         │
│     └── reviewer-agent (claude-sonnet)                             │
│         └── Reviews and suggests improvements                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## How QUAD Platform Will Work

### The Key Insight

**Claude Code features (commands, skills, subagents) work in VS Code ONLY.**

When QUAD Platform makes HTTP API calls, we must implement our own system.

### QUAD's Agent System (Custom Implementation)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    QUAD PLATFORM ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  QUAD Platform Backend (Java)                                      │
│  ├── AgentService.java                                             │
│  │   ├── loadAgentConfig(agentName)                                │
│  │   ├── buildSystemPrompt(config, context)                        │
│  │   └── routeToModel(agentName) → Claude/Gemini/etc              │
│  │                                                                 │
│  ├── Agent Templates (resources/)                                  │
│  │   ├── story-agent.json                                          │
│  │   ├── developer-agent.json                                      │
│  │   └── reviewer-agent.json                                       │
│  │                                                                 │
│  └── Agent Router                                                  │
│      ├── Decides which agent to use                                │
│      ├── Chains agents together                                    │
│      └── Manages context passing                                   │
│                                                                     │
│  HTTP Call to Claude API:                                          │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │ POST /v1/messages                                           │   │
│  │ {                                                           │   │
│  │   "model": "claude-opus-4-5-20251101",                      │   │
│  │   "system": "[Agent config + rules + context]",             │   │
│  │   "messages": [...]                                         │   │
│  │ }                                                           │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  NO skills/commands - we BUILD the system prompt ourselves         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### VS Code Extension (quad-vscode) - DIFFERENT

The VS Code extension CAN use Claude Code's native features:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    QUAD VS CODE EXTENSION                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  quad-vscode/                                                      │
│  └── .claude/                                                      │
│      ├── commands/                                                 │
│      │   ├── quad-story.md       ← /quad-story                     │
│      │   ├── quad-implement.md   ← /quad-implement                 │
│      │   └── quad-review.md      ← /quad-review                    │
│      │                                                             │
│      ├── skills/                                                   │
│      │   └── quad-methodology/                                     │
│      │       └── SKILL.md        ← Auto-applies QUAD rules         │
│      │                                                             │
│      └── agents/                                                   │
│          ├── story-agent/AGENT.md                                  │
│          ├── developer-agent/AGENT.md                              │
│          └── reviewer-agent/AGENT.md                               │
│                                                                     │
│  This USES Claude Code's native features                           │
│  User types /quad-story → Claude Code handles it                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## FAQ

### Q: Can agents use slash commands internally?

**No.** Slash commands are user-invoked only. However:
- Subagents can be INSTRUCTED to do the same actions
- QUAD Platform can chain agents programmatically

### Q: When does "Claude automatically reads these files at session start"?

**Only in Claude Code (VS Code).** When you:
1. Open VS Code in a project folder
2. Claude Code extension activates
3. It reads CLAUDE.md automatically

This does NOT happen with HTTP API calls.

### Q: Is VS Code calling skills explicitly?

**No.** Claude Code's skill system is automatic:
1. User says something
2. Claude Code checks if it matches skill triggers
3. If yes, loads skill context invisibly
4. Claude responds with enhanced knowledge

### Q: When I use HTTP API from QUAD, do I call skills explicitly?

**Skills don't exist in HTTP API.** You must:
1. Build system prompt with all rules/context
2. Send to Claude API
3. Handle response

```java
// QUAD Platform - NO skills, manual context
String systemPrompt = buildSystemPrompt(
    agentConfig,           // Agent rules
    projectContext,        // Project info
    userPreferences,       // User settings
    relevantFiles          // Context files
);

claudeClient.messages()
    .model("claude-opus-4-5-20251101")
    .system(systemPrompt)
    .messages(userMessage)
    .send();
```

### Q: Is there a "code writer agent"?

In Claude Code, the **main agent** writes code. There's no separate "writer."

In QUAD Platform, you CAN create:
- `story-agent` - Creates stories
- `developer-agent` - Writes code
- `reviewer-agent` - Reviews code

### Q: What's the trigger for skill auto-invocation?

1. **Keyword match** - User message contains trigger words
2. **Context match** - Claude detects relevant situation
3. **File match** - User is editing certain file types

Example triggers:
```yaml
triggers:
  - "review this code"      # Keyword
  - "check for bugs"        # Keyword
  - "*.test.js"             # File pattern (when editing test files)
```

---

## Summary

| Feature | Claude Code (VS Code) | Claude API (HTTP) |
|---------|----------------------|-------------------|
| Slash Commands | Yes (`/command`) | No (implement yourself) |
| Skills | Yes (auto-trigger) | No (implement yourself) |
| Subagents | Yes (`/agents name`) | No (implement yourself) |
| CLAUDE.md | Auto-loaded | Manual (put in system prompt) |
| Multi-model | Via AGENT.md | Manual (specify in API call) |

**For QUAD Platform:**
- VS Code Extension → Use Claude Code features
- Backend API calls → Implement custom agent system
- Web Dashboard → Implement custom agent system

---

**Next Steps (Pending):**
1. ✅ Migration to `.claude/` complete (Jan 4, 2026)
2. Design QUAD Agent Templates for HTTP API (pending)
3. Build AgentService.java for QUAD Platform (pending)
