# QUAD Installation Guide

Install QUAD CLI and hooks for Claude Code integration.

---

## Quick Install (Recommended)

**One-liner:**
```bash
curl -fsSL https://downloads.quadframe.work/install.sh | bash
```

Or using GitHub directly:
```bash
curl -fsSL https://raw.githubusercontent.com/a2Vibes/QUAD/main/quad-web/public/install.sh | bash
```

This will:
1. Clone QUAD to `~/.quad/quad-cli`
2. Install `quad-cli` via pip
3. Set up Claude Code hooks
4. Create config at `~/.quad/config.json`

---

## Manual Install

### Prerequisites

- Python 3.10+
- pip3
- git

### Steps

```bash
# 1. Clone QUAD
git clone https://github.com/a2Vibes/QUAD.git
cd QUAD/quad-cli

# 2. Install quad-cli
pip3 install -e .

# 3. Verify installation
quad --help
```

### Expected Output

```
Usage: quad [OPTIONS] COMMAND [ARGS]...

  QUAD CLI - Quick Unified Agentic Development

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  deploy    Deploy projects to GCP.
  hook      Run as Claude Code hook (internal use).
  init      Initialize a project from Excel or interactively.
  login     Authenticate with QUAD.
  question  Ask a question with org context.
  status    Show current QUAD configuration status.
```

---

## Post-Install Setup

### 1. Login

```bash
# Interactive login
quad login

# Or with Anthropic account
quad login -a

# Or with Enterprise SSO
quad login -e YOUR_ORG_CODE
```

### 2. Initialize a Project

```bash
# Interactive mode
quad init

# From Excel file
quad init @org-setup.xlsx
```

### 3. Ask Questions

```bash
quad question "Who has 20 hours availability?"
```

---

## Claude Code Hook Setup (Manual)

If the installer didn't set up hooks, add manually:

**~/.claude/settings.json:**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": ".*",
        "command": "python3 ~/.quad/quad-context-hook.py \"$PROMPT\""
      }
    ]
  }
}
```

---

## Configuration

### Files

| File | Purpose |
|------|---------|
| `~/.quad/config.json` | API URL, domain settings |
| `~/.quad/credentials.json` | Auth tokens (chmod 600) |
| `~/.quad/quad-context-hook.py` | Claude Code hook script |

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `QUAD_API_URL` | API endpoint | `https://api.quadframe.work` |
| `QUAD_API_KEY` | API key | - |
| `QUAD_DOMAIN` | Default org/domain | - |

---

## Updating

```bash
# If installed via quick install
cd ~/.quad/quad-cli
git pull origin main
cd quad-cli
pip3 install -e .

# If installed manually
cd /path/to/QUAD/quad-cli
git pull origin main
pip3 install -e .
```

---

## Uninstall

```bash
# Remove quad-cli
pip3 uninstall quad-cli

# Remove QUAD directory
rm -rf ~/.quad

# Remove Claude Code hooks (edit settings.json)
nano ~/.claude/settings.json
```

---

## Troubleshooting

### `quad: command not found`

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then reload:
```bash
source ~/.zshrc  # or ~/.bashrc
```

### Permission denied

```bash
chmod +x ~/.quad/quad-context-hook.py
```

### Python module errors

```bash
cd ~/.quad/quad-cli/quad-cli
pip3 install -e . --force-reinstall
```

---

## Support

- Issues: https://github.com/a2Vibes/QUAD/issues
- Docs: https://quadframe.work/docs

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
