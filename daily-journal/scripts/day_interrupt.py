#!/usr/bin/env python3
"""
Day interrupt check-in prompts.
Triggered via heartbeat at configured times.
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path

scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from config import load_config, is_configured
from db import add_day_interrupt, get_morning_setup

def get_reflection_question(time_slot: str) -> str:
    """Get appropriate reflection question for time slot."""
    questions = {
        "morning": [
            "现在在做的事，是'想成为的我'会做的吗？",
            "我在逃避什么？",
            "如果现在不做这个，我会做什么？"
        ],
        "afternoon": [
            "过去2小时，我在用什么'合理借口'？",
            "如果有人拍下过去2小时，会得出我想要什么样的生活？",
            "过去2小时，在推进还是消耗？"
        ],
        "evening": [
            "今天最接近'理想自我'的时刻是？",
            "今天最远离的时刻是？",
            "我在向想要的生活靠近，还是在向不想要的生活靠近？"
        ]
    }
    
    import random
    slot = time_slot if time_slot in questions else "afternoon"
    return random.choice(questions[slot])

def generate_prompt(time_slot: str = None) -> dict:
    """Generate interrupt prompt for agent."""
    if not is_configured():
        return None
    
    config = load_config()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Determine time slot if not provided
    if not time_slot:
        hour = datetime.now().hour
        if hour < 12:
            time_slot = "morning"
        elif hour < 18:
            time_slot = "afternoon"
        else:
            time_slot = "evening"
    
    # Get morning focus task if available
    morning = get_morning_setup(today)
    focus_hint = ""
    if morning:
        focus_task = morning[1]  # focus_task column
        focus_hint = f"是在『{focus_task}』还是别的？"
    
    question = get_reflection_question(time_slot)
    
    return {
        "action": "interrupt",
        "time_slot": time_slot,
        "message": f"嘿，现在手上在忙什么？{focus_hint}",
        "followup": question
    }

def save_interrupt(time_slot: str, doing: str, reflection: str = None, insight: str = None):
    """Save interrupt check-in."""
    if not is_configured():
        print("❌ 请先运行 setup.py 完成首次配置")
        sys.exit(1)
    
    today = datetime.now().strftime("%Y-%m-%d")
    add_day_interrupt(today, time_slot, doing, reflection, insight)
    print("✅ Day interrupt 已记录")

def main():
    parser = argparse.ArgumentParser(description="Day interrupt check-in")
    parser.add_argument("--time", choices=["morning", "afternoon", "evening"], help="Time slot")
    parser.add_argument("--doing", help="What user is doing")
    parser.add_argument("--reflection", help="Reflection answer")
    parser.add_argument("--insight", help="Any insight captured")
    parser.add_argument("--prompt", action="store_true", help="Generate prompt only")
    
    args = parser.parse_args()
    
    if args.prompt:
        result = generate_prompt(args.time)
        if result:
            import json
            print(json.dumps(result, ensure_ascii=False))
    elif args.doing:
        save_interrupt(args.time or "afternoon", args.doing, args.reflection, args.insight)
    else:
        # Generate and display prompt
        result = generate_prompt(args.time)
        if result:
            print(result["message"])
            print(f"\n追问: {result['followup']}")

if __name__ == "__main__":
    main()
