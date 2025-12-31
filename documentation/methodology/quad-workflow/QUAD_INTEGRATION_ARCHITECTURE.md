# QUAD Integration Architecture

**The Complete Picture: How Everything Works Together**

Part of QUAD™ (Quick Unified Agentic Development) Methodology
© 2025 Suman Addanke / A2 Vibe Creators LLC

---

## Table of Contents

1. [Overview](#overview)
2. [System Context Diagram](#system-context-diagram)
3. [End-to-End Flow](#end-to-end-flow)
4. [Configuration File Relationships](#configuration-file-relationships)
5. [Document Map](#document-map)
6. [Implementation Layers](#implementation-layers)
7. [Integration Points](#integration-points)
8. [Getting Started Guide](#getting-started-guide)
9. [Deployment Topology](#deployment-topology)

---

## Overview

This document provides the **complete integration picture** of QUAD methodology. It shows how all components - agents, triggers, pipelines, permissions, and tools - work together as a unified system.

### QUAD at a Glance

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           QUAD™ METHODOLOGY                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   1 METHOD      QUAD - Quick Unified Agentic Development                    │
│   2 DIMENSIONS  Business + Technical                                         │
│   3 AXIOMS      4 Circles + AI Agents + Docs-First                          │
│   4 CIRCLES     Management → Development → QA → Infrastructure              │
│                                                                              │
│   8 STEPS       First QUAD (Operational) + Second QUAD (Optimize)           │
│   7 TRIGGERS    Jira | Email | Slack | GitHub | Azure | Scheduled | Manual  │
│   7 LABELS      Priority | Status | Type | Circle | Platform | Sprint | Size│
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### What This Document Covers

| Section | What You'll Learn |
|---------|-------------------|
| [System Context](#system-context-diagram) | All components and their relationships |
| [End-to-End Flow](#end-to-end-flow) | Complete journey from trigger to output |
| [Configuration Files](#configuration-file-relationships) | How YAML configs connect |
| [Document Map](#document-map) | Which doc to read for what |
| [Implementation Layers](#implementation-layers) | Technical architecture stack |
| [Getting Started](#getting-started-guide) | Quick setup checklist |

---

## System Context Diagram

### The Complete QUAD Ecosystem

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL SYSTEMS & USERS                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  +--------+  +--------+  +--------+  +--------+  +--------+  +--------+     │
│  |  Jira  |  | GitHub |  | Slack  |  | Email  |  |Confluenc|  | Azure  |    │
│  +--------+  +--------+  +--------+  +--------+  +--------+  +--------+     │
│      │           │           │           │           │           │          │
│      └───────────┴───────────┴─────┬─────┴───────────┴───────────┘          │
│                                    │                                         │
│                            WEBHOOKS & EVENTS                                 │
│                                    ▼                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                         QUAD TRIGGER LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                      TRIGGER PROCESSOR                                 │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │  │
│  │  │  Jira   │  │  Email  │  │  Slack  │  │ GitHub  │  │  Cron   │      │  │
│  │  │ Adapter │  │ Adapter │  │ Adapter │  │ Adapter │  │ Adapter │      │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘      │  │
│  │                           │                                            │  │
│  │                    ┌──────▼───────┐                                    │  │
│  │                    │ Normalized   │                                    │  │
│  │                    │ TriggerEvent │                                    │  │
│  │                    └──────────────┘                                    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                         │
├────────────────────────────────────▼────────────────────────────────────────┤
│                        QUAD AGENT RUNTIME (QAR)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                                                                      │    │
│  │   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐       │    │
│  │   │ ORCHESTRATOR  │    │   EVENT BUS   │    │SHARED CONTEXT │       │    │
│  │   │  (Pipelines)  │◄──►│  (Pub/Sub)    │◄──►│  (State)      │       │    │
│  │   └───────────────┘    └───────────────┘    └───────────────┘       │    │
│  │          │                     │                    │                │    │
│  │          ▼                     ▼                    ▼                │    │
│  │   ┌────────────────────────────────────────────────────────────┐    │    │
│  │   │              PERMISSION CHECKER + AUDIT LOG                 │    │    │
│  │   └────────────────────────────────────────────────────────────┘    │    │
│  │                               │                                      │    │
│  │   ┌───────────────────────────▼────────────────────────────────┐    │    │
│  │   │                    AGENT REGISTRY                           │    │    │
│  │   │                                                             │    │    │
│  │   │  ┌────────────────────────────────────────────────────────┐ │    │    │
│  │   │  │              CIRCLE 1: MANAGEMENT                       │ │    │    │
│  │   │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │ │    │    │
│  │   │  │  │  Story  │ │  Code   │ │   DB    │ │  Flow   │       │ │    │    │
│  │   │  │  │  Agent  │ │  Agent  │ │  Agent  │ │  Agent  │       │ │    │    │
│  │   │  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘       │ │    │    │
│  │   │  └────────────────────────────────────────────────────────┘ │    │    │
│  │   │                                                             │    │    │
│  │   │  ┌────────────────────────────────────────────────────────┐ │    │    │
│  │   │  │              CIRCLE 2: DEVELOPMENT                      │ │    │    │
│  │   │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │ │    │    │
│  │   │  │  │ Dev UI  │ │ Dev API │ │ Dev DB  │ │ Review  │       │ │    │    │
│  │   │  │  │  Agent  │ │  Agent  │ │  Agent  │ │  Agent  │       │ │    │    │
│  │   │  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘       │ │    │    │
│  │   │  └────────────────────────────────────────────────────────┘ │    │    │
│  │   │                                                             │    │    │
│  │   │  ┌────────────────────────────────────────────────────────┐ │    │    │
│  │   │  │              CIRCLE 3: QA                               │ │    │    │
│  │   │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │ │    │    │
│  │   │  │  │Test Unit│ │Test API │ │Test E2E │ │Security │       │ │    │    │
│  │   │  │  │  Agent  │ │  Agent  │ │  Agent  │ │ Scanner │       │ │    │    │
│  │   │  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘       │ │    │    │
│  │   │  └────────────────────────────────────────────────────────┘ │    │    │
│  │   │                                                             │    │    │
│  │   │  ┌────────────────────────────────────────────────────────┐ │    │    │
│  │   │  │              CIRCLE 4: INFRASTRUCTURE                   │ │    │    │
│  │   │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │ │    │    │
│  │   │  │  │ Deploy  │ │ Monitor │ │  Alert  │ │ Rollback│       │ │    │    │
│  │   │  │  │  Agent  │ │  Agent  │ │  Agent  │ │  Agent  │       │ │    │    │
│  │   │  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘       │ │    │    │
│  │   │  └────────────────────────────────────────────────────────┘ │    │    │
│  │   │                                                             │    │    │
│  │   └─────────────────────────────────────────────────────────────┘    │    │
│  │                                                                      │    │
│  └──────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
├────────────────────────────────────▼────────────────────────────────────────┤
│                            MCP TOOL LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         MCP TOOLS                                    │    │
│  │                                                                      │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │    │
│  │  │ Gemini  │  │   Git   │  │Confluenc│  │  Jira   │  │ Slack   │   │    │
│  │  │   MCP   │  │   MCP   │  │   MCP   │  │   MCP   │  │   MCP   │   │    │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │    │
│  │                                                                      │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │    │
│  │  │ GitHub  │  │ Docker  │  │   K8s   │  │ AWS/GCP │  │ Custom  │   │    │
│  │  │   MCP   │  │   MCP   │  │   MCP   │  │   MCP   │  │   MCP   │   │    │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │    │
│  │                                                                      │    │
│  └──────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                            OUTPUT DESTINATIONS                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│  │  Jira   │  │ GitHub  │  │Confluenc│  │  Slack  │  │ Deploy  │           │
│  │ (Update)│  │  (PR)   │  │ (Docs)  │  │(Notify) │  │ (Infra) │           │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## End-to-End Flow

### Complete Journey: From Requirement to Deployment

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     END-TO-END FLOW EXAMPLE                                  │
│                     GlobalRetail Inc. Feature                                │
├─────────────────────────────────────────────────────────────────────────────┤

                        BA writes requirement in Jira
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: TRIGGER (Jira Webhook)                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Jira fires webhook:                                                         │
│  {                                                                           │
│    "event": "issue.created",                                                 │
│    "project": "RETAIL",                                                      │
│    "issue": {                                                                │
│      "key": "RETAIL-456",                                                    │
│      "type": "Story",                                                        │
│      "summary": "Customer wishlist feature",                                 │
│      "description": "Customers should be able to save products..."          │
│    }                                                                         │
│  }                                                                           │
│                                                                              │
│  Jira Adapter normalizes to TriggerEvent:                                    │
│  {                                                                           │
│    sourceSystem: "jira",                                                     │
│    eventType: "story.created",                                               │
│    payload: { story_id: "RETAIL-456", ... },                                 │
│    targetAgent: "story-agent"                                                │
│  }                                                                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: DEFINE (Story Agent)                                       [Circle 1]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  QAR receives TriggerEvent:                                                  │
│  1. Permission check: story-agent allowed to be triggered by jira? ✓        │
│  2. Invoke story-agent with normalized payload                               │
│                                                                              │
│  Story Agent executes:                                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  1. Read story from Jira MCP                                          │   │
│  │  2. Read project context from Confluence MCP                          │   │
│  │  3. Call Gemini MCP for AI expansion                                  │   │
│  │  4. Generate:                                                         │   │
│  │     - Acceptance criteria                                             │   │
│  │     - Technical specs                                                 │   │
│  │     - Test scenarios                                                  │   │
│  │     - Sub-tasks                                                       │   │
│  │  5. Write specs to Confluence MCP                                     │   │
│  │  6. Update Jira MCP with link                                         │   │
│  │  7. Emit event: "story.expanded"                                      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  Output:                                                                     │
│  - RETAIL-456 expanded with full specs                                       │
│  - Sub-tasks created: RETAIL-457, 458, 459, 460                             │
│  - Labels applied: P1, STATUS:READY, TYPE:FEATURE, CIRCLE:2, WEB            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                            Event: story.expanded
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: ESTIMATE (Estimation Pipeline)                             [Circle 1]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Orchestrator runs estimation-pipeline (SEQUENTIAL):                         │
│                                                                              │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐               │
│  │  Code   │ ──► │   DB    │ ──► │  Flow   │ ──► │Estimator│               │
│  │  Agent  │     │  Agent  │     │  Agent  │     │  Agent  │               │
│  └─────────┘     └─────────┘     └─────────┘     └─────────┘               │
│       │               │               │               │                     │
│       ▼               ▼               ▼               ▼                     │
│  complexity: 8    impact: MED    flows: 3      OCTAHEDRON (8)               │
│                                                                              │
│  Result: Story estimated at OCTAHEDRON (8 points)                            │
│  Jira updated with estimate label                                            │
│  Event emitted: "story.estimated"                                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                            Event: story.estimated
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: DEVELOP (Development Pipeline)                             [Circle 2]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Orchestrator runs development-pipeline (HYBRID):                            │
│                                                                              │
│  STAGE 1: Parallel Development                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  ┌───────────┐                           ┌───────────┐               │   │
│  │  │  Dev UI   │                           │  Dev API  │               │   │
│  │  │   Agent   │                           │   Agent   │               │   │
│  │  └───────────┘                           └───────────┘               │   │
│  │       │                                       │                      │   │
│  │       ▼                                       ▼                      │   │
│  │  - React components                      - REST endpoints            │   │
│  │  - State management                      - Service layer             │   │
│  │  - UI tests                              - API tests                 │   │
│  │  - Git MCP: commit                       - Git MCP: commit           │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                           │                                                  │
│                     (wait for both)                                          │
│                           ▼                                                  │
│  STAGE 2: Integration                                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  ┌───────────┐                                                       │   │
│  │  │Integration│  Verifies UI + API work together                      │   │
│  │  │   Agent   │  Creates integration tests                            │   │
│  │  └───────────┘  Git MCP: merge branches                              │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  Output:                                                                     │
│  - feature/RETAIL-456-wishlist branch with all code                         │
│  - PR created and ready for review                                          │
│  - Event emitted: "code.ready"                                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                               Event: code.ready
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 5: REVIEW (Review Agent)                                      [Circle 2]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Review Agent executes:                                                      │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  1. Read PR diff from GitHub MCP                                      │   │
│  │  2. Read coding standards from Confluence MCP                         │   │
│  │  3. Call Gemini MCP for code analysis                                 │   │
│  │  4. Security scan via Security Scanner MCP                            │   │
│  │  5. Generate review comments                                          │   │
│  │  6. Post comments to GitHub MCP                                       │   │
│  │  7. If approved: emit "code.approved"                                 │   │
│  │     If changes needed: emit "code.changes-requested"                  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  Result: PR approved with minor suggestions                                  │
│  Event emitted: "code.approved"                                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                              Event: code.approved
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 6: DELIVER (Testing Pipeline)                                 [Circle 3]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Orchestrator runs testing-pipeline (HYBRID):                                │
│                                                                              │
│  STAGE 1: Parallel Test Execution                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐                 │   │
│  │  │  Unit   │  │   API   │  │   E2E   │  │Security │                 │   │
│  │  │  Tests  │  │  Tests  │  │  Tests  │  │  Scan   │                 │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘                 │   │
│  │       │            │            │            │                       │   │
│  │       ▼            ▼            ▼            ▼                       │   │
│  │    ✓ Pass      ✓ Pass       ✓ Pass      ✓ Pass                      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                           │                                                  │
│                     (wait for all)                                           │
│                           ▼                                                  │
│  STAGE 2: Quality Gate                                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  ┌───────────┐                                                       │   │
│  │  │  Quality  │  Coverage: 87% ✓                                      │   │
│  │  │   Gate    │  Security: No critical ✓                              │   │
│  │  │   Agent   │  Performance: Within SLA ✓                            │   │
│  │  └───────────┘  Decision: PASS                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  Result: All tests pass, quality gate approved                               │
│  Event emitted: "tests.passed"                                              │
│  Jira updated: STATUS:READY-TO-DEPLOY                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                              Event: tests.passed
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 7: DEPLOY (Deployment Pipeline)                               [Circle 4]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Orchestrator runs deployment-pipeline (SEQUENTIAL):                         │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                                                                       │   │
│  │  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐        │   │
│  │  │  Build  │ ──► │  Stage  │ ──► │  Prod   │ ──► │  Verify │        │   │
│  │  │  Agent  │     │ Deploy  │     │ Deploy  │     │  Agent  │        │   │
│  │  └─────────┘     └─────────┘     └─────────┘     └─────────┘        │   │
│  │       │               │               │               │              │   │
│  │       ▼               ▼               ▼               ▼              │   │
│  │  Docker image    Staging OK     HUMAN APPROVE     Health ✓          │   │
│  │  pushed          smoke tests    ────────────►     Metrics ✓         │   │
│  │                                 (Required!)                          │   │
│  │                                                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ⚠️  HUMAN APPROVAL REQUIRED for production deploy                          │
│                                                                              │
│  After approval:                                                             │
│  - Production deployment complete                                            │
│  - Health checks passing                                                     │
│  - Event emitted: "deploy.completed"                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                            Event: deploy.completed
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 8: MONITOR & FEEDBACK                                         [Circle 4]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Monitor Agent continuously watches:                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                                                                       │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │   │
│  │  │  METRICS DASHBOARD                                               │ │   │
│  │  │  ─────────────────────────────────────────────────────────────── │ │   │
│  │  │  Response Time: 120ms (✓ SLA: <200ms)                           │ │   │
│  │  │  Error Rate: 0.02% (✓ SLA: <1%)                                 │ │   │
│  │  │  CPU: 45% | Memory: 62% | Disk: 38%                             │ │   │
│  │  │  Active Users: 12,450                                            │ │   │
│  │  └─────────────────────────────────────────────────────────────────┘ │   │
│  │                                                                       │   │
│  │  Alert Rules:                                                         │   │
│  │  - If error rate > 1%: Notify + prepare rollback                     │   │
│  │  - If response > 500ms: Alert on-call                                │   │
│  │  - If CPU > 80% for 5min: Scale up                                   │   │
│  │                                                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  Feedback Loop:                                                              │
│  - Collect metrics on agent performance                                      │
│  - Store learnings in Agent Knowledge Base                                   │
│  - Improve prompts and rules based on outcomes                              │
│  - Update guardrails if issues found                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

                              STORY COMPLETE
                    RETAIL-456 deployed to production
                    Time: 4 hours (vs traditional 3 days)
```

---

## Configuration File Relationships

### How Configuration Files Connect

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CONFIGURATION FILE HIERARCHY                              │
├─────────────────────────────────────────────────────────────────────────────┤

project-root/
│
├── quad.config.yaml ─────────────────── MASTER CONFIG
│   │
│   │  version: "1.0"
│   │  project: "my-project"
│   │
│   │  # References other configs
│   │  includes:
│   │    - agents/
│   │    - pipelines/
│   │    - triggers/
│   │
│   │  # Global settings
│   │  defaults:
│   │    timeout: 60000
│   │    mode: HYBRID
│   │
│   │  # Invocation methods enabled
│   │  invocation:
│   │    ide: true
│   │    cli: true
│   │    chat: true
│   │    auto: true
│   │    mcp: true
│   │
│   └──────────────────────────────────
│
├── quad/
│   │
│   ├── agents/ ──────────────────────── AGENT DEFINITIONS
│   │   │
│   │   ├── story-agent.yaml
│   │   │   │  agentId: story-agent
│   │   │   │  circle: MANAGEMENT
│   │   │   │  capabilities: [expand-story, generate-ac]
│   │   │   │  canRead: [stories/**, confluence/**]
│   │   │   │  canWrite: [stories/**, confluence/**]
│   │   │   │  canInvoke: [estimation-agent]
│   │   │   │  mcpTools: [gemini, confluence, jira]
│   │   │   └──────────────────────────
│   │   │
│   │   ├── dev-agent-ui.yaml
│   │   ├── dev-agent-api.yaml
│   │   ├── test-agent.yaml
│   │   └── deploy-agent.yaml
│   │
│   ├── pipelines/ ───────────────────── PIPELINE DEFINITIONS
│   │   │
│   │   ├── estimation.yaml
│   │   │   │  name: estimation
│   │   │   │  mode: SEQUENTIAL
│   │   │   │  steps:
│   │   │   │    - agentId: code-agent
│   │   │   │    - agentId: db-agent
│   │   │   │    - agentId: estimation-agent
│   │   │   └──────────────────────────
│   │   │
│   │   ├── development.yaml
│   │   │   │  name: development
│   │   │   │  mode: HYBRID
│   │   │   │  stages:
│   │   │   │    - name: parallel-dev
│   │   │   │      agents: [dev-ui, dev-api]
│   │   │   │      parallel: true
│   │   │   │    - name: integration
│   │   │   │      agents: [integration-agent]
│   │   │   └──────────────────────────
│   │   │
│   │   └── deployment.yaml
│   │
│   ├── triggers/ ────────────────────── TRIGGER CONFIGURATIONS
│   │   │
│   │   ├── jira.yaml
│   │   │   │  source: jira
│   │   │   │  webhookUrl: /api/webhooks/jira
│   │   │   │  rules:
│   │   │   │    story-created:
│   │   │   │      event: issue.created
│   │   │   │      filter: project=PROJ, type=Story
│   │   │   │      target: story-agent
│   │   │   └──────────────────────────
│   │   │
│   │   ├── email.yaml
│   │   ├── slack.yaml
│   │   ├── github.yaml
│   │   └── scheduled.yaml
│   │
│   └── permissions/ ─────────────────── PERMISSION OVERRIDES
│       │
│       ├── circle-1.yaml
│       ├── circle-2.yaml
│       ├── circle-3.yaml
│       └── circle-4.yaml
│
└── .quad/
    │
    ├── credentials.yaml.enc ─────────── ENCRYPTED SECRETS
    │   │  (Never commit to git)
    │   │  jira_api_token: [encrypted]
    │   │  gemini_api_key: [encrypted]
    │   └──────────────────────────
    │
    ├── local.yaml ───────────────────── LOCAL OVERRIDES
    │   │  (Developer-specific settings)
    │   │  invocation:
    │   │    auto: false  # Disable auto in local
    │   └──────────────────────────
    │
    └── audit/ ───────────────────────── AUDIT LOGS
        ├── 2025-12-30.log
        └── 2025-12-31.log
```

### Configuration Inheritance

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CONFIGURATION PRECEDENCE                                  │
├─────────────────────────────────────────────────────────────────────────────┤

LOWEST PRIORITY                                              HIGHEST PRIORITY
     │                                                              │
     ▼                                                              ▼

┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Default   │ ◄──│   Project   │ ◄──│   Local     │ ◄──│ Environment │
│   (Built-in)│    │quad.config  │    │.quad/local  │    │  Variables  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘

Example:

Built-in default:        timeout: 60000
quad.config.yaml:        timeout: 120000       ◄── Overrides built-in
.quad/local.yaml:        timeout: 30000        ◄── Overrides project
QUAD_TIMEOUT=15000       (environment var)      ◄── Overrides all
```

---

## Document Map

### Which Document to Read for What

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         QUAD DOCUMENT MAP                                    │
├─────────────────────────────────────────────────────────────────────────────┤

                         ┌──────────────────────┐
                         │      START HERE      │
                         │                      │
                         │  What do you need?   │
                         └──────────┬───────────┘
                                    │
         ┌──────────────┬───────────┼───────────┬──────────────┐
         │              │           │           │              │
         ▼              ▼           ▼           ▼              ▼
    ┌─────────┐   ┌─────────┐ ┌─────────┐ ┌─────────┐   ┌─────────┐
    │Understand│   │Configure│ │ Build   │ │ Adopt   │   │Reference│
    │  QUAD   │   │ Triggers│ │ Agents  │ │  QUAD   │   │  Info   │
    └────┬────┘   └────┬────┘ └────┬────┘ └────┬────┘   └────┬────┘
         │              │           │           │              │
         ▼              ▼           ▼           ▼              ▼
```

| Your Goal | Read This Document | What You'll Learn |
|-----------|-------------------|-------------------|
| **Understand QUAD basics** | [QUAD.md](../QUAD.md) | Core methodology, 4 circles, 3 axioms |
| **See QUAD in action** | [QUAD_SAMPLE_ENVIRONMENT.md](QUAD_SAMPLE_ENVIRONMENT.md) | GlobalRetail Inc. example with real scenarios |
| **Plan project phases** | [QUAD_PROJECT_LIFECYCLE.md](QUAD_PROJECT_LIFECYCLE.md) | From client call to deployed stories |
| **Configure triggers** | [QUAD_CUSTOMIZABLE_TRIGGERS.md](QUAD_CUSTOMIZABLE_TRIGGERS.md) | Jira, Email, Slack, GitHub webhooks |
| **Build custom agents** | [QUAD_CUSTOM_AGENTS.md](QUAD_CUSTOM_AGENTS.md) | TypeScript interfaces, implementation guide |
| **Understand agent communication** | [QUAD_AGENT_ARCHITECTURE.md](../QUAD_AGENT_ARCHITECTURE.md) | Runtime, pipelines, permissions |
| **Learn slash commands** | [QUAD_COMMANDS.md](QUAD_COMMANDS.md) | `/quad`, `/estimate`, `/review`, etc. |
| **Apply story labels** | [QUAD_STORY_LABELS.md](QUAD_STORY_LABELS.md) | 7-category labeling system |
| **Adopt QUAD in org** | [QUAD_ADOPTION_JOURNEY.md](QUAD_ADOPTION_JOURNEY.md) | 8-step journey (2×QUAD) |
| **See everything together** | [QUAD_INTEGRATION_ARCHITECTURE.md](QUAD_INTEGRATION_ARCHITECTURE.md) | This document |

### Quick Navigation Matrix

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     DOCUMENT × TOPIC MATRIX                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│              │ QUAD │SAMPLE│LIFECY│TRIGGE│AGENTS│ARCHIT│COMMAN│LABELS│ADOPT │
│              │ .md  │ ENV  │ CLE  │  RS  │      │ TURE │  DS  │      │ ION  │
│ ─────────────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────│
│ 4 Circles    │  ●   │  ●   │  ○   │      │      │  ●   │      │  ●   │  ○   │
│ AI Agents    │  ●   │  ●   │      │      │  ●   │  ●   │      │      │  ●   │
│ Triggers     │  ○   │  ●   │      │  ●   │      │  ○   │      │      │      │
│ Pipelines    │      │  ●   │  ○   │      │  ●   │  ●   │      │      │  ●   │
│ Permissions  │      │  ○   │      │      │  ●   │  ●   │      │      │      │
│ CLI/IDE      │      │  ○   │      │      │      │  ○   │  ●   │      │      │
│ Labels       │      │  ●   │      │      │      │      │      │  ●   │      │
│ Configuration│      │      │      │  ●   │  ●   │  ●   │      │      │      │
│ Adoption     │      │      │  ●   │      │      │      │      │      │  ●   │
│ Examples     │  ○   │  ●   │  ●   │  ●   │  ●   │  ●   │  ●   │  ●   │  ●   │
│ ─────────────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────│
│                                                                               │
│ ● = Primary coverage    ○ = Secondary coverage    blank = Not covered        │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Layers

### Technical Architecture Stack

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      IMPLEMENTATION LAYERS                                   │
├─────────────────────────────────────────────────────────────────────────────┤

LAYER 5: USER INTERFACE
═══════════════════════════════════════════════════════════════════════════════
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  VS Code    │  │   Cursor    │  │Claude Claude│  │   QUAD      │
│  Extension  │  │  Extension  │  │   Desktop   │  │    CLI      │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
      │                │                │                │
      └────────────────┴────────────────┴────────────────┘
                               │
                               ▼
LAYER 4: API GATEWAY
═══════════════════════════════════════════════════════════════════════════════
┌─────────────────────────────────────────────────────────────────────────────┐
│                           QUAD API                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   REST      │  │   GraphQL   │  │  WebSocket  │  │  Webhook    │        │
│  │  Endpoints  │  │   (Future)  │  │  (Events)   │  │  Handlers   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
LAYER 3: QUAD AGENT RUNTIME (QAR)
═══════════════════════════════════════════════════════════════════════════════
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                         CORE SERVICES                                 │   │
│  │                                                                       │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐     │   │
│  │  │Orchestrator│  │ Event Bus  │  │  Context   │  │ Permission │     │   │
│  │  │            │  │            │  │  Manager   │  │  Checker   │     │   │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘     │   │
│  │                                                                       │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐     │   │
│  │  │  Agent     │  │  Config    │  │   Audit    │  │   Health   │     │   │
│  │  │  Registry  │  │  Loader    │  │   Logger   │  │   Check    │     │   │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘     │   │
│  │                                                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                         TRIGGER ADAPTERS                              │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐  │   │
│  │  │  Jira  │ │ Email  │ │ Slack  │ │ GitHub │ │  Cron  │ │ Custom │  │   │
│  │  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
LAYER 2: AGENT IMPLEMENTATION
═══════════════════════════════════════════════════════════════════════════════
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐    │
│  │   Circle 1 Agents  │  │   Circle 2 Agents  │  │   Circle 3 Agents  │    │
│  │   ────────────────  │  │   ────────────────  │  │   ────────────────  │    │
│  │   story-agent      │  │   dev-agent-ui     │  │   test-unit-agent  │    │
│  │   code-agent       │  │   dev-agent-api    │  │   test-api-agent   │    │
│  │   db-agent         │  │   dev-agent-db     │  │   test-e2e-agent   │    │
│  │   flow-agent       │  │   review-agent     │  │   security-agent   │    │
│  │   estimation-agent │  │                    │  │   performance-agt  │    │
│  └────────────────────┘  └────────────────────┘  └────────────────────┘    │
│                                                                              │
│  ┌────────────────────┐                                                     │
│  │   Circle 4 Agents  │                                                     │
│  │   ────────────────  │                                                     │
│  │   build-agent      │                                                     │
│  │   deploy-dev-agent │                                                     │
│  │   deploy-prd-agent │                                                     │
│  │   monitor-agent    │                                                     │
│  │   rollback-agent   │                                                     │
│  └────────────────────┘                                                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
LAYER 1: MCP TOOLS & EXTERNAL SERVICES
═══════════════════════════════════════════════════════════════════════════════
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         MCP TOOL ADAPTERS                            │   │
│  │                                                                      │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐    │   │
│  │  │ AI Providers│  │   Source   │  │   Docs &   │  │   Infra &  │    │   │
│  │  │            │  │   Control  │  │   Comms    │  │   Deploy   │    │   │
│  │  │ ─────────── │  │ ──────────  │  │ ──────────  │  │ ──────────  │    │   │
│  │  │ Gemini     │  │ Git        │  │ Confluence │  │ Docker     │    │   │
│  │  │ OpenAI     │  │ GitHub     │  │ Jira       │  │ Kubernetes │    │   │
│  │  │ Anthropic  │  │ GitLab     │  │ Slack      │  │ AWS/GCP    │    │   │
│  │  │ Bedrock    │  │ Bitbucket  │  │ Teams      │  │ Terraform  │    │   │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘    │   │
│  │                                                                      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         EXTERNAL SERVICES                            │   │
│  │                                                                      │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐    │   │
│  │  │   Jira     │  │   GitHub   │  │ Confluence │  │   Slack    │    │   │
│  │  │   Cloud    │  │    API     │  │    API     │  │    API     │    │   │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘    │   │
│  │                                                                      │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐    │   │
│  │  │   AWS      │  │    GCP     │  │   Azure    │  │  On-Prem   │    │   │
│  │  │   Cloud    │  │   Cloud    │  │   Cloud    │  │   Infra    │    │   │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘    │   │
│  │                                                                      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Integration Points

### External System Connections

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      INTEGRATION POINTS                                      │
├─────────────────────────────────────────────────────────────────────────────┤

1. JIRA INTEGRATION
───────────────────────────────────────────────────────────────────────────────

   ┌─────────────────┐                      ┌─────────────────┐
   │      JIRA       │ ◄──── OUTBOUND ────► │      QUAD       │
   │                 │                       │                 │
   │  Webhooks OUT   │ ─────────────────────►│  Trigger Layer  │
   │                 │  issue.created         │                 │
   │                 │  issue.updated         │                 │
   │                 │                        │                 │
   │  REST API IN    │ ◄─────────────────────│  Jira MCP       │
   │                 │  Create issue          │                 │
   │                 │  Update issue          │                 │
   │                 │  Add comment           │                 │
   └─────────────────┘                       └─────────────────┘

   Configuration: quad/triggers/jira.yaml
   MCP Tool: jira-mcp
   Events: issue.created, issue.updated, issue.transitioned


2. GITHUB INTEGRATION
───────────────────────────────────────────────────────────────────────────────

   ┌─────────────────┐                      ┌─────────────────┐
   │     GITHUB      │ ◄──── OUTBOUND ────► │      QUAD       │
   │                 │                       │                 │
   │  Webhooks OUT   │ ─────────────────────►│  Trigger Layer  │
   │                 │  pull_request.opened   │                 │
   │                 │  push                  │                 │
   │                 │                        │                 │
   │  REST API IN    │ ◄─────────────────────│  Git MCP        │
   │                 │  Create PR             │                 │
   │                 │  Add comment           │                 │
   │                 │  Merge                 │                 │
   │                 │                        │                 │
   │  Git Protocol   │ ◄─────────────────────│  Git MCP        │
   │                 │  clone, push, pull     │                 │
   │                 │  commit, branch        │                 │
   └─────────────────┘                       └─────────────────┘

   Configuration: quad/triggers/github.yaml
   MCP Tool: git-mcp
   Events: pull_request.*, push, issue.*


3. CONFLUENCE INTEGRATION
───────────────────────────────────────────────────────────────────────────────

   ┌─────────────────┐                      ┌─────────────────┐
   │   CONFLUENCE    │ ◄──── OUTBOUND ────► │      QUAD       │
   │                 │                       │                 │
   │  Webhooks OUT   │ ─────────────────────►│  Trigger Layer  │
   │                 │  page.created          │                 │
   │                 │  page.updated          │                 │
   │                 │                        │                 │
   │  REST API IN    │ ◄─────────────────────│ Confluence MCP  │
   │                 │  Create page           │                 │
   │                 │  Update page           │                 │
   │                 │  Search                │                 │
   └─────────────────┘                       └─────────────────┘

   Configuration: quad/triggers/confluence.yaml
   MCP Tool: confluence-mcp
   Events: page.*, comment.*


4. SLACK INTEGRATION
───────────────────────────────────────────────────────────────────────────────

   ┌─────────────────┐                      ┌─────────────────┐
   │      SLACK      │ ◄──── OUTBOUND ────► │      QUAD       │
   │                 │                       │                 │
   │  Events API     │ ─────────────────────►│  Trigger Layer  │
   │                 │  message.posted        │                 │
   │                 │  app_mention           │                 │
   │                 │                        │                 │
   │  Web API IN     │ ◄─────────────────────│  Slack MCP      │
   │                 │  Post message          │                 │
   │                 │  Update message        │                 │
   │                 │  React with emoji      │                 │
   └─────────────────┘                       └─────────────────┘

   Configuration: quad/triggers/slack.yaml
   MCP Tool: slack-mcp
   Events: message, app_mention, reaction_added


5. EMAIL INTEGRATION
───────────────────────────────────────────────────────────────────────────────

   ┌─────────────────┐                      ┌─────────────────┐
   │   EMAIL SERVER  │ ◄──── OUTBOUND ────► │      QUAD       │
   │                 │                       │                 │
   │  IMAP Poll      │ ─────────────────────►│  Trigger Layer  │
   │  (or MS Graph)  │  New email detected    │                 │
   │                 │                        │                 │
   │  SMTP OUT       │ ◄─────────────────────│  Email Service  │
   │                 │  Send notification     │                 │
   └─────────────────┘                       └─────────────────┘

   Configuration: quad/triggers/email.yaml
   Events: email.received (matching rules)


6. AI PROVIDER INTEGRATION
───────────────────────────────────────────────────────────────────────────────

   ┌─────────────────┐                      ┌─────────────────┐
   │  AI PROVIDERS   │ ◄──── OUTBOUND ────► │      QUAD       │
   │                 │                       │                 │
   │  Gemini API     │ ◄─────────────────────│  Gemini MCP     │
   │  OpenAI API     │ ◄─────────────────────│  OpenAI MCP     │
   │  Anthropic API  │ ◄─────────────────────│  Claude MCP     │
   │  Bedrock API    │ ◄─────────────────────│  Bedrock MCP    │
   │                 │                        │                 │
   │  Used for:      │                        │                 │
   │  - Story expansion                       │                 │
   │  - Code generation                       │                 │
   │  - Code review                           │                 │
   │  - Test generation                       │                 │
   └─────────────────┘                       └─────────────────┘

   Configuration: mcp_tools section in quad.config.yaml
   Rate limiting and audit enabled per provider
```

---

## Getting Started Guide

### Quick Setup Checklist

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      QUAD QUICK START CHECKLIST                              │
├─────────────────────────────────────────────────────────────────────────────┤

PHASE 1: CORE SETUP (Day 1)
═══════════════════════════════════════════════════════════════════════════════

□ 1. Create quad.config.yaml in project root
     ┌────────────────────────────────────────┐
     │ version: "1.0"                          │
     │ project: "your-project"                 │
     │ invocation:                             │
     │   cli: true                             │
     │   ide: true                             │
     └────────────────────────────────────────┘

□ 2. Install QUAD CLI
     $ npm install -g @quad/cli
     $ quad --version

□ 3. Initialize QUAD in your project
     $ quad init
     Creates: quad/ directory with default configs

□ 4. Configure first agent (Story Agent)
     Edit: quad/agents/story-agent.yaml
     ┌────────────────────────────────────────┐
     │ agentId: story-agent                    │
     │ circle: MANAGEMENT                      │
     │ mcpTools:                               │
     │   - gemini  # or openai, anthropic     │
     │   - jira    # your ticket system       │
     └────────────────────────────────────────┘

□ 5. Add credentials
     $ quad credentials set gemini_api_key <your-key>
     $ quad credentials set jira_api_token <your-token>

□ 6. Test with CLI
     $ quad agent invoke story-agent --story-id=TEST-1


PHASE 2: TRIGGERS (Day 2-3)
═══════════════════════════════════════════════════════════════════════════════

□ 7. Choose your trigger source
     - [ ] Jira (quad/triggers/jira.yaml)
     - [ ] GitHub (quad/triggers/github.yaml)
     - [ ] Email (quad/triggers/email.yaml)
     - [ ] Slack (quad/triggers/slack.yaml)

□ 8. Configure webhook URL in external system
     Jira: Settings → Webhooks → Add: https://your-domain/api/webhooks/jira
     GitHub: Settings → Webhooks → Add: https://your-domain/api/webhooks/github

□ 9. Start QUAD server (for webhook receiving)
     $ quad server start --port 3000

□ 10. Test auto-trigger
      Create a story in Jira → Verify Story Agent runs


PHASE 3: PIPELINES (Day 4-5)
═══════════════════════════════════════════════════════════════════════════════

□ 11. Configure estimation pipeline
      Edit: quad/pipelines/estimation.yaml
      ┌────────────────────────────────────────┐
      │ name: estimation                        │
      │ mode: SEQUENTIAL                        │
      │ steps:                                  │
      │   - agentId: code-agent                │
      │   - agentId: estimation-agent          │
      └────────────────────────────────────────┘

□ 12. Test pipeline
      $ quad pipeline run estimation --story-id=TEST-1

□ 13. Add more agents as needed
      $ quad agent scaffold dev-agent-ui
      $ quad agent scaffold test-agent


PHASE 4: IDE & TEAM (Week 2)
═══════════════════════════════════════════════════════════════════════════════

□ 14. Install VS Code extension
      Extensions → Search "QUAD Agent Framework"

□ 15. Configure team permissions
      Edit: quad/permissions/circle-2.yaml
      ┌────────────────────────────────────────┐
      │ dev-agent-ui:                           │
      │   canWrite: [src/ui/**, src/components/**] │
      │   cannotWrite: [src/api/**]            │
      └────────────────────────────────────────┘

□ 16. Enable chat integration
      Edit quad.config.yaml:
      ┌────────────────────────────────────────┐
      │ invocation:                             │
      │   chat: true                            │
      └────────────────────────────────────────┘

□ 17. Train team on slash commands
      /quad estimate STORY-123
      /quad develop STORY-123
      /quad review PR-45


PHASE 5: PRODUCTION (Week 3-4)
═══════════════════════════════════════════════════════════════════════════════

□ 18. Configure production deploy agent
      Edit: quad/agents/deploy-agent-prod.yaml
      ┌────────────────────────────────────────┐
      │ requiresApproval: true                  │  ← CRITICAL!
      └────────────────────────────────────────┘

□ 19. Set up audit logging
      Edit quad.config.yaml:
      ┌────────────────────────────────────────┐
      │ audit:                                  │
      │   enabled: true                         │
      │   retentionDays: 90                    │
      └────────────────────────────────────────┘

□ 20. Enable monitoring
      $ quad monitor dashboard
      Open: http://localhost:3000/quad/dashboard

□ 21. Document your setup
      $ quad docs generate > QUAD_SETUP.md

└─────────────────────────────────────────────────────────────────────────────┘
```

### Validation Commands

```bash
# Check configuration is valid
quad config validate

# List all registered agents
quad agent list

# List all configured pipelines
quad pipeline list

# Test a trigger without external system
quad trigger test jira --event="issue.created" --data='{"key":"TEST-1"}'

# View audit log
quad audit view --last=100

# Health check
quad health

# View current permissions
quad permissions show dev-agent-ui
```

---

## Deployment Topology

### Single-Team Deployment

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SINGLE-TEAM DEPLOYMENT                                    │
├─────────────────────────────────────────────────────────────────────────────┤

                    ┌──────────────────────────────┐
                    │       QUAD SERVER            │
                    │       (Single Instance)      │
                    │                              │
                    │  ┌──────────────────────┐   │
                    │  │    QAR Runtime       │   │
                    │  │    All Agents        │   │
                    │  │    All Pipelines     │   │
                    │  └──────────────────────┘   │
                    │                              │
                    │  ┌──────────────────────┐   │
                    │  │    Webhook Server    │   │
                    │  │    Port 3000         │   │
                    │  └──────────────────────┘   │
                    └──────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
            ┌───────────────┐       ┌───────────────┐
            │     Jira      │       │    GitHub     │
            │    (Webhook)  │       │   (Webhook)   │
            └───────────────┘       └───────────────┘

Best for: Small teams (1-10 developers), single project
```

### Enterprise Deployment

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ENTERPRISE DEPLOYMENT                                     │
├─────────────────────────────────────────────────────────────────────────────┤

                         ┌─────────────────────────┐
                         │    LOAD BALANCER        │
                         │    (nginx / ALB)        │
                         └───────────┬─────────────┘
                                     │
            ┌────────────────────────┼────────────────────────┐
            │                        │                        │
            ▼                        ▼                        ▼
    ┌───────────────┐        ┌───────────────┐        ┌───────────────┐
    │  QUAD Node 1  │        │  QUAD Node 2  │        │  QUAD Node 3  │
    │               │        │               │        │               │
    │  ┌─────────┐  │        │  ┌─────────┐  │        │  ┌─────────┐  │
    │  │   QAR   │  │        │  │   QAR   │  │        │  │   QAR   │  │
    │  └─────────┘  │        │  └─────────┘  │        │  └─────────┘  │
    │               │        │               │        │               │
    │  Circle 1     │        │  Circle 2     │        │  Circle 3+4   │
    │  Agents       │        │  Agents       │        │  Agents       │
    └───────┬───────┘        └───────┬───────┘        └───────┬───────┘
            │                        │                        │
            └────────────────────────┼────────────────────────┘
                                     │
                         ┌───────────┴───────────┐
                         │                       │
                         ▼                       ▼
                ┌───────────────┐       ┌───────────────┐
                │    Redis      │       │  PostgreSQL   │
                │ (Event Bus)   │       │ (Audit/State) │
                └───────────────┘       └───────────────┘
                         │
                         ▼
                ┌───────────────────────────────────────────┐
                │             KUBERNETES CLUSTER            │
                │                                           │
                │   ┌─────────┐  ┌─────────┐  ┌─────────┐  │
                │   │ Build   │  │ Deploy  │  │ Monitor │  │
                │   │ Runners │  │ Runners │  │ Runners │  │
                │   └─────────┘  └─────────┘  └─────────┘  │
                └───────────────────────────────────────────┘

Best for: Large orgs (50+ developers), multiple projects, high availability
```

---

## Summary

### Key Takeaways

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           KEY TAKEAWAYS                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. SINGLE GATEWAY: All agent invocations flow through QAR                  │
│                                                                              │
│  2. PLUGGABLE TRIGGERS: Jira, Email, Slack, GitHub - configure what works   │
│                                                                              │
│  3. PERMISSION-FIRST: Every action validated, every action audited          │
│                                                                              │
│  4. EXECUTION MODES: SEQUENTIAL, PARALLEL, HYBRID - choose per pipeline     │
│                                                                              │
│  5. HUMAN IN LOOP: Production deployments require human approval            │
│                                                                              │
│  6. MCP TOOLS: AI, Git, Docs - external services with permission layer      │
│                                                                              │
│  7. 8-STEP JOURNEY: First QUAD (operational) + Second QUAD (optimize)       │
│                                                                              │
│  8. CONFIGURATION: YAML-based, hierarchical, environment-aware              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Quick Command Reference

| Command | Description |
|---------|-------------|
| `quad init` | Initialize QUAD in current project |
| `quad agent list` | List all registered agents |
| `quad agent invoke <id>` | Invoke agent directly |
| `quad pipeline run <name>` | Execute a pipeline |
| `quad server start` | Start webhook server |
| `quad config validate` | Validate configuration |
| `quad health` | Check system health |
| `quad audit view` | View audit logs |

---

*Part of QUAD™ (Quick Unified Agentic Development) Methodology*
*© 2025 Suman Addanke / A2 Vibe Creators LLC*
