# QUAD CLI Command Reference

## Overview

```bash
quad <command> [options] [arguments]
```

## Command Categories

### Initialization Commands

#### `quad template [filename]`

Create a new interactive Excel template.

```bash
# Create with default name
quad template

# Create with custom name
quad template my-org.xlsx
```

**Output:** Excel file with:
- Dropdowns for roles, tech stack, regions
- Validation rules
- Auto-calculated fields
- Conditional formatting

---

#### `quad init @<excel-file>`

Initialize project from Excel template interactively.

```bash
quad init @my-org.xlsx
```

**Interactive Flow:**
1. Parses Excel tabs (Overview, Resources, Projects, Deployment)
2. Asks clarifying questions for each project
3. Confirms tech stack and deliverables
4. Generates 2-month plan
5. Saves to database

---

### Deployment Commands

#### `quad dev deploy <project>`

Deploy to development environment.

```bash
quad dev deploy suma
quad dev deploy nutri
quad dev deploy all
```

**Flow:**
1. Reads config from Excel/database
2. Fetches secrets from GCP Secret Manager
3. Builds Docker image
4. Deploys to Cloud Run (dev project)

---

#### `quad prod deploy <project>`

Deploy to production (requires confirmation).

```bash
quad prod deploy suma
```

**Confirmation:**
```
⚠️  PRODUCTION DEPLOYMENT
─────────────────────────
Are you sure you want to deploy to PROD? [y/N]:
```

---

#### `quad setup <gcp-project>`

Interactive setup of GCP secrets.

```bash
quad setup suma-dev
```

**Creates secrets:**
- `DB_PASSWORD`
- `API_KEY`
- `JWT_SECRET`
- `QUAD_API_KEY`

---

### Context Query Commands

> **Note:** These require the API server to be running (`quad serve`)

#### `quad question <text>`

Ask a question with organization context.

```bash
quad question "Who has availability this week?"
quad question "What projects are we working on?"
quad q "Who can help with backend?"  # Short form
```

**Output:**
```xml
<quad-context>
Team Availability (1 members with capacity):
- Ashrith Addanke (DEVELOPER): 16 hrs available (60% allocated)
</quad-context>

Based on the above context, please answer: Who has availability?
```

---

#### `quad team`

Show team members and roles.

```bash
quad team
quad t  # Short form
```

---

#### `quad availability`

Show team availability and capacity.

```bash
quad availability
quad a  # Short form
```

---

#### `quad status`

Show project status.

```bash
quad status
quad s  # Short form
```

---

### Server Commands

#### `quad serve`

Start the QUAD API server in background.

```bash
quad serve
```

**Output:**
```
Starting QUAD API server...
✓ QUAD API started (PID: 12345)
  URL: http://localhost:3000
  Logs: quad logs
  Stop: quad stop
```

---

#### `quad stop`

Stop the running API server.

```bash
quad stop
```

---

#### `quad restart`

Restart the API server.

```bash
quad restart
```

---

#### `quad logs [-f]`

View API server logs.

```bash
quad logs        # Last 50 lines
quad logs -f     # Follow logs (like tail -f)
```

---

#### `quad ps`

Show server status and uptime.

```bash
quad ps
```

**Output:**
```
QUAD Server Status
──────────────────
Status:  Running
PID:     12345
URL:     http://localhost:3000
Uptime:  00:14
```

---

### Database Commands

#### `quad db connect`

Connect to PostgreSQL database shell.

```bash
quad db connect
```

---

#### `quad db status`

Check database connection.

```bash
quad db status
```

**Output:**
```
Checking database connection...
✓ Database connected
```

---

### Info Commands

#### `quad info`

Show configuration details.

```bash
quad info
```

**Output:**
```
QUAD Configuration
──────────────────
Version:    0.1.0
Script Dir: /path/to/quad-api-poc
PID File:   /path/to/.quad-api.pid
Log File:   /path/to/.quad-api.log

Environment:
DB_HOST:    localhost
DB_PORT:    14201
API_PORT:   3000

.env file:  Found
```

---

#### `quad version`

Show version.

```bash
quad version
quad --version
quad -v
```

---

#### `quad help`

Show help.

```bash
quad help
quad --help
quad -h
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | localhost | PostgreSQL host |
| `DB_PORT` | 14201 | PostgreSQL port |
| `DB_NAME` | quad_dev_db | Database name |
| `DB_USER` | quad_user | Database user |
| `DB_PASSWORD` | quad_dev_pass | Database password |
| `QUAD_API_KEY` | quad_dev_key_abc123 | API authentication key |
| `QUAD_API_URL` | http://localhost:3000 | API base URL |
| `QUAD_DOMAIN` | (none) | Default domain slug |
| `PORT` | 3000 | API server port |

---

## Examples

### Full Workflow

```bash
# 1. Create template
quad template acme-setup.xlsx

# 2. Open Excel, fill in:
#    - Organization name, timezone
#    - Team members with roles
#    - Projects with tech stack
#    - Deployment config

# 3. Initialize
quad init @acme-setup.xlsx

# 4. Start server
quad serve

# 5. Query team
quad team
quad availability

# 6. Ask questions
quad question "Who can work on the React frontend?"

# 7. Deploy
quad dev deploy suma

# 8. Check status
quad ps
quad logs

# 9. Stop when done
quad stop
```

---

*Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.*
