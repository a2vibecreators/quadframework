# QUAD Framework - Test Scenarios: Journey 1 - User Onboarding & Circle Setup

**Author:** Suman Addanke
**Version:** 1.0
**Last Updated:** January 2, 2026

---

## Overview

This document contains end-to-end test scenarios for **Journey 1: User Onboarding & Circle Setup**.

**Features Covered:**
- User Registration & Authentication
- Organization Creation
- Circle Setup
- Role Assignment (18 Core Roles)
- Domain Creation
- AI Tier Selection

**QUAD Terminology:**
- **Circle** = Team
- **Domain** = Project
- **Flow** = Ticket/Task
- **Cycle** = Sprint
- **Stream** = Epic/Milestone

---

## Prerequisites

Before testing, ensure:

- [ ] DEV database is running: `docker ps | grep postgres-dev`
- [ ] Prisma schema is synced: `npx prisma db push`
- [ ] Seed data is loaded: `npx prisma db seed`
- [ ] Web app is running: `npm run dev`
- [ ] App accessible at `http://localhost:3000`

---

## SECTION A: USER REGISTRATION

---

## Scenario 1A: New User Registration

**User Type:** New User
**Features Tested:** Authentication, Auto-Org Creation

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1A.1 | Navigate to `localhost:3000` | See Login/Register page | [ ] |
| 1A.2 | Click "Sign Up" or "Register" | See Registration form | [ ] |
| 1A.3 | Enter email: `newuser@test.com` | Email field accepts input | [ ] |
| 1A.4 | Enter password: `Password123!` | Password field accepts input (masked) | [ ] |
| 1A.5 | Enter name: `Test User` | Name field accepts input | [ ] |
| 1A.6 | Click "Create Account" button | Loading indicator shown | [ ] |
| 1A.7 | Wait for response | Navigate to Onboarding flow | [ ] |
| 1A.8 | Verify auto-created organization | `QUAD_organizations` has new entry | [ ] |
| 1A.9 | Verify user linked to org | `QUAD_org_members` has membership record | [ ] |

### API Endpoints Tested:
- `POST /api/auth/register`

### Expected Database State:
```sql
-- QUAD_users
SELECT * FROM "QUAD_users" WHERE email = 'newuser@test.com';
-- Should have 1 row

-- QUAD_organizations (auto-created)
SELECT * FROM "QUAD_organizations" WHERE created_by = '<user_id>';
-- Should have 1 row with name like "Test User's Organization"

-- QUAD_org_members
SELECT * FROM "QUAD_org_members" WHERE user_id = '<user_id>';
-- Should have 1 row with role 'ADMIN'
```

---

## Scenario 1B: Existing User Login

**User Type:** Registered User
**Features Tested:** Authentication

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1B.1 | Navigate to login page | See Login form | [ ] |
| 1B.2 | Enter email: `newuser@test.com` | Email field accepts input | [ ] |
| 1B.3 | Enter password: `Password123!` | Password field accepts input | [ ] |
| 1B.4 | Click "Sign In" | Loading indicator shown | [ ] |
| 1B.5 | Wait for response | Navigate to Dashboard | [ ] |
| 1B.6 | Verify user session | User name displayed in header | [ ] |

### Negative Tests:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1B.7 | Enter wrong password | Error: "Invalid credentials" | [ ] |
| 1B.8 | Enter non-existent email | Error: "User not found" | [ ] |
| 1B.9 | Submit empty form | Validation errors shown | [ ] |

### API Endpoints Tested:
- `POST /api/auth/login`

---

## SECTION B: ORGANIZATION SETUP

---

## Scenario 2A: View Organization Details

**User Type:** Org Admin
**Features Tested:** Organization Management

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 2A.1 | From Dashboard, click "Organization" | See Organization settings page | [ ] |
| 2A.2 | Verify org name displayed | Shows "Test User's Organization" | [ ] |
| 2A.3 | Verify member count | Shows "1 member" | [ ] |
| 2A.4 | Click "Edit Organization" | See edit form | [ ] |
| 2A.5 | Change name to "ACME Corp" | Name field accepts input | [ ] |
| 2A.6 | Click "Save" | Success message | [ ] |
| 2A.7 | Verify name updated | Shows "ACME Corp" | [ ] |

### API Endpoints Tested:
- `GET /api/organizations/{id}`
- `PATCH /api/organizations/{id}`

---

## Scenario 2B: Invite Member to Organization

**User Type:** Org Admin
**Features Tested:** Member Invitation

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 2B.1 | From Organization page, click "Invite Members" | See invitation form | [ ] |
| 2B.2 | Enter email: `developer@test.com` | Email field accepts input | [ ] |
| 2B.3 | Select role: "Member" | Role dropdown works | [ ] |
| 2B.4 | Click "Send Invitation" | Success: "Invitation sent" | [ ] |
| 2B.5 | Verify pending invitation in list | Shows pending status | [ ] |

### API Endpoints Tested:
- `POST /api/organizations/{id}/invites`
- `GET /api/organizations/{id}/invites`

---

## SECTION C: CIRCLE SETUP

---

## Scenario 3A: Create New Circle

**User Type:** Org Admin
**Features Tested:** Circle Creation

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 3A.1 | From Dashboard, click "Circles" | See Circles list (may be empty) | [ ] |
| 3A.2 | Click "Create Circle" | See Circle creation form | [ ] |
| 3A.3 | Enter name: "Engineering Circle" | Name field accepts input | [ ] |
| 3A.4 | Enter description: "Core dev team" | Description accepts input | [ ] |
| 3A.5 | Click "Create" | Loading indicator | [ ] |
| 3A.6 | Verify Circle created | "Engineering Circle" in list | [ ] |
| 3A.7 | Click on Circle | See Circle details page | [ ] |
| 3A.8 | Verify creator is member | Current user listed as member | [ ] |

### API Endpoints Tested:
- `POST /api/circles`
- `GET /api/circles`
- `GET /api/circles/{id}`

### Expected Database State:
```sql
-- QUAD_circles
SELECT * FROM "QUAD_circles" WHERE name = 'Engineering Circle';
-- Should have 1 row

-- QUAD_circle_members
SELECT * FROM "QUAD_circle_members" WHERE circle_id = '<circle_id>';
-- Should have 1 row (creator as lead)
```

---

## Scenario 3B: Add Member to Circle

**User Type:** Circle Lead
**Features Tested:** Circle Membership

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 3B.1 | From Circle details, click "Add Member" | See member selection | [ ] |
| 3B.2 | See list of org members | Available members displayed | [ ] |
| 3B.3 | Select a member | Member selected | [ ] |
| 3B.4 | Click "Add to Circle" | Success message | [ ] |
| 3B.5 | Verify member in Circle list | New member appears | [ ] |

### API Endpoints Tested:
- `POST /api/circles/{id}/members`
- `GET /api/circles/{id}/members`

---

## SECTION D: ROLE ASSIGNMENT

---

## Scenario 4A: View Core Roles

**User Type:** Any User
**Features Tested:** Core Role System (18 Master Roles)

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 4A.1 | Navigate to Roles section | See Roles page | [ ] |
| 4A.2 | See "Core Roles" tab | 18 master roles displayed | [ ] |
| 4A.3 | Verify ADMIN category roles | SUPER_ADMIN, ORG_ADMIN (2 roles) | [ ] |
| 4A.4 | Verify MANAGEMENT category | CIRCLE_LEAD, PROJECT_MANAGER, SCRUM_MASTER, PRODUCT_OWNER (4 roles) | [ ] |
| 4A.5 | Verify BUSINESS category | BUSINESS_ANALYST, STAKEHOLDER, CUSTOMER_SUCCESS (3 roles) | [ ] |
| 4A.6 | Verify TECHNICAL category | TECH_LEAD, SENIOR_DEVELOPER, DEVELOPER, JUNIOR_DEVELOPER, DEVOPS_ENGINEER (5 roles) | [ ] |
| 4A.7 | Verify QA category | QA_LEAD, QA_ENGINEER, QA_ANALYST, AUTOMATION_ENGINEER (4 roles) | [ ] |
| 4A.8 | Total count = 18 | All 18 core roles visible | [ ] |

### API Endpoints Tested:
- `GET /api/core-roles`

### Expected Core Roles:

| Category | Role Code | Role Name |
|----------|-----------|-----------|
| ADMIN | SUPER_ADMIN | Super Administrator |
| ADMIN | ORG_ADMIN | Organization Administrator |
| MANAGEMENT | CIRCLE_LEAD | Circle Lead |
| MANAGEMENT | PROJECT_MANAGER | Project Manager |
| MANAGEMENT | SCRUM_MASTER | Scrum Master |
| MANAGEMENT | PRODUCT_OWNER | Product Owner |
| BUSINESS | BUSINESS_ANALYST | Business Analyst |
| BUSINESS | STAKEHOLDER | Stakeholder |
| BUSINESS | CUSTOMER_SUCCESS | Customer Success |
| TECHNICAL | TECH_LEAD | Tech Lead |
| TECHNICAL | SENIOR_DEVELOPER | Senior Developer |
| TECHNICAL | DEVELOPER | Developer |
| TECHNICAL | JUNIOR_DEVELOPER | Junior Developer |
| TECHNICAL | DEVOPS_ENGINEER | DevOps Engineer |
| QA | QA_LEAD | QA Lead |
| QA | QA_ENGINEER | QA Engineer |
| QA | QA_ANALYST | QA Analyst |
| QA | AUTOMATION_ENGINEER | Automation Engineer |

---

## Scenario 4B: Assign Role to Circle Member

**User Type:** Circle Lead
**Features Tested:** Role Assignment

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 4B.1 | From Circle details, click on a member | See member details | [ ] |
| 4B.2 | Click "Assign Role" | See role selection | [ ] |
| 4B.3 | See available core roles | 18 roles in dropdown | [ ] |
| 4B.4 | Select "DEVELOPER" | Role selected | [ ] |
| 4B.5 | Click "Assign" | Success message | [ ] |
| 4B.6 | Verify role shows on member | "Developer" badge displayed | [ ] |

### API Endpoints Tested:
- `POST /api/roles`
- `GET /api/circles/{id}/members/{memberId}/roles`

---

## Scenario 4C: Create Custom Role from Core Role

**User Type:** Org Admin
**Features Tested:** Custom Role Creation

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 4C.1 | Navigate to Roles > "Create Custom Role" | See custom role form | [ ] |
| 4C.2 | Select base role: "DEVELOPER" | Core role selected | [ ] |
| 4C.3 | Enter custom name: "Frontend Developer" | Name accepts input | [ ] |
| 4C.4 | Add custom responsibility: "React components" | Text added | [ ] |
| 4C.5 | Click "Create Role" | Success message | [ ] |
| 4C.6 | Verify custom role in list | Shows with "Custom" badge | [ ] |
| 4C.7 | Verify linked to core role | Shows "Based on: Developer" | [ ] |

### API Endpoints Tested:
- `POST /api/roles` (with core_role_id)

---

## SECTION E: DOMAIN CREATION

---

## Scenario 5A: Create New Domain

**User Type:** Circle Lead
**Features Tested:** Domain (Project) Creation

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 5A.1 | From Circle, click "Create Domain" | See Domain creation form | [ ] |
| 5A.2 | Enter name: "Mobile App v2" | Name field accepts input | [ ] |
| 5A.3 | Enter description: "Complete mobile rewrite" | Description accepts input | [ ] |
| 5A.4 | Select domain type: "Development" | Type selected | [ ] |
| 5A.5 | Click "Create Domain" | Loading indicator | [ ] |
| 5A.6 | Verify Domain created | "Mobile App v2" in list | [ ] |
| 5A.7 | Click on Domain | See Domain dashboard | [ ] |
| 5A.8 | Verify Domain Canvas shown | Empty canvas displayed | [ ] |

### API Endpoints Tested:
- `POST /api/domains`
- `GET /api/domains`
- `GET /api/domains/{id}`

---

## Scenario 5B: Soft Delete Domain

**User Type:** Domain Creator / Org Admin
**Features Tested:** Domain Soft Delete

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 5B.1 | From Domain list, click "..." menu | See context menu | [ ] |
| 5B.2 | Click "Delete Domain" | Confirmation dialog | [ ] |
| 5B.3 | Confirm deletion | Success: "Domain deleted" | [ ] |
| 5B.4 | Verify Domain hidden from list | "Mobile App v2" not visible | [ ] |
| 5B.5 | Navigate to "Deleted Domains" | See archived domains | [ ] |
| 5B.6 | Verify soft-deleted domain listed | "Mobile App v2" with delete timestamp | [ ] |

### API Endpoints Tested:
- `DELETE /api/domains/{id}` (soft delete)
- `GET /api/domains?includeDeleted=true`

### Expected Database State:
```sql
-- Domain should NOT be deleted, just flagged
SELECT * FROM "QUAD_domains" WHERE name = 'Mobile App v2';
-- Should have: is_deleted = true, deleted_at = timestamp, deleted_by = user_id
```

---

## Scenario 5C: Restore Deleted Domain

**User Type:** Org Admin
**Features Tested:** Domain Restore

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 5C.1 | From "Deleted Domains", find "Mobile App v2" | See domain entry | [ ] |
| 5C.2 | Click "Restore" button | Confirmation dialog | [ ] |
| 5C.3 | Confirm restoration | Success: "Domain restored" | [ ] |
| 5C.4 | Navigate to active Domains | See restored domain | [ ] |
| 5C.5 | Verify domain is active | "Mobile App v2" visible and accessible | [ ] |

### API Endpoints Tested:
- `PATCH /api/domains/{id}` (restore - set is_deleted = false)

---

## SECTION F: AI TIER SELECTION

---

## Scenario 6A: View AI Tiers

**User Type:** Org Admin
**Features Tested:** AI Tier Display

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 6A.1 | Navigate to Settings > "AI Configuration" | See AI settings | [ ] |
| 6A.2 | See 4 AI Tiers displayed | Turbo, Balanced, Quality, BYOK | [ ] |
| 6A.3 | Verify Turbo tier | Icon: rocket, ~$5/dev, Green color | [ ] |
| 6A.4 | Verify Balanced tier | Icon: lightning, ~$15/dev, Blue color | [ ] |
| 6A.5 | Verify Quality tier | Icon: gem, ~$35/dev, Purple color | [ ] |
| 6A.6 | Verify BYOK tier | Icon: key, "You pay direct", Gray color | [ ] |

### Expected Tier Display:

| Tier | Icon | Cost/Dev | Color | Providers |
|------|------|----------|-------|-----------|
| Turbo | rocket | ~$5 | green | Groq, DeepSeek, Haiku |
| Balanced | lightning | ~$15 | blue | DeepSeek, Haiku, Sonnet |
| Quality | gem | ~$35 | purple | Haiku, Sonnet, Opus |
| BYOK | key | You pay | gray | User-configured |

---

## Scenario 6B: Select AI Tier

**User Type:** Org Admin
**Features Tested:** AI Tier Selection

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 6B.1 | From AI Configuration, current tier shown | Default tier displayed | [ ] |
| 6B.2 | Click on "Balanced" tier card | Card highlighted | [ ] |
| 6B.3 | See provider breakdown | Shows fixed combination (no custom) | [ ] |
| 6B.4 | See extraction provider | DeepSeek shown | [ ] |
| 6B.5 | See coding provider | Claude Haiku/Sonnet shown | [ ] |
| 6B.6 | Click "Select This Tier" | Confirmation dialog | [ ] |
| 6B.7 | Confirm selection | Success: "AI tier updated" | [ ] |
| 6B.8 | Verify tier applied to org | Settings show "Balanced" | [ ] |

### API Endpoints Tested:
- `GET /api/ai/tiers`
- `PUT /api/organizations/{id}/ai-tier`

---

## API Endpoint Coverage Matrix

### Authentication

| Endpoint | Method | Scenario(s) |
|----------|--------|-------------|
| `/api/auth/register` | POST | 1A |
| `/api/auth/login` | POST | 1B |
| `/api/auth/logout` | POST | (future) |

### Organizations

| Endpoint | Method | Scenario(s) |
|----------|--------|-------------|
| `/api/organizations` | POST | 1A (auto) |
| `/api/organizations/{id}` | GET | 2A |
| `/api/organizations/{id}` | PATCH | 2A |
| `/api/organizations/{id}/invites` | POST | 2B |
| `/api/organizations/{id}/invites` | GET | 2B |
| `/api/organizations/{id}/ai-tier` | PUT | 6B |

### Circles

| Endpoint | Method | Scenario(s) |
|----------|--------|-------------|
| `/api/circles` | GET | 3A |
| `/api/circles` | POST | 3A |
| `/api/circles/{id}` | GET | 3A |
| `/api/circles/{id}/members` | GET | 3B |
| `/api/circles/{id}/members` | POST | 3B |

### Roles

| Endpoint | Method | Scenario(s) |
|----------|--------|-------------|
| `/api/core-roles` | GET | 4A |
| `/api/roles` | POST | 4B, 4C |
| `/api/circles/{id}/members/{memberId}/roles` | GET | 4B |

### Domains

| Endpoint | Method | Scenario(s) |
|----------|--------|-------------|
| `/api/domains` | GET | 5A |
| `/api/domains` | POST | 5A |
| `/api/domains/{id}` | GET | 5A |
| `/api/domains/{id}` | DELETE | 5B (soft) |
| `/api/domains/{id}` | PATCH | 5C (restore) |
| `/api/domains?includeDeleted=true` | GET | 5B |

### AI Configuration

| Endpoint | Method | Scenario(s) |
|----------|--------|-------------|
| `/api/ai/tiers` | GET | 6A |

---

## Test Results Summary

| Scenario | Description | Status | Notes |
|----------|-------------|--------|-------|
| 1A | New User Registration | [ ] Pending | |
| 1B | Existing User Login | [ ] Pending | |
| 2A | View Organization Details | [ ] Pending | |
| 2B | Invite Member to Organization | [ ] Pending | |
| 3A | Create New Circle | [ ] Pending | |
| 3B | Add Member to Circle | [ ] Pending | |
| 4A | View Core Roles | [ ] Pending | |
| 4B | Assign Role to Circle Member | [ ] Pending | |
| 4C | Create Custom Role | [ ] Pending | |
| 5A | Create New Domain | [ ] Pending | |
| 5B | Soft Delete Domain | [ ] Pending | |
| 5C | Restore Deleted Domain | [ ] Pending | |
| 6A | View AI Tiers | [ ] Pending | |
| 6B | Select AI Tier | [ ] Pending | |

**Total Scenarios:** 14
**Passed:** ___ / 14
**Failed:** ___ / 14

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 2, 2026 | Initial version - 14 scenarios covering onboarding |

---
