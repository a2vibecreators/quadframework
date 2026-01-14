#!/usr/bin/env python3
"""
QUAD Login Command
==================

Authenticate with QUAD via Anthropic or Enterprise SSO.

Usage:
  quad login                  # Interactive selection
  quad login -a               # Anthropic account
  quad login -e MM            # Enterprise SSO (org code)

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import sys
import os
import json
import webbrowser
from datetime import datetime, timedelta
from typing import Optional

from quad_cli.utils.console import Console
from quad_cli.utils.config import (
    save_credentials,
    load_credentials,
    get_api_url,
    get_config_dir,
)


def show_login_menu():
    """Show login method selection menu"""
    Console.header("QUAD Authentication")

    print("  [1] Anthropic Account")
    print("      • Individual developers")
    print("      • Use your Claude API quota")
    print()
    print("  [2] Enterprise SSO")
    print("      • Corporate teams (MM, MM-WM, etc.)")
    print("      • Company pays via QUAD billing")
    print("      • SSO: Okta, Azure AD, Google")
    print()

    choice = Console.ask("Select", "1")
    return choice


def login_anthropic():
    """Login with Anthropic account"""
    Console.header("Anthropic Login")

    # For now, just collect API key
    # TODO: Implement OAuth flow with Anthropic
    Console.info("Enter your Anthropic API key")
    Console.info("Get one at: https://console.anthropic.com/settings/keys")
    print()

    api_key = Console.ask("API Key")
    if not api_key:
        Console.error("API key required")
        return False

    # Validate the key (basic check)
    if not api_key.startswith("sk-ant-"):
        Console.warn("Key doesn't look like an Anthropic key (should start with sk-ant-)")
        if not Console.confirm("Continue anyway?", default=False):
            return False

    # Save credentials
    credentials = {
        "auth_type": "anthropic",
        "api_key": api_key,
        "created_at": datetime.now().isoformat(),
    }
    save_credentials(credentials)

    Console.success("Logged in with Anthropic account")
    Console.info(f"Credentials saved to {get_config_dir() / 'credentials.json'}")
    return True


def login_enterprise(org_code: str):
    """Login with Enterprise SSO"""
    Console.header(f"Enterprise Login: {org_code}")

    # Lookup org configuration from API
    import urllib.request
    import urllib.error

    api_url = get_api_url()
    lookup_url = f"{api_url}/auth/org/{org_code}"

    Console.info(f"Looking up organization: {org_code}")

    try:
        req = urllib.request.Request(lookup_url)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            Console.error(f"Organization not found: {org_code}")
            Console.info("Contact your admin to register your organization")
        else:
            Console.error(f"API error: {e.code}")
        return False
    except Exception as e:
        Console.error(f"Failed to connect to QUAD API: {e}")
        Console.info("Using offline mode...")
        # For demo, allow offline enterprise login
        data = {
            "org_code": org_code,
            "sso_provider": "demo",
            "auth_url": None
        }

    org_name = data.get("org_name", org_code)
    sso_provider = data.get("sso_provider", "unknown")
    auth_url = data.get("auth_url")

    Console.info(f"Organization: {org_name}")
    Console.info(f"SSO Provider: {sso_provider}")

    if auth_url:
        Console.info("Opening browser for SSO login...")
        webbrowser.open(auth_url)
        Console.info("Complete login in browser, then return here")

        # Wait for callback or manual token entry
        token = Console.ask("Enter token from browser (or press Enter to skip)")
    else:
        # Demo mode - generate a mock token
        Console.info("Demo mode - generating temporary token")
        token = f"quad_demo_{org_code}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    if not token:
        Console.warn("Login cancelled")
        return False

    # Save credentials
    credentials = {
        "auth_type": "enterprise",
        "org_code": org_code,
        "org_name": org_name,
        "sso_provider": sso_provider,
        "token": token,
        "created_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(hours=8)).isoformat(),
    }
    save_credentials(credentials)

    Console.success(f"Logged in to {org_name}")
    Console.info(f"Token expires: {credentials['expires_at']}")
    return True


def run_login(anthropic: bool = False, enterprise: str = None):
    """Entry point for CLI integration.

    Args:
        anthropic: If True, login with Anthropic account
        enterprise: Org code for Enterprise SSO login
    """
    if enterprise:
        login_enterprise(enterprise)
    elif anthropic:
        login_anthropic()
    else:
        # Interactive menu
        choice = show_login_menu()
        if choice == "1":
            login_anthropic()
        elif choice == "2":
            org_code = Console.ask("Organization code (e.g., MM, MM-WM)")
            if org_code:
                login_enterprise(org_code)
            else:
                Console.error("Organization code required")
        else:
            Console.error("Invalid selection")


def main():
    """Command-line entry point"""
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ("-a", "--anthropic"):
            run_login(anthropic=True)
        elif arg in ("-e", "--enterprise"):
            if len(sys.argv) > 2:
                run_login(enterprise=sys.argv[2])
            else:
                Console.error("Organization code required: quad-login -e ORG")
        elif arg in ("-h", "--help"):
            print(__doc__)
        else:
            # Assume it's an org code
            run_login(enterprise=arg)
    else:
        run_login()


if __name__ == "__main__":
    main()
