#!/usr/bin/env python3
"""
Configuration management for Daily Journal skill.
"""

import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".openclaw/workspace/skills/daily-journal/config.json"

def get_default_config():
    """Return default configuration."""
    return {
        "vault_path": "",
        "journal_dir": "journal",
        "archive_dir": "",
        "day_interrupt_times": ["14:00", "20:00"],
        "morning_time": "08:00",
        "idea_backlog_path": "",
        "project_tracking_path": "",
        "first_run": True
    }

def load_config():
    """Load configuration from file."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return get_default_config()

def save_config(config):
    """Save configuration to file."""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def is_configured():
    """Check if skill has been configured."""
    config = load_config()
    return bool(config.get("vault_path")) and not config.get("first_run", True)

def get_journal_path(date: str = None):
    """Get full journal directory path."""
    config = load_config()
    vault = Path(config["vault_path"])
    journal = config["journal_dir"]
    return vault / journal

def get_entry_path(date: str):
    """Get path for a specific day's journal entry."""
    journal_dir = get_journal_path()
    return journal_dir / f"{date} Daily Journal.md"

def get_raw_archive_path(date: str):
    """Get path for monthly raw archive."""
    config = load_config()
    vault = Path(config["vault_path"])
    year_month = date[:7]  # YYYY-MM
    archive_dir = config.get("archive_dir") or config["journal_dir"]
    return vault / archive_dir / f"Raw{year_month}.md"

if __name__ == "__main__":
    # Print current config
    config = load_config()
    print(json.dumps(config, indent=2, ensure_ascii=False))
