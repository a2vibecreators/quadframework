# QUAD Story Labeling System

## Full Labels (Option B) - Comprehensive 7-Category System

Part of QUAD™ (Quick Unified Agentic Development) Methodology
© 2025 Suman Addanke / A2 Vibe Creators LLC

---

## Table of Contents

1. [Overview](#overview)
2. [The 7 Label Categories](#the-7-label-categories)
3. [Label Definitions](#label-definitions)
4. [Auto-Labeling Rules](#auto-labeling-rules)
5. [Filtering & Queries](#filtering--queries)
6. [Label Commands](#label-commands)
7. [Visual Label Guide](#visual-label-guide)
8. [Best Practices](#best-practices)

---

## Overview

### Why Labels Matter

```
WITHOUT LABELS:                      WITH LABELS:
──────────────                       ───────────
"Which stories for QA?"              priority/P0 + status/QA-READY
→ Manual search, miss things         → Instant filter, nothing missed

"What's blocking us?"                status/BLOCKED
→ Ask around, waste time             → One click, see all blockers

"Security audit scope?"              type/SECURITY
→ Dig through every story            → Complete list in seconds
```

### Label Philosophy

- **Mutually Exclusive**: Each category has ONE value per story (except Platform)
- **Required Labels**: Priority, Status, Type, Circle (minimum)
- **Optional Labels**: Platform, Sprint, Complexity
- **Hierarchical**: Labels are namespaced (priority/P0, status/BACKLOG)

---

## The 7 Label Categories

```
┌─────────────────────────────────────────────────────────────────────┐
│                    QUAD STORY LABEL CATEGORIES                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  1. PRIORITY │  │  2. STATUS   │  │   3. TYPE    │              │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤              │
│  │ P0 Critical  │  │ BACKLOG      │  │ FEATURE      │              │
│  │ P1 High      │  │ READY        │  │ BUG          │              │
│  │ P2 Medium    │  │ IN_PROGRESS  │  │ SECURITY     │              │
│  │ P3 Low       │  │ BLOCKED      │  │ TECH_DEBT    │              │
│  │              │  │ QA_READY     │  │ INFRA        │              │
│  │              │  │ QA_PASS      │  │ DOCS         │              │
│  │              │  │ QA_FAIL      │  │ SPIKE        │              │
│  │              │  │ DONE         │  │              │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  4. CIRCLE   │  │ 5. PLATFORM  │  │  6. SPRINT   │              │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤              │
│  │ 1-MGMT       │  │ API          │  │ SPRINT-01    │              │
│  │ 2-DEV        │  │ WEB          │  │ SPRINT-02    │              │
│  │ 3-QA         │  │ IOS          │  │ SPRINT-03    │              │
│  │ 4-INFRA      │  │ ANDROID      │  │ ...          │              │
│  │              │  │ BATCH        │  │ SPRINT-NN    │              │
│  │              │  │ SHARED       │  │              │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│                                                                     │
│  ┌──────────────────────────────────────────────────┐              │
│  │              7. COMPLEXITY (Platonic Solids)      │              │
│  ├──────────────────────────────────────────────────┤              │
│  │ TETRAHEDRON (4)  │ CUBE (6)      │ OCTAHEDRON (8)│              │
│  │ DODECAHEDRON(12) │ ICOSAHEDRON(20)               │              │
│  └──────────────────────────────────────────────────┘              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Label Definitions

### 1. Priority Labels

| Label | Code | Description | SLA |
|-------|------|-------------|-----|
| `priority/P0` | Critical | Production down, security breach, data loss | < 4 hours |
| `priority/P1` | High | Major feature blocked, significant bug | < 24 hours |
| `priority/P2` | Medium | Standard feature work, minor bugs | Sprint |
| `priority/P3` | Low | Nice-to-have, polish, minor improvements | Backlog |

**Decision Matrix:**
```
Is production broken?           → P0
Is a major feature blocked?     → P1
Is it committed for sprint?     → P2
Everything else                 → P3
```

### 2. Status Labels

| Label | Description | Who Moves It |
|-------|-------------|--------------|
| `status/BACKLOG` | Not yet prioritized | BA/PM |
| `status/READY` | Groomed, ready for sprint | BA after grooming |
| `status/IN_PROGRESS` | Developer working on it | Developer |
| `status/BLOCKED` | Waiting on dependency | Developer |
| `status/CODE_REVIEW` | PR submitted, awaiting review | Developer |
| `status/QA_READY` | Code merged, ready for QA | Developer |
| `status/QA_PASS` | QA verified, passed | QA |
| `status/QA_FAIL` | QA found issues | QA |
| `status/DONE` | Deployed, verified | PM/Tech Lead |

**Status Flow:**
```
BACKLOG → READY → IN_PROGRESS → CODE_REVIEW → QA_READY → QA_PASS → DONE
                       ↓                          ↓
                   BLOCKED                    QA_FAIL
                       ↓                          ↓
                   (resolved)              IN_PROGRESS (fix)
```

### 3. Type Labels

| Label | Description | Examples |
|-------|-------------|----------|
| `type/FEATURE` | New functionality | Login page, payment flow |
| `type/BUG` | Defect fix | Crash on submit, wrong calculation |
| `type/SECURITY` | Security related | SQL injection fix, auth bypass |
| `type/TECH_DEBT` | Code improvement | Refactor, upgrade library |
| `type/INFRA` | Infrastructure | CI/CD, deploy scripts |
| `type/DOCS` | Documentation | README, API docs |
| `type/SPIKE` | Research/POC | "Can we use X library?" |

### 4. Circle Labels

| Label | Circle | Owner |
|-------|--------|-------|
| `circle/1-MGMT` | Management | BA, PM, Tech Lead |
| `circle/2-DEV` | Development | Full Stack, Backend, UI, Mobile |
| `circle/3-QA` | Quality | QA Engineer, Automation |
| `circle/4-INFRA` | Infrastructure | DevOps, SRE, DBA |

**Assignment Rules:**
- Features → circle/2-DEV
- Test automation → circle/3-QA
- Deploy/CI-CD → circle/4-INFRA
- Documentation → circle/1-MGMT (or owner circle)

### 5. Platform Labels (Multi-Select Allowed)

| Label | Platform |
|-------|----------|
| `platform/API` | Backend REST API |
| `platform/WEB` | Web application |
| `platform/IOS` | iOS native app |
| `platform/ANDROID` | Android native app |
| `platform/BATCH` | Batch jobs, scheduled tasks |
| `platform/SHARED` | Shared libraries, common code |

**Multi-Platform Example:**
```yaml
labels:
  - platform/API       # Backend endpoint
  - platform/WEB       # Web UI
  - platform/IOS       # iOS implementation
  - platform/ANDROID   # Android implementation
```

### 6. Sprint Labels

| Label | Description |
|-------|-------------|
| `sprint/SPRINT-01` | First sprint |
| `sprint/SPRINT-02` | Second sprint |
| ... | ... |
| `sprint/SPRINT-NN` | Nth sprint |
| `sprint/BACKLOG` | Not assigned to sprint |

### 7. Complexity Labels (Platonic Solids)

| Label | Shape | Points | Typical Scope |
|-------|-------|--------|---------------|
| `complexity/TETRAHEDRON` | Tetrahedron | 4 | Simple task, 1 file, < 1 day |
| `complexity/CUBE` | Cube | 6 | Standard task, 2-3 files, 1-2 days |
| `complexity/OCTAHEDRON` | Octahedron | 8 | Multi-component, 3-5 files, 2-3 days |
| `complexity/DODECAHEDRON` | Dodecahedron | 12 | Complex feature, multiple services, 3-5 days |
| `complexity/ICOSAHEDRON` | Icosahedron | 20 | Epic-level, cross-team, 5+ days |

**Estimation Guide:**
```
┌───────────────┬────────┬─────────────────────────────────────────┐
│ Complexity    │ Points │ Characteristics                         │
├───────────────┼────────┼─────────────────────────────────────────┤
│ TETRAHEDRON   │   4    │ Single platform, simple logic           │
│               │        │ No external dependencies                │
│               │        │ Clear acceptance criteria               │
├───────────────┼────────┼─────────────────────────────────────────┤
│ CUBE          │   6    │ 1-2 platforms, some business logic      │
│               │        │ Minor dependencies                      │
│               │        │ Standard patterns                       │
├───────────────┼────────┼─────────────────────────────────────────┤
│ OCTAHEDRON    │   8    │ Multi-platform, complex logic           │
│               │        │ Multiple dependencies                   │
│               │        │ Needs design discussion                 │
├───────────────┼────────┼─────────────────────────────────────────┤
│ DODECAHEDRON  │  12    │ All platforms, significant complexity   │
│               │        │ External service integration            │
│               │        │ Architecture decisions                  │
├───────────────┼────────┼─────────────────────────────────────────┤
│ ICOSAHEDRON   │  20    │ Epic scope, should probably be split    │
│               │        │ Cross-team coordination                 │
│               │        │ Unknown unknowns                        │
└───────────────┴────────┴─────────────────────────────────────────┘
```

---

## Auto-Labeling Rules

### Story Agent Auto-Labels

When Story Agent generates stories, it automatically applies labels:

```yaml
# Auto-labeling rules (in quad.config.yaml)
auto_labeling:
  rules:
    # Priority based on keywords
    - match: "security|vulnerability|breach|CVE"
      apply: ["priority/P0", "type/SECURITY"]

    - match: "crash|data loss|cannot login"
      apply: ["priority/P0", "type/BUG"]

    - match: "bug|fix|broken|not working"
      apply: ["priority/P2", "type/BUG"]

    # Type based on context
    - match: "refactor|cleanup|upgrade"
      apply: ["type/TECH_DEBT"]

    - match: "deploy|ci|cd|pipeline"
      apply: ["type/INFRA", "circle/4-INFRA"]

    - match: "document|readme|api doc"
      apply: ["type/DOCS"]

    # Platform detection
    - match: "ios|iphone|swift"
      apply: ["platform/IOS"]

    - match: "android|kotlin"
      apply: ["platform/ANDROID"]

    - match: "api|endpoint|rest"
      apply: ["platform/API"]

    - match: "web|react|next"
      apply: ["platform/WEB"]

    # Complexity based on scope
    - platforms_count: 1
      apply: ["complexity/TETRAHEDRON"]

    - platforms_count: 2
      apply: ["complexity/CUBE"]

    - platforms_count: [3, 4]
      apply: ["complexity/OCTAHEDRON"]

    - platforms_count: 5+
      apply: ["complexity/DODECAHEDRON"]
```

### Default Labels

If no rules match, Story Agent applies defaults:
- `priority/P2` (Medium)
- `status/BACKLOG`
- `type/FEATURE`
- `circle/2-DEV`
- `complexity/CUBE`

---

## Filtering & Queries

### Common Queries

**"What's ready for QA this sprint?"**
```bash
quad stories list \
  --label status/QA_READY \
  --label sprint/SPRINT-03
```

**"All security issues in progress"**
```bash
quad stories list \
  --label type/SECURITY \
  --label status/IN_PROGRESS
```

**"P0/P1 blockers for iOS"**
```bash
quad stories list \
  --label priority/P0,priority/P1 \
  --label status/BLOCKED \
  --label platform/IOS
```

**"What did QA pass this week?"**
```bash
quad stories list \
  --label status/QA_PASS \
  --since "2025-01-01"
```

**"Tech debt for Circle 2"**
```bash
quad stories list \
  --label type/TECH_DEBT \
  --label circle/2-DEV
```

**"All stories touching API"**
```bash
quad stories list \
  --label platform/API
```

### Filter Syntax

```
# Single label
--label status/IN_PROGRESS

# Multiple labels (AND)
--label status/IN_PROGRESS --label priority/P0

# Multiple values (OR)
--label priority/P0,priority/P1

# Exclude
--not-label status/DONE

# Complex query
--label type/SECURITY --label status/IN_PROGRESS,status/BLOCKED --not-label priority/P3
```

### Dashboard Views

Pre-configured views for common needs:

| View | Filter | Purpose |
|------|--------|---------|
| `sprint-board` | sprint/SPRINT-XX | Current sprint work |
| `qa-queue` | status/QA_READY | QA team's queue |
| `blockers` | status/BLOCKED | All blockers |
| `security-audit` | type/SECURITY | Security review |
| `my-work` | assignee/@me + status/IN_PROGRESS | Personal work |
| `p0-alert` | priority/P0 + !status/DONE | Critical items |

---

## Label Commands

### Apply Labels

```bash
# Add single label
quad story label add STORY-001 priority/P0

# Add multiple labels
quad story label add STORY-001 priority/P0 type/SECURITY status/IN_PROGRESS

# Remove label
quad story label remove STORY-001 priority/P2

# Replace label (within category)
quad story label replace STORY-001 status/QA_READY
# Automatically removes status/IN_PROGRESS
```

### Bulk Operations

```bash
# Move all P0 security to IN_PROGRESS
quad stories bulk-label \
  --filter "priority/P0 AND type/SECURITY" \
  --add status/IN_PROGRESS \
  --remove status/BACKLOG

# Assign sprint to ready stories
quad stories bulk-label \
  --filter "status/READY AND circle/2-DEV" \
  --add sprint/SPRINT-04

# Clear sprint from backlog
quad stories bulk-label \
  --filter "status/BACKLOG" \
  --remove "sprint/*"
```

### Sprint Management

```bash
# Start new sprint
quad sprint create SPRINT-04 --start "2025-01-15" --end "2025-01-28"

# Move stories to sprint
quad sprint add SPRINT-04 STORY-001 STORY-002 STORY-003

# View sprint
quad sprint view SPRINT-04

# Sprint velocity
quad sprint velocity SPRINT-04
```

---

## Visual Label Guide

### Label Badge Colors

```
┌────────────────────────────────────────────────────────────────┐
│                      LABEL COLOR CODING                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  PRIORITY                                                      │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  P0  │ RED         #FF0000  │ Critical, immediate action │ │
│  │  P1  │ ORANGE      #FF8C00  │ High, within 24h           │ │
│  │  P2  │ YELLOW      #FFD700  │ Medium, sprint             │ │
│  │  P3  │ GRAY        #808080  │ Low, backlog               │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  STATUS                                                        │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  BACKLOG      │ LIGHT GRAY  #D3D3D3  │ Not started      │ │
│  │  READY        │ LIGHT BLUE  #87CEEB  │ Ready for work   │ │
│  │  IN_PROGRESS  │ BLUE        #4169E1  │ Being worked on  │ │
│  │  BLOCKED      │ RED         #DC143C  │ Blocked          │ │
│  │  CODE_REVIEW  │ PURPLE      #9370DB  │ In review        │ │
│  │  QA_READY     │ TEAL        #20B2AA  │ Ready for QA     │ │
│  │  QA_PASS      │ GREEN       #32CD32  │ QA passed        │ │
│  │  QA_FAIL      │ ORANGE      #FF6347  │ QA failed        │ │
│  │  DONE         │ DARK GREEN  #228B22  │ Completed        │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  TYPE                                                          │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  FEATURE      │ BLUE        #4169E1  │ New functionality│ │
│  │  BUG          │ RED         #DC143C  │ Defect           │ │
│  │  SECURITY     │ DARK RED    #8B0000  │ Security issue   │ │
│  │  TECH_DEBT    │ BROWN       #8B4513  │ Tech debt        │ │
│  │  INFRA        │ GRAY        #708090  │ Infrastructure   │ │
│  │  DOCS         │ LIGHT GREEN #90EE90  │ Documentation    │ │
│  │  SPIKE        │ PURPLE      #9932CC  │ Research         │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  CIRCLE                                                        │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  1-MGMT       │ GOLD        #FFD700  │ Management       │ │
│  │  2-DEV        │ BLUE        #1E90FF  │ Development      │ │
│  │  3-QA         │ GREEN       #32CD32  │ Quality          │ │
│  │  4-INFRA      │ GRAY        #696969  │ Infrastructure   │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  PLATFORM                                                      │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  API          │ NAVY        #000080  │ Backend          │ │
│  │  WEB          │ SKY BLUE    #87CEEB  │ Web app          │ │
│  │  IOS          │ SILVER      #C0C0C0  │ iOS app          │ │
│  │  ANDROID      │ GREEN       #3DDC84  │ Android app      │ │
│  │  BATCH        │ PURPLE      #800080  │ Batch jobs       │ │
│  │  SHARED       │ PINK        #FF69B4  │ Common           │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  COMPLEXITY (Platonic Solids)                                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  TETRAHEDRON  │ LIGHT GREEN #98FB98  │ 4 pts  - Simple  │ │
│  │  CUBE         │ YELLOW      #FFFF00  │ 6 pts  - Medium  │ │
│  │  OCTAHEDRON   │ ORANGE      #FFA500  │ 8 pts  - Complex │ │
│  │  DODECAHEDRON │ RED         #FF4500  │ 12 pts - Large   │ │
│  │  ICOSAHEDRON  │ DARK RED    #B22222  │ 20 pts - Epic    │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Story Card Example

```
┌──────────────────────────────────────────────────────────────────┐
│ STORY-001                                                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Apply 20% Seasonal Discount at Checkout                         │
│                                                                  │
│  ┌──────┐ ┌───────────────┐ ┌─────────┐ ┌──────────────┐        │
│  │  P0  │ │ IN_PROGRESS   │ │ FEATURE │ │   2-DEV      │        │
│  │ RED  │ │    BLUE       │ │  BLUE   │ │   BLUE       │        │
│  └──────┘ └───────────────┘ └─────────┘ └──────────────┘        │
│                                                                  │
│  ┌───────┐ ┌───────┐ ┌─────────┐ ┌───────┐ ┌──────────────┐     │
│  │  API  │ │  WEB  │ │   IOS   │ │ANDROID│ │ SPRINT-03    │     │
│  │ NAVY  │ │ SKY   │ │ SILVER  │ │ GREEN │ │   CYAN       │     │
│  └───────┘ └───────┘ └─────────┘ └───────┘ └──────────────┘     │
│                                                                  │
│  ┌───────────────────┐                                          │
│  │  CUBE (6 pts)     │                                          │
│  │     YELLOW        │                                          │
│  └───────────────────┘                                          │
│                                                                  │
│  Assignee: @dev-john          Due: Jan 15, 2025                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Best Practices

### Do's

1. **Always set Priority and Status** - Minimum required labels
2. **Update Status immediately** - When work state changes
3. **Use Platform labels** - Helps with assignment and tracking
4. **Review labels in grooming** - Ensure consistency
5. **Let Story Agent auto-label first** - Then refine manually

### Don'ts

1. **Don't create custom labels** without team discussion
2. **Don't leave stories unlabeled** - At least Priority + Status
3. **Don't over-label** - 5-7 labels per story is typical
4. **Don't change Priority without PM approval** - Especially P0/P1
5. **Don't skip Complexity** - Needed for sprint planning

### Label Review Checklist

Before sprint planning, review all ready stories:

- [ ] Priority set and appropriate
- [ ] Status is READY (groomed)
- [ ] Type correctly categorized
- [ ] Circle assigned to owner team
- [ ] Platform(s) identified
- [ ] Complexity estimated
- [ ] Sprint label applied

---

## Configurable Ticket Label Format

Organizations can configure their preferred ticket label format. The label format is assembled from components:

### Label Format Builder

```yaml
# quad.config.yaml

ticket_labels:
  # Format template
  format: "{circle}-{estimate}-{type}"

  # Available tokens:
  # {circle}    - C1, C2, C3, C4 (Management, Dev, QA, Infra)
  # {estimate}  - D4, D6, D8, D12, D20 (Platonic Solids) or custom
  # {type}      - FEAT, BUG, SEC, DEBT, INFRA, DOC, SPIKE
  # {priority}  - P0, P1, P2, P3
  # {platform}  - API, WEB, IOS, AND, BATCH

  # Example outputs:
  # C2-D8-FEAT     → Circle 2, Octahedron (8pts), Feature
  # C3-D6-BUG      → Circle 3, Hexahedron (6pts), Bug
  # C4-D12-INFRA   → Circle 4, Dodecahedron (12pts), Infrastructure
```

### Preset Formats

```yaml
presets:
  mathematical:
    format: "{circle}-{estimate}-{type}"
    circle_prefix: "C"
    estimate_prefix: "D"
    examples:
      - "C2-D8-FEAT"
      - "C3-D6-BUG"
      - "C1-D4-DOC"

  descriptive:
    format: "{circle_name}/{type}/{priority}"
    examples:
      - "DEV/FEATURE/P2"
      - "QA/BUG/P1"
      - "INFRA/SECURITY/P0"

  simple:
    format: "{type}-{estimate}"
    examples:
      - "FEAT-8"
      - "BUG-6"
      - "SEC-12"

  github_style:
    format: "{type}: {priority}"
    examples:
      - "feat: P2"
      - "fix: P1"
      - "security: P0"

  jira_style:
    format: "[{circle}] {type}"
    examples:
      - "[DEV] Feature"
      - "[QA] Bug"
      - "[INFRA] Tech Debt"
```

### Estimation Naming Presets

```yaml
estimation:
  preset: "platonic"  # platonic | dice | tshirt | fibonacci | powers

  presets:
    platonic:
      name: "Platonic Solids"
      values:
        - { key: "D4", name: "Tetrahedron", points: 4 }
        - { key: "D6", name: "Hexahedron", points: 6 }
        - { key: "D8", name: "Octahedron", points: 8 }
        - { key: "D12", name: "Dodecahedron", points: 12 }
        - { key: "D20", name: "Icosahedron", points: 20 }

    dice:
      name: "Dice Notation"
      values:
        - { key: "d4", name: "d4", points: 4 }
        - { key: "d6", name: "d6", points: 6 }
        - { key: "d8", name: "d8", points: 8 }
        - { key: "d12", name: "d12", points: 12 }
        - { key: "d20", name: "d20", points: 20 }

    tshirt:
      name: "T-Shirt Sizes"
      values:
        - { key: "XS", name: "Extra Small", points: 1 }
        - { key: "S", name: "Small", points: 2 }
        - { key: "M", name: "Medium", points: 4 }
        - { key: "L", name: "Large", points: 8 }
        - { key: "XL", name: "Extra Large", points: 16 }

    fibonacci:
      name: "Fibonacci"
      values:
        - { key: "1", name: "1", points: 1 }
        - { key: "2", name: "2", points: 2 }
        - { key: "3", name: "3", points: 3 }
        - { key: "5", name: "5", points: 5 }
        - { key: "8", name: "8", points: 8 }
        - { key: "13", name: "13", points: 13 }

    powers:
      name: "Powers of 2"
      values:
        - { key: "2^0", name: "1", points: 1 }
        - { key: "2^1", name: "2", points: 2 }
        - { key: "2^2", name: "4", points: 4 }
        - { key: "2^3", name: "8", points: 8 }
        - { key: "2^4", name: "16", points: 16 }
```

### Type Abbreviations

```yaml
types:
  preset: "short"  # short | long | emoji

  presets:
    short:
      - { key: "FEAT", full: "Feature" }
      - { key: "BUG", full: "Bug" }
      - { key: "SEC", full: "Security" }
      - { key: "DEBT", full: "Tech Debt" }
      - { key: "INFRA", full: "Infrastructure" }
      - { key: "DOC", full: "Documentation" }
      - { key: "SPIKE", full: "Research/POC" }

    long:
      - { key: "FEATURE", full: "Feature" }
      - { key: "BUGFIX", full: "Bug Fix" }
      - { key: "SECURITY", full: "Security" }
      - { key: "TECHDEBT", full: "Tech Debt" }
      - { key: "INFRASTRUCTURE", full: "Infrastructure" }
      - { key: "DOCUMENTATION", full: "Documentation" }
      - { key: "RESEARCH", full: "Research/POC" }

    emoji:
      - { key: "✨", full: "Feature" }
      - { key: "🐛", full: "Bug" }
      - { key: "🔒", full: "Security" }
      - { key: "🔧", full: "Tech Debt" }
      - { key: "🏗️", full: "Infrastructure" }
      - { key: "📝", full: "Documentation" }
      - { key: "🔬", full: "Research/POC" }
```

### Interactive Ticket Label Builder

The `/configure` page provides an interactive builder:

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                    QUAD TICKET LABEL CONFIGURATOR                               │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  1. SELECT FORMAT TEMPLATE                                                      │
│  ─────────────────────────                                                      │
│                                                                                 │
│  ○ Mathematical: {circle}-{estimate}-{type}         Example: C2-D8-FEAT        │
│  ○ Descriptive:  {circle_name}/{type}/{priority}    Example: DEV/FEATURE/P2    │
│  ● Custom:       [ {circle}-{estimate}-{type} ]     Example: C2-D8-FEAT        │
│                                                                                 │
│  2. SELECT ESTIMATION SCHEME                                                    │
│  ───────────────────────────                                                    │
│                                                                                 │
│  ● Platonic Solids (D4, D6, D8, D12, D20)                                      │
│  ○ Dice Notation (d4, d6, d8, d12, d20)                                        │
│  ○ T-Shirt Sizes (XS, S, M, L, XL)                                             │
│  ○ Fibonacci (1, 2, 3, 5, 8, 13)                                               │
│  ○ Powers of 2 (1, 2, 4, 8, 16)                                                │
│                                                                                 │
│  3. SELECT TYPE ABBREVIATION                                                    │
│  ───────────────────────────                                                    │
│                                                                                 │
│  ● Short (FEAT, BUG, SEC)                                                      │
│  ○ Long (FEATURE, BUGFIX, SECURITY)                                            │
│  ○ Emoji (✨, 🐛, 🔒)                                                           │
│                                                                                 │
│  4. LIVE PREVIEW                                                                │
│  ───────────────                                                                │
│                                                                                 │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │                                                                         │    │
│  │   Your ticket labels will look like:                                    │    │
│  │                                                                         │    │
│  │   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐                  │    │
│  │   │ C1-D4-DOC│ │C2-D8-FEAT│ │C3-D6-BUG │ │C4-D12-SEC│                  │    │
│  │   └──────────┘ └──────────┘ └──────────┘ └──────────┘                  │    │
│  │                                                                         │    │
│  │   Circle 1 + Tetrahedron + Documentation                                │    │
│  │   Circle 2 + Octahedron + Feature                                       │    │
│  │   Circle 3 + Hexahedron + Bug                                           │    │
│  │   Circle 4 + Dodecahedron + Security                                    │    │
│  │                                                                         │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  5. EXPORT                                                                      │
│  ─────────                                                                      │
│                                                                                 │
│  [Download quad.config.yaml]  [Copy to Clipboard]  [Apply to Project]          │
│                                                                                 │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## Summary

| Category | Purpose | Values |
|----------|---------|--------|
| **Priority** | Urgency | P0, P1, P2, P3 |
| **Status** | Workflow state | BACKLOG → DONE |
| **Type** | Work classification | FEATURE, BUG, SECURITY, etc. |
| **Circle** | Team ownership | 1-MGMT, 2-DEV, 3-QA, 4-INFRA |
| **Platform** | Target systems | API, WEB, IOS, ANDROID, BATCH |
| **Sprint** | Time allocation | SPRINT-01 to SPRINT-NN |
| **Complexity** | Effort estimate | Platonic Solids (4-20 pts) |

**Total unique labels:** ~30 standard labels across 7 categories

**Configurable elements:**
- Label format template
- Estimation naming scheme (Platonic, Dice, T-Shirt, Fibonacci, Powers)
- Type abbreviations (Short, Long, Emoji)
- All exportable via quad.config.yaml

---

*Part of QUAD™ (Quick Unified Agentic Development) Methodology*
*© 2025 Suman Addanke / A2 Vibe Creators LLC*
