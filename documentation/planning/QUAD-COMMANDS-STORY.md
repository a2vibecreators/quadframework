# QUAD Commands - Full Developer Story

**Version:** 1.0
**Created:** January 14, 2026

---

## Installation (Friend's Machine)

```bash
# One command to install everything
curl -fsSL https://downloads.quadframe.work/install.sh | bash

# This does:
# 1. Clone quad-cli to ~/.quad/quad-cli/
# 2. pip3 install -e . (installs quad command)
# 3. Add to PATH
# 4. Configure Claude Code hook

# After install, friend can use:
quad --help
```

---

## Developer Journey

### Day 1: First Time Setup

```bash
# Step 1: Login (Google SSO → QUAD Web)
$ quad login
→ Opens browser: https://quadframe.work/auth/google
→ User logs in with Google
→ Redirects back with token
→ Saves to ~/.quad/config.json

# Result:
~/.quad/
├── config.json          # User + Org info
│   {
│     "user_email": "pradeep@company.com",
│     "user_name": "Pradeep Kumar",
│     "org_code": "ACME",
│     "org_name": "Acme Corp",
│     "token": "eyJ...",
│     "api_url": "https://api.quadframe.work"
│   }
└── quad-cli/            # CLI installation
```

### Day 2: Create New Project

```bash
# Step 2: Initialize project
$ cd ~/projects
$ quad init my-banking-app

→ Creates: ~/projects/my-banking-app/
→ Creates: ~/projects/my-banking-app/.quad/config.json
→ Creates: ~/projects/my-banking-app/documentation/*/README.md
→ Saves to database: quad_domains

# Result:
my-banking-app/
├── README.md
├── CLAUDE.md
├── .quad/
│   └── config.json      # Project config
│       {
│         "domain_slug": "my-banking-app",
│         "org_code": "ACME",
│         "project_type": "fullstack",
│         "created_at": "2026-01-14"
│       }
└── documentation/
    ├── architecture/README.md
    ├── database/README.md
    ├── api/README.md
    ├── web/README.md
    ├── mobile/README.md
    ├── deployment/README.md
    ├── security/README.md
    ├── testing/README.md
    └── misc/README.md
```

### Day 3: Start Working on Ticket

```bash
# Step 3: Pick up a ticket
$ quad ticket start ACME-123

→ Fetches ticket from database
→ Creates branch: feature/ACME-123-add-login
→ Adds ticket to .quad/tickets.json (max 3)

# Result:
.quad/
├── config.json
└── tickets.json         # Active tickets
    {
      "active": [
        {
          "id": "ACME-123",
          "title": "Add login page",
          "branch": "feature/ACME-123-add-login",
          "started_at": "2026-01-14T10:00:00"
        }
      ],
      "max_tickets": 3
    }
```

### Day 4: Switch Tickets

```bash
# Working on multiple tickets
$ quad ticket start ACME-456
→ Adds ACME-456 to active list
→ Switches branch

$ quad ticket start ACME-789
→ Adds ACME-789 to active list
→ Now have 3 tickets (max)

$ quad ticket start ACME-999
→ WARNING: Max 3 tickets reached
→ Removes oldest (ACME-123) from .quad/tickets.json
→ Adds ACME-999
→ ACME-123 data stays in database

# View active tickets
$ quad ticket list
  ACME-456 - Fix payment bug (2 days)
  ACME-789 - Add dashboard (1 day)
  ACME-999 - Update API (just started)
```

### Day 5: Complete Ticket

```bash
# Finish a ticket
$ quad ticket done ACME-456

→ Updates database: ticket status = done
→ Removes from .quad/tickets.json
→ Optionally: creates PR

# Or just switch branch
$ git checkout main
$ quad ticket sync
→ Detects branch change
→ Updates active ticket context
```

---

## All Commands

### Authentication

| Command | Description |
|---------|-------------|
| `quad login` | Login via Google SSO (opens browser) |
| `quad logout` | Clear local credentials |
| `quad whoami` | Show current user + org |

### Project Management

| Command | Description |
|---------|-------------|
| `quad init <name>` | Create new project with docs structure |
| `quad status` | Show project + ticket status |
| `quad sync` | Sync local .quad with database |

### Ticket Management

| Command | Description |
|---------|-------------|
| `quad ticket list` | List active tickets (max 3) |
| `quad ticket start <id>` | Start working on ticket |
| `quad ticket done <id>` | Mark ticket complete |
| `quad ticket sync` | Sync tickets with current branch |

### Documentation

| Command | Description |
|---------|-------------|
| `quad doc generate` | Generate docs from code |
| `quad doc validate` | Validate docs structure |
| `quad doc status` | Show docs coverage |

### Analytics / Questions

| Command | Description |
|---------|-------------|
| `quad question "<query>"` | Ask with org context |
| `quad burnout` | Show team burnout analysis |
| `quad workload` | Show workload distribution |
| `quad chart tickets` | Pie chart of ticket status |
| `quad chart velocity` | Sprint velocity chart |
| `quad notifications` | List notifications |

### Deployment

| Command | Description |
|---------|-------------|
| `quad deploy dev` | Deploy to dev environment |
| `quad deploy qa` | Deploy to QA |
| `quad deploy prod` | Deploy to production |

---

## Data Storage

### Global (~/.quad/) - User/Org Level

```json
// ~/.quad/config.json
{
  "user_email": "pradeep@company.com",
  "user_name": "Pradeep Kumar",
  "user_id": "uuid-123",
  "org_code": "ACME",
  "org_name": "Acme Corp",
  "org_id": "uuid-456",
  "token": "eyJ...",
  "api_url": "https://api.quadframe.work",
  "logged_in_at": "2026-01-14T09:00:00"
}
```

### Project (<project>/.quad/) - Project Level

```json
// <project>/.quad/config.json
{
  "domain_slug": "my-banking-app",
  "domain_id": "uuid-789",
  "org_code": "ACME",
  "project_name": "My Banking App",
  "project_type": "fullstack",
  "created_at": "2026-01-14T10:00:00",
  "created_by": "pradeep@company.com"
}

// <project>/.quad/tickets.json
{
  "active": [
    {
      "id": "ACME-123",
      "title": "Add login page",
      "branch": "feature/ACME-123-add-login",
      "started_at": "2026-01-14T10:00:00",
      "time_spent_minutes": 120
    }
  ],
  "max_tickets": 3
}
```

### Database - Everything Else

| Table | Data |
|-------|------|
| `quad_organizations` | Org details |
| `quad_users` | User accounts |
| `quad_user_sessions` | Auth tokens |
| `quad_domains` | Projects |
| `quad_tickets` | All tickets |
| `quad_ticket_time_logs` | Time tracking |
| `quad_workload_metrics` | Burnout data |
| `quad_notifications` | Notifications |

---

## Authentication Flow

```
┌─────────────────┐
│  quad login     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Open Browser    │
│ quadframe.work  │
│ /auth/google    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Google SSO      │
│ (Gmail login)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Redirect back   │
│ with token      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Save to         │
│ ~/.quad/config  │
└─────────────────┘
```

---

## Install on Friend's Machine

```bash
# Friend runs this ONE command:
curl -fsSL https://downloads.quadframe.work/install.sh | bash

# Then:
quad login                    # Login with Google
quad init my-project          # Create project
quad ticket start PROJ-001    # Start working
quad question "how to add auth?"  # Ask with context
quad burnout                  # Check team health
quad deploy dev               # Deploy
```

---

## Priority for POC Demo

| Priority | Command | Status |
|----------|---------|--------|
| 1 | `quad login` | Build (Google SSO) |
| 2 | `quad init` | Fix (create project folder) |
| 3 | `quad ticket start/list/done` | Build |
| 4 | `quad status` | Done |
| 5 | `quad question` | Done |
| 6 | `quad burnout` | Build |
| 7 | `quad chart` | Build |
| 8 | `quad notifications` | Build |

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
