# QUAD Setup Guide

Set up QUAD hooks for Claude Code to build applications using the QUAD methodology.

## Quick Install (One-liner)

```bash
curl -fsSL https://raw.githubusercontent.com/a2vibes/quad/main/setup/install.sh | bash
```

## Manual Setup

### 1. Download the hook script

```bash
mkdir -p ~/.quad
curl -fsSL https://raw.githubusercontent.com/a2vibes/quad/main/quad-context-hook.py -o ~/.quad/quad-context-hook.py
chmod +x ~/.quad/quad-context-hook.py
```

### 2. Configure Claude Code

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": ".*",
        "command": "python3 ~/.quad/quad-context-hook.py \"$PROMPT\""
      }
    ],
    "AssistantResponse": [
      {
        "matcher": ".*",
        "command": "python3 ~/.quad/quad-context-hook.py \"$RESPONSE\" --post"
      }
    ]
  }
}
```

### 3. Set API Key

Option A - Environment variable:
```bash
export QUAD_API_URL="https://api.quadframe.work"
export QUAD_API_KEY="your-api-key"
```

Option B - Config file (`~/.quad/config.json`):
```json
{
  "api_url": "https://api.quadframe.work",
  "api_key": "your-api-key",
  "domain_slug": "your-org"
}
```

## Usage

Open Claude Code in any directory and use QUAD commands:

```
quad-init MyProject       # Initialize new project
quad-plan                 # Generate feature plan (PGCE)
quad-story                # Create user stories
quad-ticket               # Create development tickets
quad-write                # Generate code
quad-cleanup [project]    # Summarize session
quad-help                 # Show all commands
quad-stats                # Show token usage
```

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  QUAD HOOK FLOW                                             │
└─────────────────────────────────────────────────────────────┘

YOU: "quad-init MyProject"
       │
       ▼
PRE-HOOK:
  1. Detects "quad-" command
  2. Calls api.quadframe.work for context
  3. Enriches prompt with org/methodology context
       │
       ▼
CLAUDE: Processes enriched prompt, creates project
       │
       ▼
POST-HOOK: Logs response for token tracking
```

## Files Created

| File | Purpose |
|------|---------|
| `~/.quad/quad-context-hook.py` | Hook script |
| `~/.quad/config.json` | API configuration |
| `~/.quad/request-log.jsonl` | Token tracking |
| `.quad/project.json` | Project config (per project) |
| `.quad/session-summary.md` | Session context (per project) |

## Token Tracking

Run `quad-stats` to see:
- Total requests
- QUAD vs non-QUAD breakdown
- Context tokens added
- Response sizes

## Support

- Website: [quadframe.work](https://quadframe.work)
- API Docs: [api.quadframe.work/docs](https://api.quadframe.work/docs)
- Email: support@quadframe.work

---

Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.
