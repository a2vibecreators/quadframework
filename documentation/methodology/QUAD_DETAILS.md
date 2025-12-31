# QUAD™ - Quick Unified Agentic Development (Detailed Guide)

---

## Table of Contents

1. [Shared vs Dedicated Resources](#shared-vs-dedicated-resources)
2. [QUAD Hierarchy & Rules](#quad-hierarchy--rules)
3. [Agent Class-Object Pattern](#agent-class-object-pattern)
4. [AI Agent Pipeline](#ai-agent-pipeline)
5. [Agents by Circle](#agents-by-circle)
6. [Estimation Agent Pipeline](#estimation-agent-pipeline-deep-dive)
7. [Flow Documentation](#flow-documentation)
8. [Technical Debt Handling](#technical-debt-handling)
9. [Enabling Teams](#enabling-teams)
10. [Team Setup & Project Lifecycle](#team-setup--project-lifecycle)

---

## Shared vs Dedicated Resources

QUAD allows flexible resource allocation based on project needs:

```
+-------------------------------------------------------------------+
|                    SHARED vs DEDICATED SPECTRUM                    |
+-------------------------------------------------------------------+
|                                                                    |
|  MORE DEDICATED                              MORE SHARED           |
|  <-------------------------------------------------->              |
|                                                                    |
|  +----------+  +----------+  +----------+  +----------+            |
|  | CIRCLE 1 |  | CIRCLE 2 |  | CIRCLE 3 |  | CIRCLE 4 |            |
|  |   MGMT   |  |   DEV    |  |    QA    |  |  INFRA   |            |
|  +----------+  +----------+  +----------+  +----------+            |
|       |             |             |             |                   |
|    Dedicated     Dedicated      Shared       Shared                |
|    per project   per project    across       across                |
|                                 projects     directors             |
|                                                                    |
+-------------------------------------------------------------------+
```

### Default Allocation

| Circle | Default Mode | Can Be Changed? |
|--------|--------------|-----------------|
| **Circle 1 (Management)** | More Dedicated | Yes - can share BA/PM across small projects |
| **Circle 2 (Development)** | More Dedicated | Yes - devs can help other projects |
| **Circle 3 (QA)** | More Shared | Yes - can dedicate if project has enough work |
| **Circle 4 (Infrastructure)** | Purely Shared | Typically shared across all directors |

### Organizational Structure

```
+-------------------------------------------------------------------+
|                    GROUP (e.g., Wealth Management)                 |
+-------------------------------------------------------------------+
|                                                                    |
|    +-----------+    +-----------+    +-----------+                 |
|    |Director A |    |Director B |    |Director C |                 |
|    +-----+-----+    +-----+-----+    +-----+-----+                 |
|          |               |               |                         |
|    +-----+-----+   +-----+-----+   +-----+-----+                   |
|    |Project 1  |   |Project 3  |   |Project 5  |                   |
|    |Project 2  |   |Project 4  |   |Project 6  |                   |
|    +-----------+   +-----------+   +-----------+                   |
|                                                                    |
+--------------------------------------------------------------------+
|                     SHARED RESOURCES                               |
|  +-------------+  +-------------+  +-------------------+           |
|  |  Circle 4   |  |  Circle 3   |  | Enabling Teams    |           |
|  |   (Infra)   |  |  (QA Pool)  |  | (Architect, etc.) |           |
|  |   ALWAYS    |  |   USUALLY   |  |     OPTIONAL      |           |
|  |   SHARED    |  |   SHARED    |  |                   |           |
|  +-------------+  +-------------+  +-------------------+           |
+-------------------------------------------------------------------+
```

---

## QUAD Hierarchy & Rules

### Rule Hierarchy

```
+---------------------------------------+
|     BASE RULES (QUAD Platform)        |  <-- Universal do's and don'ts
+---------------------------------------+
|     COMPANY-WIDE RESTRICTIONS         |  <-- Entity/Org level policies
+---------------------------------------+
|     DIRECTOR RESTRICTIONS             |  <-- Program/Portfolio level
+---------------------------------------+
|     TECH LEAD RESTRICTIONS            |  <-- Team level
+---------------------------------------+
|     TEAM MEMBER CUSTOMIZATION         |  <-- Personal preferences
+---------------------------------------+

RULE: Each level can ADD restrictions, never CONTRADICT upper levels
```

### Example Rules

| Level | Example Rule |
|-------|--------------|
| **Base Rules** | "Never commit secrets to Git" |
| **Company-wide** | "All PRs require 2 reviewers" |
| **Director** | "Use Java 21 only for this program" |
| **Tech Lead** | "Follow our naming conventions" |
| **Team Member** | "I prefer dark mode in IDE" |

### What Can Be Customized

| Setting | Levels That Can Set |
|---------|---------------------|
| Agent on/off | All levels |
| Approval requirements | Company → Director → TL |
| Code standards | Company → Director → TL |
| Tool choices | Director → TL |
| Personal preferences | Team Member |
| Security rules | Company only |

---

## Agent Class-Object Pattern

QUAD agents follow a class-object instantiation pattern:

### How It Works

```
+-------------------------------------------------------------------+
|                      AGENT LIFECYCLE                               |
+-------------------------------------------------------------------+
|                                                                    |
|   CLASS (Template)                 OBJECT (Instance)               |
|   +-------------------+            +-------------------+           |
|   |   Story Agent     |   assign   |  Suman's Story    |           |
|   |   (Template)      | ---------> |     Agent         |           |
|   |                   |  + setup   |                   |           |
|   | - Capabilities    |            | - Connected       |           |
|   | - Base rules      |            | - App password    |           |
|   | - No connection   |            | - Local machine   |           |
|   | - "Ready" state   |            | - User context    |           |
|   +-------------------+            +-------------------+           |
|                                                                    |
|   Cannot execute tasks             Can execute tasks               |
|   Just a definition                Knows who it serves             |
|                                                                    |
+-------------------------------------------------------------------+
```

### Setup Flow

| Step | What Happens | How |
|------|--------------|-----|
| 1 | Agent Template exists | QUAD Platform provides |
| 2 | User joins team | Gets web app access |
| 3 | App Password created | Not SSO - restricted permissions |
| 4 | Local machine setup | Agent installed locally |
| 5 | Agent = Object | Connected, contextualized, active |

### Key Points

- Agent uses **App Password**, not user's SSO
- App Password has **restricted permissions** per hierarchy
- Agent runs on **user's local machine**
- Each user has their **own agent instance**
- Templates may have **readonly access** in future

---

## AI Agent Pipeline

### Agent Pipeline

```
+-----------+    +-----------+    +-------------+    +-------------+
|   Story   |--->|    Dev    |--->| Deploy(DEV) |--->|    Test     |
|   Agent   |    |   Agent   |    |    Agent    |    |   Agents    |
+-----------+    +-----------+    +-------------+    +-------------+
      |                |                |                   |
   Horizon         Code Push        DEV Ready          Tests Pass
                                                           |
                                                           v
+-------------+    +--------------+    +-------------+
|Deploy(PROD) |<---|  Deploy(QA)  |<---|     PR      |
|    Agent    |    |    Agent     |    |    Agent    |
+-------------+    +--------------+    +-------------+
      |                  |                   |
   Production         QA Ready           PR Created
```

---

## Agents by Circle

### Circle 1: Management Agents

| Agent | Trigger | What It Does | Replaces |
|-------|---------|--------------|----------|
| **Story Agent** | BA writes requirement | Enhances with specs, acceptance criteria, edge cases, test cases | Junior BA work |
| **Scheduling Agent** | Meeting needed | Analyzes calendars, finds optimal time, tracks action items | Scrum Master |
| **Documentation Agent** | Feature complete | Auto-generates flow docs, updates wiki, links artifacts | Manual doc updates |
| **Estimation Agent** | Story ready | Orchestrates multi-agent analysis for complexity, confidence, and effort estimation | Planning poker |

---

### Estimation Agent Pipeline (Deep Dive)

The Estimation Agent is unique - it orchestrates multiple agents in a **sequential pipeline** to produce accurate, confidence-based estimates.

#### Pipeline Architecture

```
+-------------------------------------------------------------------+
|                   ESTIMATION AGENT PIPELINE                        |
+-------------------------------------------------------------------+
|                                                                    |
|  TRIGGER: Story marked "Ready for Estimation"                      |
|                                                                    |
|  +--------+    +--------+    +--------+    +-------------+         |
|  | Code   |--->|   DB   |--->|  Flow  |--->| Estimation  |         |
|  | Agent  |    | Agent  |    | Agent  |    |    Agent    |         |
|  +--------+    +--------+    +--------+    +-------------+         |
|      |             |             |               |                 |
|      v             v             v               v                 |
|  Analyzes:     Analyzes:     Analyzes:     Aggregates:            |
|  - Files       - Tables      - Screens     - All inputs           |
|  - Components  - Migrations  - User flows  - Confidence           |
|  - Complexity  - Queries     - Integrations- Final estimate       |
|                                                                    |
+-------------------------------------------------------------------+
```

#### Pluggable Interface

Each agent in the pipeline implements a standard interface:

```typescript
interface EstimationContributor {
  name: string;
  analyze(story: Story, context: Context): AgentAnalysis;
  getConfidenceImpact(): number;  // -20 to +10
  isRequired(): boolean;          // Can be skipped?
}
```

**Pluggable Design:** Agents can be added/removed from pipeline:
- Add: Security Agent, Performance Agent, etc.
- Remove: DB Agent (if story has no DB changes)
- Order can be adjusted per project needs

#### Agent Contributions

| Agent | Analyzes | Contributes to Estimate |
|-------|----------|-------------------------|
| **Code Agent** | Files to modify, component complexity, dependencies | Base complexity score |
| **DB Agent** | Table changes, migrations, query complexity | Migration risk, data volume impact |
| **Flow Agent** | UI screens affected, API endpoints, integration points | User flow complexity |
| **Estimation Agent** | Aggregates all, historical comparison, team velocity | Final complexity + confidence |

#### Confidence Calculation

```
+-------------------------------------------------------------------+
|                   CONFIDENCE CALCULATION                           |
+-------------------------------------------------------------------+
|                                                                    |
|  BASE CONFIDENCE: 90%                                              |
|                                                                    |
|  DEDUCTIONS (reduce confidence):                                   |
|  +----------------------------------+------------+                 |
|  | Factor                           | Deduction  |                 |
|  +----------------------------------+------------+                 |
|  | High code complexity (>50 files) | -15%       |                 |
|  | Database migration required      | -10%       |                 |
|  | External API integration         | -10%       |                 |
|  | New technology/framework         | -15%       |                 |
|  | Cross-team dependency            | -10%       |                 |
|  | Unclear requirements             | -20%       |                 |
|  | No similar past stories          | -10%       |                 |
|  +----------------------------------+------------+                 |
|                                                                    |
|  ADDITIONS (boost confidence):                                     |
|  +----------------------------------+------------+                 |
|  | Factor                           | Addition   |                 |
|  +----------------------------------+------------+                 |
|  | Similar story completed before   | +10%       |                 |
|  | High test coverage in area       | +5%        |                 |
|  | Clear requirements               | +5%        |                 |
|  | Same developer did similar       | +5%        |                 |
|  +----------------------------------+------------+                 |
|                                                                    |
|  FINAL CONFIDENCE = 90% + additions - deductions                   |
|  (Minimum: 30%, Maximum: 95%)                                      |
|                                                                    |
+-------------------------------------------------------------------+
```

#### Output Format (Full Breakdown)

```
+-------------------------------------------------------------------+
|                     ESTIMATION RESULT                              |
+-------------------------------------------------------------------+
| Story: "Add dark mode toggle to settings"                         |
+-------------------------------------------------------------------+
|                                                                    |
| COMPLEXITY:     Octahedron (8)                                     |
| CONFIDENCE:     78%                                                |
| EFFORT:         5-6 days                                           |
|                                                                    |
+-------------------------------------------------------------------+
| BREAKDOWN BY AGENT:                                                |
|                                                                    |
| Code Agent:     3 files, 2 components, medium complexity           |
| DB Agent:       1 new column (user_preferences.theme)              |
| Flow Agent:     2 screens affected, 1 API endpoint                 |
|                                                                    |
+-------------------------------------------------------------------+
| RISKS:                                                             |
| ⚠️  CSS variable system not standardized                           |
| ⚠️  No existing theme context in app                               |
|                                                                    |
+-------------------------------------------------------------------+
| SIMILAR PAST STORIES:                                              |
| • "Add language toggle" - Cube (6) - Actual: 5 days ✅             |
| • "Add notification preferences" - Octahedron (8) - Actual: 7d    |
|                                                                    |
+-------------------------------------------------------------------+
```

#### Human Override with AI Learning

```
+-------------------------------------------------------------------+
|                    HUMAN OVERRIDE FLOW                             |
+-------------------------------------------------------------------+
|                                                                    |
|  1. AI PRESENTS ESTIMATE                                           |
|     Complexity: Octahedron (8), Confidence: 78%                    |
|                                                                    |
|  2. HUMAN REVIEWS                                                  |
|     [Accept AI Estimate]  or  [Override]                           |
|                                                                    |
|  3. IF OVERRIDE:                                                   |
|     Human Estimate: [Cube (6) ▼]                                   |
|     Reason: "I've done this exact thing before, simpler"           |
|     [Submit Override]                                              |
|                                                                    |
|  4. STORY COMPLETION (later)                                       |
|     Story completed in: 5 days                                     |
|                                                                    |
|  5. AI LEARNING                                                    |
|     +-------------------------------------------------------+      |
|     | ESTIMATION FEEDBACK                                    |      |
|     | AI Estimate: 8  →  Human Override: 6  →  Actual: 5    |      |
|     |                                                        |      |
|     | ✅ Human was closer!                                   |      |
|     | 📚 AI learning: Adjusting confidence for similar       |      |
|     |    stories involving "toggle" + "settings" patterns    |      |
|     +-------------------------------------------------------+      |
|                                                                    |
+-------------------------------------------------------------------+
```

**Key Points:**
- Override requires a reason (tracked for retrospectives)
- After story completion, actual effort is compared to estimates
- AI adjusts its models based on who was more accurate
- Over time, AI learns team-specific patterns

---

### Circle 2: Development Agents

| Agent | Trigger | What It Does | Replaces |
|-------|---------|--------------|----------|
| **Dev Agent (UI)** | Story assigned | Scaffolds UI components, generates platform-specific code | Boilerplate coding |
| **Dev Agent (API)** | Story assigned | Generates controllers, services, DTOs, entities | Boilerplate coding |
| **Code Review Agent** | PR created | Pre-reviews for patterns, security, style | First-pass review |
| **Refactor Agent** | Code smell detected | Suggests improvements, removes duplication | Tech debt discovery |

---

### Circle 3: QA Agents

| Agent | Trigger | What It Does | Replaces |
|-------|---------|--------------|----------|
| **UI Test Agent** | DEV deployed | Runs Playwright/XCTest automation | Manual UI testing |
| **API Test Agent** | DEV deployed | Runs REST API test suites | Manual API testing |
| **Performance Agent** | QA deployed | Runs load tests, identifies bottlenecks | Manual perf testing |
| **Test Generator Agent** | New code pushed | Generates test cases from code and flow docs | Writing test cases |
| **Bug Triage Agent** | Bug reported | Categorizes, assigns severity, suggests owner | Manual triage |

---

### Circle 4: Infrastructure Agents

| Agent | Trigger | What It Does | Replaces |
|-------|---------|--------------|----------|
| **Deploy Agent (DEV)** | PR merged to develop | Builds and deploys to DEV | Manual deployment |
| **Deploy Agent (QA)** | Tests pass + PR approved | Deploys to QA environment | Manual deployment |
| **Deploy Agent (PROD)** | QA approved | Deploys to production with rollback ready | Manual deployment |
| **Monitoring Agent** | Always running | Watches logs, metrics, alerts on anomalies | Manual monitoring |
| **Incident Agent** | Alert triggered | Creates ticket, pages on-call, suggests runbook | Manual incident mgmt |
| **Cost Agent** | Daily/Weekly | Analyzes cloud spend, suggests optimizations | Manual cost review |

---

## Flow Documentation

### Flow Document Structure

```
+-------------------------------------------------------------------+
|                    FLOW DOCUMENT TEMPLATE                          |
+-------------------------------------------------------------------+

# FLOW: [Feature Name]

## Overview
| Field        | Value                    |
|--------------|--------------------------|
| Flow ID      | FLOW_XXX_001             |
| Owner        | Circle 1 (BA/PM/TL)      |
| Last Updated | YYYY-MM-DD               |
| Status       | Draft / Active / Retired |

---

## Step 1: [Action Name]

### UI
| Element      | Type       | Validation           |
|--------------|------------|----------------------|
| Field name   | TextInput  | Required, format     |
| Button       | Button     | Disabled until valid |

### Screenshot
[Include screenshot or mockup]

### API
    POST /api/endpoint
    Content-Type: application/json

    Request:
    {
      "field": "value"
    }

    Response (200):
    {
      "result": "data"
    }

    Response (4xx/5xx):
    {
      "error": "message",
      "code": "ERROR_CODE"
    }

### Database
    -- Query executed
    SELECT columns FROM table WHERE condition;

    -- Insert/Update
    INSERT INTO table (columns) VALUES (values);

### Test Cases
| TC ID | Scenario        | Input       | Expected | API | DB Check  |
|-------|-----------------|-------------|----------|-----|-----------|
| TC001 | Happy path      | valid input | 200      | Yes | row added |
| TC002 | Invalid input   | bad input   | 422      | No  | no change |

---

## Step 2: [Next Action]
...

+-------------------------------------------------------------------+
```

---

### QA Testing View (Auto-Generated from Flow)

```
+-------------------------------------------------------------------+
|                      QA TESTING VIEW                               |
+-------------------------------------------------------------------+
|                                                                    |
|  Flow: FLOW_LOGIN_001                                              |
|                                                                    |
|  Test Checklist (auto-generated from flow):                        |
|                                                                    |
|  UI Tests:                                                         |
|  [ ] Email field shows keyboard                                    |
|  [ ] Password field masks input                                    |
|  [ ] Login button disabled when empty                              |
|  [ ] Error message displays on failure                             |
|                                                                    |
|  API Tests:                                                        |
|  [ ] POST /api/auth/login returns 200 with valid creds             |
|  [ ] Returns 401 with invalid password                             |
|  [ ] Returns 422 with malformed email                              |
|  [ ] Response contains token and user object                       |
|                                                                    |
|  Database Tests:                                                   |
|  [ ] users.last_login_at updated on success                        |
|  [ ] device_login_history row created                              |
|  [ ] login_attempts incremented on failure                         |
|  [ ] No data changed on validation failure                         |
|                                                                    |
|  Edge Cases:                                                       |
|  [ ] SQL injection attempt blocked                                 |
|  [ ] Account lockout after 5 failures                              |
|  [ ] Concurrent login from 2 devices                               |
|                                                                    |
+-------------------------------------------------------------------+
```

---

### One Source of Truth Architecture

```
+-------------------------------------------------------------------+
|                   ONE SOURCE OF TRUTH                              |
+-------------------------------------------------------------------+
|                                                                    |
|                      GIT REPOSITORY                                |
|                    (Version Controlled)                            |
|                           |                                        |
|         +-----------------+-----------------+                      |
|         |                 |                 |                      |
|         v                 v                 v                      |
|   +----------+     +----------+     +----------+                   |
|   |  /docs   |     |  /src    |     |  /tests  |                   |
|   |  flows/  |     |  code    |     |  specs   |                   |
|   +----+-----+     +----+-----+     +----+-----+                   |
|        |                |                |                         |
|        +--------+-------+--------+-------+                         |
|                 |                                                  |
|                 v                                                  |
|      +---------------------+                                       |
|      |    QUAD WEB APP     |                                       |
|      +---------------------+                                       |
|      | - Flow viewer       |                                       |
|      | - API browser       |                                       |
|      | - DB schema viewer  |                                       |
|      | - AI chat (RAG)     |                                       |
|      | - Test dashboard    |                                       |
|      +---------------------+                                       |
|                 |                                                  |
|   +-------------+-------------+                                    |
|   |             |             |                                    |
|   v             v             v                                    |
| +----------+ +----------+ +----------+                             |
| |Confluence| |   Jira   | | Swagger  |                             |
| |  (sync)  | |  (sync)  | |  (auto)  |                             |
| +----------+ +----------+ +----------+                             |
|                                                                    |
|   All tools sync FROM Git (single source)                          |
|   Never edit in Confluence directly                                |
|                                                                    |
+-------------------------------------------------------------------+
```

---

### Productivity Benefits

| Metric | Without QUAD Docs | With QUAD Docs | Improvement |
|--------|-------------------|----------------|-------------|
| Onboarding time | 2-4 weeks | 3-5 days | 75% faster |
| "Where is X?" questions | 10+/day | Near zero | 90% reduction |
| QA test case creation | 2 hours/feature | Auto-generated | 80% faster |
| Knowledge transfer | Meetings + shadowing | Read the flow | 70% faster |
| Bug reproduction | "Works on my machine" | Check flow + DB | Much faster |
| New feature estimation | Guessing | Similar flows exist | More accurate |

---

## Technical Debt Handling

QUAD handles technical debt continuously, not in batches:

### Approach: Continuous + Visibility

```
+-------------------------------------------------------------------+
|                  TECHNICAL DEBT APPROACH                           |
+-------------------------------------------------------------------+
|                                                                    |
|  1. REFACTOR AGENT (Continuous Scanning)                           |
|     - Scans for code duplication                                   |
|     - Identifies long methods (>50 lines)                          |
|     - Flags high cyclomatic complexity                             |
|     - Checks outdated dependencies                                 |
|     - Detects security vulnerabilities                             |
|     - Finds missing tests                                          |
|     - Creates tickets automatically                                |
|                                                                    |
|  2. BOY SCOUT RULE                                                 |
|     "Leave code better than you found it"                          |
|     - When dev touches a file, fix small issues                    |
|     - Include quick improvements with feature work                 |
|     - No separate "tech debt stories" for small items              |
|                                                                    |
|  3. DEBT DASHBOARD (Visibility)                                    |
|     - Overall debt score visible to all                            |
|     - Trends: improving, stable, declining                         |
|     - Alerts when score drops below threshold                      |
|                                                                    |
|  4. DEBT CEILING                                                   |
|     - If score < 60, Director is alerted                           |
|     - May pause features until debt reduced                        |
|                                                                    |
+-------------------------------------------------------------------+
```

---

### Tech Debt Dashboard

```
+-------------------------------------------------------------------+
|                   TECH DEBT DASHBOARD                              |
+-------------------------------------------------------------------+
|                                                                    |
|  Overall Debt Score: 72/100 (Healthy)                              |
|  ████████████████████░░░░░░░░░░                                    |
|                                                                    |
|  By Category:                                                      |
|  +------------------+----------+--------------+                    |
|  | Category         | Score    | Trend        |                    |
|  +------------------+----------+--------------+                    |
|  | Code Quality     | 85/100   | ^ Improving  |                    |
|  | Test Coverage    | 70/100   | - Stable     |                    |
|  | Dependencies     | 60/100   | v Declining  |                    |
|  | Documentation    | 75/100   | ^ Improving  |                    |
|  +------------------+----------+--------------+                    |
|                                                                    |
|  Action Items: 3 Critical items need attention                     |
|                                                                    |
+-------------------------------------------------------------------+
```

---

## Enabling Teams

Enabling Teams are optional support groups that are NOT counted as QUAD circles:

```
+-------------------------------------------------------------------+
|                      ENABLING TEAMS                                |
|                       (Optional)                                   |
+-------------------------------------------------------------------+
|                                                                    |
|  +----------------+  +----------------+  +----------------+        |
|  |   Architect    |  |   Security     |  |  Compliance    |        |
|  |     Group      |  |     Team       |  |     Team       |        |
|  +----------------+  +----------------+  +----------------+        |
|  | - Solution     |  | - Vuln scans   |  | - HIPAA check  |        |
|  | - Domain       |  | - Pen testing  |  | - SOC2 audit   |        |
|  | - Database     |  | - Code review  |  | - GDPR review  |        |
|  | - Cloud        |  |                |  |                |        |
|  +----------------+  +----------------+  +----------------+        |
|         |                  |                   |                   |
|         v                  v                   v                   |
|  +----------------+  +----------------+  +----------------+        |
|  | Design Agent   |  | Security       |  | Compliance     |        |
|  |                |  | Scanner        |  | Checker        |        |
|  +----------------+  +----------------+  +----------------+        |
|                                                                    |
+-------------------------------------------------------------------+

QUAD = 4 Circles + AI Core + Optional Enabling Teams
```

---

## Team Setup & Project Lifecycle

### Team Setup Checklist

| Step | Action | Owner |
|------|--------|-------|
| 1 | Assign 4 Circle roles to team | Director |
| 2 | Set up docs-first repository | Circle 4 |
| 3 | Configure Story Agent | Circle 1 |
| 4 | Configure Dev Agents | Circle 2 |
| 5 | Set up CI/CD with Deploy Agents | Circle 4 |
| 6 | Configure Test Agents | Circle 3 |
| 7 | Create team customization rules | Tech Lead |
| 8 | Train team on QUAD concepts | All |

---

### Project Lifecycle (12-Month Example)

| Phase | Months | Circles Active | Focus |
|-------|--------|----------------|-------|
| Phase 1 | 1-3 | Circle 1 + Circle 4 | Requirements + Infra setup |
| Phase 2 | 4-6 | Circle 1 + Circle 2 + Circle 4 | Development + Environments |
| Phase 3 | 7-9 | Circle 2 + Circle 3 + Circle 4 | Dev + QA + CI/CD |
| Phase 4 | 10-12 | Circle 3 + Circle 4 | Testing + Production |

---

## Related Documentation

- [QUAD Summary](/methodology/QUAD_SUMMARY) - High-level overview
- [QUAD Jargons](/methodology/QUAD_JARGONS) - Terminology and glossary
- [QUAD Case Study](/methodology/QUAD_CASE_STUDY) - Calculator App: Agile vs QUAD comparison
- [QUAD (Full)](/methodology/QUAD) - Original comprehensive document

---

**QUAD™** - A methodology by Suman Addanki | First Published: December 2025
