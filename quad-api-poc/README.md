# QUAD API POC

Local API for QUAD context retrieval. **NO AI calls** - just database lookup.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Claude Code    │────▶│  QUAD API       │────▶│  PostgreSQL     │
│  (quad-* cmds)  │     │  (localhost:3000)│     │  (port 14201)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │
         │                       │ NO AI
         ▼                       ▼
   AI processing          DB lookup only
   (Claude CLI)           (context fetch)
```

## Quick Start

```bash
# 1. Start PostgreSQL (if not running)
docker start postgres-quad-dev

# 2. Create virtual environment & install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Start API
python main.py
# Server runs at http://localhost:3000

# 4. Test
curl http://localhost:3000/health
```

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/context` | POST | Get org context for a question |
| `/domains` | GET | List active domains |

## Usage

### Direct API Call

```bash
curl -X POST http://localhost:3000/context \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer quad_dev_key_abc123" \
  -d '{"question": "Who has availability?"}'
```

### CLI Wrapper

```bash
# Add to PATH
export PATH="$PATH:/path/to/quad-api-poc/bin"

# Use commands
quad help
quad team
quad availability
quad question "Who can take on a 20 hour task?"
```

### Claude Code Hook

Add to `.claude/hooks.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "^quad-",
        "command": "python3 /path/to/quad-context-hook.py \"$PROMPT\""
      }
    ]
  }
}
```

Then use in Claude Code:
```
quad-question Who has availability this week?
quad-team
quad-availability
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | localhost | PostgreSQL host |
| `DB_PORT` | 14201 | PostgreSQL port |
| `DB_NAME` | quad_dev_db | Database name |
| `DB_USER` | quad_user | Database user |
| `DB_PASSWORD` | quad_dev_pass | Database password |
| `QUAD_API_KEY` | quad_dev_key_abc123 | API key |
| `HOST` | 0.0.0.0 | API host |
| `PORT` | 3000 | API port |

### Config File (optional)

Create `~/.quad/config.json`:

```json
{
  "domain_slug": "suma"
}
```

## Context Types

The API analyzes question keywords to return relevant context:

| Keywords | Context Type | Returns |
|----------|--------------|---------|
| available, hours, capacity | availability | Team capacity |
| team, who, members | team | Team roster |
| project, domain | project | Project info |
| (default) | full | All context |

## Files

```
quad-api-poc/
├── main.py                  # FastAPI server
├── quad-context-hook.py     # Claude Code hook
├── requirements.txt         # Dependencies
├── .env                     # Configuration
├── bin/
│   └── quad                 # CLI wrapper
└── claude-hooks-example.json
```

---

*Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.*
