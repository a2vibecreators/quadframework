#!/usr/bin/env python3
"""
QUAD Question Command
=====================

Ask questions with org context from QUAD API.

Usage:
  quad question "Who has 20 hours availability?"
  quad question "What projects is Dev One working on?" -d bank-demo

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import sys
import os
import json
import urllib.request
import urllib.error
from typing import Optional

from quad_cli.utils.console import Console
from quad_cli.utils.config import (
    get_api_url,
    get_api_key,
    get_domain_slug,
    load_credentials,
)


def get_context(question: str, domain_slug: str = None) -> dict:
    """Fetch context from QUAD API.

    Args:
        question: The question to ask
        domain_slug: Optional domain/org slug

    Returns:
        dict with context data or error
    """
    api_url = get_api_url()
    api_key = get_api_key()

    if not domain_slug:
        domain_slug = get_domain_slug()

    # Build request
    url = f"{api_url}/context"
    payload = {
        "question": question,
    }
    if domain_slug:
        payload["domain_slug"] = domain_slug

    headers = {
        "Content-Type": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    # Check for token-based auth
    creds = load_credentials()
    if creds.get("token"):
        headers["X-QUAD-Token"] = creds["token"]

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return {"success": True, **result}

    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else str(e)
        try:
            error_data = json.loads(error_body)
            error_msg = error_data.get("error", error_body)
        except Exception:
            error_msg = error_body
        return {"success": False, "error": f"API error {e.code}: {error_msg}"}

    except urllib.error.URLError as e:
        return {"success": False, "error": f"Connection error: {e.reason}"}

    except Exception as e:
        return {"success": False, "error": str(e)}


def format_context_response(result: dict) -> str:
    """Format the context response for display.

    Args:
        result: API response dict

    Returns:
        Formatted string for display
    """
    if not result.get("success"):
        return f"Error: {result.get('error', 'Unknown error')}"

    output = []

    # Summary
    if result.get("summary"):
        output.append(result["summary"])

    # Context type
    context_type = result.get("context_type", "general")
    if context_type != "general":
        output.append(f"\n[Context: {context_type}]")

    # Raw data (if detailed)
    if result.get("data"):
        data = result["data"]
        if isinstance(data, list) and len(data) > 0:
            output.append("\nDetails:")
            for item in data[:10]:  # Limit to 10 items
                if isinstance(item, dict):
                    name = item.get("name", item.get("title", "Unknown"))
                    details = item.get("role", item.get("status", ""))
                    output.append(f"  • {name}: {details}")
                else:
                    output.append(f"  • {item}")
            if len(data) > 10:
                output.append(f"  ... and {len(data) - 10} more")

    return "\n".join(output)


def run_question(question: str, domain: str = None, raw: bool = False):
    """Entry point for CLI integration.

    Args:
        question: The question to ask
        domain: Optional domain/org slug
        raw: If True, output raw JSON
    """
    Console.header("QUAD Question")
    Console.info(f"Question: {question}")
    if domain:
        Console.info(f"Domain: {domain}")
    print()

    result = get_context(question, domain)

    if raw:
        print(json.dumps(result, indent=2))
    else:
        if result.get("success"):
            Console.success("Context retrieved")
            print()
            print(format_context_response(result))
        else:
            Console.error(result.get("error", "Unknown error"))
            Console.info("Make sure you're logged in: quad login")
            Console.info("Or set QUAD_API_URL for local development")


def main():
    """Command-line entry point"""
    if len(sys.argv) < 2:
        Console.error("Question required")
        print("Usage: quad-question \"Your question here\"")
        sys.exit(1)

    question = sys.argv[1]

    # Parse options
    domain = None
    raw = False

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg in ("-d", "--domain") and i + 1 < len(sys.argv):
            domain = sys.argv[i + 1]
            i += 2
        elif arg == "--raw":
            raw = True
            i += 1
        else:
            i += 1

    run_question(question, domain, raw)


if __name__ == "__main__":
    main()
