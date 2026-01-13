# QUAD Excel Template Guide

## Overview

The QUAD Excel template provides an interactive way to configure your organization, team, projects, and deployment settings.

## Creating a Template

```bash
quad template my-org.xlsx
```

## Template Structure

```
my-org.xlsx
├── Tab 1: Overview          # Organization details
├── Tab 2: Resources         # Team members
├── Tab 3: Project 1         # First project config
├── Tab 4: Project 2         # Second project config
├── Tab 5: Deployment        # Deployment targets
└── Tab 6: _Lookups (hidden) # Reference data
```

---

## Tab 1: Overview

Organization-level configuration.

| Field | Description | Example | Validation |
|-------|-------------|---------|------------|
| Organization Name | Company/team name | Acme Corp | Required |
| Organization Code | Short code (3-6 chars) | ACME | Required |
| Timezone | Team timezone | America/New_York | Dropdown |
| Industry | Business sector | Technology | Dropdown |
| Contact Email | Primary contact | admin@acme.com | Email format |

**Dropdowns:**
- Timezone: America/New_York, America/Chicago, UTC, Europe/London, etc.
- Industry: Technology, Healthcare, Finance, Retail, etc.

---

## Tab 2: Resources (Team)

Team member configuration.

| Column | Description | Validation |
|--------|-------------|------------|
| Name | Full name | Required |
| Email | Email address | Email format |
| Role | Job role | Dropdown |
| Skills | Comma-separated skills | Free text |
| Allocation % | % allocated to projects | 0-100, error if >100 |
| Available Hrs | Auto-calculated | Formula: `40*(100-E)/100` |
| Notes | Additional notes | Free text |

**Role Dropdown:**
- DIRECTOR
- MANAGER
- TECH_LEAD
- SENIOR_DEVELOPER
- DEVELOPER
- JUNIOR_DEVELOPER
- QA_ENGINEER
- DESIGNER
- DEVOPS
- PRODUCT_MANAGER
- SCRUM_MASTER

**Visual Indicators:**
- 🟨 Yellow cells = Editable
- ⬜ Gray cells = Auto-calculated (Available Hrs)
- 🟥 Red highlight = Error (Allocation > 100%)

---

## Tab 3 & 4: Projects

Project configuration.

### Basic Information

| Field | Description | Validation |
|-------|-------------|------------|
| Project Name | Project title | Required |
| Description | Brief description | Free text |
| Project Type | Type of project | Dropdown |
| Start Date | Project start | Date format |
| Deadline | Project deadline | Date format |
| Project Owner | Owner from team | Dropdown (linked to Resources) |

**Project Type Dropdown:**
- Web Application
- Mobile App
- API/Backend
- Desktop App
- Library/Package
- Microservice

### Tech Stack

| Field | Dropdown Options |
|-------|-----------------|
| Frontend | React.js, Next.js, Vue.js, Angular, Swift, Kotlin, Flutter, None |
| Backend | Node.js, Python/FastAPI, Java/Spring Boot, Go, .NET Core, Ruby, None |
| Database | PostgreSQL, MySQL, MongoDB, SQLite, Redis, DynamoDB, None |

### Deliverables

Yes/No selection for each:
- Web Application
- API Server
- Mobile App
- JAR File
- Docker Image
- Documentation

### Team Assignment

| Column | Description | Validation |
|--------|-------------|------------|
| Team Member | From Resources | Dropdown (linked) |
| Role on Project | Project-specific role | Free text |
| Allocation % | % on this project | 0-100 |
| Start Date | Assignment start | Date |
| End Date | Assignment end | Date |

---

## Tab 5: Deployment

Deployment target configuration.

| Column | Description | Validation |
|--------|-------------|------------|
| Project | Project name | Required |
| Environment | dev/staging/prod | Dropdown |
| GCP Project ID | GCP project | Required |
| Region | GCP region | Dropdown |
| Git Repo | Repository URL | URL format |
| Service Name | Cloud Run service name | Required |

**Environment Dropdown:**
- dev
- staging
- prod

**Region Dropdown:**
- us-central1
- us-east1
- us-west1
- europe-west1
- asia-east1
- asia-southeast1

---

## Cell Color Legend

| Color | Meaning |
|-------|---------|
| 🟨 Light Yellow | Editable - fill this in |
| ⬜ Light Gray | Calculated/locked - don't edit |
| 🟥 Light Red | Error - needs attention |
| 🟩 Light Green | Valid/success |

---

## Using the Template

### Step 1: Create Template

```bash
quad template acme-setup.xlsx
```

### Step 2: Fill in Excel

1. Open in Excel/Numbers
2. Fill yellow cells on each tab
3. Use dropdowns where available
4. Check for red error highlights
5. Save file

### Step 3: Initialize

```bash
quad init @acme-setup.xlsx
```

The CLI will:
1. Parse all tabs
2. Ask clarifying questions
3. Show confirmation prompts
4. Generate project plan
5. Save to database

---

## Validation Rules

| Field | Rule | Error Message |
|-------|------|---------------|
| Allocation % | 0-100 | "Allocation must be between 0 and 100" |
| Email | Valid format | "Please enter valid email" |
| Date | YYYY-MM-DD | "Please enter valid date" |
| Required fields | Not empty | "This field is required" |

---

## Tips

1. **Linked Dropdowns:** Project Owner pulls from Resources tab
2. **Auto-Calculate:** Available Hours updates when you change Allocation
3. **Conditional Formatting:** Red highlight shows errors immediately
4. **Hidden Sheet:** _Lookups contains reference data (don't edit)

---

*Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.*
