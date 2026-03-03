#!/usr/bin/env python3
"""
Send morning greeting to Discord channel.
Called by cron job.
"""

import sys
from pathlib import Path

scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from config import is_configured

def send_morning_greeting():
    if not is_configured():
        print("Skill not configured yet")
        return
    
    # Output the message that should be sent
    # The actual sending will be handled by the caller (openclaw message tool)
    message = "🌅 早上好！开始今天的记录吗？给今天的状态打个分（1-10）"
    print(message)
    
    # Return channel info for the caller
    return {
        "channel": "discord",
        "target": "1470328409694539818",
        "announce": True,
        "message": message
    }

if __name__ == "__main__":
    result = send_morning_greeting()
    if result:
        import json
        print(json.dumps(result, ensure_ascii=False))
