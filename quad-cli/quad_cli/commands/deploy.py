#!/usr/bin/env python3
"""
QUAD Deployment Commands
========================

Deploy projects to GCP Cloud Run with secrets from GCP Secret Manager.

Usage:
  quad-deploy dev suma      # Deploy SUMA to dev
  quad-deploy prod suma     # Deploy SUMA to prod
  quad-deploy dev all       # Deploy all projects to dev

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass

# ─────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────

@dataclass
class ProjectConfig:
    """Project deployment configuration"""
    name: str
    slug: str
    git_repo: str
    service_name: str
    gcp_project_dev: str
    gcp_project_prod: str
    region: str = "us-central1"
    secrets: List[str] = None  # Secret names to inject

    def __post_init__(self):
        if self.secrets is None:
            self.secrets = ["DB_PASSWORD", "API_KEY"]


# Default project configs (can be loaded from Excel later)
PROJECTS = {
    "suma": ProjectConfig(
        name="SUMA Platform",
        slug="suma",
        git_repo="github.com/a2vibes/quad-suma-api",
        service_name="suma-api",
        gcp_project_dev="suma-dev",
        gcp_project_prod="suma-prod",
        secrets=["DB_PASSWORD", "QUAD_API_KEY", "JWT_SECRET"]
    ),
    "nutri": ProjectConfig(
        name="NutriNine",
        slug="nutri",
        git_repo="github.com/a2vibes/nutrinne-api",
        service_name="nutrinne-api",
        gcp_project_dev="nutrinne-dev",
        gcp_project_prod="nutrinne-prod",
        secrets=["DB_PASSWORD", "API_KEY"]
    ),
}


# ─────────────────────────────────────────────────────────────
# Console Helpers
# ─────────────────────────────────────────────────────────────

class Console:
    @staticmethod
    def header(text: str):
        print(f"\n  {text}")
        print(f"  {'─' * len(text)}\n")

    @staticmethod
    def step(num: int, text: str):
        print(f"  {num}. {text}")

    @staticmethod
    def success(text: str):
        print(f"     ✓ {text}")

    @staticmethod
    def error(text: str):
        print(f"     ✗ {text}")

    @staticmethod
    def info(text: str):
        print(f"     → {text}")

    @staticmethod
    def warn(text: str):
        print(f"     ⚠ {text}")


# ─────────────────────────────────────────────────────────────
# GCP Secret Manager
# ─────────────────────────────────────────────────────────────

class SecretManager:
    """Interface to GCP Secret Manager"""

    def __init__(self, project_id: str):
        self.project_id = project_id

    def get_secret(self, secret_name: str, version: str = "latest") -> Optional[str]:
        """Fetch secret from GCP Secret Manager"""
        try:
            result = subprocess.run(
                [
                    "gcloud", "secrets", "versions", "access", version,
                    "--secret", secret_name,
                    "--project", self.project_id
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                Console.error(f"Failed to get secret {secret_name}: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            Console.error(f"Timeout getting secret {secret_name}")
            return None
        except FileNotFoundError:
            Console.error("gcloud CLI not found. Install: https://cloud.google.com/sdk/docs/install")
            return None

    def secret_exists(self, secret_name: str) -> bool:
        """Check if secret exists"""
        result = subprocess.run(
            [
                "gcloud", "secrets", "describe", secret_name,
                "--project", self.project_id
            ],
            capture_output=True,
            timeout=30
        )
        return result.returncode == 0

    def create_secret(self, secret_name: str, value: str) -> bool:
        """Create a new secret"""
        # Create the secret
        result = subprocess.run(
            [
                "gcloud", "secrets", "create", secret_name,
                "--project", self.project_id,
                "--replication-policy", "automatic"
            ],
            capture_output=True,
            timeout=30
        )

        if result.returncode != 0 and "already exists" not in result.stderr:
            Console.error(f"Failed to create secret: {result.stderr}")
            return False

        # Add version with value
        process = subprocess.Popen(
            [
                "gcloud", "secrets", "versions", "add", secret_name,
                "--project", self.project_id,
                "--data-file", "-"
            ],
            stdin=subprocess.PIPE,
            capture_output=True,
            text=True
        )
        stdout, stderr = process.communicate(input=value, timeout=30)

        return process.returncode == 0


# ─────────────────────────────────────────────────────────────
# Deployer
# ─────────────────────────────────────────────────────────────

class Deployer:
    """Deploy projects to GCP Cloud Run"""

    def __init__(self, env: str, project_slug: str):
        self.env = env.lower()
        self.project_slug = project_slug.lower()

        if self.project_slug not in PROJECTS and self.project_slug != "all":
            raise ValueError(f"Unknown project: {project_slug}. Available: {list(PROJECTS.keys())}")

        if self.env not in ("dev", "prod"):
            raise ValueError(f"Invalid environment: {env}. Use 'dev' or 'prod'")

    def deploy(self):
        """Run deployment"""
        if self.project_slug == "all":
            for slug in PROJECTS:
                self._deploy_project(PROJECTS[slug])
        else:
            self._deploy_project(PROJECTS[self.project_slug])

    def _deploy_project(self, config: ProjectConfig):
        """Deploy a single project"""
        gcp_project = config.gcp_project_dev if self.env == "dev" else config.gcp_project_prod

        Console.header(f"QUAD Deployment: {config.name} → {self.env.upper()}")

        # Step 1: Read config
        Console.step(1, "Reading configuration...")
        Console.success(f"GCP Project: {gcp_project}")
        Console.success(f"Region: {config.region}")
        Console.success(f"Git: {config.git_repo}")
        Console.success(f"Service: {config.service_name}")

        # Step 2: Verify GCP auth
        Console.step(2, "Verifying GCP authentication...")
        if not self._check_gcp_auth(gcp_project):
            Console.error("Not authenticated. Run: gcloud auth login")
            return False

        Console.success("Authenticated")

        # Step 3: Fetch secrets
        Console.step(3, "Fetching secrets from GCP Secret Manager...")
        secrets = self._fetch_secrets(gcp_project, config.secrets)
        if secrets is None:
            Console.warn("Some secrets missing - deployment may fail")
        else:
            for name in config.secrets:
                Console.success(f"{name} loaded")

        # Step 4: Build
        Console.step(4, "Building Docker image...")
        image_url = self._build_image(config, gcp_project)
        if not image_url:
            Console.error("Build failed")
            return False
        Console.success(f"Image: {image_url}")

        # Step 5: Deploy to Cloud Run
        Console.step(5, "Deploying to Cloud Run...")
        url = self._deploy_cloud_run(config, gcp_project, image_url, secrets)
        if url:
            Console.success(f"Deployed!")
            print(f"\n  URL: {url}\n")
            return True
        else:
            Console.error("Deployment failed")
            return False

    def _check_gcp_auth(self, project_id: str) -> bool:
        """Check if authenticated to GCP"""
        result = subprocess.run(
            ["gcloud", "auth", "print-access-token"],
            capture_output=True,
            timeout=30
        )
        return result.returncode == 0

    def _fetch_secrets(self, project_id: str, secret_names: List[str]) -> Optional[Dict[str, str]]:
        """Fetch all required secrets"""
        sm = SecretManager(project_id)
        secrets = {}
        all_found = True

        for name in secret_names:
            value = sm.get_secret(name)
            if value:
                secrets[name] = value
            else:
                Console.warn(f"Secret not found: {name}")
                all_found = False

        return secrets if all_found else None

    def _build_image(self, config: ProjectConfig, project_id: str) -> Optional[str]:
        """Build and push Docker image"""
        image_url = f"gcr.io/{project_id}/{config.service_name}:latest"

        # For POC, just return the image URL (actual build would use docker/cloud build)
        Console.info(f"Would build: {image_url}")
        Console.info("(Skipping actual build in POC mode)")

        return image_url

    def _deploy_cloud_run(self, config: ProjectConfig, project_id: str,
                          image_url: str, secrets: Dict[str, str] = None) -> Optional[str]:
        """Deploy to Cloud Run"""
        # Build secret env vars for Cloud Run
        secret_args = []
        if secrets:
            for name in secrets:
                # Cloud Run secret syntax: --set-secrets=ENV_VAR=SECRET_NAME:latest
                secret_args.extend([
                    "--set-secrets", f"{name}={name}:latest"
                ])

        # For POC, simulate the deployment
        Console.info(f"Would run: gcloud run deploy {config.service_name}")
        Console.info(f"  --image {image_url}")
        Console.info(f"  --project {project_id}")
        Console.info(f"  --region {config.region}")
        if secret_args:
            Console.info(f"  --set-secrets {', '.join(secrets.keys())}")
        Console.info("(Skipping actual deploy in POC mode)")

        # Return simulated URL
        return f"https://{config.service_name}-xxx.{config.region}.run.app"


# ─────────────────────────────────────────────────────────────
# Secret Setup Command
# ─────────────────────────────────────────────────────────────

def setup_secrets(project_id: str):
    """Interactive secret setup"""
    Console.header(f"Setting up secrets for {project_id}")

    sm = SecretManager(project_id)

    secrets_to_create = [
        ("DB_PASSWORD", "Database password"),
        ("API_KEY", "API authentication key"),
        ("JWT_SECRET", "JWT signing secret"),
        ("QUAD_API_KEY", "QUAD API key"),
    ]

    for secret_name, description in secrets_to_create:
        if sm.secret_exists(secret_name):
            Console.success(f"{secret_name} exists")
        else:
            Console.info(f"{secret_name} not found")
            value = input(f"     Enter {description}: ").strip()
            if value:
                if sm.create_secret(secret_name, value):
                    Console.success(f"Created {secret_name}")
                else:
                    Console.error(f"Failed to create {secret_name}")


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────

def print_usage():
    print("""
QUAD Deployment Commands
────────────────────────

Usage:
  quad-deploy <env> <project>     Deploy a project
  quad-deploy setup <gcp-project> Setup secrets

Commands:
  quad-deploy dev suma            Deploy SUMA to dev
  quad-deploy prod suma           Deploy SUMA to prod
  quad-deploy dev nutri           Deploy NutriNine to dev
  quad-deploy prod nutri          Deploy NutriNine to prod
  quad-deploy dev all             Deploy all to dev
  quad-deploy setup suma-dev      Setup secrets for suma-dev

Environments:
  dev   Development (suma-dev, nutrinne-dev)
  prod  Production (suma-prod, nutrinne-prod)

Projects:
  suma   SUMA Platform
  nutri  NutriNine
  all    All projects
""")


def main():
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    command = sys.argv[1].lower()
    target = sys.argv[2]

    if command == "setup":
        # Setup secrets for a GCP project
        setup_secrets(target)

    elif command in ("dev", "prod"):
        # Deploy
        env = command
        project = target

        try:
            deployer = Deployer(env, project)
            deployer.deploy()
        except ValueError as e:
            Console.error(str(e))
            sys.exit(1)

    else:
        print_usage()
        sys.exit(1)


def run_deploy(environment: str, project: str, dry_run: bool = False):
    """Entry point for CLI integration.

    Args:
        environment: 'dev' or 'prod'
        project: Project slug (suma, nutri, all)
        dry_run: If True, show what would be deployed without deploying
    """
    try:
        deployer = Deployer(environment, project)
        if dry_run:
            Console.header(f"Dry Run: {project} → {environment}")
            Console.info(f"Would deploy {project} to {environment}")
            Console.info(f"GCP Project: {deployer.config.gcp_project_dev if environment == 'dev' else deployer.config.gcp_project_prod}")
            return
        deployer.deploy()
    except ValueError as e:
        Console.error(str(e))


if __name__ == "__main__":
    main()
