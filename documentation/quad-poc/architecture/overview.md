# QUAD Architecture Overview

## Core Principle

**QUAD API performs NO AI calls** - only database/RAG lookups. Claude CLI handles all AI processing.

## System Components

```
┌──────────────────────────────────────────────────────────────────────┐
│                         USER WORKSTATION                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   ┌─────────────────┐                                                │
│   │  Claude Code    │ ◄─── User types: quad-question "..."           │
│   │  (CLI)          │                                                │
│   └────────┬────────┘                                                │
│            │                                                          │
│            │ Hook intercepts quad-* commands                         │
│            ▼                                                          │
│   ┌─────────────────┐     ┌─────────────────┐                        │
│   │  QUAD Hook      │────▶│  QUAD API       │                        │
│   │  (Python)       │     │  (FastAPI)      │                        │
│   └────────┬────────┘     └────────┬────────┘                        │
│            │                       │                                  │
│            │                       │ Database lookup                  │
│            │                       ▼                                  │
│            │              ┌─────────────────┐                        │
│            │              │  PostgreSQL     │                        │
│            │              │  (Docker)       │                        │
│            │              └─────────────────┘                        │
│            │                                                          │
│            │ Returns: <quad-context>...</quad-context>               │
│            ▼                                                          │
│   ┌─────────────────┐                                                │
│   │  Claude AI      │ ◄─── AI processes context + question          │
│   │  (Anthropic)    │                                                │
│   └─────────────────┘                                                │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. User Query Flow

```
User: "quad-question Who has availability?"
         │
         ▼
    ┌─────────────────────────────────────────┐
    │ 1. Hook intercepts "quad-*" command     │
    │ 2. Calls QUAD API /context endpoint     │
    │ 3. API analyzes question keywords       │
    │ 4. Queries PostgreSQL for context       │
    │ 5. Returns context (NO AI)              │
    │ 6. Hook injects context into prompt     │
    │ 7. Claude CLI processes with AI         │
    └─────────────────────────────────────────┘
         │
         ▼
Claude: "Based on the team data, Ashrith has 16 hours available..."
```

### 2. Deployment Flow

```
User: "quad dev deploy suma"
         │
         ▼
    ┌─────────────────────────────────────────┐
    │ 1. Read config from Excel/DB            │
    │ 2. Fetch secrets from GCP Secret Mgr    │
    │ 3. Build Docker image                   │
    │ 4. Push to GCR                          │
    │ 5. Deploy to Cloud Run                  │
    │ 6. Return service URL                   │
    └─────────────────────────────────────────┘
```

## Components

### QUAD CLI (`bin/quad`)

Shell wrapper that routes commands to appropriate handlers:

| Category | Commands |
|----------|----------|
| **Init** | `template`, `init` |
| **Deploy** | `dev deploy`, `prod deploy`, `setup` |
| **Context** | `question`, `team`, `availability`, `status` |
| **Server** | `serve`, `stop`, `restart`, `logs`, `ps` |
| **Database** | `db connect`, `db status` |
| **Info** | `info`, `version`, `help` |

### QUAD API (`main.py`)

FastAPI server with endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/context` | POST | Get org context (NO AI) |
| `/domains` | GET | List active domains |

### QUAD Hook (`quad-context-hook.py`)

Claude Code hook that:
1. Intercepts `quad-*` commands
2. Calls QUAD API for context
3. Injects context into prompt
4. Passes enhanced prompt to Claude

### Excel Template

Interactive Excel with:
- Dropdowns linked to reference data
- Validation rules (allocation 0-100)
- Auto-calculated fields
- Conditional formatting

## Technology Stack

| Component | Technology |
|-----------|------------|
| CLI | Bash |
| API | Python/FastAPI |
| Database | PostgreSQL |
| Secrets | GCP Secret Manager |
| Deployment | GCP Cloud Run |
| Hook | Python |
| Template | Excel/openpyxl |

## Security Model

### What's Protected

| Item | Location | Security |
|------|----------|----------|
| Public Config | Excel | Plain text |
| GCP Project IDs | Excel | Plain text |
| Git URLs | Excel | Plain text |
| **Secrets** | GCP Secret Manager | **Encrypted** |
| **API Keys** | GCP Secret Manager | **Encrypted** |
| **DB Passwords** | GCP Secret Manager | **Encrypted** |

### Authentication

- **Local Dev:** API Key in `.env` file
- **Production:** GCP Secret Manager + IAM

---

*Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.*
