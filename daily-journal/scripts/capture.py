#!/usr/bin/env python3
"""
Capture insights, ideas, seeds, and fleeting notes.
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path

scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from config import is_configured
from db import add_capture

def capture_entry(entry_type: str, content: str, tags: list = None, context: str = None):
    """Capture an entry to database."""
    if not is_configured():
        print("❌ 请先运行 setup.py 完成首次配置")
        sys.exit(1)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    add_capture(today, entry_type, content, tags, context)
    
    type_names = {
        "insight": "🔥 Insight",
        "idea": "💭 Idea", 
        "seed": "🎬 Seed",
        "fleeting": "🔗 Fleeting Note"
    }
    
    print(f"✅ {type_names.get(entry_type, entry_type)} 已记录")
    if tags:
        print(f"   标签: {', '.join(tags)}")

def main():
    parser = argparse.ArgumentParser(description="Capture journal entries")
    parser.add_argument("--type", choices=["insight", "idea", "seed", "fleeting"], required=True)
    parser.add_argument("--content", required=True, help="Entry content")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--context", help="Trigger context")
    
    args = parser.parse_args()
    
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
    
    capture_entry(args.type, args.content, tags, args.context)

if __name__ == "__main__":
    main()
