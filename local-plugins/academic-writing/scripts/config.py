#!/usr/bin/env python3
"""
Configuration helper for academic-writing plugin.
"""

import argparse
import json
import sys
from pathlib import Path


CONFIG_DIR = Path.home() / ".config" / "auto-writing"
CONFIG_PATH = CONFIG_DIR / "config.json"


def load_config() -> dict:
    """Load existing configuration."""
    if not CONFIG_PATH.exists():
        return {}

    try:
        with open(CONFIG_PATH) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}
    except Exception:
        return {}


def save_config(config: dict) -> bool:
    """Save configuration to file."""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception:
        return False


def get_provider() -> str:
    """Get current MCP provider."""
    config = load_config()
    return config.get("mcp_provider", "")


def set_provider(provider: str) -> bool:
    """Set MCP provider."""
    config = load_config()
    config["mcp_provider"] = provider
    return save_config(config)


def main():
    parser = argparse.ArgumentParser(description="Configure academic-writing plugin")
    parser.add_argument("--get", action="store_true", help="Get current provider")
    parser.add_argument("--set", choices=["zotero-mcp", "zotero-mcp-plugin"], help="Set provider")
    parser.add_argument("--path", action="store_true", help="Show config file path")

    args = parser.parse_args()

    if args.path:
        print(CONFIG_PATH)
        return 0

    if args.get:
        provider = get_provider()
        if provider:
            print(provider)
        return 0

    if args.set:
        if set_provider(args.set):
            print(f"Provider set to: {args.set}")
            return 0
        else:
            print("Failed to save configuration")
            return 1

    # No arguments: show current config
    config = load_config()
    provider = config.get("mcp_provider", "not set")
    print(f"MCP Provider: {provider}")
    print(f"Config file: {CONFIG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
