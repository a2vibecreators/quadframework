# QUAD Framework - Test Scenarios: Journey 3 - U-Stage (Development)

**Author:** Suman Addanke
**Version:** 1.0
**Last Updated:** January 2, 2026

---

## Overview

This document contains end-to-end test scenarios for **Journey 3: U-Stage (Development)**.

**Q-U-A-D Stage:** U = Understand (Develop, code, review)

**Features Covered:**
- Cycle Management (Sprints)
- Flow Management (Tickets)
- Time Logging
- Git Repository Linking
- Branch Management
- PR Creation
- Code Review (Code Sentinel)

**Flow Accelerators Tested:**
- **Code Sentinel** - Reviews PRs before merge
- **Velocity Vectors** - Measures delivery speed

---

## Prerequisites

Before testing, ensure:

- [ ] Journey 1 & 2 completed (Domain with Flows exists)
- [ ] GitHub/GitLab account connected (for Git tests)
- [ ] Sample repository available for linking

---

## SECTION A: CYCLE MANAGEMENT

---

## Scenario 1A: Create New Cycle

**User Type:** Circle Lead / Scrum Master
**Features Tested:** Cycle (Sprint) Creation

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1A.1 | Navigate to Domain "Mobile App v2" | Domain dashboard shown | [ ] |
| 1A.2 | Click "Cycles" in sidebar | Cycles view shown | [ ] |
| 1A.3 | Click "Create Cycle" | Cycle creation form | [ ] |
| 1A.4 | Enter name: "Cycle 14" | Name accepts input | [ ] |
| 1A.5 | Select start date: today | Date picker works | [ ] |
| 1A.6 | Select end date: +2 weeks | End date set | [ ] |
| 1A.7 | Set goal: "Complete authentication epic" | Goal accepts input | [ ] |
| 1A.8 | Click "Create Cycle" | Success message | [ ] |
| 1A.9 | Verify Cycle in list | "Cycle 14" visible | [ ] |
| 1A.10 | Click on Cycle | See Cycle dashboard | [ ] |

### API Endpoints Tested:
- `POST /api/cycles`
- `GET /api/domains/{id}/cycles`
- `GET /api/cycles/{id}`

---

## Scenario 1B: Add Flows to Cycle (Sprint Planning)

**User Type:** Circle Lead / Scrum Master
**Features Tested:** Cycle Planning

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1B.1 | From Cycle dashboard, click "Add Flows" | Flow selection modal | [ ] |
| 1B.2 | See backlog Flows | Unassigned Flows listed | [ ] |
| 1B.3 | See effort estimates | S/M/L/XL shown per Flow | [ ] |
| 1B.4 | See total capacity indicator | "0 / 40 points" shown | [ ] |
| 1B.5 | Select Flow "Implement Google OAuth" | Flow highlighted | [ ] |
| 1B.6 | See capacity update | "5 / 40 points" | [ ] |
| 1B.7 | Select 3 more Flows | Total: 4 Flows selected | [ ] |
| 1B.8 | Click "Add to Cycle" | Success message | [ ] |
| 1B.9 | Verify Flows in Cycle | All 4 Flows visible | [ ] |
| 1B.10 | Verify capacity filled | Shows effort committed | [ ] |

### API Endpoints Tested:
- `GET /api/domains/{id}/flows?status=backlog`
- `POST /api/cycles/{id}/flows`
- `GET /api/cycles/{id}/flows`

---

## Scenario 1C: View Cycle Burndown

**User Type:** Any Circle Member
**Features Tested:** Cycle Progress Tracking

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1C.1 | From Cycle dashboard, see "Trajectory Chart" | Chart displayed | [ ] |
| 1C.2 | See ideal burndown line | Diagonal line shown | [ ] |
| 1C.3 | See actual progress line | Current progress shown | [ ] |
| 1C.4 | See days remaining | "10 days left" displayed | [ ] |
| 1C.5 | See Flow status breakdown | To Do, In Progress, Done counts | [ ] |
| 1C.6 | Hover on chart point | Shows detail tooltip | [ ] |

### API Endpoints Tested:
- `GET /api/cycles/{id}/burndown`
- `GET /api/cycles/{id}/metrics`

---

## SECTION B: FLOW MANAGEMENT

---

## Scenario 2A: View Flow Details

**User Type:** Any Circle Member
**Features Tested:** Flow (Ticket) Display

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 2A.1 | From Cycle, click on a Flow | Flow details modal | [ ] |
| 2A.2 | See Flow title | Title displayed | [ ] |
| 2A.3 | See Flow description | Description shown | [ ] |
| 2A.4 | See status | "To Do" / "In Progress" / "Done" | [ ] |
| 2A.5 | See priority | HIGH/MEDIUM/LOW indicator | [ ] |
| 2A.6 | See effort estimate | S/M/L/XL shown | [ ] |
| 2A.7 | See assignee | Member avatar and name | [ ] |
| 2A.8 | See linked requirement | Source requirement visible | [ ] |
| 2A.9 | See AI confidence | Percentage if AI-generated | [ ] |
| 2A.10 | See activity log | History of changes | [ ] |

### API Endpoints Tested:
- `GET /api/flows/{id}`
- `GET /api/flows/{id}/activity`

---

## Scenario 2B: Update Flow Status

**User Type:** Assigned Developer
**Features Tested:** Flow Status Workflow

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 2B.1 | From Flow details, see status dropdown | Current status shown | [ ] |
| 2B.2 | Change status from "To Do" to "In Progress" | Status dropdown opens | [ ] |
| 2B.3 | Select "In Progress" | Status selected | [ ] |
| 2B.4 | Automatic timestamp | "Started at" recorded | [ ] |
| 2B.5 | Verify status updated | Shows "In Progress" | [ ] |
| 2B.6 | Change to "In Review" | Status changes | [ ] |
| 2B.7 | Change to "Done" | Status changes | [ ] |
| 2B.8 | Automatic completion time | "Completed at" recorded | [ ] |
| 2B.9 | Flow removed from "In Progress" lane | Moves to "Done" lane | [ ] |

### Status Flow:
```
TO_DO → IN_PROGRESS → IN_REVIEW → DONE
                   ↓
                 BLOCKED
```

### API Endpoints Tested:
- `PATCH /api/flows/{id}/status`

---

## Scenario 2C: Assign Flow to Member

**User Type:** Circle Lead / Scrum Master
**Features Tested:** Flow Assignment

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 2C.1 | From Flow details, click "Assign" | Member selection | [ ] |
| 2C.2 | See Circle members list | All members shown | [ ] |
| 2C.3 | See member current workload | "3 Flows assigned" shown | [ ] |
| 2C.4 | Select a member | Member highlighted | [ ] |
| 2C.5 | Click "Assign" | Success message | [ ] |
| 2C.6 | Verify assignee updated | Avatar shown on Flow | [ ] |
| 2C.7 | Notification sent to assignee | (Check notifications) | [ ] |

### API Endpoints Tested:
- `GET /api/circles/{id}/members`
- `PATCH /api/flows/{id}/assignee`

---

## SECTION C: TIME LOGGING

---

## Scenario 3A: Log Time Manually

**User Type:** Assigned Developer
**Features Tested:** Manual Time Logging

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 3A.1 | From Flow details, click "Log Time" | Time logging form | [ ] |
| 3A.2 | Enter hours: 2.5 | Hours field accepts input | [ ] |
| 3A.3 | Enter description: "Implemented OAuth flow" | Description accepts input | [ ] |
| 3A.4 | Select date: today | Date picker works | [ ] |
| 3A.5 | Click "Log" | Success message | [ ] |
| 3A.6 | See time logged in Flow | "2.5h logged" shown | [ ] |
| 3A.7 | See time log entry | Entry visible in history | [ ] |

### API Endpoints Tested:
- `POST /api/flows/{id}/time-logs`
- `GET /api/flows/{id}/time-logs`

---

## Scenario 3B: Start/Stop Timer (Auto-Track)

**User Type:** Assigned Developer
**Features Tested:** Automatic Time Tracking

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 3B.1 | From Flow details, click "Start Timer" | Timer starts | [ ] |
| 3B.2 | See running timer | "00:00:00" counting up | [ ] |
| 3B.3 | Continue working... | Timer continues | [ ] |
| 3B.4 | Click "Stop Timer" | Timer stops | [ ] |
| 3B.5 | See elapsed time | "01:23:45" shown | [ ] |
| 3B.6 | Prompt to add description | Description field shown | [ ] |
| 3B.7 | Enter description | Description saved | [ ] |
| 3B.8 | Time automatically logged | Entry created | [ ] |

### API Endpoints Tested:
- `POST /api/work-sessions/start`
- `POST /api/work-sessions/stop`
- `GET /api/flows/{id}/work-sessions`

---

## SECTION D: GIT INTEGRATION

---

## Scenario 4A: Link Repository to Domain

**User Type:** Tech Lead / DevOps
**Features Tested:** Repository Linking

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 4A.1 | From Domain settings, click "Repositories" | Repository settings | [ ] |
| 4A.2 | Click "Link Repository" | Link form shown | [ ] |
| 4A.3 | Select provider: GitHub | Provider selected | [ ] |
| 4A.4 | Authenticate with GitHub | OAuth flow completes | [ ] |
| 4A.5 | See list of repositories | User's repos shown | [ ] |
| 4A.6 | Select "mobile-app-v2" repo | Repo selected | [ ] |
| 4A.7 | Click "Link" | Success message | [ ] |
| 4A.8 | Verify repo in list | Repository visible | [ ] |
| 4A.9 | See branch list | Main branch shown | [ ] |

### API Endpoints Tested:
- `POST /api/git/repositories`
- `GET /api/domains/{id}/repositories`
- `GET /api/git/repositories/{id}/branches`

---

## Scenario 4B: Create Feature Branch

**User Type:** Developer
**Features Tested:** Branch Creation

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 4B.1 | From Flow details, click "Create Branch" | Branch creation modal | [ ] |
| 4B.2 | See suggested branch name | `feature/FLOW-123-google-oauth` | [ ] |
| 4B.3 | Select base branch: main | Dropdown works | [ ] |
| 4B.4 | Click "Create Branch" | Loading indicator | [ ] |
| 4B.5 | Branch created on GitHub | Success message | [ ] |
| 4B.6 | Branch linked to Flow | Branch name shown on Flow | [ ] |

### API Endpoints Tested:
- `POST /api/git/branches`
- `PATCH /api/flows/{id}/branch`

---

## Scenario 4C: Create Pull Request

**User Type:** Developer
**Features Tested:** PR Creation

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 4C.1 | From Flow details, click "Create PR" | PR creation modal | [ ] |
| 4C.2 | See auto-generated title | Flow title used | [ ] |
| 4C.3 | See auto-generated description | Flow description used | [ ] |
| 4C.4 | See linked Flow reference | "Closes FLOW-123" | [ ] |
| 4C.5 | Select target branch: main | Dropdown works | [ ] |
| 4C.6 | Click "Create PR" | Loading indicator | [ ] |
| 4C.7 | PR created on GitHub | Success message | [ ] |
| 4C.8 | PR linked to Flow | PR URL shown on Flow | [ ] |
| 4C.9 | Flow status → In Review | Auto-status change | [ ] |

### API Endpoints Tested:
- `POST /api/git/pull-requests`
- `PATCH /api/flows/{id}/pull-request`

---

## SECTION E: CODE REVIEW

---

## Scenario 5A: AI Code Review (Code Sentinel)

**User Type:** Any Circle Member
**Features Tested:** Code Sentinel Flow Accelerator

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 5A.1 | From PR details, click "Request AI Review" | AI review modal | [ ] |
| 5A.2 | AI analyzes PR | Loading: "Code Sentinel analyzing..." | [ ] |
| 5A.3 | See review summary | Overview shown | [ ] |
| 5A.4 | See issues found | Issue list displayed | [ ] |
| 5A.5 | Each issue has severity | CRITICAL/HIGH/MEDIUM/LOW | [ ] |
| 5A.6 | Each issue has file/line | Location shown | [ ] |
| 5A.7 | Each issue has suggestion | Fix recommendation | [ ] |
| 5A.8 | See overall score | "Code Quality: 85%" | [ ] |
| 5A.9 | See "Approve" / "Request Changes" recommendation | AI recommendation shown | [ ] |

### API Endpoints Tested:
- `POST /api/ai/review-code`
- `GET /api/pull-requests/{id}/reviews`

### Code Sentinel Output:
```json
{
  "prId": "<pr_id>",
  "overallScore": 85,
  "recommendation": "APPROVE_WITH_COMMENTS",
  "issues": [
    {
      "severity": "MEDIUM",
      "file": "src/auth/oauth.ts",
      "line": 42,
      "message": "Consider adding error handling for network failures",
      "suggestion": "Wrap OAuth call in try-catch with retry logic"
    }
  ],
  "summary": "PR implements OAuth correctly. Minor improvements suggested.",
  "securityIssues": [],
  "performanceIssues": []
}
```

---

## Scenario 5B: Manual Code Review

**User Type:** Senior Developer / Tech Lead
**Features Tested:** Human Code Review

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 5B.1 | From PR details, click "Add Review" | Review form shown | [ ] |
| 5B.2 | See diff viewer | Code changes displayed | [ ] |
| 5B.3 | Click on line to comment | Comment form opens | [ ] |
| 5B.4 | Enter comment | Comment saved | [ ] |
| 5B.5 | Add overall review comment | Comment saved | [ ] |
| 5B.6 | Select verdict: Approve / Request Changes | Selection works | [ ] |
| 5B.7 | Submit review | Success message | [ ] |
| 5B.8 | Review visible on PR | Comments shown | [ ] |

### API Endpoints Tested:
- `POST /api/pull-requests/{id}/reviews`
- `GET /api/pull-requests/{id}/reviews`

---

## Scenario 5C: Merge PR and Complete Flow

**User Type:** Tech Lead / Reviewer
**Features Tested:** PR Merge + Flow Completion

### Steps:

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 5C.1 | From PR details, see approval status | "1 approval" shown | [ ] |
| 5C.2 | Click "Merge PR" | Merge confirmation | [ ] |
| 5C.3 | Select merge strategy | Squash/Merge/Rebase options | [ ] |
| 5C.4 | Click "Confirm Merge" | Loading indicator | [ ] |
| 5C.5 | PR merged on GitHub | Success message | [ ] |
| 5C.6 | Flow status → Done | Auto-status change | [ ] |
| 5C.7 | Branch auto-deleted | If configured | [ ] |
| 5C.8 | Notification to Flow creator | Notification sent | [ ] |

### API Endpoints Tested:
- `POST /api/git/pull-requests/{id}/merge`
- `PATCH /api/flows/{id}/status`

---

## API Endpoint Coverage Matrix

### Cycles

| Endpoint | Method | Scenario(s) |
|----------|--------|-------------|
| `/api/cycles` | POST | 1A |
| `/api/cycles/{id}` | GET | 1A, 1C |
| `/api/cycles/{id}/flows` | POST | 1B |
| `/api/cycles/{id}/flows` | GET | 1B |
| `/api/cycles/{id}/burndown` | GET | 1C |
| `/api/cycles/{id}/metrics` | GET | 1C |
| `/api/domains/{id}/cycles` | GET | 1A |

### Flows

| Endpoint | Method | Scenario(s) |
|----------|--------|-------------|
| `/api/flows/{id}` | GET | 2A |
| `/api/flows/{id}/status` | PATCH | 2B |
| `/api/flows/{id}/assignee` | PATCH | 2C |
| `/api/flows/{id}/activity` | GET | 2A |
| `/api/flows/{id}/branch` | PATCH | 4B |
| `/api/flows/{id}/pull-request` | PATCH | 4C |
| `/api/flows/{id}/time-logs` | GET, POST | 3A |
| `/api/flows/{id}/work-sessions` | GET | 3B |
| `/api/domains/{id}/flows` | GET | 1B |

### Time Tracking

| Endpoint | Method | Scenario(s) |
|----------|--------|-------------|
| `/api/work-sessions/start` | POST | 3B |
| `/api/work-sessions/stop` | POST | 3B |

### Git

| Endpoint | Method | Scenario(s) |
|----------|--------|-------------|
| `/api/git/repositories` | POST | 4A |
| `/api/git/repositories/{id}/branches` | GET | 4A |
| `/api/git/branches` | POST | 4B |
| `/api/git/pull-requests` | POST | 4C |
| `/api/git/pull-requests/{id}/merge` | POST | 5C |
| `/api/git/pull-requests/{id}/reviews` | GET, POST | 5A, 5B |
| `/api/domains/{id}/repositories` | GET | 4A |

### AI

| Endpoint | Method | Scenario(s) |
|----------|--------|-------------|
| `/api/ai/review-code` | POST | 5A |

---

## Test Results Summary

| Scenario | Description | Status | Notes |
|----------|-------------|--------|-------|
| 1A | Create New Cycle | [ ] Pending | |
| 1B | Add Flows to Cycle | [ ] Pending | |
| 1C | View Cycle Burndown | [ ] Pending | |
| 2A | View Flow Details | [ ] Pending | |
| 2B | Update Flow Status | [ ] Pending | |
| 2C | Assign Flow to Member | [ ] Pending | |
| 3A | Log Time Manually | [ ] Pending | |
| 3B | Start/Stop Timer | [ ] Pending | |
| 4A | Link Repository to Domain | [ ] Pending | |
| 4B | Create Feature Branch | [ ] Pending | |
| 4C | Create Pull Request | [ ] Pending | |
| 5A | AI Code Review | [ ] Pending | |
| 5B | Manual Code Review | [ ] Pending | |
| 5C | Merge PR and Complete Flow | [ ] Pending | |

**Total Scenarios:** 14
**Passed:** ___ / 14
**Failed:** ___ / 14

---

## Implementation Status (Gap Analysis)

| Feature | Table | API | UI | Status |
|---------|-------|-----|----|----|
| Cycle Management | QUAD_cycles | Yes | Yes | 90% |
| Flow Management | QUAD_flows | Yes | Yes | 85% |
| Time Logging | QUAD_ticket_time_logs | Yes | Yes | 80% |
| Repository Linking | QUAD_git_repositories | Partial | Partial | 40% |
| Branch Management | Fields exist | No | No | 5% |
| PR Creation | QUAD_pull_requests | No | No | 5% |
| AI Code Review | QUAD_ai_code_reviews | No | No | 0% |

**Overall U-Stage: ~37% Complete**

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 2, 2026 | Initial version - 14 scenarios |

---
