# QUAD Agent Communication Architecture (QACA)

**Part of QUAD™ (Quick Unified Agentic Development) Methodology**
**© 2025 Suman Addanke / A2 Vibe Creators LLC**

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Core Components](#core-components)
4. [Communication Patterns](#communication-patterns)
5. [Permission System](#permission-system)
6. [Invocation Methods](#invocation-methods)
7. [Pipeline Examples](#pipeline-examples)
8. [Configuration Reference](#configuration-reference)
9. [Implementation Files](#implementation-files)

---

## Overview

QACA (QUAD Agent Communication Architecture) is the runtime infrastructure that enables AI agents to communicate, collaborate, and execute workflows within the QUAD methodology.

### Key Design Principles

1. **Single Gateway**: All agent invocations flow through QUADAgentRuntime (QAR)
2. **Pluggable Execution**: Support SEQUENTIAL, PARALLEL, and HYBRID modes
3. **Permission-First**: Every action is validated against permission matrix
4. **Full Audit Trail**: Complete logging of all agent actions
5. **Human in Loop**: Production deployments require human approval

### The 4 Circles

```
+------------------------------------------------------------------+
|                      QUAD™ - 4 CIRCLES                            |
+------------------------------------------------------------------+
|                                                                   |
|   CIRCLE 1              CIRCLE 2           CIRCLE 3      CIRCLE 4 |
|   MANAGEMENT            DEVELOPMENT        QA            INFRA    |
|   +---------+          +---------+       +---------+   +---------+|
|   | Story   |          | Dev UI  |       | Test    |   | Deploy  ||
|   | Agent   |    -->   | Agent   |  -->  | Agent   |-->| Agent   ||
|   | Code    |          | Dev API |       | QA      |   | Monitor ||
|   | DB      |          | Review  |       | Scanner |   | Alert   ||
|   +---------+          +---------+       +---------+   +---------+|
|                                                                   |
+------------------------------------------------------------------+
```

---

## Architecture Diagram

### High-Level Architecture

```
+======================================================================+
||                    QUAD AGENT RUNTIME (QAR)                        ||
||                    ========================                        ||
||                                                                    ||
||  +----------------+    +----------------+    +------------------+  ||
||  |   ORCHESTRATOR |    |   EVENT BUS    |    |  SHARED CONTEXT  |  ||
||  |   (Sequential) |<-->|   (Parallel)   |<-->|  (Collaboration) |  ||
||  |                |    |                |    |                  |  ||
||  | Pipeline exec  |    | Pub/Sub events |    | Key-value state  |  ||
||  | Step chaining  |    | Async delivery |    | Permission-gated |  ||
||  +----------------+    +----------------+    +------------------+  ||
||          |                    |                      |             ||
||          v                    v                      v             ||
||  +------------------------------------------------------------+   ||
||  |              PERMISSION CHECKER                             |   ||
||  |  - Pre-invocation validation                               |   ||
||  |  - Post-invocation audit                                   |   ||
||  |  - Resource access control (glob patterns)                 |   ||
||  +------------------------------------------------------------+   ||
||                              |                                     ||
||  +------------------------------------------------------------+   ||
||  |                    AGENT REGISTRY                           |   ||
||  +------------------------------------------------------------+   ||
||  |                         |                         |         |   ||
||  v                         v                         v         v   ||
|| +--------+  +--------+  +--------+  +--------+  +--------+         ||
|| | Story  |  | Dev UI |  | Dev API|  | Test   |  | Deploy |  ...    ||
|| | Agent  |  | Agent  |  | Agent  |  | Agent  |  | Agent  |         ||
|| +--------+  +--------+  +--------+  +--------+  +--------+         ||
||                                                                    ||
+======================================================================+
         |              |              |              |
         v              v              v              v
    +--------+    +--------+    +--------+    +--------+
    |  IDE   |    |  CLI   |    |  Chat  |    |  MCP   |
    | Plugin |    | Command|    |Interface|   | Server |
    +--------+    +--------+    +--------+    +--------+

INVOCATION ENTRY POINTS (All flow through QAR)
```

### Component Interactions

```
                    USER REQUEST
                         |
                         v
+============================================+
|           QUAD AGENT RUNTIME              |
|============================================|
|                                            |
|  1. RECEIVE REQUEST                        |
|     |                                      |
|     v                                      |
|  2. PERMISSION CHECK                       |
|     | - Can user invoke this agent?        |
|     | - Does agent have required perms?    |
|     |                                      |
|     v                                      |
|  3. ROUTE TO EXECUTION ENGINE              |
|     |                                      |
|     +---> ORCHESTRATOR (if pipeline)       |
|     |         |                            |
|     |         v                            |
|     |    Execute steps in order            |
|     |    Chain outputs to inputs           |
|     |                                      |
|     +---> EVENT BUS (if async/parallel)    |
|     |         |                            |
|     |         v                            |
|     |    Broadcast to subscribers          |
|     |    Parallel execution                |
|     |                                      |
|     +---> SHARED CONTEXT (if collaborative)|
|               |                            |
|               v                            |
|          Read/write shared state           |
|                                            |
|  4. EXECUTE AGENT                          |
|     |                                      |
|     v                                      |
|  5. VALIDATE OUTPUT                        |
|     | - Did agent write to allowed paths?  |
|     | - Is output within bounds?           |
|     |                                      |
|     v                                      |
|  6. LOG AUDIT TRAIL                        |
|     |                                      |
|     v                                      |
|  7. RETURN RESULT                          |
|                                            |
+============================================+
                    |
                    v
               RESPONSE
```

---

## Core Components

### 1. QUADAgentRuntime (QAR)

The **single gateway** for all agent operations.

```
+---------------------------------------------------------------+
|                    QUADAgentRuntime                            |
+---------------------------------------------------------------+
|                                                                |
|  PROPERTIES:                                                   |
|  - permissions: PermissionChecker                              |
|  - orchestrator: Orchestrator                                  |
|  - eventBus: EventBus                                          |
|  - context: SharedContext                                      |
|  - agents: Map<string, QUADAgent>                             |
|                                                                |
|  METHODS:                                                      |
|  +----------------------------------------------------------+  |
|  | registerAgent(agent)     | Add agent to registry          | |
|  | invoke(agentId, data)    | Direct single invocation       | |
|  | invokeParallel(ids, data)| Multiple agents at once        | |
|  | executePipeline(name)    | Run configured pipeline        | |
|  | emit(event)              | Broadcast event to bus         | |
|  | setContext(key, value)   | Write to shared context        | |
|  | getContext(key)          | Read from shared context       | |
|  +----------------------------------------------------------+  |
|                                                                |
+---------------------------------------------------------------+
```

### 2. QUADAgent Interface

Every agent must implement this interface:

```
+---------------------------------------------------------------+
|                      QUADAgent Interface                       |
+---------------------------------------------------------------+
|                                                                |
|  IDENTITY:                                                     |
|  +------------------+----------------------------------+       |
|  | agentId          | Unique identifier (e.g., "story-agent") |
|  | circle           | MANAGEMENT | DEVELOPMENT | QA | INFRA   |
|  | version          | Semantic version (e.g., "1.0.0")        |
|  +------------------+----------------------------------+       |
|                                                                |
|  CAPABILITIES:                                                 |
|  +------------------+----------------------------------+       |
|  | capabilities[]   | What this agent can do                  |
|  | requiredInputs[] | Input fields this agent needs           |
|  | outputs[]        | Output fields this agent produces       |
|  +------------------+----------------------------------+       |
|                                                                |
|  PERMISSIONS:                                                  |
|  +------------------+----------------------------------+       |
|  | canRead[]        | Resources agent CAN read                |
|  | canWrite[]       | Resources agent CAN modify              |
|  | canInvoke[]      | Other agents this agent CAN call        |
|  | cannotInvoke[]   | Agents explicitly BLOCKED               |
|  +------------------+----------------------------------+       |
|                                                                |
|  EXECUTION:                                                    |
|  +------------------+----------------------------------+       |
|  | invoke(input)    | Main execution method -> Promise<Output>|
|  | onEvent?(event)  | Handle async events (optional)          |
|  | onRegister?()    | Called when registered (optional)       |
|  | onShutdown?()    | Called when unregistered (optional)     |
|  +------------------+----------------------------------+       |
|                                                                |
+---------------------------------------------------------------+
```

### 3. Orchestrator

Executes pipelines step-by-step:

```
+---------------------------------------------------------------+
|                        Orchestrator                            |
+---------------------------------------------------------------+
|                                                                |
|  EXECUTION MODES:                                              |
|                                                                |
|  SEQUENTIAL:                                                   |
|  +------+     +------+     +------+     +------+               |
|  |  A   | --> |  B   | --> |  C   | --> |  D   |               |
|  +------+     +------+     +------+     +------+               |
|     |            ^            ^            ^                   |
|     |            |            |            |                   |
|     +-- output --+-- chains --+-- to next-+                   |
|                                                                |
|  PARALLEL:                                                     |
|  +------+                                                      |
|  |  A   |--+                                                   |
|  +------+  |                                                   |
|            |    (all at once)                                  |
|  +------+  |                                                   |
|  |  B   |--+====> Results collected                            |
|  +------+  |                                                   |
|            |                                                   |
|  +------+  |                                                   |
|  |  C   |--+                                                   |
|  +------+                                                      |
|                                                                |
|  HYBRID (Stages):                                              |
|  Stage 1           Stage 2           Stage 3                   |
|  +------+------+   +------+------+   +------+                  |
|  | A    | B    |-->| C    | D    |-->| E    |                  |
|  +------+------+   +------+------+   +------+                  |
|  (parallel)        (parallel)        (sequential)              |
|                                                                |
+---------------------------------------------------------------+
```

### 4. Event Bus

Async pub/sub communication:

```
+---------------------------------------------------------------+
|                         Event Bus                              |
+---------------------------------------------------------------+
|                                                                |
|                    +------------------+                        |
|                    |    EVENT BUS     |                        |
|                    +------------------+                        |
|                           |                                    |
|          +----------------+----------------+                   |
|          |                |                |                   |
|          v                v                v                   |
|    +---------+      +---------+      +---------+               |
|    | Agent A |      | Agent B |      | Agent C |               |
|    | (emit)  |      | (listen)|      | (listen)|               |
|    +---------+      +---------+      +---------+               |
|                                                                |
|  EVENT FLOW:                                                   |
|                                                                |
|  Agent A                    Event Bus                Agents    |
|     |                          |                        |      |
|     |  emit("story.created")   |                        |      |
|     |------------------------->|                        |      |
|     |                          |  broadcast to          |      |
|     |                          |  all subscribers       |      |
|     |                          |----------------------->|      |
|     |                          |                        |      |
|     |                          |  Agent B handles       |      |
|     |                          |  Agent C handles       |      |
|     |                          |                        |      |
|                                                                |
|  EVENT TYPES:                                                  |
|  - story.created, story.expanded, story.estimated              |
|  - code.pushed, code.reviewed, pr.created, pr.merged           |
|  - test.started, test.passed, test.failed, bug.found           |
|  - build.started, build.completed, deploy.started              |
|  - pipeline.started, pipeline.completed, pipeline.failed       |
|                                                                |
+---------------------------------------------------------------+
```

### 5. Shared Context

Permission-gated key-value state:

```
+---------------------------------------------------------------+
|                      Shared Context                            |
+---------------------------------------------------------------+
|                                                                |
|  +----------------------------------------------------------+  |
|  |                    CONTEXT STORE                          | |
|  |  +------+  +------+  +------+  +------+  +------+        | |
|  |  | key1 |  | key2 |  | key3 |  | key4 |  | key5 |        | |
|  |  +------+  +------+  +------+  +------+  +------+        | |
|  +----------------------------------------------------------+  |
|           ^           ^           ^                            |
|           |           |           |                            |
|      +----+----+ +----+----+ +----+----+                       |
|      | Agent A | | Agent B | | Agent C |                       |
|      | (write) | | (read)  | | (read)  |                       |
|      +---------+ +---------+ +---------+                       |
|                                                                |
|  ACCESS CONTROL:                                               |
|  +----------------------------------------------------------+  |
|  | Agent A writes "story_123" = {...data...}                 | |
|  | Agent B reads  "story_123" (if has READ permission)       | |
|  | Agent C reads  "story_123" (if has READ permission)       | |
|  | Agent D DENIED "story_123" (lacks READ permission)        | |
|  +----------------------------------------------------------+  |
|                                                                |
|  FEATURES:                                                     |
|  - TTL support (auto-expire keys)                             |
|  - Atomic increment/decrement                                  |
|  - Pattern matching for keys                                   |
|  - History tracking (optional)                                 |
|                                                                |
+---------------------------------------------------------------+
```

---

## Communication Patterns

### Pattern A: Direct Invocation (One-to-One)

```
                    DIRECT INVOCATION
                    =================

     User/Agent                QAR                   Target Agent
         |                      |                         |
         |  invoke("dev-ui",    |                         |
         |         {story_id})  |                         |
         |--------------------->|                         |
         |                      |                         |
         |                      |  1. Check permissions   |
         |                      |  2. Validate input      |
         |                      |                         |
         |                      |  invoke(input)          |
         |                      |------------------------>|
         |                      |                         |
         |                      |                         | (process)
         |                      |                         |
         |                      |        output           |
         |                      |<------------------------|
         |                      |                         |
         |                      |  3. Validate output     |
         |                      |  4. Log audit           |
         |                      |                         |
         |       result         |                         |
         |<---------------------|                         |
         |                      |                         |

USE CASE: Single agent task, direct response needed
```

### Pattern B: Sequential Pipeline (Chain)

```
                    SEQUENTIAL PIPELINE
                    ===================

  Orchestrator --> Agent A --> Agent B --> Agent C --> Agent D
                      |            |            |           |
                      v            v            v           v
                  output_A --> output_B --> output_C --> FINAL

  DETAILED FLOW:
  ==============

  +-----+     +-----+     +-----+     +-----+
  |  A  |     |  B  |     |  C  |     |  D  |
  +-----+     +-----+     +-----+     +-----+
     |           ^           ^           ^
     |           |           |           |
     +-----------+-----------+-----------+
        output      output      output
        chained     chained     chained

  EXECUTION:

  Step 1: Invoke Agent A with initial input
          A returns {code_complexity: 8}

  Step 2: Invoke Agent B with A's output merged
          B receives {code_complexity: 8}
          B returns {db_impact: "HIGH"}

  Step 3: Invoke Agent C with A+B outputs merged
          C receives {code_complexity: 8, db_impact: "HIGH"}
          C returns {flow_complexity: 5}

  Step 4: Invoke Agent D with all outputs merged
          D receives {code_complexity: 8, db_impact: "HIGH", flow_complexity: 5}
          D returns {final_estimate: "DODECAHEDRON"}

  FINAL RESULT: All outputs combined

USE CASE: Estimation pipeline, code review chain
```

### Pattern C: Parallel Invocation (Fan-Out)

```
                    PARALLEL INVOCATION
                    ===================

                    +-------+
                    |  QAR  |
                    +-------+
                        |
        +---------------+---------------+
        |               |               |
        v               v               v
    +-------+       +-------+       +-------+
    |   A   |       |   B   |       |   C   |
    +-------+       +-------+       +-------+
        |               |               |
        v               v               v
    output_A        output_B        output_C
        |               |               |
        +---------------+---------------+
                        |
                        v
                +---------------+
                | Collected Map |
                | A -> output_A |
                | B -> output_B |
                | C -> output_C |
                +---------------+

  EXECUTION TIMELINE:
  ===================

  T=0ms   +---A starts---+
          +---B starts---+
          +---C starts---+

  T=50ms       A completes (50ms)
  T=80ms            B completes (80ms)
  T=120ms                C completes (120ms)

  Total time: 120ms (slowest agent)
  vs Sequential: 50+80+120 = 250ms

USE CASE: Independent UI and API development, parallel testing
```

### Pattern D: Hybrid (Staged Parallel)

```
                    HYBRID EXECUTION
                    ================

  Stage 1 (Parallel)    Stage 2 (Parallel)    Stage 3 (Sequential)
  ==================    ==================    ====================

  +------+  +------+    +------+  +------+    +------+
  |Dev UI|  |DevAPI|    |TestUI|  |TestAPI|   |Review|
  +------+  +------+    +------+  +------+    +------+
      |         |           |         |           |
      v         v           v         v           v
   output    output      output    output      output
      |         |           |         |           |
      +----+----+           +----+----+           |
           |                     |                |
           v                     v                v
      (wait for all)        (wait for all)     FINAL

  TIMELINE:
  =========

  Stage 1: Dev UI and Dev API run in parallel
           Wait until BOTH complete
           Merge their outputs

  Stage 2: Test UI and Test API run in parallel
           Wait until BOTH complete
           Merge their outputs with Stage 1

  Stage 3: Review Agent runs alone
           Has access to all previous outputs
           Produces final review

USE CASE: Development pipeline with dependent testing and review
```

### Pattern E: Event-Driven (Pub/Sub)

```
                    EVENT-DRIVEN COMMUNICATION
                    ==========================

  +-------+                                   +-------+
  | Agent |                                   | Agent |
  |   A   |                                   |   B   |
  +-------+                                   +-------+
      |                                           ^
      | emit("story.created",                     |
      |      {story_id: 123})                     |
      |                                           |
      v                                           |
  +------------------EVENT BUS------------------+ |
  |                                              |-+
  |  Subscriptions:                              |
  |  - Agent B subscribes to "story.*"           |
  |  - Agent C subscribes to "story.created"     |
  |  - Agent D subscribes to "*" (all events)    |
  |                                              |
  +----------------------------------------------+
      |                   |
      v                   v
  +-------+           +-------+
  | Agent |           | Agent |
  |   C   |           |   D   |
  +-------+           +-------+

  EVENT FLOW:
  ===========

  1. Agent A emits "story.created" event

  2. Event Bus receives event

  3. Event Bus finds matching subscriptions:
     - Agent B: "story.*" matches "story.created" YES
     - Agent C: "story.created" matches YES
     - Agent D: "*" matches all YES

  4. Event Bus delivers to B, C, D in parallel

  5. Each agent handles event independently

USE CASE: Notifications, monitoring, loosely-coupled workflows
```

---

## Permission System

### Permission Levels

```
+---------------------------------------------------------------+
|                     PERMISSION LEVELS                          |
+---------------------------------------------------------------+
|                                                                |
|  Level 0: NONE                                                 |
|  +---------------------------------------------------------+   |
|  |  Cannot access resource at all                           |  |
|  |  Example: Dev UI Agent cannot access database/**         |  |
|  +---------------------------------------------------------+   |
|                                                                |
|  Level 1: READ                                                 |
|  +---------------------------------------------------------+   |
|  |  Can read/view resource, cannot modify                   |  |
|  |  Example: Dev UI Agent can READ src/api/** (not write)   |  |
|  +---------------------------------------------------------+   |
|                                                                |
|  Level 2: SUGGEST                                              |
|  +---------------------------------------------------------+   |
|  |  Can suggest changes, human must approve                 |  |
|  |  Example: Review Agent SUGGESTS improvements             |  |
|  +---------------------------------------------------------+   |
|                                                                |
|  Level 3: WRITE                                                |
|  +---------------------------------------------------------+   |
|  |  Can modify resource (with audit logging)                |  |
|  |  Example: Dev UI Agent can WRITE src/ui/**               |  |
|  +---------------------------------------------------------+   |
|                                                                |
|  Level 4: ADMIN                                                |
|  +---------------------------------------------------------+   |
|  |  Full access including delete (rare, use sparingly)      |  |
|  |  Example: Admin Agent managing system configuration      |  |
|  +---------------------------------------------------------+   |
|                                                                |
+---------------------------------------------------------------+
```

### Permission Matrix Example

```
+---------------------------------------------------------------+
|              PERMISSION MATRIX (Agent → Resource)              |
+---------------------------------------------------------------+
|                                                                |
|  Agent: dev-agent-ui                                           |
|  Circle: DEVELOPMENT                                           |
|                                                                |
|  +------------------+-------+--------------------------------+ |
|  | Resource Pattern | Level | Notes                          | |
|  +------------------+-------+--------------------------------+ |
|  | src/ui/**        | WRITE | Can modify UI code             | |
|  | src/components/**| WRITE | Can modify components          | |
|  | src/api/**       | READ  | Can read API, NOT modify       | |
|  | database/**      | NONE  | No database access             | |
|  | tests/ui/**      | WRITE | Can write UI tests             | |
|  | tests/api/**     | NONE  | No API test access             | |
|  +------------------+-------+--------------------------------+ |
|                                                                |
|  Can Invoke: [test-agent-ui, review-agent]                     |
|  Cannot Invoke: [deploy-agent-prod, db-agent]                  |
|                                                                |
+---------------------------------------------------------------+
|                                                                |
|  Agent: deploy-agent-prod                                      |
|  Circle: INFRASTRUCTURE                                        |
|                                                                |
|  +------------------+-------+--------------------------------+ |
|  | Resource Pattern | Level | Notes                          | |
|  +------------------+-------+--------------------------------+ |
|  | infrastructure/**| ADMIN | Full infra access              | |
|  | deployments/**   | WRITE | Can create deployments         | |
|  +------------------+-------+--------------------------------+ |
|                                                                |
|  Can Invoke: [] (terminal agent - cannot invoke others)        |
|  REQUIRES HUMAN APPROVAL: true                                 |
|                                                                |
+---------------------------------------------------------------+
```

### Permission Check Flow

```
                    PERMISSION CHECK FLOW
                    =====================

  Request: Agent A wants to invoke Agent B

  +-------+                                   +-------+
  |Agent A|                                   |Agent B|
  +-------+                                   +-------+
      |                                           |
      |  Request to invoke Agent B                |
      |                                           |
      v                                           |
  +------------------+                            |
  | Permission       |                            |
  | Checker          |                            |
  +------------------+                            |
      |                                           |
      |  CHECK 1: Can A invoke B?                 |
      |  - Is B in A's canInvoke[]?               |
      |  - Is B NOT in A's cannotInvoke[]?        |
      |                                           |
      |  CHECK 2: Does A have required perms?     |
      |  - For each input B needs                 |
      |  - Does A have READ on that resource?     |
      |                                           |
      |  CHECK 3: Does B require approval?        |
      |  - If B.requiresApproval = true           |
      |  - Wait for human confirmation            |
      |                                           |
      |  All checks pass?                         |
      |  YES --> Allow invocation                 |
      |  NO  --> Throw PermissionError            |
      |                                           |
      +------------------------------------------>|
                                                  |
                                            (execute)
```

---

## Invocation Methods

QUAD supports 5 invocation entry points, all flowing through QAR:

```
+---------------------------------------------------------------+
|                    INVOCATION METHODS                          |
+---------------------------------------------------------------+
|                                                                |
|  1. IDE (VS Code, Cursor)                                      |
|  +----------------------------------------------------------+  |
|  |  User right-clicks on story in IDE                        | |
|  |  --> "Expand with Story Agent"                            | |
|  |  --> IDE plugin calls QAR.invoke("story-agent", {...})    | |
|  +----------------------------------------------------------+  |
|                                                                |
|  2. CLI (Command Line)                                         |
|  +----------------------------------------------------------+  |
|  |  $ quad agent invoke story-agent --story-id=123           | |
|  |  $ quad pipeline run estimation --story-id=123            | |
|  |  --> CLI parses args, calls QAR                           | |
|  +----------------------------------------------------------+  |
|                                                                |
|  3. CHAT (Claude, Copilot)                                     |
|  +----------------------------------------------------------+  |
|  |  User: "Estimate story #123"                              | |
|  |  --> AI detects estimation intent                         | |
|  |  --> AI calls QAR.executePipeline("estimation", {...})    | |
|  |  --> Returns: "Estimated at DODECAHEDRON (12)"            | |
|  +----------------------------------------------------------+  |
|                                                                |
|  4. AUTO (CI/CD, Git Hooks)                                    |
|  +----------------------------------------------------------+  |
|  |  on: pull_request                                         | |
|  |    types: [opened, synchronize]                           | |
|  |  --> GitHub Action triggers review-agent                  | |
|  |  --> Results posted as PR comment                         | |
|  +----------------------------------------------------------+  |
|                                                                |
|  5. MCP (Model Context Protocol)                               |
|  +----------------------------------------------------------+  |
|  |  Claude Desktop connects via MCP                          | |
|  |  --> Agents exposed as MCP tools                          | |
|  |  --> User: "Use the story agent to expand this"           | |
|  |  --> Claude calls tool, agent executes                    | |
|  +----------------------------------------------------------+  |
|                                                                |
+---------------------------------------------------------------+
```

### Invocation Method Matrix

```
+---------------------------------------------------------------+
|              INVOCATION METHOD CAPABILITIES                    |
+---------------------------------------------------------------+
|                                                                |
|  +----------+------+------+------+------+------+               |
|  | Feature  | IDE  | CLI  | Chat | Auto | MCP  |               |
|  +----------+------+------+------+------+------+               |
|  | Direct   |  Y   |  Y   |  Y   |  Y   |  Y   |               |
|  | Pipeline |  Y   |  Y   |  Y   |  Y   |  Y   |               |
|  | Parallel |  Y   |  Y   |  N*  |  Y   |  Y   |               |
|  | Events   |  Y   |  Y   |  N   |  Y   |  Y   |               |
|  | Context  |  Y   |  Y   |  Y   |  Y   |  Y   |               |
|  | Approval |  Y   |  Y   |  Y   |  N** |  Y   |               |
|  +----------+------+------+------+------+------+               |
|                                                                |
|  * Chat can orchestrate parallel via pipeline                  |
|  ** Auto mode must use non-approval agents                     |
|                                                                |
+---------------------------------------------------------------+
```

---

## Pipeline Examples

### Example 1: Estimation Pipeline (SEQUENTIAL)

```
+---------------------------------------------------------------+
|              ESTIMATION PIPELINE (SEQUENTIAL)                  |
+---------------------------------------------------------------+
|                                                                |
|  Input: {story_id: "STORY-123", story_text: "As a user..."}   |
|                                                                |
|  +----------+     +----------+     +----------+     +----------+
|  |   Code   |     |    DB    |     |   Flow   |     |Estimation|
|  |   Agent  | --> |   Agent  | --> |   Agent  | --> |   Agent  |
|  +----------+     +----------+     +----------+     +----------+
|       |                |                |                |
|       v                v                v                v
|  code_complexity   db_impact      flow_complexity  final_estimate
|       8             "HIGH"              5           "DODECAHEDRON"
|                                                                |
|  Step-by-Step:                                                 |
|                                                                |
|  Step 1: Code Agent                                            |
|    Input: {story_id, story_text}                              |
|    Output: {code_complexity: 8}                               |
|                                                                |
|  Step 2: DB Agent                                              |
|    Input: {story_id, story_text, code_complexity: 8}          |
|    Output: {db_impact: "HIGH"}                                |
|                                                                |
|  Step 3: Flow Agent                                            |
|    Input: {story_id, story_text, code_complexity: 8,          |
|            db_impact: "HIGH"}                                  |
|    Output: {flow_complexity: 5}                               |
|                                                                |
|  Step 4: Estimation Agent                                      |
|    Input: {story_id, story_text, code_complexity: 8,          |
|            db_impact: "HIGH", flow_complexity: 5}              |
|    Output: {final_estimate: "DODECAHEDRON",                   |
|             complexity_score: 12,                              |
|             reasoning: "..."}                                  |
|                                                                |
|  Final Result: DODECAHEDRON (12 complexity points)             |
|                                                                |
+---------------------------------------------------------------+
```

### Example 2: Development Pipeline (HYBRID)

```
+---------------------------------------------------------------+
|               DEVELOPMENT PIPELINE (HYBRID)                    |
+---------------------------------------------------------------+
|                                                                |
|  STAGE 1: DEVELOPMENT (Parallel)                               |
|  +--------------------------+                                  |
|  |   +-------+  +-------+   |                                  |
|  |   |Dev UI |  |Dev API|   |  <-- Both work simultaneously    |
|  |   +-------+  +-------+   |                                  |
|  |       |          |       |                                  |
|  |       v          v       |                                  |
|  |   ui_code    api_code    |                                  |
|  +--------------------------+                                  |
|              |                                                 |
|              v (wait for BOTH)                                 |
|                                                                |
|  STAGE 2: TESTING (Parallel)                                   |
|  +--------------------------+                                  |
|  |   +-------+  +-------+   |                                  |
|  |   |Test UI|  |TestAPI|   |  <-- Both test simultaneously    |
|  |   +-------+  +-------+   |                                  |
|  |       |          |       |                                  |
|  |       v          v       |                                  |
|  |   ui_tests   api_tests   |                                  |
|  +--------------------------+                                  |
|              |                                                 |
|              v (wait for BOTH)                                 |
|                                                                |
|  STAGE 3: REVIEW (Sequential)                                  |
|  +--------------------------+                                  |
|  |       +--------+         |                                  |
|  |       | Review |         |  <-- Single reviewer             |
|  |       +--------+         |                                  |
|  |           |              |                                  |
|  |           v              |                                  |
|  |      review_comments     |                                  |
|  +--------------------------+                                  |
|              |                                                 |
|              v                                                 |
|         FINAL OUTPUT                                           |
|                                                                |
+---------------------------------------------------------------+
```

### Example 3: Code Review Pipeline (SEQUENTIAL with Optional)

```
+---------------------------------------------------------------+
|            CODE REVIEW PIPELINE (SEQUENTIAL)                   |
+---------------------------------------------------------------+
|                                                                |
|  +----------+     +----------+     +----------+                |
|  | Security |     |  Code    |     |   A11y   |                |
|  | Scanner  | --> |  Review  | --> | Scanner  |                |
|  | (optional)|    | (required)|    | (optional)|               |
|  +----------+     +----------+     +----------+                |
|       |                |                |                      |
|       v                v                v                      |
|  security_issues   review_comments   a11y_issues              |
|                                                                |
|  FLOW:                                                         |
|                                                                |
|  Step 1: Security Scanner (optional: true)                     |
|    - Runs SAST/DAST scans                                     |
|    - If FAILS: Log warning, continue to next step             |
|    - Output: {security_issues: [...]}                         |
|                                                                |
|  Step 2: Code Review (required)                                |
|    - Main review logic                                        |
|    - If FAILS: Pipeline stops!                                |
|    - Output: {review_comments: [...], approved: true/false}   |
|                                                                |
|  Step 3: A11y Scanner (optional: true)                         |
|    - WCAG compliance checks                                   |
|    - If FAILS: Log warning, pipeline completes                |
|    - Output: {a11y_issues: [...]}                             |
|                                                                |
|  NOTE: Optional steps don't break the pipeline if they fail   |
|                                                                |
+---------------------------------------------------------------+
```

---

## Configuration Reference

### quad.config.yaml Structure

```yaml
# =============================================================================
# QUAD CONFIGURATION FILE
# =============================================================================

version: "1.0"
project: "my-project"

# Default settings
defaultTimeout: 60000        # 1 minute
defaultMode: HYBRID          # SEQUENTIAL | PARALLEL | HYBRID

# =============================================================================
# INVOCATION METHODS
# =============================================================================
invocation:
  ide: true                  # VS Code, Cursor
  cli: true                  # Command line
  chat: true                 # Claude, Copilot
  auto: true                 # CI/CD, git hooks
  mcp: true                  # Model Context Protocol

# =============================================================================
# PIPELINES
# =============================================================================
pipelines:
  # Sequential pipeline example
  estimation:
    description: "Multi-agent complexity estimation"
    mode: SEQUENTIAL
    timeout: 120000
    steps:
      - agentId: code-agent
        requiredOutput: code_complexity
        timeout: 30000
      - agentId: db-agent
        requiredOutput: db_impact
      - agentId: flow-agent
        requiredOutput: flow_complexity
      - agentId: estimation-agent
        requiredOutput: final_estimate

  # Hybrid pipeline example
  development:
    description: "Full development cycle"
    mode: HYBRID
    stages:
      - name: development
        agents: [dev-agent-ui, dev-agent-api]
        parallel: true
        waitForAll: true
      - name: testing
        agents: [test-agent-ui, test-agent-api]
        parallel: true
        waitForAll: true
      - name: review
        agents: [review-agent]
        parallel: false

  # Sequential with optional steps
  code-review:
    description: "Automated code review"
    mode: SEQUENTIAL
    steps:
      - agentId: security-scanner-agent
        optional: true           # Won't break pipeline if fails
      - agentId: code-review-agent
        requiredOutput: review_comments
      - agentId: a11y-scanner-agent
        optional: true

# =============================================================================
# PERMISSIONS
# =============================================================================
permissions:
  dev-agent-ui:
    canRead:
      - "src/**"
      - "stories/**"
    canWrite:
      - "src/ui/**"
      - "src/components/**"
      - "tests/ui/**"
    cannotWrite:
      - "src/api/**"
      - "database/**"
    canInvoke:
      - test-agent-ui
      - review-agent

  dev-agent-api:
    canRead:
      - "src/**"
      - "database/schema/**"
    canWrite:
      - "src/api/**"
      - "src/services/**"
      - "tests/api/**"
    cannotWrite:
      - "src/ui/**"
      - "database/data/**"
    canInvoke:
      - test-agent-api
      - review-agent

  deploy-agent-dev:
    canInvoke: []              # Terminal agent
    requiresApproval: false

  deploy-agent-prod:
    canInvoke: []              # Terminal agent
    requiresApproval: true     # HUMAN MUST APPROVE

# =============================================================================
# AUDIT SETTINGS
# =============================================================================
audit:
  enabled: true
  retentionDays: 90
  sensitiveFields:
    - password
    - token
    - secret
    - apiKey

# =============================================================================
# SHARED CONTEXT
# =============================================================================
context:
  maxKeys: 10000
  maxValueSize: 1048576        # 1MB
  enablePersistence: false

# =============================================================================
# EVENT BUS
# =============================================================================
events:
  maxQueueSize: 10000
  eventRetentionMs: 3600000    # 1 hour
  enableReplay: true
  logEvents: false             # Set true for debugging
```

---

## Implementation Files

### File Structure

```
quadframework/
├── src/
│   ├── types/
│   │   └── agent.ts              # Core TypeScript interfaces
│   │
│   ├── lib/
│   │   ├── permissions.ts        # Permission checker
│   │   ├── orchestrator.ts       # Pipeline execution
│   │   ├── event-bus.ts          # Event pub/sub
│   │   ├── shared-context.ts     # Shared state
│   │   └── agent-runtime.ts      # Main runtime (QAR)
│   │
│   ├── examples/
│   │   ├── example-agents.ts     # Demo agents
│   │   └── demo.ts               # Demo script
│   │
│   └── app/
│       └── architecture/
│           └── page.tsx          # Visual documentation
│
├── quad.config.example.yaml      # Example configuration
│
└── documentation/
    └── QUAD_AGENT_ARCHITECTURE.md  # This file
```

### File Descriptions

| File | Purpose |
|------|---------|
| `types/agent.ts` | Core TypeScript interfaces (QUADAgent, Pipeline, Permission, etc.) |
| `lib/permissions.ts` | Permission checking, resource validation, audit logging |
| `lib/orchestrator.ts` | Pipeline execution (SEQUENTIAL, PARALLEL, HYBRID modes) |
| `lib/event-bus.ts` | Async event pub/sub between agents |
| `lib/shared-context.ts` | Permission-gated key-value state sharing |
| `lib/agent-runtime.ts` | Main QUADAgentRuntime - the single gateway |
| `examples/example-agents.ts` | Full implementation of example agents |
| `examples/demo.ts` | Runnable demo script with explanations |
| `quad.config.example.yaml` | Example YAML configuration file |

---

## Quick Reference

### Agent Lifecycle

```
1. CREATE    --> Define agent with interface
2. REGISTER  --> runtime.registerAgent(agent)
3. INVOKE    --> runtime.invoke(agentId, data)
4. EXECUTE   --> Agent processes input
5. VALIDATE  --> Output checked against permissions
6. LOG       --> Audit trail recorded
7. RETURN    --> Output returned to caller
```

### Pipeline Lifecycle

```
1. DEFINE    --> Configure in quad.config.yaml
2. REGISTER  --> Loaded by runtime on startup
3. EXECUTE   --> runtime.executePipeline(name, data)
4. RUN STEPS --> Execute according to mode
5. COLLECT   --> Gather all step results
6. RETURN    --> PipelineResult with all outputs
```

### Event Lifecycle

```
1. EMIT      --> agent emits event
2. ROUTE     --> Event bus finds subscribers
3. FILTER    --> Apply subscription filters
4. DELIVER   --> Async delivery to handlers
5. PROCESS   --> Each subscriber handles event
6. LOG       --> Event recorded in history
```

---

## MCP Tool Permissions (Gemini, Git, Confluence)

MCP (Model Context Protocol) tools are **external services** that QUAD agents can use. They have their own permission layer.

### MCP Permission Architecture

```
+------------------------------------------------------------------+
|                    MCP PERMISSION MODEL                           |
+------------------------------------------------------------------+
|                                                                   |
|  QUAD AGENT (internal)          MCP TOOL (external)               |
|  +------------------+           +------------------+               |
|  |   Story Agent    |  uses →   |   Gemini API     |               |
|  |   Dev Agent UI   |  uses →   |   Git MCP        |               |
|  |   Doc Agent      |  uses →   |   Confluence MCP |               |
|  +------------------+           +------------------+               |
|                                                                   |
|  Permission Checks:                                               |
|  1. Is QUAD agent allowed to USE this MCP tool?                   |
|  2. What SCOPES can the agent access via MCP?                     |
|  3. What ACTIONS can the agent perform?                          |
|  4. Rate limits and audit logging                                |
|                                                                   |
+------------------------------------------------------------------+
```

### MCP Tool Configuration

```yaml
# In quad.config.yaml
mcp_tools:
  # ========================================================================
  # GEMINI (AI Provider)
  # ========================================================================
  gemini:
    type: AI_PROVIDER
    scopes:
      - text_generation
      - code_analysis
      - summarization
    allowed_agents:
      - story-agent        # Can use for story expansion
      - estimation-agent   # Can use for complexity analysis
      - review-agent       # Can use for code review
    denied_agents:
      - deploy-agent-prod  # No AI assistance for prod deploy
    rate_limit: 100/hour
    audit: true

  # ========================================================================
  # GIT (Source Control)
  # ========================================================================
  git:
    type: SOURCE_CONTROL
    scopes:
      read: [clone, fetch, log, diff, status]
      write: [commit, push, branch, merge]
    allowed_agents:
      dev-agent-ui:
        scopes: [read, write]
        branches: ["feature/*", "fix/*"]      # Can work on feature/fix
        protected: ["main", "release/*"]       # Cannot touch main/release
      dev-agent-api:
        scopes: [read, write]
        branches: ["feature/*", "fix/*"]
      test-agent:
        scopes: [read]                         # Read-only
      deploy-agent-dev:
        scopes: [read]
        branches: ["main"]                     # Read main for deploy
    denied_agents:
      - story-agent                            # No git access

  # ========================================================================
  # CONFLUENCE (Documentation)
  # ========================================================================
  confluence:
    type: DOCUMENTATION
    scopes:
      read: [get_page, search, get_space]
      write: [create_page, update_page, add_comment]
    allowed_agents:
      story-agent:
        scopes: [read, write]
        spaces: ["PROJ", "SPECS"]              # Only project/specs spaces
      doc-agent:
        scopes: [read, write]
        spaces: ["*"]                          # All spaces
      dev-agent-ui:
        scopes: [read]                         # Read-only
    denied_agents:
      - deploy-agent-prod
```

### MCP Permission Check Flow

```
                    MCP PERMISSION CHECK
                    ====================

  Story Agent wants to use Gemini for story expansion

  +-------------+                              +-------------+
  | Story Agent |                              | Gemini MCP  |
  +-------------+                              +-------------+
        |                                            |
        |  1. Request: "Expand this story"           |
        v                                            |
  +------------------+                               |
  | QAR Permission   |                               |
  | Checker          |                               |
  +------------------+                               |
        |                                            |
        |  CHECK 1: Is story-agent in allowed_agents?|
        |  ✓ Yes, story-agent is allowed             |
        |                                            |
        |  CHECK 2: Is scope allowed?                |
        |  Request: text_generation                  |
        |  Allowed: [text_generation, code_analysis] |
        |  ✓ Yes, scope is allowed                   |
        |                                            |
        |  CHECK 3: Rate limit OK?                   |
        |  Current: 45 requests this hour            |
        |  Limit: 100/hour                           |
        |  ✓ Yes, under limit                        |
        |                                            |
        |  All checks pass → Allow MCP call          |
        +-------------------------------------------->|
                                                     |
                                              (Gemini processes)
                                                     |
        <--------------------------------------------+
        |                                            |
        |  4. Log audit entry                        |
        |  {agent: story-agent, mcp: gemini,         |
        |   scope: text_generation, success: true}   |
```

---

## Story Agent Trigger Flow

How does "BA writes requirement → Story Agent triggers" actually work?

### Who/What Can Trigger Story Agent?

```
┌──────────────────────────────────────────────────────────────────────┐
│                    WHO TRIGGERS STORY AGENT?                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  TWO CATEGORIES OF TRIGGERS:                                         │
│                                                                      │
│  ╔═══════════════════════════════════════════════════════════════╗  │
│  ║  A. HUMAN TRIGGERS (BA, PM, Developer)                         ║  │
│  ╠═══════════════════════════════════════════════════════════════╣  │
│  ║                                                                 ║  │
│  ║  1. BA clicks "Expand Story" button in Jira                    ║  │
│  ║     └── Jira plugin sends request to QAR                       ║  │
│  ║                                                                 ║  │
│  ║  2. BA types in chat: "@QUAD expand story PROJ-123"            ║  │
│  ║     └── Claude/AI detects intent → calls Story Agent           ║  │
│  ║                                                                 ║  │
│  ║  3. BA right-clicks in VS Code → "Expand with Story Agent"     ║  │
│  ║     └── IDE plugin → QAR.invoke("story-agent")                 ║  │
│  ║                                                                 ║  │
│  ║  4. Developer runs CLI: quad agent invoke story-agent          ║  │
│  ║     └── Direct command line invocation                         ║  │
│  ║                                                                 ║  │
│  ╚═══════════════════════════════════════════════════════════════╝  │
│                                                                      │
│  ╔═══════════════════════════════════════════════════════════════╗  │
│  ║  B. AUTOMATED TRIGGERS (Webhooks, Other Agents)                ║  │
│  ╠═══════════════════════════════════════════════════════════════╣  │
│  ║                                                                 ║  │
│  ║  1. Jira Webhook (Auto on ticket create)                       ║  │
│  ║     └── BA saves ticket → Jira fires webhook → Story Agent     ║  │
│  ║     └── BA doesn't click anything, it's automatic              ║  │
│  ║                                                                 ║  │
│  ║  2. Confluence Webhook (Auto on page save)                     ║  │
│  ║     └── BA saves requirements doc → webhook → Story Agent      ║  │
│  ║                                                                 ║  │
│  ║  3. Another AI Agent triggers Story Agent                      ║  │
│  ║     └── PM Agent creates rough outline                         ║  │
│  ║     └── PM Agent emits "requirement.created" event             ║  │
│  ║     └── Story Agent subscribes to this event → auto-runs       ║  │
│  ║                                                                 ║  │
│  ║  4. Scheduled Trigger (Cron)                                   ║  │
│  ║     └── Every morning, re-expand incomplete stories            ║  │
│  ║                                                                 ║  │
│  ╚═══════════════════════════════════════════════════════════════╝  │
│                                                                      │
│  KEY INSIGHT:                                                        │
│  ═══════════                                                         │
│  "BA writes requirement" doesn't mean BA manually triggers.          │
│  It means: When BA SAVES their work, automation picks it up.         │
│                                                                      │
│  The BA's ACTION is:    Write & Save                                 │
│  The TRIGGER is:        Webhook/Event (automatic)                    │
│  The EXECUTOR is:       Story Agent (AI)                             │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Trigger Configuration (quad.config.yaml)

```yaml
# Configure what triggers Story Agent
story-agent:
  triggers:
    # ========================================
    # HUMAN TRIGGERS (explicit invocation)
    # ========================================
    human:
      enabled: true
      methods:
        - ide: true           # VS Code, Cursor
        - chat: true          # Claude, Copilot
        - cli: true           # Command line
        - jira_button: true   # "Expand Story" button in Jira

    # ========================================
    # AUTOMATIC TRIGGERS (webhooks, events)
    # ========================================
    auto:
      enabled: true

      # Jira webhook - when story is created/updated
      jira_webhook:
        events: [issue.created, issue.updated]
        filter:
          project: "PROJ"
          issueType: ["Story", "Epic"]
          fields_changed: ["description", "summary"]  # Only on these changes
        skip_if:
          - status: "Done"                # Don't re-expand done stories
          - label: "no-ai-expand"         # Manual opt-out label

      # Confluence webhook - when requirements page saved
      confluence_webhook:
        events: [page.created, page.updated]
        filter:
          space: ["PROJ", "SPECS"]
          label: "requirement"            # Only pages with this label

      # Agent-to-Agent trigger
      event_subscription:
        - event: "pm-agent.requirement.created"
          action: expand_story
        - event: "pm-agent.epic.created"
          action: expand_epic

      # Scheduled trigger
      cron:
        enabled: false                    # Optional, off by default
        schedule: "0 6 * * *"             # 6 AM daily
        filter: "status = 'Draft' AND age > 24h"
```

### Example: Agent-to-Agent Trigger

```
┌──────────────────────────────────────────────────────────────────────┐
│        AGENT-TO-AGENT TRIGGER EXAMPLE                                │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  PM Agent creates high-level requirement                             │
│  Story Agent automatically expands it                                │
│                                                                      │
│  +------------------+                                                │
│  | PM Agent         |  1. PM Agent creates rough requirement         │
│  | (AI)             |     "Users should be able to login"            │
│  +------------------+                                                │
│          │                                                           │
│          │ 2. PM Agent emits event:                                  │
│          │    emit("pm-agent.requirement.created", {                 │
│          │      requirement_id: "REQ-001",                           │
│          │      text: "Users should be able to login",               │
│          │      priority: "HIGH"                                     │
│          │    })                                                     │
│          ▼                                                           │
│  +------------------+                                                │
│  | Event Bus        |  3. Event Bus routes to subscribers            │
│  +------------------+                                                │
│          │                                                           │
│          │ 4. Story Agent is subscribed to this event type           │
│          ▼                                                           │
│  +------------------+                                                │
│  | Story Agent      |  5. Story Agent auto-triggers                  │
│  | (AI)             |     invocationMethod: "AUTO"                   │
│  +------------------+     source: "pm-agent"                         │
│          │                                                           │
│          │ 6. Story Agent expands into full stories:                 │
│          │    - STORY-001: User registration                         │
│          │    - STORY-002: User login                                │
│          │    - STORY-003: Password reset                            │
│          │    - STORY-004: Session management                        │
│          ▼                                                           │
│  +------------------+                                                │
│  | Jira MCP         |  7. Stories created in Jira                    │
│  +------------------+                                                │
│                                                                      │
│  RESULT: PM Agent's rough idea → 4 detailed stories automatically   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Complete Trigger Flow

```
+------------------------------------------------------------------+
|              STORY AGENT TRIGGER FLOW                             |
+------------------------------------------------------------------+
|                                                                   |
|  STEP 1: BA writes requirement in Jira/Confluence                 |
|  ================================================================ |
|                                                                   |
|  +------------------+                                             |
|  | BA (Human)       |                                             |
|  | Types in Jira:   |                                             |
|  | "As a user, I    |                                             |
|  |  want to login"  |                                             |
|  +------------------+                                             |
|          |                                                        |
|          | (saves ticket)                                         |
|          v                                                        |
|  +------------------+                                             |
|  | Jira Webhook     |                                             |
|  | fires event      |                                             |
|  +------------------+                                             |
|          |                                                        |
|          | POST /api/webhooks/jira/story-created                  |
|          v                                                        |
|                                                                   |
|  STEP 2: Webhook triggers QAR                                     |
|  ================================================================ |
|                                                                   |
|  +------------------+                                             |
|  | QAR Webhook      |                                             |
|  | Handler          |                                             |
|  +------------------+                                             |
|          |                                                        |
|          | runtime.invoke("story-agent", {                        |
|          |   story_id: "PROJ-123",                                |
|          |   story_text: "As a user...",                          |
|          |   invocationMethod: "AUTO"                             |
|          | })                                                     |
|          v                                                        |
|                                                                   |
|  STEP 3: Story Agent executes with MCP tools                      |
|  ================================================================ |
|                                                                   |
|  +------------------+     +------------------+                    |
|  | Story Agent      |     | Gemini MCP       |                    |
|  +------------------+     +------------------+                    |
|          |                        |                               |
|          |  1. Read original      |                               |
|          |     story from Jira    |                               |
|          |                        |                               |
|          |  2. Call Gemini to     |                               |
|          |     expand story       |                               |
|          |----------------------->|                               |
|          |                        |                               |
|          |  3. Gemini returns     |                               |
|          |     expanded content   |                               |
|          |<-----------------------|                               |
|          |                        |                               |
|          |  4. Generate:          |                               |
|          |     - User stories     |                               |
|          |     - Acceptance       |                               |
|          |       criteria         |                               |
|          |     - Technical specs  |                               |
|          |     - Test scenarios   |                               |
|          v                                                        |
|                                                                   |
|  STEP 4: Output written back via Confluence MCP                   |
|  ================================================================ |
|                                                                   |
|  +------------------+     +------------------+                    |
|  | Story Agent      |     | Confluence MCP   |                    |
|  +------------------+     +------------------+                    |
|          |                        |                               |
|          |  Write expanded story  |                               |
|          |  to Confluence page    |                               |
|          |----------------------->|                               |
|          |                        |                               |
|          |  Update Jira ticket    |                               |
|          |  with link to specs    |                               |
|          |----------------------->|                               |
|          v                                                        |
|                                                                   |
|  STEP 5: Emit event for downstream agents                         |
|  ================================================================ |
|                                                                   |
|  +------------------+     +------------------+                    |
|  | Story Agent      |     | Event Bus        |                    |
|  +------------------+     +------------------+                    |
|          |                        |                               |
|          |  emit("story.expanded",|                               |
|          |    {story_id, specs})  |                               |
|          |----------------------->|                               |
|          |                        |                               |
|          |               Subscribers notified:                    |
|          |               - Estimation Agent (estimates)           |
|          |               - Dev Agents (start development)         |
|          |                        |                               |
|                                                                   |
+------------------------------------------------------------------+
```

### 5 Ways to Trigger Any Agent

```
+------------------------------------------------------------------+
|                    TRIGGER METHODS                                |
+------------------------------------------------------------------+

1. AUTO (Webhook) - Automated Triggers
   ===================================
   Source: Jira, GitHub, Confluence, CI/CD

   Jira creates ticket → Webhook → QAR → Story Agent

   Configuration:
   webhooks:
     story-created:
       source: jira
       event: issue.created
       filter: "project = PROJ AND type = Story"
       agent: story-agent
       invocationMethod: AUTO

2. CHAT (Conversation with AI)
   ============================
   User: "Hey Claude, expand story PROJ-123"
   Claude detects intent → QAR.invoke("story-agent")

   Trigger phrases:
   - "expand story..."
   - "enhance this requirement..."
   - "generate acceptance criteria for..."
   - "what's the technical spec for..."

3. IDE (VS Code / Cursor)
   =======================
   User right-clicks → "Expand with Story Agent"
   IDE plugin → QAR.invoke("story-agent")

   Keyboard shortcut: Cmd+Shift+E

4. CLI (Command Line)
   ===================
   $ quad agent invoke story-agent --story-id=PROJ-123
   $ quad pipeline run estimation --story-id=PROJ-123 --verbose

5. MCP (Claude Desktop)
   =====================
   Story Agent exposed as MCP tool
   User: "Use the story expansion tool on PROJ-123"
   Claude Desktop → MCP call → QAR → Story Agent
```

### Story Agent Input/Output Spec

```
+------------------------------------------------------------------+
|                    STORY AGENT I/O                                |
+------------------------------------------------------------------+

INPUT (what BA provides):
=========================
{
  "story_id": "PROJ-123",
  "story_text": "As a user, I want to login with my email so that
                I can access my account",
  "project_context": "NutriNine health app",
  "priority": "HIGH",
  "sprint": "Sprint 5"
}


OUTPUT (what Story Agent produces):
===================================
{
  "success": true,
  "data": {
    "expanded_story": {
      "title": "User Email Login",
      "epic": "Authentication",

      "user_stories": [
        "As a new user, I want to register with email/password",
        "As a returning user, I want to login with email/password",
        "As a user who forgot password, I want to reset it",
        "As a logged-in user, I want to logout securely"
      ],

      "acceptance_criteria": [
        "GIVEN a valid email and password",
        "WHEN user clicks Login button",
        "THEN user is redirected to dashboard",
        "AND JWT token is stored in secure storage",
        "AND session is created in database",
        "",
        "GIVEN an invalid password",
        "WHEN user clicks Login button",
        "THEN error message 'Invalid credentials' is shown",
        "AND login attempt is logged for security"
      ],

      "technical_specs": {
        "api_endpoints": [
          "POST /api/auth/login",
          "POST /api/auth/register",
          "POST /api/auth/logout",
          "POST /api/auth/forgot-password",
          "POST /api/auth/reset-password"
        ],
        "database_tables": [
          "users",
          "user_sessions",
          "password_reset_tokens"
        ],
        "security_requirements": [
          "BCrypt password hashing (cost factor 12)",
          "JWT tokens with 24h expiry",
          "Rate limiting: 5 attempts per 15 minutes",
          "Account lockout after 10 failed attempts"
        ]
      },

      "test_scenarios": [
        "✓ Valid login with correct credentials succeeds",
        "✓ Invalid password returns 401 error",
        "✓ Non-existent email returns 401 (no user enumeration)",
        "✓ Account locks after 10 failed attempts",
        "✓ Password reset email is sent",
        "✓ JWT token expires after 24 hours",
        "✓ Logout invalidates session"
      ],

      "edge_cases": [
        "Email with special characters (test+tag@example.com)",
        "Very long password (>100 characters)",
        "Unicode characters in password",
        "Concurrent login from multiple devices",
        "Session handling across time zones"
      ],

      "dependencies": [
        "Email service (SendGrid/SES) for password reset",
        "Redis for session management",
        "Rate limiting middleware"
      ]
    },

    "complexity_hints": {
      "platonic_solid": "OCTAHEDRON",
      "complexity_score": 8,
      "estimated_circle": "DEVELOPMENT",
      "affected_systems": ["auth", "database", "email", "cache"],
      "risk_level": "MEDIUM",
      "suggested_assignees": ["backend-dev", "security-reviewer"]
    },

    "confluence_link": "https://wiki.company.com/PROJ/stories/PROJ-123-specs",
    "jira_updated": true
  },

  "modifiedResources": [
    "confluence/PROJ/stories/PROJ-123-specs",
    "jira/PROJ-123"
  ],
  "readResources": [
    "jira/PROJ-123",
    "confluence/PROJ/project-context"
  ],
  "duration": 4500,
  "mcp_calls": [
    {"tool": "gemini", "scope": "text_generation", "duration": 2800},
    {"tool": "confluence", "scope": "create_page", "duration": 450},
    {"tool": "jira", "scope": "update_issue", "duration": 320}
  ]
}
```

### Webhook Configuration for Auto-Trigger

```yaml
# In quad.config.yaml
webhooks:
  # Jira story created → Story Agent
  jira-story-created:
    source: jira
    event: issue.created
    filter:
      project: "PROJ"
      issueType: "Story"
    agent: story-agent
    invocationMethod: AUTO

  # Jira story updated → Re-expand if needed
  jira-story-updated:
    source: jira
    event: issue.updated
    filter:
      project: "PROJ"
      issueType: "Story"
      fields: ["description", "summary"]  # Only on these field changes
    agent: story-agent
    invocationMethod: AUTO
    condition: "issue.fields.status != 'Done'"  # Skip if already done

  # GitHub PR opened → Code Review Agent
  github-pr-opened:
    source: github
    event: pull_request.opened
    filter:
      base: ["main", "develop"]
    agent: review-agent
    invocationMethod: AUTO

  # GitHub push to main → Deploy Agent
  github-push-main:
    source: github
    event: push
    filter:
      ref: "refs/heads/main"
    pipeline: deployment-pipeline  # Run full pipeline, not single agent
    invocationMethod: AUTO
```

---

## Summary Table

| Component | Purpose | Key Methods |
|-----------|---------|-------------|
| **QAR** | Single gateway | `invoke()`, `executePipeline()`, `emit()` |
| **Orchestrator** | Pipeline execution | `executeSequential()`, `executeParallel()`, `executeHybrid()` |
| **Event Bus** | Async pub/sub | `emit()`, `subscribe()`, `replayTo()` |
| **Shared Context** | State sharing | `read()`, `write()`, `increment()` |
| **Permission Checker** | Access control | `canInvokeAgent()`, `canWriteResource()`, `logAction()` |
| **MCP Tools** | External services | Gemini, Git, Confluence, Jira |

---

**Author:** QUAD Methodology Team
**Version:** 1.0.0
**Last Updated:** December 31, 2025
**© 2025 Suman Addanke / A2 Vibe Creators LLC**
