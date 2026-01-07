# QUAD Platform - Agent Rules (Claude Code)

**Purpose:** Guidelines for Claude Code when working on QUAD Platform
**Last Updated:** January 5, 2026

> **Note:** This is the Claude Code-specific version (14 rules).
> For the full 40-rule developer reference, see [documentation/agents/AGENT_RULES.md](../../documentation/agents/AGENT_RULES.md)

---

## Table of Contents

1. [Core Rules](#core-rules)
   - [1. Session Management](#1-session-management)
   - [2. Always Check Context First](#2-always-check-context-first)
   - [3. Update Session History After Major Milestones](#3-update-session-history-after-major-milestones)
   - [4. Use TodoWrite for Multi-Step Tasks](#4-use-todowrite-for-multi-step-tasks)
   - [5. Database Tables Use QUAD_ Prefix](#5-database-tables-use-quad_-prefix)
   - [6. Follow Architecture Decisions](#6-follow-architecture-decisions)
   - [7. Agent Role Philosophy](#7-agent-role-philosophy-combined-by-default-flexible-for-enterprises)
   - [8. Documentation Structure](#8-documentation-structure)
   - [9. Ask Before Production Deployment](#9-ask-before-production-deployment)
   - [10. Git Commit Messages](#10-git-commit-messages)
   - [11. Code Style](#11-code-style)
   - [12. Consistency is Critical](#12-consistency-is-critical-user-priority)
   - [13. API Versioning Strategy](#13-api-versioning-strategy-branch-based)
   - [14. Always Read Files Before Editing](#14-always-read-files-before-editing)
2. [Project-Specific Context](#project-specific-context)
3. [When Context is Lost](#when-context-is-lost)

---

## Core Rules

### 1. Session Management

**7-Day Active Context Window:**
- Keep detailed context for last 7 days of work
- After 7 days, compress conversation into "Problem → Solution" format
- Archive compressed sessions in `.claude/archive/`

**Compression Format:**
```markdown
## [Date] - [Feature Name]

**Problem:** What we needed to build
**Solution:** What was built (outcome only, not how)
**Code:** Key files created/modified
**Next:** What comes next
```

**Example (Compressed):**
```markdown
## December 31, 2025 - OAuth SSO

**Problem:** Need enterprise SSO authentication (Okta, Azure AD, Google, etc.)
**Solution:** Implemented NextAuth.js with 6 SSO providers. Free tier enforces 5 user limit.
**Code:** `src/app/api/auth/[...nextauth]/route.ts`, `QUAD_users` table updated with `oauth_provider` column
**Next:** Build auth pages (signup/login UI)
```

**Don't keep:**
- ❌ Back-and-forth discussion ("what if we use X?" "no, Y is better")
- ❌ Debugging steps ("tried A, failed, tried B, worked")
- ❌ Alternative approaches that weren't chosen

**Do keep:**
- ✅ Final architectural decision
- ✅ Why we chose it
- ✅ What was built
- ✅ Where code lives

### 2. Always Check Context First

Before starting work, read:
1. [SESSION_HISTORY.md](SESSION_HISTORY.md) - Previous session context
2. [CONTEXT_FILES.md](CONTEXT_FILES.md) - Key files reference
3. Current TodoWrite list

### 3. Update Session History After Major Milestones

**When to update:**
- ✅ Feature complete (OAuth SSO, Dashboard, etc.)
- ✅ Architectural decision made (self-hosted, polling, etc.)
- ✅ Sprint/milestone complete

**Don't update for:**
- ❌ Small bug fixes
- ❌ Minor documentation changes
- ❌ Work in progress

**CRITICAL:** When making ANY design/architecture change, ALSO update:
1. ✅ Sitemap: `documentation/sitemap/sitemap_documentation.md`
2. ✅ Project structure: `.claude/rules/PROJECT_STRUCTURE.md`
3. ✅ Codebase index: If schema/API/component changes

**Why:** Until version 1.0 is finalized, documentation MUST stay in sync with code changes.

### 4. Use TodoWrite for Multi-Step Tasks

Always use TodoWrite when:
- Task has 3+ steps
- Multiple files affected
- Takes > 30 minutes

**Update status immediately:**
- Mark "in_progress" when starting
- Mark "completed" immediately after finishing (don't batch)

### 5. Database Tables Use QUAD_ Prefix

**Location:** `/Users/semostudio/git/a2vibecreators/nutrinine/nutrinine-database/sql/tables/quad_platform/`

**Tables:**
- `QUAD_companies`
- `QUAD_users`
- `QUAD_company_integrations`
- `QUAD_agent_downloads`
- `QUAD_sessions`
- `QUAD_login_codes`

**Important:** QUAD_ tables share database with NutriNine, but **NO foreign keys** between them.

### 6. Follow Architecture Decisions

**Deployment:** Self-hosted (customer's cloud), not SaaS
**Auth:** OAuth SSO only (Okta, Azure AD, Google, GitHub, Auth0, OIDC)
**Data Sync:** Polling (30s interval), not webhooks
**Pricing:** Free (5 users), Pro ($99/month), Enterprise ($499/month)

### 7. Agent Role Philosophy: Combined by Default, Flexible for Enterprises

**QUAD Platform's Ideology:**

**Default (Recommended for Startups/Small Teams):**
- ✅ Combined PM/BA/TL Agent - One agent handles Product Manager + Business Analyst + Tech Lead responsibilities
- **Why:** Startups often have one person wearing multiple hats (PM/BA/TL combined)
- **Agent:** `agent-product-tech-lead.md`

**Flexible (Available for Enterprise Clients):**
- 🔧 Separate PM, BA, TL Agents - If client explicitly requests separation
- **Why:** Large enterprises may have dedicated roles for each
- **Agents:** `agent-product-manager.md`, `agent-business-analyst.md`, `agent-tech-lead.md`
- **When to offer:** Only when client asks ("Do you have separate PM and TL agents?")

**Default Agent Roles (Static Site - quadframe.work):**
| Agent | Role | Targets |
|-------|------|---------|
| `agent-product-tech-lead` | PM + BA + TL (combined) | Startups, small teams |
| `agent-developer` | Backend developer | Circle 1 backend development |
| `agent-qa` | QA engineer | Circle 2 testing |
| `agent-infrastructure` | DevOps/SRE | Circle 3 infrastructure |
| `agent-solution-architect` | Solution architect | Enabling team |

**Agent Hierarchy (Inheritance):**

```
agent-base.md (session mgmt, tool config)
  ├── agent-ui.md (Figma, GitHub, Jira, Slack)
  │   ├── agent-ios.md (TestFlight, Xcode, SwiftUI)
  │   ├── agent-android.md (Play Console, Android Studio, Jetpack Compose)
  │   └── agent-web.md (Vercel, npm, Browser DevTools)
  │       ├── agent-nextjs.md (App Router, SSR/SSG, Server Components)
  │       ├── agent-reactjs.md (Hooks, Context, State Management)
  │       ├── agent-vuejs.md (Composition API, Pinia, Vite) [Future]
  │       └── agent-angular.md (Modules, Services, RxJS) [Future]
  │
  ├── agent-database.md (Drivers, Migrations, Backups)
  │   ├── agent-postgresql.md (pg_stat_statements, PgBouncer, Replication)
  │   ├── agent-mssql.md (Query Store, Always On, SSMS)
  │   ├── agent-mysql.md (InnoDB, Replication, Partitioning) [Future]
  │   ├── agent-mongodb.md (Sharding, Replica Sets, Aggregation) [Future]
  │   └── agent-redis.md (Cache strategies, Pub/Sub, Persistence) [Future]
  │
  ├── agent-developer.md (Backend, APIs, Microservices)
  ├── agent-qa.md (Selenium, API testing, Bug tracking)
  ├── agent-infrastructure.md (Docker, Kubernetes, CI/CD)
  └── agent-product-tech-lead.md (PM + BA + TL combined)
```

**Framework-Specific Agents (Web):**
- `agent-nextjs.md` - Next.js do's and don'ts (App Router, SSR vs SSG vs ISR, server components, caching)
- `agent-reactjs.md` - React.js best practices (hooks, state management, performance optimization)
- `agent-vuejs.md` - Vue.js patterns (Composition API, Pinia, reactivity) [Future]
- `agent-angular.md` - Angular best practices (modules, dependency injection, RxJS) [Future]

**Enterprise Customization (Self-Hosted - QUAD Platform):**
If enterprise client requests:
- "We need separate PM and TL agents" → Create `agent-product-manager.md` and `agent-tech-lead.md`
- "We need a dedicated BA" → Create `agent-business-analyst.md`
- "We need mobile + backend on same agent" → Create custom `agent-fullstack-mobile.md`

**Rule:** Don't proactively offer separate agents. Default to combined PM/BA/TL. Only discuss separation if client asks.

**Example Conversation:**
```
Client: "Do you have separate agents for Product Manager and Tech Lead?"
You: "Yes! We default to a combined PM/BA/TL agent for startups, but we can provide
separate agents for enterprises. Would you like us to split these into:
- agent-product-manager (roadmap, requirements, stakeholder management)
- agent-business-analyst (requirements gathering, user stories)
- agent-tech-lead (technical decisions, architecture, code reviews)?"
```

### 8. Documentation Structure

Follow NutriNine pattern:
```
documentation/
├── architecture/
├── deployment/
├── integration/
└── testing/
```

### 9. Ask Before Production Deployment

**Never deploy to production without explicit user approval.**

DEV deployment: ✅ Can do freely
QA/Production: ⚠️ Ask first

### 10. Git Commit Messages

Use conventional commits:
```
feat: Add OAuth SSO with 6 providers
fix: Correct free tier user limit check
docs: Add SSO setup guide
chore: Update .env.example with SSO vars
```

### 11. Code Style

- TypeScript strict mode
- ESLint rules from Next.js
- Tailwind CSS for styling
- Components use shadcn/ui when possible

### 12. Consistency is Critical (User Priority)

**"Macha, consistency is very important to me!"** - User emphasis on patterns and standards.

**Always maintain consistency across:**
1. **Naming Conventions**
   - Java: camelCase methods, PascalCase classes
   - TypeScript/React: camelCase variables, PascalCase components
   - Database: snake_case table/column names with QUAD_ prefix
   - Files: kebab-case for routes, PascalCase for components

2. **Documentation Patterns**
   - Javadoc for Java classes and methods (/** ... */)
   - JSDoc for TypeScript functions
   - Consistent comment style within each language
   - Always include @author and @since tags

3. **Code Structure**
   - Follow established patterns in existing files
   - If one controller has detailed @Operation annotations, all should
   - If one DTO has validation, all should
   - Match indentation, spacing, and formatting of surrounding code

4. **API Patterns**
   - Consistent response format (AuthResponse pattern)
   - Consistent error handling (Map.of("error", message))
   - Consistent endpoint naming (/resource/{id}/action)

**Industry Standards Followed:**
- RESTful API conventions
- Spring Boot best practices
- Next.js App Router patterns
- PostgreSQL naming conventions

**Remember:** Users care more about consistency than perfection. If the codebase does something in a certain way, follow that pattern even if there's a "better" way.

### 13. API Versioning Strategy (Branch-Based)

**User Philosophy:** "I hate AuthController2.java - use Git branches instead!"

**The QUAD Way:**
- Use Git branches (v1, v2) with SAME controller code
- Version prefix comes from environment variable (`api.version.prefix`)
- NO code duplication between versions
- Deploy different branches as separate pods only when both versions need to run

**Code Pattern:**
```java
@RestController
@RequestMapping("${api.version.prefix:/v1}/auth")
public class AuthController {
    // Same code in v1 and v2 branches!
}
```

**Properties Configuration:**
```properties
# application-dev.properties, application-qa.properties, application-prod.properties
api.version.prefix=/v1
```

**When Creating v2:**
1. Create v2 branch from main
2. **NO code changes** to controllers
3. Change properties: `api.version.prefix=/v2`
4. Deploy v2 pod only if both versions need to run simultaneously
5. Database changes **MUST be additive** (add columns/tables, never delete)

**Why This Approach:**
- ✅ Zero code duplication
- ✅ Zero dependency on reverse proxies (Caddy not in PROD)
- ✅ Gradual migration (v1 and v2 run on same database)
- ✅ Simple rollback (keep v1 pod running)

**Never Do:**
- ❌ AuthController2.java
- ❌ Hardcoded /v1 in @RequestMapping (use variable)
- ❌ Breaking database changes (delete columns/tables)
- ❌ Depend on Caddy/nginx for versioning (not in PROD)

### 14. Always Read Files Before Editing

**Critical Rule:** Never use Edit or Write tools without reading the file first.

**Why:**
- Edit tool will ERROR if file hasn't been read
- You need current content to make correct changes
- Prevents accidental overwrites or breaking changes

**Correct Workflow:**
1. ✅ Read file with Read tool
2. ✅ Understand current content
3. ✅ Use Edit tool with exact old_string/new_string
4. ✅ Verify edit was successful

**Wrong Workflow:**
1. ❌ Use Edit tool directly (will fail)
2. ❌ Guess what's in the file
3. ❌ Use Write tool on existing files (overwrites everything)

**Exception:** Only use Write tool for NEW files that don't exist yet.

**Example:**
```
# WRONG
<Edit file_path="SecurityConfig.java" old_string="..." />  ❌ ERROR: File not read

# CORRECT
<Read file_path="SecurityConfig.java" />  ✅ Read first
<Edit file_path="SecurityConfig.java" old_string="..." />  ✅ Now can edit
```

---

## Project-Specific Context

**Two Products:**
1. **quadframe.work** - Static website (free forever)
2. **QUAD Platform** - Self-hosted Docker product (free tier + paid)

**Shared Database:**
- NutriNine tables (no prefix) - Family health app
- QUAD_ tables (QUAD_ prefix) - QUAD Platform
- Same PostgreSQL instance, zero connection between them

**Target Market:**
- Mid-size companies (50-200 developers)
- Enterprises (200+ developers)
- Teams using Jira, GitHub, Slack

---

## When Context is Lost

If conversation compacts or user switches projects:

**You should:**
1. Read [SESSION_HISTORY.md](SESSION_HISTORY.md)
2. Read [AGENT_RULES.md](AGENT_RULES.md) (this file)
3. Read [CONTEXT_FILES.md](CONTEXT_FILES.md)
4. Summarize current state
5. Ask: "Ready to continue? What should I work on next, macha?"

---

**Last Updated:** January 4, 2026
**Maintained By:** Claude Code + Suman Addanki
