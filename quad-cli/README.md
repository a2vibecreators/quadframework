# QUAD CLI

Command line tools for the QUAD platform (Quick Unified Agentic Development).

## Installation

```bash
# From source (development)
cd QUAD/quad-cli
pip install -e .

# From PyPI (when published)
pip install quad-cli
```

## Commands

### `quad login`

Authenticate with QUAD.

```bash
# Interactive login selection
quad login

# Login with Anthropic account (uses your Claude API quota)
quad login -a

# Login with Enterprise SSO (company pays via QUAD billing)
quad login -e MM
quad login -e MM-WM
```

### `quad init`

Initialize a project from Excel or interactively.

```bash
# Interactive mode
quad init

# From Excel file
quad init @org-setup.xlsx

# Resume saved draft
quad init --resume bank-demo

# List saved drafts
quad init --list-drafts
```

### `quad question`

Ask questions with org context.

```bash
# Basic question
quad question "Who has 20 hours availability?"

# With specific domain
quad question "What projects is Dev One working on?" -d bank-demo

# Raw JSON output
quad question "Team members" --raw
```

### `quad deploy`

Deploy projects to GCP.

```bash
# Deploy to dev
quad deploy dev suma

# Deploy to prod
quad deploy prod suma

# Deploy all projects
quad deploy dev all

# Dry run (show what would be deployed)
quad deploy dev suma --dry-run
```

### `quad status`

Show current configuration status.

```bash
quad status
```

## Configuration

Configuration is stored in `~/.quad/`:

```
~/.quad/
├── config.json         # General settings
├── credentials.json    # Auth tokens (chmod 600)
├── drafts/             # Saved quad-init drafts
└── request-log.jsonl   # Request logging
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `QUAD_API_URL` | QUAD API base URL | `https://api.quadframe.work` |
| `QUAD_API_KEY` | API key (alternative to login) | - |
| `QUAD_DOMAIN` | Default domain/org slug | - |
| `QUAD_LOG_REQUESTS` | Enable request logging | `true` |

## Claude Code Integration

Use the hook script for Claude Code context injection:

```json
// ~/.claude/settings.json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "^quad-",
        "command": "python3 ~/.local/bin/quad-context-hook.py \"$PROMPT\""
      }
    ]
  }
}
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black quad_cli/
ruff check quad_cli/
```

## License

Proprietary - Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
