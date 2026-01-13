#!/usr/bin/env python3
"""
QUAD Context Hook for Claude Code
==================================

Intercepts quad-* commands and injects org context from the QUAD API.

Usage:
  Add to Claude Code hooks config:

  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "^quad-",
        "command": "python3 /path/to/quad-context-hook.py \"$PROMPT\""
      }
    ]
  }

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import sys
import os
import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# Configuration
LOG_REQUESTS = os.getenv("QUAD_LOG_REQUESTS", "true").lower() == "true"
REQUEST_LOG_FILE = Path.home() / ".quad" / "request-log.jsonl"
API_URL = os.getenv("QUAD_API_URL", "http://localhost:3000")
API_KEY = os.getenv("QUAD_API_KEY", "quad_dev_key_abc123")
DOMAIN_SLUG = os.getenv("QUAD_DOMAIN", None)


def estimate_tokens(text: str) -> int:
    """Rough token estimate (4 chars = 1 token on average)"""
    return len(text) // 4


def log_request(user_prompt: str, enhanced_prompt: str, command: str = None, phase: str = "pre", is_quad: bool = False):
    """Log request to ~/.quad/request-log.jsonl for tracking"""
    if not LOG_REQUESTS:
        return

    REQUEST_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    if phase == "pre":
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "phase": "pre",
            "is_quad": is_quad,
            "command": command or "unknown",
            "user_prompt": {
                "text": user_prompt[:200] + "..." if len(user_prompt) > 200 else user_prompt,
                "chars": len(user_prompt),
                "tokens_est": estimate_tokens(user_prompt)
            },
            "enhanced_prompt": {
                "chars": len(enhanced_prompt),
                "tokens_est": estimate_tokens(enhanced_prompt)
            },
            "context_added": {
                "chars": len(enhanced_prompt) - len(user_prompt),
                "tokens_est": estimate_tokens(enhanced_prompt) - estimate_tokens(user_prompt)
            }
        }
    else:  # post
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "phase": "post",
            "command": command or "response",
            "response": {
                "chars": len(enhanced_prompt),
                "tokens_est": estimate_tokens(enhanced_prompt)
            }
        }

    with open(REQUEST_LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def load_config():
    """Load config from ~/.quad/config.json if exists"""
    config_path = Path.home() / ".quad" / "config.json"
    if config_path.exists():
        try:
            with open(config_path) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def get_context(question: str, domain_slug: str = None) -> dict:
    """Call QUAD API to get context for the question"""
    url = f"{API_URL}/context"

    payload = {
        "question": question
    }
    if domain_slug:
        payload["domain_slug"] = domain_slug

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"API error: {e.code}"}
    except urllib.error.URLError as e:
        return {"success": False, "error": f"Connection error: {e.reason}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def process_command(prompt: str) -> str:
    """
    Process a quad-* command and return enhanced prompt.

    Commands:
      quad-question <question>  - Ask with org context
      quad-team                 - Show team info
      quad-status               - Show project status
      quad-availability         - Show availability
    """
    parts = prompt.strip().split(maxsplit=1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    # Load config
    config = load_config()
    domain = DOMAIN_SLUG or config.get("domain_slug")

    # Handle different commands
    if command == "quad-question":
        if not args:
            return "Error: Please provide a question. Usage: quad-question <your question>"
        result = get_context(args, domain)

    elif command == "quad-team":
        result = get_context("Who is on the team?", domain)

    elif command == "quad-status":
        result = get_context("What is the project status?", domain)

    elif command == "quad-availability":
        result = get_context("Who has availability?", domain)

    elif command == "quad-help":
        return """QUAD Commands:
  quad-question <question>  - Ask a question with org context
  quad-team                 - Show team members and roles
  quad-status               - Show project status
  quad-availability         - Show team availability

Configuration:
  Set QUAD_API_URL, QUAD_API_KEY, QUAD_DOMAIN env vars
  Or create ~/.quad/config.json with domain_slug"""

    else:
        # Unknown quad command, pass through with general context
        result = get_context(prompt, domain)

    # Return enhanced prompt or error
    if result.get("success"):
        return result.get("prompt_addition", prompt)
    else:
        error = result.get("error", "Unknown error")
        # On error, return original prompt with warning
        return f"[QUAD API unavailable: {error}]\n\n{prompt}"


def main():
    if len(sys.argv) < 2:
        print("Usage: quad-context-hook.py <prompt> [--post]", file=sys.stderr)
        sys.exit(1)

    # Check for post-hook mode (called after response)
    is_post = "--post" in sys.argv
    prompt = sys.argv[1]

    if is_post:
        # Post-hook: log the response
        response_text = prompt  # In post-hook, this is the response
        log_request("", response_text, "response", phase="post")
        # Don't print anything in post-hook (passthrough)
        return

    # Pre-hook: Check if this is a quad-* command
    is_quad = prompt.strip().lower().startswith(("quad-", "quad "))

    if is_quad:
        command = prompt.strip().split()[0].lower()
        if command == "quad":
            command = "quad-" + prompt.strip().split()[1].lower() if len(prompt.strip().split()) > 1 else "quad"
        enhanced = process_command(prompt)

        # Log QUAD request with context
        log_request(prompt, enhanced, command, phase="pre", is_quad=True)
        print(enhanced)
    else:
        # Non-QUAD request - log but don't enrich
        log_request(prompt, prompt, "general", phase="pre", is_quad=False)
        print(prompt)


if __name__ == "__main__":
    main()
