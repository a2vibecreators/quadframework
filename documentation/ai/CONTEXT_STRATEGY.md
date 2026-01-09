# AI Context Strategy - When to Use RAG

## Overview

QUAD builds intelligent context for Claude AI using multiple sources:
1. **Rules** (from database) - Industry defaults + org customizations
2. **QUAD Sync** (from external systems) - Jira, GitHub, Slack history
3. **RAG Search** (from project history) - Past code, decisions, patterns

---

## Context Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTEXT SENT TO CLAUDE AI                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Layer 1: ALWAYS INCLUDE (Cheap - Cached)                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ • Industry rules (DO/DONT)                                │  │
│  │ • Org customizations                                      │  │
│  │ • Activity type context                                   │  │
│  │ • Tech stack (Java/TypeScript/etc.)                       │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Layer 2: WHEN AVAILABLE (From QUAD Sync)                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ • Jira ticket details (acceptance criteria, comments)     │  │
│  │ • Related tickets (linked issues)                         │  │
│  │ • GitHub PR context (if modifying existing code)          │  │
│  │ • Slack thread (if task came from discussion)             │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Layer 3: RAG SEARCH (When Pattern Matching Needed)             │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ • Similar past implementations                            │  │
│  │ • User's coding style from history                        │  │
│  │ • Previous decisions on similar tasks                     │  │
│  │ • Existing codebase patterns                              │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## When to Use RAG Search

### ✅ USE RAG (Search Project History)

| Scenario | What to Search | Why |
|----------|---------------|-----|
| **"Add similar endpoint"** | Past API implementations in same domain | Match existing patterns |
| **"Follow existing pattern"** | User's previous code for same activity type | Consistency |
| **"Like we did for X"** | Specific past ticket/PR | Exact reference |
| **New developer on project** | Team's coding conventions | Onboarding context |
| **Complex business logic** | Past decisions, comments, discussions | Institutional knowledge |

### ❌ SKIP RAG (Save Tokens)

| Scenario | Why Skip |
|----------|----------|
| Simple CRUD operations | Industry rules are enough |
| Greenfield project (no history) | Nothing to search |
| Explicit user instructions | User provided all context |
| Standard library usage | No org-specific patterns |

---

## RAG Search Strategy

### Database Tables for RAG

```sql
-- Project history (from QUAD Sync)
QUAD_sync_jira_tickets      -- Synced Jira tickets with descriptions
QUAD_sync_github_commits    -- Commit messages and diffs
QUAD_sync_github_prs        -- PR descriptions and reviews
QUAD_sync_slack_threads     -- Relevant Slack discussions

-- Code generation history (our own)
QUAD_generated_code         -- Past generated code
QUAD_generation_feedback    -- User feedback (thumbs up/down, edits)
QUAD_user_preferences       -- User's coding style preferences
```

### Search Algorithm

```
1. Extract keywords from task description
   - "Add payment API" → ["payment", "API", "endpoint"]

2. Filter by relevance
   - Same org
   - Same domain (if specified)
   - Same activity type
   - Recent (last 6 months weighted higher)

3. Rank results
   - Exact keyword match: +10
   - Same author (user preference): +5
   - Positive feedback (thumbs up): +3
   - Recency: +1 per month recent

4. Return top 3-5 results
   - Include: code snippet, context, why it matched
   - Truncate if too long (token budget)
```

---

## QUAD Sync Integration Points

### Jira Sync
```
When: Task comes from Jira ticket
What to fetch:
  - Ticket description
  - Acceptance criteria
  - Comments (last 10)
  - Linked tickets (Epic, related issues)
  - Attachments (if design specs)
```

### GitHub Sync
```
When: Modifying existing code
What to fetch:
  - File content being modified
  - Recent commits to that file
  - Open PRs for same area
  - Code review comments
```

### Slack Sync
```
When: Task references Slack discussion
What to fetch:
  - Thread messages
  - Shared files/links
  - Decision points
```

---

## Token Budget Management

```
Total context budget: 8000 tokens (configurable)

Allocation:
├── Rules (Layer 1):        500-1000 tokens (always)
├── QUAD Sync (Layer 2):    2000-3000 tokens (when available)
├── RAG Results (Layer 3):  2000-3000 tokens (when searching)
└── User prompt:            1000-2000 tokens (task description)

If over budget:
1. Truncate RAG results first
2. Summarize QUAD Sync context
3. Keep rules intact (never truncate)
```

---

## Implementation Example

```typescript
// Context builder for code generation
async function buildContext(task: Task, org: Organization, user: User) {
  const context: AIContext = {
    rules: [],      // Layer 1
    quadSync: {},   // Layer 2
    ragResults: [], // Layer 3
  };

  // Layer 1: Always fetch rules (CACHED)
  context.rules = await getAgentRules(org.id, task.activityType);

  // Layer 2: Fetch from QUAD Sync (if task has source)
  if (task.jiraTicketId) {
    context.quadSync.jira = await fetchJiraContext(task.jiraTicketId);
  }
  if (task.githubPrId) {
    context.quadSync.github = await fetchGitHubContext(task.githubPrId);
  }
  if (task.slackThreadId) {
    context.quadSync.slack = await fetchSlackContext(task.slackThreadId);
  }

  // Layer 3: RAG search (if pattern matching needed)
  if (shouldUseRAG(task)) {
    context.ragResults = await searchProjectHistory({
      orgId: org.id,
      keywords: extractKeywords(task.description),
      activityType: task.activityType,
      userId: user.id,  // For coding style matching
      limit: 5,
    });
  }

  // Build final prompt with token budget
  return buildPromptWithBudget(context, MAX_TOKENS);
}

// Decision: When to use RAG
function shouldUseRAG(task: Task): boolean {
  const triggers = [
    task.description.includes("similar"),
    task.description.includes("like we did"),
    task.description.includes("follow pattern"),
    task.description.includes("existing"),
    task.activityType === "refactor",
    task.isComplexBusinessLogic,
  ];
  return triggers.some(t => t);
}
```

---

## Caching Strategy

| Cache | TTL | Invalidation |
|-------|-----|--------------|
| Agent Rules | 5 min | On rule update |
| Org Context | 10 min | On org settings change |
| QUAD Sync (Jira) | 1 min | On ticket update webhook |
| RAG Search Results | 15 min | On new code generation |

---

## Metrics to Track

```
1. Context effectiveness
   - User acceptance rate by context type
   - Edits required after generation

2. Token efficiency
   - Tokens used vs generation quality
   - Cache hit rate

3. RAG relevance
   - Click-through on suggested patterns
   - "Use this pattern" selections
```

---

## Summary

**Simple Rule:**
- **Layer 1 (Rules)**: Always include - cheap, cached
- **Layer 2 (QUAD Sync)**: Include if source exists - adds relevance
- **Layer 3 (RAG)**: Search only when pattern matching needed - saves tokens

**User Philosophy:**
> "QUAD Sync connects to their systems, so we can build rich context from their Jira, GitHub, Slack. RAG searches their project history for patterns. Rules are always there. Smart context = better code generation."
