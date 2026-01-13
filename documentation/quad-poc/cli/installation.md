# QUAD CLI Installation Guide

## Prerequisites

- Python 3.10+
- PostgreSQL (Docker recommended)
- GCP CLI (for deployment)

## Quick Install

### 1. Clone Repository

```bash
cd /path/to/a2vibes/QUAD
```

### 2. Setup Virtual Environment

```bash
cd quad-api-poc
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy the example `.env` file:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Database
DB_HOST=localhost
DB_PORT=14201
DB_NAME=quad_dev_db
DB_USER=quad_user
DB_PASSWORD=quad_dev_pass

# API
QUAD_API_KEY=quad_dev_key_abc123
HOST=0.0.0.0
PORT=3000
```

### 5. Add to PATH

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$PATH:/path/to/a2vibes/QUAD/quad-api-poc/bin"
```

Reload shell:

```bash
source ~/.bashrc  # or ~/.zshrc
```

### 6. Verify Installation

```bash
quad version
# Output: QUAD CLI v0.1.0

quad help
```

---

## Database Setup

### Option A: Docker (Recommended)

```bash
# Start PostgreSQL container
docker run -d \
  --name postgres-quad-dev \
  -e POSTGRES_USER=quad_user \
  -e POSTGRES_PASSWORD=quad_dev_pass \
  -e POSTGRES_DB=quad_dev_db \
  -p 14201:5432 \
  postgres:15

# Verify connection
quad db status
```

### Option B: Existing PostgreSQL

Update `.env` with your PostgreSQL credentials:

```env
DB_HOST=your-host
DB_PORT=5432
DB_NAME=your-db
DB_USER=your-user
DB_PASSWORD=your-password
```

---

## First Run

### 1. Start API Server

```bash
quad serve
```

Expected output:
```
Starting QUAD API server...
✓ QUAD API started (PID: 12345)
  URL: http://localhost:3000
  Logs: quad logs
  Stop: quad stop
```

### 2. Check Status

```bash
quad ps
```

### 3. Test Context Query

```bash
quad question "Hello"
```

---

## Claude Code Integration

### Add Hook Configuration

Create/edit `~/.claude/hooks.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "^quad-",
        "command": "python3 /path/to/quad-api-poc/quad-context-hook.py \"$PROMPT\""
      }
    ]
  }
}
```

### Test Integration

In Claude Code, type:

```
quad-question Who is on the team?
```

---

## Troubleshooting

### Command Not Found

```bash
# Verify PATH
echo $PATH | grep quad

# If missing, add to PATH
export PATH="$PATH:/path/to/quad-api-poc/bin"
```

### Port Already in Use

```bash
# Find process using port 3000
lsof -i :3000

# Kill it
kill -9 <PID>

# Or use different port
PORT=3001 quad serve
```

### Database Connection Failed

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Start if stopped
docker start postgres-quad-dev

# Verify connection
quad db status
```

### Python Version Issues

```bash
# Check version
python3 --version

# Should be 3.10+
# If not, install newer Python
brew install python@3.11  # macOS
```

---

## Directory Structure

```
quad-api-poc/
├── bin/
│   └── quad              # CLI wrapper script
├── templates/
│   └── quad-org-template.xlsx  # Sample template
├── venv/                 # Virtual environment
├── main.py               # FastAPI server
├── quad-init.py          # Interactive init
├── quad-deploy.py        # Deployment handler
├── quad-context-hook.py  # Claude Code hook
├── create-template.py    # Excel template generator
├── requirements.txt      # Python dependencies
├── .env                  # Environment config
├── .quad-api.pid         # Server PID file
└── .quad-api.log         # Server logs
```

---

## Uninstall

```bash
# Stop server
quad stop

# Remove from PATH (edit ~/.bashrc or ~/.zshrc)
# Remove the export PATH line

# Remove virtual environment
rm -rf /path/to/quad-api-poc/venv

# Optionally remove database
docker stop postgres-quad-dev
docker rm postgres-quad-dev
```

---

*Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.*
