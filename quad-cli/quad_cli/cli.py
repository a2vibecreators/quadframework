#!/usr/bin/env python3
"""
QUAD CLI - Main Entry Point
============================

Usage:
  quad <command> [options]

Commands:
  init      Initialize a project from Excel or interactively
  login     Authenticate with Anthropic or Enterprise SSO
  question  Ask a question with org context
  deploy    Deploy projects to GCP
  status    Show current configuration status

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import click
from rich import print as rprint

from quad_cli import __version__
from quad_cli.utils import Console


@click.group()
@click.version_option(version=__version__, prog_name="quad")
def main():
    """QUAD CLI - Quick Unified Agentic Development"""
    pass


@main.command()
@click.argument("excel_file", required=False)
@click.option("--resume", "-r", help="Resume from a saved draft")
@click.option("--interactive", "-i", is_flag=True, help="Force interactive mode")
def init(excel_file, resume, interactive):
    """Initialize a project from Excel or interactively.

    Examples:
      quad init                      # Interactive mode
      quad init @org-setup.xlsx      # From Excel file
      quad init --resume bank-demo   # Resume saved draft
    """
    from quad_cli.commands.init import run_init
    run_init(excel_file, resume, interactive)


@main.command()
@click.option("--anthropic", "-a", is_flag=True, help="Login with Anthropic account")
@click.option("--enterprise", "-e", metavar="ORG", help="Login with Enterprise SSO")
def login(anthropic, enterprise):
    """Authenticate with QUAD.

    Examples:
      quad login                  # Interactive login selection
      quad login -a               # Login with Anthropic account
      quad login -e MM            # Login with Enterprise SSO (org code)
    """
    from quad_cli.commands.login import run_login
    run_login(anthropic, enterprise)


@main.command()
@click.argument("question", required=True)
@click.option("--domain", "-d", help="Domain/org slug to query")
@click.option("--raw", is_flag=True, help="Output raw JSON response")
def question(question, domain, raw):
    """Ask a question with org context.

    Examples:
      quad question "Who has 20 hours availability?"
      quad question "What projects is Dev One working on?" -d bank-demo
    """
    from quad_cli.commands.question import run_question
    run_question(question, domain, raw)


@main.command()
@click.argument("environment", type=click.Choice(["dev", "prod"]))
@click.argument("project", required=True)
@click.option("--dry-run", is_flag=True, help="Show what would be deployed")
def deploy(environment, project, dry_run):
    """Deploy projects to GCP.

    Examples:
      quad deploy dev suma        # Deploy SUMA to dev
      quad deploy prod suma       # Deploy SUMA to prod
      quad deploy dev all         # Deploy all to dev
    """
    from quad_cli.commands.deploy import run_deploy
    run_deploy(environment, project, dry_run)


@main.command()
def status():
    """Show current QUAD configuration status."""
    from quad_cli.utils.config import load_config, load_credentials, get_api_url

    Console.header("QUAD Status")

    config = load_config()
    creds = load_credentials()

    # Auth status
    if creds.get("token"):
        auth_type = creds.get("auth_type", "unknown")
        user = creds.get("user", "unknown")
        Console.success(f"Authenticated: {user} ({auth_type})")
    else:
        Console.warn("Not authenticated. Run: quad login")

    # Domain status
    domain = config.get("domain_slug")
    if domain:
        Console.info(f"Domain: {domain}")
    else:
        Console.info("No domain set")

    # API status
    Console.info(f"API URL: {get_api_url()}")

    print()


@main.command()
def hook():
    """Run as Claude Code hook (internal use).

    This command is used by the quad-context-hook.py for Claude Code integration.
    """
    from quad_cli.commands.hook import run_hook
    run_hook()


if __name__ == "__main__":
    main()
