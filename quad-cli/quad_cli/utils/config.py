"""
Configuration utilities for QUAD CLI
====================================

Manages ~/.quad/ configuration directory and files.
"""

import json
import os
from pathlib import Path
from typing import Any, Optional


def get_config_dir() -> Path:
    """Get the QUAD config directory (~/.quad/)"""
    config_dir = Path.home() / ".quad"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_config_file() -> Path:
    """Get the main config file path"""
    return get_config_dir() / "config.json"


def get_credentials_file() -> Path:
    """Get the credentials file path"""
    return get_config_dir() / "credentials.json"


def get_drafts_dir() -> Path:
    """Get the drafts directory for quad-init"""
    drafts_dir = get_config_dir() / "drafts"
    drafts_dir.mkdir(parents=True, exist_ok=True)
    return drafts_dir


def load_config() -> dict:
    """Load config from ~/.quad/config.json"""
    config_file = get_config_file()
    if config_file.exists():
        try:
            with open(config_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def save_config(config: dict) -> None:
    """Save config to ~/.quad/config.json"""
    config_file = get_config_file()
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)


def get_config_value(key: str, default: Any = None) -> Any:
    """Get a specific config value"""
    config = load_config()
    return config.get(key, default)


def set_config_value(key: str, value: Any) -> None:
    """Set a specific config value"""
    config = load_config()
    config[key] = value
    save_config(config)


def load_credentials() -> dict:
    """Load credentials from ~/.quad/credentials.json"""
    creds_file = get_credentials_file()
    if creds_file.exists():
        try:
            with open(creds_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def save_credentials(credentials: dict) -> None:
    """Save credentials to ~/.quad/credentials.json"""
    creds_file = get_credentials_file()
    # Set restrictive permissions
    with open(creds_file, "w") as f:
        json.dump(credentials, f, indent=2)
    os.chmod(creds_file, 0o600)


def get_api_url() -> str:
    """Get the QUAD API URL from config or environment"""
    return os.getenv("QUAD_API_URL") or get_config_value("api_url", "https://api.quadframe.work")


def get_api_key() -> Optional[str]:
    """Get the QUAD API key from credentials or environment"""
    env_key = os.getenv("QUAD_API_KEY")
    if env_key:
        return env_key
    creds = load_credentials()
    return creds.get("api_key")


def get_domain_slug() -> Optional[str]:
    """Get the current domain/org slug"""
    return os.getenv("QUAD_DOMAIN") or get_config_value("domain_slug")
