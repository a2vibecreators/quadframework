# QUAD Slash Commands

## Custom Commands for QUAD Methodology

Part of QUAD™ (Quick Unified Agentic Development) Methodology
© 2025 Suman Addanke / A2 Vibe Creators LLC

---

## Table of Contents

1. [Overview](#overview)
2. [Command Categories](#command-categories)
3. [Story Commands](#story-commands)
4. [Estimation Commands](#estimation-commands)
5. [Pipeline Commands](#pipeline-commands)
6. [Agent Commands](#agent-commands)
7. [Label Commands](#label-commands)
8. [Sprint Commands](#sprint-commands)
9. [Context Commands](#context-commands)
10. [Configuration](#configuration)

---

## Overview

### What Are QUAD Commands?

QUAD provides custom slash commands that users can invoke from:
- **Chat** (Claude, Copilot, ChatGPT)
- **IDE** (VS Code, Cursor)
- **CLI** (Terminal)
- **Jira/Confluence** (via plugins)

```
┌──────────────────────────────────────────────────────────────────────┐
│                    QUAD COMMAND ARCHITECTURE                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  USER TYPES:        WHERE IT'S PARSED:      WHAT EXECUTES:           │
│                                                                      │
│  /expand-story      Chat Interface          QAR invokes              │
│  PROJ-123          (Claude, Copilot)        story-agent              │
│       │                   │                      │                   │
│       │                   ▼                      ▼                   │
│       │            ┌─────────────┐        ┌─────────────┐            │
│       └───────────▶│ QUAD        │───────▶│ Story       │            │
│                    │ Command     │        │ Agent       │            │
│                    │ Router      │        │             │            │
│                    └─────────────┘        └─────────────┘            │
│                                                                      │
│  Command Format:                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │  /command-name [target] [--options]                              ││
│  │                                                                   ││
│  │  Examples:                                                        ││
│  │  /expand-story PROJ-123                                          ││
│  │  /estimate PROJ-123 --detailed                                   ││
│  │  /pipeline estimation --story=PROJ-123                           ││
│  │  /label add PROJ-123 priority/P0 type/SECURITY                   ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Command Prefix

All QUAD commands start with `/` followed by the command name:

| Prefix Style | Example | Use Case |
|--------------|---------|----------|
| `/command` | `/expand-story` | Standard QUAD command |
| `/quad command` | `/quad expand-story` | Explicit namespace (if conflicts) |
| `quad command` | `quad expand-story` | CLI style (no slash in terminal) |

---

## Command Categories

```
┌──────────────────────────────────────────────────────────────────────┐
│                    QUAD COMMAND CATEGORIES                           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐      │
│  │  STORY          │  │  ESTIMATION     │  │  PIPELINE       │      │
│  │  Commands       │  │  Commands       │  │  Commands       │      │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤      │
│  │ /expand-story   │  │ /estimate       │  │ /pipeline       │      │
│  │ /split-story    │  │ /complexity     │  │ /run            │      │
│  │ /merge-stories  │  │ /effort         │  │ /status         │      │
│  │ /refine-story   │  │                 │  │ /cancel         │      │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘      │
│                                                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐      │
│  │  AGENT          │  │  LABEL          │  │  SPRINT         │      │
│  │  Commands       │  │  Commands       │  │  Commands       │      │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤      │
│  │ /agent          │  │ /label          │  │ /sprint         │      │
│  │ /invoke         │  │ /filter         │  │ /plan           │      │
│  │ /agents         │  │ /bulk-label     │  │ /velocity       │      │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘      │
│                                                                      │
│  ┌─────────────────┐  ┌─────────────────┐                           │
│  │  CONTEXT        │  │  CONFIG         │                           │
│  │  Commands       │  │  Commands       │                           │
│  ├─────────────────┤  ├─────────────────┤                           │
│  │ /context        │  │ /config         │                           │
│  │ /project        │  │ /setup          │                           │
│  │ /history        │  │ /audit          │                           │
│  └─────────────────┘  └─────────────────┘                           │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Story Commands

### /expand-story

**Purpose:** Expand a brief requirement into full user stories with acceptance criteria.

```bash
# Basic usage
/expand-story PROJ-123

# With options
/expand-story PROJ-123 --detailed --include-tests
/expand-story PROJ-123 --format=gherkin
/expand-story "As a user, I want to login" --project=PROJ
```

**What happens:**
1. Story Agent reads the original requirement
2. Uses AI (Gemini/Claude) to expand
3. Generates:
   - Detailed user stories
   - Acceptance criteria (Given/When/Then)
   - Technical specifications
   - Test scenarios
   - Edge cases
4. Writes output to Confluence/Jira

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--detailed` | Include technical specs | false |
| `--include-tests` | Generate test scenarios | false |
| `--format` | Output format: `standard`, `gherkin`, `yaml` | standard |
| `--project` | Project key if not in story ID | auto-detect |
| `--output` | Where to write: `jira`, `confluence`, `stdout` | jira |

**Example Output:**
```
✓ Story PROJ-123 expanded successfully

Generated:
  • 4 user stories (PROJ-124, PROJ-125, PROJ-126, PROJ-127)
  • 12 acceptance criteria
  • 8 test scenarios
  • Technical spec linked in Confluence

Complexity estimate: OCTAHEDRON (8 points)
```

---

### /split-story

**Purpose:** Split a large story (ICOSAHEDRON) into smaller stories.

```bash
# Basic usage
/split-story PROJ-123

# Split into specific number
/split-story PROJ-123 --into=3

# Split by platform
/split-story PROJ-123 --by=platform
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--into` | Target number of stories | auto (by complexity) |
| `--by` | Split strategy: `platform`, `layer`, `feature` | auto |
| `--preserve-parent` | Keep original as epic | true |

**Example:**
```
/split-story PROJ-123 --by=platform

✓ Story PROJ-123 split into 4 stories:

  PROJ-124: [API] User authentication endpoint
            Complexity: CUBE (6 pts)

  PROJ-125: [WEB] Login page UI
            Complexity: CUBE (6 pts)

  PROJ-126: [IOS] Native login screen
            Complexity: TETRAHEDRON (4 pts)

  PROJ-127: [ANDROID] Native login screen
            Complexity: TETRAHEDRON (4 pts)

Original PROJ-123 converted to Epic (parent of above)
```

---

### /refine-story

**Purpose:** Improve an existing story based on feedback or questions.

```bash
# Refine with specific feedback
/refine-story PROJ-123 --feedback="Need to handle SSO case"

# Refine based on BA answers
/refine-story PROJ-123 --answers-from=CONF-456

# Interactive refinement
/refine-story PROJ-123 --interactive
```

---

### /merge-stories

**Purpose:** Combine related stories that should be one.

```bash
/merge-stories PROJ-123 PROJ-124 PROJ-125 --into=PROJ-123
```

---

## Estimation Commands

### /estimate

**Purpose:** Estimate complexity using Platonic Solid scale.

```bash
# Basic estimation
/estimate PROJ-123

# Detailed breakdown
/estimate PROJ-123 --detailed

# Estimate multiple
/estimate PROJ-123 PROJ-124 PROJ-125

# Re-estimate with new info
/estimate PROJ-123 --reason="API complexity higher than expected"
```

**What happens:**
1. Runs Estimation Pipeline (SEQUENTIAL):
   - Code Agent: Analyzes code complexity
   - DB Agent: Analyzes database impact
   - Flow Agent: Analyzes integration complexity
   - Estimation Agent: Produces final estimate
2. Returns Platonic Solid complexity

**Example Output:**
```
/estimate PROJ-123 --detailed

┌─────────────────────────────────────────────────────────────────┐
│  ESTIMATION: PROJ-123 - User Authentication                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Final Estimate: OCTAHEDRON (8 points)                         │
│                                                                 │
│  Breakdown:                                                     │
│  ┌──────────────┬────────┬─────────────────────────────────┐   │
│  │ Dimension    │ Score  │ Notes                           │   │
│  ├──────────────┼────────┼─────────────────────────────────┤   │
│  │ Code         │  7/10  │ Multi-layer: API, Service, DTO  │   │
│  │ Database     │  5/10  │ 3 tables, simple schema         │   │
│  │ Integration  │  8/10  │ Redis, Email service, JWT       │   │
│  │ Testing      │  6/10  │ Security tests required         │   │
│  └──────────────┴────────┴─────────────────────────────────┘   │
│                                                                 │
│  Risk Factors:                                                  │
│  ⚠ Security-sensitive (auth bypass risk)                       │
│  ⚠ External dependency (email service)                         │
│                                                                 │
│  Suggested Team: backend-dev + security-reviewer               │
│  Suggested Sprint Duration: 3-4 days                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### /complexity

**Purpose:** Quick complexity check without full pipeline.

```bash
# Quick check
/complexity PROJ-123

# Output:
# PROJ-123: CUBE (6 points) - Standard feature, 2-3 days
```

---

## Pipeline Commands

### /pipeline

**Purpose:** Run or manage agent pipelines.

```bash
# Run estimation pipeline
/pipeline estimation --story=PROJ-123

# Run development pipeline
/pipeline development --story=PROJ-123

# Run custom pipeline
/pipeline code-review --pr=456

# List available pipelines
/pipeline list

# Check pipeline status
/pipeline status --id=pipeline-abc123
```

**Available Pipelines:**

| Pipeline | Mode | Agents |
|----------|------|--------|
| `estimation` | SEQUENTIAL | code → db → flow → estimation |
| `development` | HYBRID | [dev-ui, dev-api] → [test-ui, test-api] → review |
| `code-review` | SEQUENTIAL | security-scanner → code-review → a11y-scanner |
| `deployment` | SEQUENTIAL | test → build → deploy-dev → deploy-qa |

**Example:**
```
/pipeline estimation --story=PROJ-123

✓ Pipeline 'estimation' started

  Pipeline ID: est-20250101-abc123
  Mode: SEQUENTIAL

  Progress:
  [████████░░░░░░░░░░░░] 40%

  Steps:
  ✓ code-agent     (2.3s)  code_complexity: 7
  ✓ db-agent       (1.1s)  db_impact: 5
  ○ flow-agent     (running...)
  ○ estimation-agent

  ETA: ~15 seconds
```

---

### /run

**Purpose:** Shorthand for running pipelines or agents.

```bash
# Run pipeline
/run estimation PROJ-123

# Run single agent
/run story-agent PROJ-123

# Run with verbose output
/run estimation PROJ-123 --verbose
```

---

## Agent Commands

### /agent

**Purpose:** Invoke or manage individual agents.

```bash
# Invoke specific agent
/agent invoke story-agent --story-id=PROJ-123

# Check agent status
/agent status story-agent

# List all agents
/agent list

# Get agent info
/agent info dev-agent-ui
```

**Example:**
```
/agent list

┌──────────────────────────────────────────────────────────────────────┐
│                        AVAILABLE AGENTS                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Circle 1: MANAGEMENT                                                │
│  ├── story-agent        Expands requirements into stories            │
│  ├── estimation-agent   Calculates complexity estimates              │
│  └── pm-agent           Project management assistance                │
│                                                                      │
│  Circle 2: DEVELOPMENT                                               │
│  ├── dev-agent-ui       Frontend development (React, iOS, Android)   │
│  ├── dev-agent-api      Backend development (API, Services)          │
│  ├── code-agent         Code analysis and metrics                    │
│  └── review-agent       Code review and suggestions                  │
│                                                                      │
│  Circle 3: QA                                                        │
│  ├── test-agent         Test generation and execution                │
│  ├── security-agent     Security scanning and analysis               │
│  └── perf-agent         Performance testing                          │
│                                                                      │
│  Circle 4: INFRASTRUCTURE                                            │
│  ├── deploy-agent-dev   Deploy to development environment            │
│  ├── deploy-agent-qa    Deploy to QA environment                     │
│  ├── db-agent           Database analysis and migrations             │
│  └── infra-agent        Infrastructure provisioning                  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

### /invoke

**Purpose:** Shorthand for agent invocation.

```bash
# Equivalent to /agent invoke
/invoke story-agent PROJ-123
/invoke dev-agent-ui --story=PROJ-123 --branch=feature/auth
```

---

## Label Commands

### /label

**Purpose:** Manage story labels.

```bash
# Add labels
/label add PROJ-123 priority/P0 type/SECURITY

# Remove label
/label remove PROJ-123 priority/P2

# Replace label (within category)
/label replace PROJ-123 status/IN_PROGRESS

# View labels
/label show PROJ-123

# Suggest labels (AI analyzes story and suggests)
/label suggest PROJ-123
```

**Example:**
```
/label suggest PROJ-123

Analyzing story PROJ-123: "Implement user authentication with OAuth2"

Suggested labels:
  ✓ priority/P1      (security-related, high business value)
  ✓ type/FEATURE     (new functionality)
  ✓ circle/2-DEV     (development work)
  ✓ platform/API     (backend endpoint)
  ✓ platform/WEB     (frontend integration)
  ✓ complexity/OCTAHEDRON (8 pts - OAuth integration complexity)

Apply these labels? [Y/n]
```

---

### /filter

**Purpose:** Filter and list stories by labels.

```bash
# Find all P0 bugs
/filter priority/P0 type/BUG

# Find blocked items for iOS
/filter status/BLOCKED platform/IOS

# Complex filter
/filter "priority/P0 OR priority/P1" status/IN_PROGRESS circle/2-DEV

# Output as list
/filter status/QA_READY --format=list
```

---

### /bulk-label

**Purpose:** Apply labels to multiple stories.

```bash
# Add sprint label to all ready stories
/bulk-label --filter="status/READY" --add="sprint/SPRINT-04"

# Move all security to P0
/bulk-label --filter="type/SECURITY" --replace="priority/P0"
```

---

## Sprint Commands

### /sprint

**Purpose:** Sprint management.

```bash
# Create new sprint
/sprint create SPRINT-04 --start="2025-01-15" --end="2025-01-28"

# View sprint
/sprint view SPRINT-04

# Add stories to sprint
/sprint add SPRINT-04 PROJ-123 PROJ-124 PROJ-125

# Sprint report
/sprint report SPRINT-04

# Sprint velocity
/sprint velocity SPRINT-04
```

**Example:**
```
/sprint view SPRINT-04

┌──────────────────────────────────────────────────────────────────────┐
│  SPRINT-04: Jan 15 - Jan 28, 2025                                   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Capacity: 120 points    Committed: 98 points    Done: 42 points    │
│                                                                      │
│  Progress: [████████████░░░░░░░░░░░░░░░░░░] 43%                     │
│                                                                      │
│  Status Breakdown:                                                   │
│  ┌────────────────┬─────────┬────────┐                              │
│  │ Status         │ Count   │ Points │                              │
│  ├────────────────┼─────────┼────────┤                              │
│  │ DONE           │    7    │   42   │                              │
│  │ IN_PROGRESS    │    5    │   34   │                              │
│  │ BLOCKED        │    2    │   12   │   ⚠ Needs attention         │
│  │ READY          │    2    │   10   │                              │
│  └────────────────┴─────────┴────────┘                              │
│                                                                      │
│  Blockers:                                                           │
│  • PROJ-156: Waiting for API from vendor                            │
│  • PROJ-162: Security review pending                                │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

### /plan

**Purpose:** Sprint planning assistance.

```bash
# AI-assisted sprint planning
/plan SPRINT-05 --capacity=120

# Plan from backlog
/plan SPRINT-05 --from-backlog --priority=P0,P1
```

---

### /velocity

**Purpose:** Team velocity metrics.

```bash
# Last 5 sprints velocity
/velocity --sprints=5

# By team
/velocity --team=dev-ui

# Trend analysis
/velocity --trend
```

---

## Context Commands

### /context

**Purpose:** Manage project context for agents.

```bash
# Set project context
/context set @project_xyz

# View current context
/context show

# Add context file
/context add ./requirements.md

# Clear context
/context clear
```

**Example:**
```
/context show

Current Context: @globalretail
───────────────────────────────

Loaded files:
  • README.md (project overview)
  • tech_stack.yaml (Java/Oracle/Vertica/React)
  • architecture.md (system diagrams)
  • api_standards.md (REST conventions)
  • domain_glossary.md (business terms)

Active stories in context: 47
Sprint: SPRINT-04
```

---

### /project

**Purpose:** Project-level commands.

```bash
# Switch project
/project switch PROJ

# Project overview
/project overview

# Project health
/project health
```

---

### /history

**Purpose:** View agent invocation history.

```bash
# Recent activity
/history

# For specific story
/history PROJ-123

# Filter by agent
/history --agent=story-agent --limit=10
```

---

## Configuration

### Where Commands Are Defined

```yaml
# .quad/commands.yaml (in your project)
commands:
  # Custom command for this project
  expand-story:
    alias: [es, expand]      # Short forms
    agent: story-agent
    defaults:
      --format: standard
      --output: jira
    permissions:
      circles: [1, 2]        # Management, Development

  # Override default behavior
  estimate:
    pipeline: estimation
    defaults:
      --detailed: true       # Always show details
```

### Registering Custom Commands

```yaml
# Add project-specific command
custom_commands:
  # Deploy to GlobalRetail staging
  deploy-staging:
    description: "Deploy to GlobalRetail staging environment"
    agent: deploy-agent-staging
    requires_approval: true
    allowed_users: [devops-team]

  # Run legacy system analysis
  analyze-cobol:
    description: "Analyze COBOL batch job"
    pipeline: cobol-analysis
    defaults:
      --include-dependencies: true
```

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────────────────────────┐
│                    QUAD COMMANDS QUICK REFERENCE                     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  STORY                            ESTIMATION                         │
│  ─────                            ──────────                         │
│  /expand-story PROJ-123           /estimate PROJ-123                 │
│  /split-story PROJ-123            /complexity PROJ-123               │
│  /refine-story PROJ-123                                              │
│  /merge-stories PROJ-1 PROJ-2                                        │
│                                                                      │
│  PIPELINE                         AGENT                              │
│  ────────                         ─────                              │
│  /pipeline estimation --story=X   /agent invoke NAME --args          │
│  /pipeline development --story=X  /agent list                        │
│  /run estimation PROJ-123         /invoke story-agent PROJ-123       │
│                                                                      │
│  LABELS                           SPRINT                             │
│  ──────                           ──────                             │
│  /label add PROJ-123 priority/P0  /sprint create SPRINT-04           │
│  /label suggest PROJ-123          /sprint view SPRINT-04             │
│  /filter status/BLOCKED           /sprint add SPRINT-04 PROJ-123     │
│  /bulk-label --filter=X --add=Y   /velocity --sprints=5              │
│                                                                      │
│  CONTEXT                          CONFIG                             │
│  ───────                          ──────                             │
│  /context set @project_xyz        /config show                       │
│  /context show                    /audit --story=PROJ-123            │
│  /project switch PROJ                                                │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

*Part of QUAD™ (Quick Unified Agentic Development) Methodology*
*© 2025 Suman Addanke / A2 Vibe Creators LLC*
