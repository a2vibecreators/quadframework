# QUAD Platform - Authenticated Pages Sitemap

**Purpose:** Visual sitemap of all authenticated pages and dashboard flows in QUAD Platform.

**Last Updated:** January 5, 2026

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication Gates](#authentication-gates)
3. [Dashboard Structure](#dashboard-structure)
4. [User Flows](#user-flows)

---

## Overview

This sitemap covers **authenticated pages** that require user login. These pages are accessible after:
- OAuth sign-in (Google, GitHub, Azure AD, Okta, Auth0)
- Email/OTP sign-in
- Credentials sign-in (deprecated)

**Related:** See [sitemap_static.md](sitemap_static.md) for public marketing pages.

---

## Authentication Gates

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION ENTRY POINTS                   │
└─────────────────────────────────────────────────────────────────┘

/auth/login
├─ OAuth Sign-In (Google, GitHub, etc.)
│  └─ New User → /auth/signup?oauth=true → /dashboard
│  └─ Existing User → /dashboard
│
├─ Email/OTP Sign-In
│  └─ Enter email → Verify OTP → /dashboard
│
└─ Credentials (deprecated)
   └─ Email + password → /dashboard

/auth/signup
├─ OAuth Sign-Up
│  └─ Select org type → Complete profile → /dashboard
│
└─ Email/OTP Sign-Up
   └─ Fill form → Verify OTP → /dashboard
```

---

## Dashboard Structure

### Main Navigation

```
┌─────────────────────────────────────────────────────────────────┐
│                         DASHBOARD HOME                           │
│                        /dashboard                                │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
         ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
         │  Domains    │ │ Requirements│ │   Tickets   │
         │  /domains   │ │/requirements│ │  /tickets   │
         └─────────────┘ └─────────────┘ └─────────────┘
                │               │               │
                └───────────────┼───────────────┘
                                │
                        ┌───────┴────────┐
                        │                │
                        ▼                ▼
                 ┌─────────────┐  ┌─────────────┐
                 │   Account   │  │   Settings  │
                 │  /account   │  │  /settings  │
                 └─────────────┘  └─────────────┘
```

### Domain Management

```
/domains
├─ List all domains
├─ Create new domain
│  └─ /domains/create
│     ├─ Select domain type (project/product)
│     ├─ Enter basic info
│     └─ → /domains/[id]
│
└─ Domain Detail
   └─ /domains/[id]
      ├─ Overview
      ├─ Members
      ├─ Resources
      ├─ Flows (Q-U-A-D)
      ├─ Circles (4 circles)
      └─ Settings
```

### Requirements Management

```
/requirements
├─ List all requirements
├─ Create new requirement
│  └─ /requirements/create
│     ├─ Enter title, description
│     ├─ Link to domain
│     ├─ Set priority
│     └─ → /requirements/[id]
│
└─ Requirement Detail
   └─ /requirements/[id]
      ├─ Description
      ├─ Acceptance criteria
      ├─ Linked tickets
      ├─ Comments
      └─ History
```

### Ticket/Flow Management

```
/tickets
├─ Kanban board view
│  ├─ Q (Question)
│  ├─ U (Understand)
│  ├─ A (Allocate)
│  └─ D (Deliver)
│
├─ Create new ticket
│  └─ /tickets/create
│     ├─ Link to requirement
│     ├─ Assign to circle
│     ├─ Set Q-U-A-D stage
│     └─ → /tickets/[id]
│
└─ Ticket Detail
   └─ /tickets/[id]
      ├─ Description
      ├─ Stage history
      ├─ Assigned circle
      ├─ Time tracking
      ├─ Comments
      └─ Attachments
```

---

## User Flows

### Flow 1: First-Time User Journey

```
1. Login (OAuth or Email)
   └─ /auth/login

2. Complete Profile (if OAuth new user)
   └─ /auth/signup?oauth=true
      ├─ Select org type
      ├─ Enter company name
      └─ Submit

3. Dashboard Welcome
   └─ /dashboard
      ├─ "Welcome!" message
      ├─ Quick start guide
      └─ "Create your first domain" CTA

4. Create First Domain
   └─ /domains/create
      ├─ Enter domain name (e.g., "HealthTrack Mobile App")
      ├─ Select type (project)
      └─ Submit → /domains/[id]

5. Domain Setup
   └─ /domains/[id]
      ├─ Add team members
      ├─ Set up circles
      └─ Create first requirement

6. Daily Workflow
   └─ /dashboard → /tickets → /requirements
```

### Flow 2: Returning User Daily Workflow

```
1. Quick Login
   └─ /auth/login
      └─ OAuth auto-approve OR email/OTP

2. Dashboard Overview
   └─ /dashboard
      ├─ See active domains (3 cards)
      ├─ See recent activity
      └─ Quick actions

3. Domain Work
   └─ /domains/[id]
      ├─ View flows in progress
      ├─ Move tickets through Q-U-A-D
      └─ Track time on tasks

4. Create Requirement
   └─ /requirements/create
      ├─ Document user story
      ├─ Link to domain
      └─ Auto-create ticket

5. Work on Tickets
   └─ /tickets
      ├─ Drag from Q → U → A → D
      ├─ Add comments
      └─ Mark complete
```

### Flow 3: Domain Admin Workflow

```
1. Domain Management
   └─ /domains/[id]
      ├─ Invite team members
      │  └─ /domains/[id]/members
      │     ├─ Enter email
      │     ├─ Assign circle
      │     └─ Set role (DOMAIN_ADMIN, DOMAIN_MEMBER)
      │
      ├─ Manage Resources
      │  └─ /domains/[id]/resources
      │     ├─ Link GitHub repos
      │     ├─ Add database configs
      │     └─ Connect cloud projects
      │
      └─ View Analytics
         └─ /domains/[id]/analytics
            ├─ Flow velocity
            ├─ Time per stage
            └─ Team utilization

2. Circle Management
   └─ /domains/[id]/circles
      ├─ Circle 1: Management
      ├─ Circle 2: Development
      ├─ Circle 3: QA
      └─ Circle 4: Infrastructure
         └─ Assign members to circles
```

---

## Page Hierarchy

```
/ (marketing site - public)
│
├─ /auth/login (public)
├─ /auth/signup (public)
│
└─ /dashboard (authenticated) ★ Main Hub
   │
   ├─ /domains (authenticated)
   │  ├─ /domains/create
   │  └─ /domains/[id]
   │     ├─ /domains/[id]/members
   │     ├─ /domains/[id]/resources
   │     ├─ /domains/[id]/circles
   │     ├─ /domains/[id]/flows
   │     └─ /domains/[id]/analytics
   │
   ├─ /requirements (authenticated)
   │  ├─ /requirements/create
   │  └─ /requirements/[id]
   │     ├─ /requirements/[id]/edit
   │     └─ /requirements/[id]/history
   │
   ├─ /tickets (authenticated)
   │  ├─ /tickets/create
   │  └─ /tickets/[id]
   │     ├─ /tickets/[id]/edit
   │     ├─ /tickets/[id]/comments
   │     └─ /tickets/[id]/time-tracking
   │
   ├─ /account (authenticated)
   │  ├─ /account/profile
   │  ├─ /account/security
   │  └─ /account/notifications
   │
   └─ /settings (authenticated)
      ├─ /settings/organization
      ├─ /settings/billing
      └─ /settings/integrations
```

---

## Access Control

### Public Pages (No Auth Required)
- `/` - Homepage
- `/concept`, `/pitch`, `/demo` - Marketing pages
- `/auth/login` - Login page
- `/auth/signup` - Signup page

### Authenticated Pages (Login Required)
- `/dashboard` - Main dashboard
- `/domains/*` - All domain pages
- `/requirements/*` - All requirement pages
- `/tickets/*` - All ticket pages
- `/account/*` - User account pages
- `/settings/*` - Organization settings

### Role-Based Access
| Page | User | Domain Member | Domain Admin | Org Admin |
|------|------|---------------|--------------|-----------|
| `/dashboard` | ✅ View own domains | ✅ View assigned domains | ✅ View all domains | ✅ All |
| `/domains/[id]` | ❌ No access | ✅ View | ✅ View + Edit | ✅ All |
| `/domains/[id]/members` | ❌ | ❌ | ✅ Manage | ✅ All |
| `/settings/organization` | ❌ | ❌ | ❌ | ✅ Only |

---

## Navigation Components

### Top Navigation (Authenticated)

```
┌────────────────────────────────────────────────────────────┐
│ ◇ QUAD Home │ User Profile ▼ │ Menu ☰                      │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  User Dropdown:                                            │
│  ├─ 📊 Dashboard                                           │
│  ├─ 📋 Requirements                                         │
│  ├─ 🎫 Tickets                                              │
│  ├─ 👤 My Account                                           │
│  └─ 🚪 Sign Out                                             │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### Dashboard Sidebar (Future)

```
┌─────────────────────┐
│ My Domains          │
├─────────────────────┤
│ 📁 HealthTrack      │
│ 📁 E-commerce       │
│ 📁 CRM System       │
├─────────────────────┤
│ + Create Domain     │
└─────────────────────┘
```

---

## Related Documentation

- **[sitemap_static.md](sitemap_static.md)** - Public marketing pages
- **[AUTHENTICATION_FLOWS.md](../auth/AUTHENTICATION_FLOWS.md)** - Login/signup flows
- **[../getting-started/TEAM_ACCESS.md](../getting-started/TEAM_ACCESS.md)** - Team collaboration
- **[../features/](../features/)** - Feature documentation

---

## Future Pages (Planned)

### Phase 2
- `/blueprint-agent` - AI-assisted UI blueprint creation
- `/analytics` - Cross-domain analytics
- `/reports` - Custom reporting
- `/integrations` - Third-party integrations (Jira, Slack, GitHub)

### Phase 3
- `/ai-agents` - Manage AI agents per domain
- `/knowledge-base` - Searchable documentation
- `/templates` - Project templates
- `/marketplace` - Community templates and plugins

---

**Last Updated:** January 5, 2026
**Status:** Phase 1 implemented, Phase 2-3 planned
**Maintainer:** Suman Addanki
