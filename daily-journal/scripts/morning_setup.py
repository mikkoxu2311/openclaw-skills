#!/usr/bin/env python3
"""
Morning setup routine for Daily Journal skill.
Captures energy level, context, and recommends focus tasks.
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path

scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from config import load_config, is_configured, get_journal_path
from db import save_morning_setup

def select_template(energy_score: int, context: str) -> str:
    """Auto-select template based on energy and context."""
    context_lower = context.lower()
    
    # Priority order
    if energy_score <= 4:
        return "low-energy"
    
    if any(word in context_lower for word in ["带娃", "带孩子", "亲子", "parent", "kid", "baby"]):
        return "parenting"
    
    if any(word in context_lower for word in ["困惑", "纠结", "迷茫", "想不通", "confused", "struggle"]):
        return "reflection"
    
    if any(word in context_lower for word in ["完成", "搞定", "finish", "complete", "done", "ship"]):
        return "project"
    
    return "daily"

def get_template_display_name(template: str) -> str:
    """Get human-readable template name."""
    names = {
        "daily": "Daily Journal",
        "low-energy": "低能量日",
        "parenting": "带娃日",
        "project": "项目推进日",
        "reflection": "对话式反思"
    }
    return names.get(template, "Daily Journal")

def morning_setup_cli():
    """CLI version of morning setup."""
    if not is_configured():
        print("❌ 请先运行 setup.py 完成首次配置")
        sys.exit(1)
    
    config = load_config()
    today = datetime.now().strftime("%Y-%m-%d")
    
    print("🌅 早晨设定")
    print("-" * 40)
    
    # Step 1: Energy score
    while True:
        try:
            energy = input("今天状态几分？（1-10）> ").strip()
            energy_score = int(energy)
            if 1 <= energy_score <= 10:
                break
            print("请输入 1-10 之间的数字")
        except ValueError:
            print("请输入数字")
    
    # Step 2: Context
    print("\n今天有什么特别安排？")
    print("比如：带娃 / 重要会议 / 轻松的一天 / 项目收尾 / 有点累")
    context = input("> ").strip()
    
    # Step 3: Auto-select template
    template = select_template(energy_score, context)
    print(f"\n📋 已选择模板: {get_template_display_name(template)}")
    
    # Step 4: Recommend focus task
    print("\n🎯 今天建议 focus 的事情：")
    print("根据你的历史记录，今天可以推进：")
    print("1. [示例] 完成项目方案 - 来源：Next Actions")
    print("2. [示例] 联系设计师 - 来源：项目A")
    print("3. [示例] 整理笔记 - 来源：Idea Backlog")
    print("\n建议今天专注：【完成项目方案】")
    print("第一步：打开 Obsidian，列出3个核心论点")
    
    focus_task = input("\n你想 focus 在什么？（直接回车接受建议）> ").strip()
    if not focus_task:
        focus_task = "完成项目方案"
    
    # Save to database
    save_morning_setup(today, energy_score, focus_task, template, context)
    
    print("\n✅ 早晨设定已保存！")
    print(f"状态: {energy_score}/10 | Focus: {focus_task}")
    
    return {
        "date": today,
        "energy_score": energy_score,
        "template": template,
        "focus_task": focus_task,
        "context": context
    }

def morning_setup_auto():
    """Auto-trigger version (for cron/heartbeat)."""
    if not is_configured():
        return None
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Return a prompt for the agent to ask user
    return {
        "action": "ask_user",
        "channel": "discord",
        "channel_id": "1470328409694539818",
        "announce": True,
        "message": "🌅 早上好！开始今天的记录吗？给今天的状态打个分（1-10）"
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Morning setup for Daily Journal")
    parser.add_argument("--auto", action="store_true", help="Auto-trigger mode")
    args = parser.parse_args()
    
    if args.auto:
        result = morning_setup_auto()
        if result:
            print(result["message"])
    else:
        morning_setup_cli()
