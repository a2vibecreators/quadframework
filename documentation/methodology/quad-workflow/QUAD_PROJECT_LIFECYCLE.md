# QUAD Project Lifecycle

## From Client Call to Deliverable Stories

Part of QUAD™ (Quick Unified Agentic Development) Methodology
© 2025 Suman Addanke / A2 Vibe Creators LLC

---

## Table of Contents

1. [The Problem We're Solving](#the-problem-were-solving)
2. [The Vicious Cycle](#the-vicious-cycle)
3. [QUAD Solution Overview](#quad-solution-overview)
4. [Phase 0: Client Engagement](#phase-0-client-engagement)
5. [Phase 1: Requirement Intake](#phase-1-requirement-intake)
6. [Phase 2: Story Generation](#phase-2-story-generation)
7. [Phase 3: Story Refinement](#phase-3-story-refinement)
8. [**DETAILED: Button-Level Workflow**](#detailed-button-level-workflow)
9. [Project Context System](#project-context-system)

---

## The Problem We're Solving

### Real-World Scenario

```
Manager: "We have problems. Slow delivery. Quality issues. Team burnout."

Why? Let's trace it back:

1. SLOW DELIVERY        ← Because of rework
2. QUALITY ISSUES       ← Because building wrong things
3. TEAM BURNOUT         ← Because requirements keep changing
4. TECHNICAL DEBT       ← Because of quick fixes under pressure
5. ROOT CAUSE           ← VAGUE REQUIREMENTS
```

### The Pain Points

| Symptom | Real Impact |
|---------|-------------|
| Requirement Gaps | Developers guess, build wrong thing |
| Frequent Changes | Team redoes work 2-3 times |
| Burned Out Team | Best engineers leave |
| Technical Debt | "We'll fix it later" (never happens) |
| Quality Issues | Bugs shipped to production |
| Slow Delivery | Missed deadlines, unhappy clients |

---

## The Vicious Cycle

```
                    ┌─────────────────┐
                    │  VAGUE REQS     │
                    │  from client    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  WRONG BUILD    │
                    │  devs guess     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  REWORK         │
                    │  "not what I    │
                    │   wanted!"      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  DEADLINE       │
                    │  PRESSURE       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  QUICK FIXES    │
                    │  skip tests     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  TECH DEBT      │
                    │  accumulates    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  TEAM BURNOUT   │
                    │  best leave     │
                    └────────┬────────┘
                             │
                             │
              ┌──────────────┴──────────────┐
              │  CYCLE REPEATS              │
              │  New project, same problems │
              └─────────────────────────────┘
```

**QUAD breaks this cycle at the SOURCE: Requirements.**

---

## QUAD Solution Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     QUAD PROJECT LIFECYCLE                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Phase 0          Phase 1           Phase 2          Phase 3        │
│  ────────         ────────          ────────         ────────       │
│                                                                     │
│  ┌────────┐      ┌────────┐        ┌────────┐       ┌────────┐     │
│  │ CLIENT │      │ RAW    │        │ STORY  │       │ REFINED│     │
│  │ CALL   │ ──▶  │ DOCS   │  ──▶   │ AGENT  │  ──▶  │ STORIES│     │
│  └────────┘      └────────┘        └────────┘       └────────┘     │
│                                                                     │
│  Budget: $400K   "20% off          AI generates     Complete with   │
│  Scope: API,     seasonal          base stories     acceptance      │
│  Web, iOS,       promo,            with questions   criteria,       │
│  Android, Batch  lottery..."                        labels, est.    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Phase 0: Client Engagement

### What Happens

1. **Client Call**: "I have $400K budget. Need API, Batch, Web, iOS, Android."
2. **Business Context**: Client explains their business goals
3. **Stakeholder Meeting**: Discuss promotions, timelines, features

### Example Scenario

```
CLIENT: "We want to reach customers faster. Here's our plan:
        - 20% seasonal discount (Jan 15 - Feb 15)
        - Lottery giveaway (random gifts)
        - New customer onboarding flow
        - Push notifications for deals"

US:     "Got it. Let's document this and generate stories."
```

### Output: Raw Requirement Document

The client provides whatever they have:
- Email threads
- Meeting notes
- PowerPoint slides
- Verbal descriptions
- Screenshots of competitors

**Key Principle**: Client input may be incomplete or wrong, but we RESPECT it. We don't dismiss - we CLARIFY.

---

## Phase 1: Requirement Intake

### Document Processing

```
┌─────────────────────────────────────────────────────────────┐
│                   REQUIREMENT INTAKE                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  INPUT                          OUTPUT                      │
│  ─────                          ──────                      │
│                                                             │
│  ┌──────────────┐              ┌──────────────────┐        │
│  │ Email Thread │              │ Structured       │        │
│  │ "20% off..." │              │ Requirements     │        │
│  └──────┬───────┘              │ Document         │        │
│         │                      │                  │        │
│  ┌──────▼───────┐              │ - Business Goals │        │
│  │ Meeting Notes│    ────▶     │ - User Personas  │        │
│  │ "lottery..." │              │ - Feature List   │        │
│  └──────┬───────┘              │ - Constraints    │        │
│         │                      │ - Questions      │        │
│  ┌──────▼───────┐              └──────────────────┘        │
│  │ Verbal Notes │                                          │
│  │ "fast app"   │                                          │
│  └──────────────┘                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Structured Output

```yaml
# requirement_intake.yaml
project:
  name: "Customer Rewards Platform"
  budget: 400000
  timeline: "Q1 2025"

platforms:
  - api
  - batch
  - web
  - ios
  - android

business_goals:
  - "Increase customer acquisition by 30%"
  - "Reduce cart abandonment by 20%"
  - "Launch seasonal promotion campaign"

features_mentioned:
  - "20% seasonal discount"
  - "Lottery/giveaway system"
  - "Push notifications"
  - "Customer onboarding"

constraints:
  - "Must launch before Jan 15"
  - "Budget cap: $400K"
  - "PCI compliance required for payments"

open_questions:
  - "What happens if discount conflicts with existing promo?"
  - "Who picks lottery winners? Manual or automatic?"
  - "What's the notification frequency limit?"
```

---

## Phase 2: Story Generation

### Story Agent Activation

```
┌─────────────────────────────────────────────────────────────────┐
│                      STORY AGENT FLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐                                                │
│  │     BA      │                                                │
│  │  (Human)    │                                                │
│  └──────┬──────┘                                                │
│         │                                                       │
│         │ 1. Writes requirement                                 │
│         │    "read @project_xyz sample"                         │
│         ▼                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    STORY AGENT                           │   │
│  │                                                          │   │
│  │  Inputs:                                                 │   │
│  │  ├── Project context (@project_xyz)                      │   │
│  │  ├── Requirement document                                │   │
│  │  └── BA's question/request                               │   │
│  │                                                          │   │
│  │  Processing:                                             │   │
│  │  ├── Parse business requirements                         │   │
│  │  ├── Identify user personas                              │   │
│  │  ├── Break into user stories                             │   │
│  │  ├── Generate acceptance criteria                        │   │
│  │  └── Flag ambiguities                                    │   │
│  │                                                          │   │
│  │  Outputs:                                                │   │
│  │  ├── Base stories (STORY-001 to STORY-nnn)              │   │
│  │  ├── Clarifying questions for BA                         │   │
│  │  └── Suggested labels                                    │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Sample Generated Stories

**STORY-001: Seasonal Discount Application**
```yaml
story_id: STORY-001
title: "Apply 20% Seasonal Discount at Checkout"
type: FEATURE
priority: P0
circle: 2  # Development
platform: [API, WEB, IOS, ANDROID]

as_a: "Customer"
i_want: "to see and apply the 20% seasonal discount at checkout"
so_that: "I can save money during the promotion period"

acceptance_criteria:
  - GIVEN promotion period is active (Jan 15 - Feb 15)
    WHEN customer views cart
    THEN 20% discount is automatically applied
  - GIVEN discount is applied
    WHEN customer views order summary
    THEN original price, discount amount, and final price are shown
  - GIVEN promotion period has ended
    WHEN customer views cart
    THEN no discount is applied and no error is shown

questions_for_ba:
  - "Does discount apply to all products or specific categories?"
  - "Can discount stack with existing promo codes?"
  - "Is there a minimum cart value for discount eligibility?"

suggested_labels:
  - priority/P0
  - type/FEATURE
  - circle/2-development
  - platform/API
  - platform/WEB
  - platform/IOS
  - platform/ANDROID
  - complexity/CUBE

estimated_complexity: CUBE  # 6 points - Multi-platform, business logic
```

**STORY-002: Lottery Entry System**
```yaml
story_id: STORY-002
title: "Enter Customer Into Lottery After Purchase"
type: FEATURE
priority: P1
circle: 2  # Development
platform: [API, BATCH]

as_a: "Customer"
i_want: "to be automatically entered into the gift lottery after purchase"
so_that: "I have a chance to win prizes"

acceptance_criteria:
  - GIVEN customer completes a purchase during promo period
    WHEN order is confirmed
    THEN customer is automatically entered into lottery
  - GIVEN customer is entered into lottery
    WHEN entry is recorded
    THEN customer receives confirmation notification
  - GIVEN lottery drawing occurs
    WHEN winners are selected
    THEN winning customers are notified via email and push

questions_for_ba:
  - "One entry per purchase or per customer?"
  - "When and how often are drawings?"
  - "What are the prizes? Need to display them?"
  - "Manual or automatic winner selection?"

suggested_labels:
  - priority/P1
  - type/FEATURE
  - circle/2-development
  - platform/API
  - platform/BATCH
  - complexity/OCTAHEDRON

estimated_complexity: OCTAHEDRON  # 8 points - Async, notifications
```

---

## Phase 3: Story Refinement

### BA Review Cycle

```
┌─────────────────────────────────────────────────────────────────┐
│                    STORY REFINEMENT LOOP                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │   STORY     │      │     BA      │      │   STORY     │     │
│  │   AGENT     │ ───▶ │   REVIEW    │ ───▶ │   AGENT     │     │
│  │  (Draft)    │      │  (Clarify)  │      │  (Refine)   │     │
│  └─────────────┘      └─────────────┘      └─────────────┘     │
│                              │                    │             │
│                              │                    │             │
│                              ▼                    ▼             │
│                       ┌─────────────┐      ┌─────────────┐     │
│                       │ "Discount   │      │ Updated     │     │
│                       │  only on    │      │ Stories     │     │
│                       │  orders     │      │ with BA     │     │
│                       │  over $50"  │      │ answers     │     │
│                       └─────────────┘      └─────────────┘     │
│                                                                 │
│  ITERATION COUNT: Usually 2-3 rounds until stories are clear   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Refined Story Example

After BA answers: "Discount only applies to orders over $50, cannot stack with other promos"

```yaml
story_id: STORY-001
title: "Apply 20% Seasonal Discount at Checkout"
status: REFINED  # Was DRAFT

acceptance_criteria:
  - GIVEN promotion period is active (Jan 15 - Feb 15)
    AND cart total is >= $50
    WHEN customer views cart
    THEN 20% discount is automatically applied
  - GIVEN cart total is < $50
    WHEN customer views cart
    THEN message shows "Add $X more to qualify for 20% off"
  - GIVEN customer has another promo code applied
    WHEN seasonal discount would apply
    THEN only the higher discount is used (no stacking)
  - GIVEN discount is applied
    WHEN customer views order summary
    THEN original price, discount amount, savings, and final price shown

ba_clarifications:
  - "Minimum order: $50"
  - "No promo stacking - use higher discount"
  - "All product categories eligible"

refinement_date: "2025-01-05"
refined_by: "BA-John"
```

---

## DETAILED: Button-Level Workflow

This section shows **exactly who clicks what button, where** at each step.

### Complete Story Lifecycle: From Draft to Development

```
┌────────────────────────────────────────────────────────────────────────────┐
│           COMPLETE WORKFLOW: WHO DOES WHAT, WHERE                          │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  STEP 1: BA CREATES RAW REQUIREMENT                                        │
│  ════════════════════════════════════                                      │
│                                                                            │
│  WHO:     BA (Business Analyst)                                            │
│  WHERE:   Jira → Create Issue                                              │
│  BUTTON:  [Create] button in Jira                                          │
│                                                                            │
│  WHAT BA DOES:                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │  Jira: Create Issue                                                   │ │
│  │  ┌────────────────────────────────────────────────────────────────┐  │ │
│  │  │  Project:     [PROJ ▼]                                         │  │ │
│  │  │  Type:        [Story ▼]                                        │  │ │
│  │  │  Summary:     "User login with OAuth2"                         │  │ │
│  │  │  Description: "As a user, I want to login using Google..."     │  │ │
│  │  │                                                                │  │ │
│  │  │  Labels:      [requirement] [needs-expansion]                  │  │ │
│  │  │                                                                │  │ │
│  │  │             [Create]  [Cancel]                                 │  │ │
│  │  └────────────────────────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  WHAT HAPPENS NEXT:                                                        │
│  • Jira fires webhook to QUAD Agent Runtime (QAR)                          │
│  • QAR sees label "needs-expansion" → triggers Story Agent                 │
│  • Story status changes to "Draft" automatically                           │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  STEP 2: STORY AGENT EXPANDS (AUTOMATIC)                                   │
│  ════════════════════════════════════════                                  │
│                                                                            │
│  WHO:     Story Agent (AI) - AUTOMATIC, no human action                    │
│  WHERE:   Background processing                                            │
│  BUTTON:  None - triggered by webhook                                      │
│                                                                            │
│  WHAT STORY AGENT DOES:                                                    │
│  1. Reads the raw requirement from Jira                                    │
│  2. Loads project context (@project_xyz)                                   │
│  3. Uses Gemini/Claude to expand into full stories                         │
│  4. Generates acceptance criteria                                          │
│  5. Identifies questions that need BA clarification                        │
│  6. Creates Confluence page with detailed specs                            │
│  7. Updates Jira story with:                                               │
│     • Link to Confluence specs                                             │
│     • Suggested labels                                                     │
│     • Status: "Draft - Pending Review"                                     │
│     • Comment: "@BA-John: Please review and answer questions"              │
│                                                                            │
│  JIRA AFTER EXPANSION:                                                     │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │  PROJ-123: User login with OAuth2                                    │ │
│  │  Status: [Draft - Pending Review]                                    │ │
│  │                                                                       │ │
│  │  📎 Attachments:                                                      │ │
│  │  └── 📄 Specs: PROJ-123-specs (Confluence)                           │ │
│  │                                                                       │ │
│  │  💬 Comments:                                                         │ │
│  │  ┌────────────────────────────────────────────────────────────────┐  │ │
│  │  │  🤖 Story Agent (just now)                                     │  │ │
│  │  │                                                                │  │ │
│  │  │  Story expanded. Please review and answer:                     │  │ │
│  │  │                                                                │  │ │
│  │  │  ❓ Q1: Which OAuth providers? (Google, Apple, Facebook?)      │  │ │
│  │  │  ❓ Q2: Should we support password fallback?                   │  │ │
│  │  │  ❓ Q3: Session duration: 24h or 7 days?                       │  │ │
│  │  │                                                                │  │ │
│  │  │  @BA-John please clarify                                       │  │ │
│  │  └────────────────────────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  STEP 3: BA REVIEWS AND ANSWERS QUESTIONS                                  │
│  ════════════════════════════════════════                                  │
│                                                                            │
│  WHO:     BA (Business Analyst)                                            │
│  WHERE:   Jira → Story Comments OR Confluence → Specs Page                 │
│  BUTTON:  [Comment] in Jira OR [Edit] in Confluence                        │
│                                                                            │
│  OPTION A: Answer in Jira Comments                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │  Add Comment:                                                         │ │
│  │  ┌────────────────────────────────────────────────────────────────┐  │ │
│  │  │  @story-agent                                                  │  │ │
│  │  │                                                                │  │ │
│  │  │  A1: Google and Apple only, no Facebook                        │  │ │
│  │  │  A2: Yes, password fallback for existing users                 │  │ │
│  │  │  A3: 7 days for mobile, 24h for web                           │  │ │
│  │  │                                                                │  │ │
│  │  │                           [Save]  [Cancel]                     │  │ │
│  │  └────────────────────────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  OPTION B: Answer in Confluence (More Detailed)                            │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │  Confluence: PROJ-123-specs                              [Edit]       │ │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │ │
│  │                                                                       │ │
│  │  ## BA Clarifications                                                 │ │
│  │                                                                       │ │
│  │  | Question | Answer | Answered By |                                  │ │
│  │  |----------|--------|-------------|                                  │ │
│  │  | OAuth providers | Google, Apple | @BA-John |                       │ │
│  │  | Password fallback | Yes, for existing | @BA-John |                 │ │
│  │  | Session duration | 7d mobile, 24h web | @BA-John |                 │ │
│  │                                                                       │ │
│  │  [Publish]                                                            │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  WHAT HAPPENS NEXT:                                                        │
│  • Jira/Confluence webhook fires on BA's comment/edit                      │
│  • QAR triggers Story Agent to refine based on answers                     │
│  • Story Agent updates story with new acceptance criteria                  │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  STEP 4: STORY AGENT REFINES (AUTOMATIC)                                   │
│  ════════════════════════════════════════                                  │
│                                                                            │
│  WHO:     Story Agent (AI) - AUTOMATIC                                     │
│  WHERE:   Background processing                                            │
│  BUTTON:  None - triggered by BA's comment                                 │
│                                                                            │
│  WHAT STORY AGENT DOES:                                                    │
│  1. Reads BA's answers                                                     │
│  2. Updates acceptance criteria with specific details                      │
│  3. Updates Confluence specs                                               │
│  4. Changes status to "Refined - Ready for Approval"                       │
│  5. Notifies BA: "Story refined. Please approve or request changes."       │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  STEP 5: BA APPROVES STORY                                                 │
│  ══════════════════════════                                                │
│                                                                            │
│  WHO:     BA (Business Analyst)                                            │
│  WHERE:   Jira → Story Detail                                              │
│  BUTTON:  [Approve] custom button OR transition workflow                   │
│                                                                            │
│  OPTION A: Custom QUAD Button in Jira                                      │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │  PROJ-123: User login with OAuth2                                    │ │
│  │  Status: [Refined - Ready for Approval]                              │ │
│  │                                                                       │ │
│  │  QUAD Actions:                                                        │ │
│  │  ┌────────────────────────────────────────────────────────────────┐  │ │
│  │  │  [✓ Approve Story]  [↻ Request Changes]  [✕ Reject]            │  │ │
│  │  └────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                       │ │
│  │  BA clicks [✓ Approve Story]                                         │ │
│  │                                                                       │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  OPTION B: Jira Workflow Transition                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │  Workflow transitions in Jira:                                        │ │
│  │                                                                       │ │
│  │  [Draft] → [Pending Review] → [Refined] → [Approved] → [Ready]       │ │
│  │                                                    ↑                  │ │
│  │                                              BA clicks here           │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  WHAT HAPPENS NEXT:                                                        │
│  • Status changes to "Approved - Ready for Sprint"                         │
│  • Story Agent applies final labels: priority, complexity                  │
│  • Story appears in backlog for sprint planning                            │
│  • Estimation Agent may auto-run to calculate points                       │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  STEP 6: PM ADDS TO SPRINT                                                 │
│  ═════════════════════════                                                 │
│                                                                            │
│  WHO:     PM (Project Manager) or Tech Lead                                │
│  WHERE:   Jira → Backlog or Sprint Board                                   │
│  BUTTON:  Drag & Drop OR [Add to Sprint] button                            │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │  Jira Backlog                                                         │ │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │ │
│  │                                                                       │ │
│  │  Sprint 5 (Jan 15-28)         │  Backlog                             │ │
│  │  ─────────────────────────────│──────────────────────────────────    │ │
│  │                               │                                       │ │
│  │  □ PROJ-100 (8 pts)           │  ✓ PROJ-123 (8 pts) ←── Drag here    │ │
│  │  □ PROJ-101 (6 pts)           │  □ PROJ-124 (4 pts)                  │ │
│  │  □ PROJ-102 (4 pts)           │  □ PROJ-125 (12 pts)                 │ │
│  │                               │                                       │ │
│  │  Capacity: 40 pts             │  Backlog: 67 pts                     │ │
│  │  Committed: 18 pts            │                                       │ │
│  │                               │                                       │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  WHAT HAPPENS NEXT:                                                        │
│  • Story is assigned sprint/SPRINT-05 label                                │
│  • Story status: "Ready for Development"                                   │
│  • Dev team sees it in their sprint board                                  │
│                                                                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  STEP 7: DEV STARTS WORK                                                   │
│  ═══════════════════════                                                   │
│                                                                            │
│  WHO:     Developer                                                        │
│  WHERE:   Jira → Sprint Board                                              │
│  BUTTON:  [Start Progress] or drag to "In Progress"                        │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │  Sprint 5 Board                                                       │ │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │ │
│  │                                                                       │ │
│  │  TODO          │  IN PROGRESS    │  CODE REVIEW    │  DONE           │ │
│  │  ──────────────│─────────────────│─────────────────│────────────     │ │
│  │                │                 │                 │                 │ │
│  │  PROJ-123      │                 │                 │                 │ │
│  │  (8 pts)       │                 │                 │                 │ │
│  │  [Start] ──────┼────────────────▶│                 │                 │ │
│  │                │  PROJ-123       │                 │                 │ │
│  │                │  @dev-john      │                 │                 │ │
│  │                │                 │                 │                 │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  OPTIONAL: Dev can use /commands in IDE or chat:                           │
│  • /context @proj-123  → Load story context                                │
│  • /estimate PROJ-123  → Get complexity breakdown                          │
│  • /agent invoke dev-agent-api --story=PROJ-123 → Get AI help              │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### Summary: Who Clicks What

| Step | WHO | WHERE | BUTTON/ACTION | RESULT |
|------|-----|-------|---------------|--------|
| 1 | BA | Jira | [Create] | Raw story created, webhook fires |
| 2 | AI | Background | (Automatic) | Story expanded, questions posted |
| 3 | BA | Jira/Confluence | [Comment] or [Edit] | Answers provided |
| 4 | AI | Background | (Automatic) | Story refined with answers |
| 5 | BA | Jira | [Approve Story] | Story approved for sprint |
| 6 | PM | Jira Backlog | Drag & Drop | Story added to sprint |
| 7 | Dev | Jira Board | [Start Progress] | Development begins |

### Jira Workflow States

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       JIRA STORY WORKFLOW                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  [DRAFT]                                                                │
│     │                                                                   │
│     │ (Auto: Story Agent expands)                                       │
│     ▼                                                                   │
│  [PENDING REVIEW]                                                       │
│     │                                                                   │
│     │ (BA answers questions)                                            │
│     ▼                                                                   │
│  [REFINED]                                                              │
│     │                                                                   │
│     ├────────────────────────────────────────────┐                     │
│     │ (BA approves)                              │ (BA requests changes)│
│     ▼                                            ▼                      │
│  [APPROVED]                                   [NEEDS WORK]              │
│     │                                            │                      │
│     │ (PM adds to sprint)                        │ (Back to PENDING)    │
│     ▼                                            │                      │
│  [READY FOR DEV]                                 └──────────────────────┘
│     │                                                                   │
│     │ (Dev starts work)                                                 │
│     ▼                                                                   │
│  [IN PROGRESS]                                                          │
│     │                                                                   │
│     │ (Dev creates PR)                                                  │
│     ▼                                                                   │
│  [CODE REVIEW]                                                          │
│     │                                                                   │
│     │ (PR merged)                                                       │
│     ▼                                                                   │
│  [QA READY]                                                             │
│     │                                                                   │
│     ├────────────────────────────────────────────┐                     │
│     │ (QA passes)                                │ (QA fails)           │
│     ▼                                            ▼                      │
│  [DONE]                                       [QA FAILED]               │
│                                                  │                      │
│                                                  │ (Back to IN PROGRESS)│
│                                                  └──────────────────────┘
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Alternative: BA Uses Chat Instead of Jira

BA can also work through chat (Claude, Copilot, Slack):

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     CHAT-BASED WORKFLOW                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Slack / Claude / Copilot Chat                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                         │
│  BA-John: @QUAD create story: "User login with OAuth2"                  │
│                                                                         │
│  🤖 QUAD: Story PROJ-123 created. Expanding...                          │
│                                                                         │
│  🤖 QUAD: Story expanded. I have 3 questions:                           │
│                                                                         │
│           ❓ Which OAuth providers? (Google, Apple, Facebook?)          │
│           ❓ Password fallback for existing users?                      │
│           ❓ Session duration preference?                                │
│                                                                         │
│  BA-John: Google and Apple only. Yes password fallback.                 │
│           7 days mobile, 24h web.                                       │
│                                                                         │
│  🤖 QUAD: Got it. Updating story...                                     │
│                                                                         │
│  🤖 QUAD: ✓ Story PROJ-123 refined.                                     │
│           📎 Specs: confluence.com/PROJ/123-specs                       │
│           📊 Complexity: OCTAHEDRON (8 pts)                             │
│           🏷️ Labels: priority/P1, platform/API, platform/WEB            │
│                                                                         │
│           Ready to approve? [Yes, approve] [No, more changes]           │
│                                                                         │
│  BA-John: *clicks [Yes, approve]*                                       │
│                                                                         │
│  🤖 QUAD: ✓ Story PROJ-123 approved. Added to backlog.                  │
│           PM can now add to sprint.                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Alternative: BA Uses IDE (VS Code)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     IDE-BASED WORKFLOW (VS Code)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  VS Code with QUAD Extension                                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  File: requirement.md                                            │   │
│  │  ─────────────────────────────────────────────────────────────   │   │
│  │                                                                  │   │
│  │  # User Login Feature                                            │   │
│  │                                                                  │   │
│  │  As a user, I want to login using OAuth2 so that I can          │   │
│  │  access my account without remembering a password.               │   │
│  │                                                                  │   │
│  │  ## Requirements                                                 │   │
│  │  - Google OAuth                                                  │   │
│  │  - Apple Sign In                                                 │   │
│  │  - Session management                                            │   │
│  │                                                                  │   │
│  │  [Right-click shows context menu]                                │   │
│  │  ┌────────────────────────────┐                                  │   │
│  │  │ 🤖 QUAD: Expand Story      │ ← BA clicks here                │   │
│  │  │ 🤖 QUAD: Estimate          │                                  │   │
│  │  │ 🤖 QUAD: Create in Jira    │                                  │   │
│  │  └────────────────────────────┘                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  After clicking "Expand Story":                                         │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  QUAD Panel (sidebar)                                            │   │
│  │  ─────────────────────────────────────────────────────────────   │   │
│  │                                                                  │   │
│  │  Story: PROJ-123 - User Login                                   │   │
│  │  Status: Expanded ✓                                              │   │
│  │                                                                  │   │
│  │  Questions:                                                      │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ Q1: OAuth providers?                                     │    │   │
│  │  │ [Google] [Apple] [Facebook] [Other...]                   │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ Q2: Password fallback?                                   │    │   │
│  │  │ (Yes) (No)                                               │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ Q3: Session duration?                                    │    │   │
│  │  │ Mobile: [7 days ▼]  Web: [24 hours ▼]                    │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  │                                                                  │   │
│  │  [Refine Story]  [Skip to Approve]                              │   │
│  │                                                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Project Context System

### How @project_xyz Works

When BA writes `@project_xyz`, the Story Agent loads project-specific context:

```
┌─────────────────────────────────────────────────────────────────┐
│                     PROJECT CONTEXT SYSTEM                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  @project_xyz resolves to:                                      │
│                                                                 │
│  /.quad/contexts/project_xyz/                                   │
│  ├── README.md              # Project overview                  │
│  ├── tech_stack.yaml        # Technologies used                 │
│  ├── architecture.md        # System architecture               │
│  ├── api_standards.md       # API conventions                   │
│  ├── naming_conventions.md  # Code naming rules                 │
│  ├── existing_stories/      # Previously completed stories      │
│  │   ├── STORY-001.yaml                                        │
│  │   └── STORY-002.yaml                                        │
│  └── domain_glossary.md     # Business terms definitions        │
│                                                                 │
│  Story Agent uses this context to:                              │
│  ✓ Maintain consistency with existing architecture              │
│  ✓ Use correct terminology                                      │
│  ✓ Reference related stories                                    │
│  ✓ Follow established patterns                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Context File Examples

**tech_stack.yaml**
```yaml
backend:
  language: Java
  framework: Spring Boot 3.2
  database: PostgreSQL 15

frontend:
  web: React 18 / Next.js 14
  ios: SwiftUI
  android: Kotlin Jetpack Compose

infrastructure:
  cloud: GCP
  container: Docker / Cloud Run
  ci_cd: GitHub Actions
```

**api_standards.md**
```markdown
# API Standards

- REST endpoints prefixed with `/api/v1/`
- Use kebab-case for URLs: `/api/v1/user-profiles`
- Response format: JSON with envelope
- Authentication: JWT Bearer tokens
- Pagination: `?page=1&size=20`
- Error format: `{ "error": { "code": "ERR_001", "message": "..." } }`
```

---

## Summary

| Phase | Input | Output | Agent |
|-------|-------|--------|-------|
| 0: Client Engagement | Client call, budget, scope | Raw requirements doc | Human (BA/PM) |
| 1: Requirement Intake | Raw docs, emails, notes | Structured requirements | Human + AI assist |
| 2: Story Generation | @project context + requirements | Base stories + questions | Story Agent |
| 3: Story Refinement | BA answers to questions | Refined stories, ready for dev | Story Agent + BA |

**Key Benefits of QUAD Approach:**

1. **No More Guessing** - AI generates questions, humans answer
2. **Consistent Format** - All stories follow same structure
3. **Traceable** - Every decision documented
4. **Context-Aware** - AI knows your project's patterns
5. **Iterative** - Refinement loop until clear

---

**Next**: See [QUAD_STORY_LABELS.md](QUAD_STORY_LABELS.md) for the labeling system.

---

*Part of QUAD™ (Quick Unified Agentic Development) Methodology*
*© 2025 Suman Addanke / A2 Vibe Creators LLC*
