# QUAD Role-Based Dashboards

**Last Updated:** January 3, 2026
**Status:** Design Phase

---

## Table of Contents

1. [Overview](#1-overview)
2. [Role Hierarchy](#2-role-hierarchy)
3. [Dashboard Structure](#3-dashboard-structure)
4. [IDE Tab](#4-ide-tab)
5. [Widget System](#5-widget-system)
6. [Access Control](#6-access-control)
7. [Implementation Plan](#7-implementation-plan)

---

## 1. Overview

### Vision

QUAD dashboards should feel like an **IDE experience**, not just another web dashboard. Each role gets a tailored view with appropriate depth of access.

### Key Principles

| Principle | Description |
|-----------|-------------|
| **IDE-First** | Developer-friendly interface with panels, tabs, and keyboard shortcuts |
| **Role-Appropriate** | Show what's relevant, restrict drilling to prevent micromanagement |
| **Customizable** | Users can configure their home screen with widgets |
| **Context-Aware** | Dashboard adapts to current project, sprint, and role |

---

## 2. Role Hierarchy

### Access Pyramid

```
                    ┌───────────────┐
                    │ COMPANY ADMIN │ ← Platform Configuration
                    └───────┬───────┘
                            │
              ┌─────────────┴─────────────┐
              │     SENIOR DIRECTOR       │ ← Portfolio Overview
              └─────────────┬─────────────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    ┌────┴────┐       ┌────┴────┐       ┌────┴────┐
    │DIRECTOR │       │DIRECTOR │       │DIRECTOR │ ← Domain Projects
    └────┬────┘       └────┬────┘       └────┬────┘
         │                  │                  │
    ┌────┴────┐       ┌────┴────┐       ┌────┴────┐
    │TEAM LEAD│       │TEAM LEAD│       │TEAM LEAD│ ← Circle Management
    └────┬────┘       └────┬────┘       └────┬────┘
         │                  │                  │
    ┌────┴────┐       ┌────┴────┐       ┌────┴────┐
    │OPERATOR │       │OPERATOR │       │OPERATOR │ ← Individual Work
    └─────────┘       └─────────┘       └─────────┘
```

### Role Dashboard Summary

| Role | Primary View | Can Drill To | Cannot Access |
|------|-------------|--------------|---------------|
| **Company Admin** | Platform health, all orgs | Everything | N/A |
| **Senior Director** | Portfolio overview | Director dashboards | Individual tickets |
| **Director** | Domain projects | Project/team details | Individual ticket work |
| **Team Lead** | Circle dashboard | Member work, tickets | Other circles |
| **Operator** | Personal dashboard | Own assignments | Other members' work |

---

## 3. Dashboard Structure

### Main Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ QUAD  [Acme Corp ▼]  [Project Alpha ▼]                    [🔔] [👤]  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ [🖥️ IDE] [📊 Projects] [🎫 Tickets] [📈 Reports] [⚙️ Settings]      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │                         TAB CONTENT AREA                            │   │
│  │                                                                     │   │
│  │   (Content varies based on selected tab and user role)              │   │
│  │                                                                     │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐               │
│  │    Widget 1    │  │    Widget 2    │  │    Widget 3    │               │
│  │   My Tickets   │  │ Project Status │  │  Agent Queue   │               │
│  └────────────────┘  └────────────────┘  └────────────────┘               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Tab Definitions

| Tab | Icon | Purpose | Available To |
|-----|------|---------|--------------|
| **IDE** | 🖥️ | Full coding environment with QUAD integration | Developers, Team Leads |
| **Projects** | 📊 | Project overview, status, drill-down | Directors, Team Leads |
| **Tickets** | 🎫 | Ticket list filtered by access level | All roles |
| **Reports** | 📈 | Analytics, metrics, trends | Directors, Admins |
| **Settings** | ⚙️ | Personal preferences, widget config | All roles |

---

## 4. IDE Tab

### QUAD IDE Experience

The IDE tab provides a full coding environment inspired by VS Code + Cursor, but integrated with QUAD.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  IDE Tab                                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────┐ ┌────────────────────────────────────────┐ ┌──────────┐ │
│  │ TICKET PANEL  │ │            CODE EDITOR                  │ │ CHAT     │ │
│  │               │ │                                         │ │ PANEL    │ │
│  │ 🎫 QUAD-123   │ │  // AI: Based on ticket QUAD-123        │ │          │ │
│  │ Status: Prog  │ │  function validateUser(email) {        │ │ Ask QUAD │ │
│  │               │ │    if (!email) {                       │ │          │ │
│  │ Acceptance:   │ │      throw new Error('Required');      │ │ > Help   │ │
│  │ ✓ Email valid │ │    }                                   │ │   me     │ │
│  │ ○ Test passes │ │    return email.includes('@');         │ │          │ │
│  │               │ │  }                                     │ │ AI:      │ │
│  │ Related:      │ │                                         │ │ Based on │ │
│  │ • QUAD-120    │ │                                         │ │ your...  │ │
│  │ • QUAD-115    │ │                                         │ │          │ │
│  │               │ │                                         │ │          │ │
│  └───────────────┘ └────────────────────────────────────────┘ └──────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ QUAD-123 in_progress │ 🤖 Dev Agent Ready │ Claude 3.5 │ 1.2K tokens │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### IDE Components

| Component | Purpose |
|-----------|---------|
| **Ticket Panel** | Current ticket context, acceptance criteria, related tickets |
| **Code Editor** | Monaco editor with AI suggestions |
| **Chat Panel** | QUAD AI assistant for context-aware help |
| **Status Bar** | Current ticket, agent status, model, token usage |

### IDE Features by Role

| Feature | Operator | Team Lead | Director |
|---------|----------|-----------|----------|
| View code | ✓ | ✓ | View only |
| Edit code | ✓ | ✓ | ✗ |
| AI suggestions | ✓ | ✓ | ✗ |
| Ticket context | Own | Circle | All |
| Agent control | Own | Circle | View |

---

## 5. Widget System

### Available Widgets

| Widget | Description | Best For |
|--------|-------------|----------|
| **My Tickets** | Tickets assigned to user by status | All operators |
| **All Projects Status** | Overview cards for all accessible projects | Directors |
| **Team Velocity** | Sprint burndown, points completed | Team Leads |
| **AI Agent Status** | Running agents, queue, costs | Developers |
| **Recent Activity** | Latest updates in user's scope | All |
| **Meeting Action Items** | Pending items from meeting notes | Management |
| **Sprint Calendar** | Current sprint timeline, milestones | Team Leads |
| **Quick Actions** | Common actions (new ticket, start agent) | Developers |

### Widget Layout

```
┌────────────────────────────────────────────────────────────────┐
│  Widget Area (Customizable)                                    │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │ 📋 My Tickets  │  │ 📊 Projects    │  │ 🤖 Agents      │   │
│  ├────────────────┤  ├────────────────┤  ├────────────────┤   │
│  │ In Progress: 3 │  │ Alpha: 85%     │  │ Running: 2     │   │
│  │ Review: 2      │  │ Beta: 40%      │  │ Queue: 5       │   │
│  │ Blocked: 1     │  │ Gamma: 10%     │  │ Cost: $2.30    │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Phase 1 vs Phase 2

| Feature | Phase 1 | Phase 2 |
|---------|---------|---------|
| Widget selection | ✓ | ✓ |
| Widget reordering | Fixed | Drag & drop |
| Widget resizing | Fixed | Resizable |
| Custom widgets | ✗ | Plugin API |
| Shared layouts | ✗ | Team templates |
| Widget settings | Basic | Advanced |

---

## 6. Access Control

### Restriction Philosophy

> **"Restrict drilling depth, not visibility"**

Users can see high-level status of everything in their scope, but cannot drill into details beyond their role.

### Example: Director View

```
Director Dashboard
├── Project Alpha (can drill down)
│   ├── Team Overview (✓ can view)
│   ├── Sprint Status (✓ can view)
│   └── Individual Tickets (✗ blocked - shows summary only)
└── Project Beta (can drill down)
    ├── Team Overview (✓ can view)
    └── Sprint Status (✓ can view)
```

### Drill-Down Limits

| Role | Can See | Drill Limit |
|------|---------|-------------|
| **Senior Director** | All domains | Domain level |
| **Director** | Domain projects | Project/Sprint level |
| **Team Lead** | Circle details | Individual tickets |
| **Operator** | Own work | Full ticket detail |

### Why This Matters

- **Prevents micromanagement** - Directors focus on outcomes, not implementation details
- **Protects team autonomy** - Team leads manage without executives watching every move
- **Encourages delegation** - Forced to trust the hierarchy
- **Reduces noise** - Higher levels see signals, not noise

---

## 7. Implementation Plan

### Phase 1: Foundation (Current)

| Item | Status | Notes |
|------|--------|-------|
| Role-based routing | 🔜 | Redirect based on role |
| Tab structure | 🔜 | Fixed tabs per role |
| IDE tab shell | 🔜 | Basic layout |
| Widget selection | 🔜 | Choose from list |
| Access control | 🔜 | Restrict drill-down |

### Phase 2: Enhancement

| Item | Status | Notes |
|------|--------|-------|
| Full IDE integration | ⏳ | Monaco + AI |
| Drag-drop widgets | ⏳ | Customizable layout |
| Saved layouts | ⏳ | Per-user preferences |
| Widget settings | ⏳ | Configure each widget |

### Phase 3: Advanced

| Item | Status | Notes |
|------|--------|-------|
| Custom widgets | ⏳ | Plugin API |
| Shared templates | ⏳ | Team layouts |
| Dashboard export | ⏳ | PDF reports |
| Real-time updates | ⏳ | WebSocket feeds |

---

## Related Documents

- [SUCCESS_STORY.md](../strategy/SUCCESS_STORY.md) - QUAD IDE vision
- [QUAD_SUBMODULES.md](../architecture/QUAD_SUBMODULES.md) - Architecture for services
- [QUAD_SERVICES_SPEC.md](../architecture/QUAD_SERVICES_SPEC.md) - Services package

---

*This document defines the vision for QUAD's role-based dashboard system.*
