#!/usr/bin/env python3
"""
First-time setup wizard for Daily Journal skill.
Run this when user first activates the skill.
"""

import sys
import subprocess
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from config import load_config, save_config, get_default_config
from db import init_db


def create_day_interrupt_cron(time_str, name_suffix, greeting, followup_question):
    """Create an OpenClaw cron job for day interrupt."""
    # Parse time (HH:MM format)
    try:
        hour, minute = time_str.split(':')
        cron_expr = f"{int(minute)} {int(hour)} * * *"
    except ValueError:
        print(f"   ⚠️ 时间格式错误: {time_str}，跳过")
        return False
    
    # Determine time slot for context
    hour_int = int(hour)
    if hour_int < 12:
        time_slot = "morning"
    elif hour_int < 18:
        time_slot = "afternoon"
    else:
        time_slot = "evening"
    
    job_name = f"day-interrupt-{name_suffix}"
    message = f"【Day Interrupt - {time_slot.capitalize()}】{greeting} 询问用户当前在做什么，追问'{followup_question}'，捕获任何 insight 并存储到 day_interrupts 表。"
    
    # Create cron job using openclaw cli
    cmd = [
        "openclaw", "cron", "add",
        "--name", job_name,
        "--cron", cron_expr,
        "--tz", "Asia/Shanghai",
        "--session", "isolated",
        "--announce",
        "--channel", "discord",
        "--to", "1470328409694539818",
        "--message", message
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"   ✅ 已创建 {time_str} 的提醒任务")
            return True
        else:
            print(f"   ⚠️ 创建 {time_str} 任务失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ⚠️ 创建 {time_str} 任务失败: {e}")
        return False


def setup_wizard():
    """Interactive setup wizard."""
    print("📝 Daily Journal Skill - 首次配置")
    print("大约需要 2 分钟\n")
    
    config = get_default_config()
    
    # 1. Vault path
    print("1. Obsidian Vault 路径是什么？")
    print("   例如: /Users/username/Library/Mobile Documents/iCloud~md~obsidian/Documents/My Vault")
    vault_path = input("   > ").strip()
    config["vault_path"] = vault_path
    
    # 2. Journal directory
    print("\n2. 日记想存在哪个文件夹？（直接回车使用默认 'journal'）")
    journal_dir = input("   > ").strip()
    config["journal_dir"] = journal_dir or "journal"
    
    # 3. Archive directory (optional)
    print("\n3. 月度归档文件放在哪里？（直接回车使用日记文件夹）")
    archive_dir = input("   > ").strip()
    if archive_dir:
        config["archive_dir"] = archive_dir
    
    # 4. Day interrupt times
    print("\n4. 每天想被提醒几次？什么时间？")
    print("   格式: 10:00, 15:00（用逗号分隔）")
    interrupt_times = input("   > ").strip()
    if interrupt_times:
        times_list = [t.strip() for t in interrupt_times.split(",")]
        config["day_interrupt_times"] = times_list
        
        # Create cron jobs for day interrupts
        print("\n   正在创建定时提醒任务...")
        greetings = [
            "🎯 你在干啥？别光想不干哦",
            "👀 进展如何？别总看手机",
            "🌙 晚上检查时间！今天有什么想改变/保持的？"
        ]
        followups = [
            "现在在做的事，是'想成为的我'会做的吗？",
            "过去2小时，在推进还是消耗？",
            "今天有什么想改变/保持的？"
        ]
        
        for i, time_str in enumerate(times_list):
            greeting = greetings[min(i, len(greetings)-1)]
            followup = followups[min(i, len(followups)-1)]
            create_day_interrupt_cron(time_str, f"{i+1}", greeting, followup)
    
    # 5. Morning time
    print("\n5. 如果没有主动对话，几点主动问候？（直接回车使用 08:00）")
    morning_time = input("   > ").strip()
    config["morning_time"] = morning_time or "08:00"
    
    # Create morning greeting cron job
    print("\n   正在创建晨间问候任务...")
    try:
        hour, minute = config["morning_time"].split(':')
        morning_cron = f"{int(minute)} {int(hour)} * * *"
        cmd = [
            "openclaw", "cron", "add",
            "--name", "daily-journal-morning",
            "--cron", morning_cron,
            "--tz", "Asia/Shanghai",
            "--session", "isolated",
            "--announce",
            "--channel", "discord",
            "--to", "1470328409694539818",
            "--message", "🌅 早上好！开始今天的记录吗？给今天的状态打个分（1-10）"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("   ✅ 已创建晨间问候任务")
        else:
            print(f"   ⚠️ 创建晨间问候失败: {result.stderr}")
    except Exception as e:
        print(f"   ⚠️ 创建晨间问候失败: {e}")
    
    # Create evening archive cron job
    print("\n   正在创建晚间归档任务...")
    try:
        cmd = [
            "openclaw", "cron", "add",
            "--name", "daily-journal-archive",
            "--cron", "59 23 * * *",
            "--tz", "Asia/Shanghai",
            "--session", "isolated",
            "--announce",
            "--channel", "discord",
            "--to", "1470328409694539818",
            "--message", "📓 归档今天的日记"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("   ✅ 已创建晚间归档任务")
        else:
            print(f"   ⚠️ 创建晚间归档失败: {result.stderr}")
    except Exception as e:
        print(f"   ⚠️ 创建晚间归档失败: {e}")
    
    # 6. Optional paths
    print("\n6. [可选] Idea Backlog 路径是什么？（直接回车跳过）")
    idea_path = input("   > ").strip()
    if idea_path:
        config["idea_backlog_path"] = idea_path
    
    print("\n7. [可选] 项目追踪文件路径是什么？（直接回车跳过）")
    project_path = input("   > ").strip()
    if project_path:
        config["project_tracking_path"] = project_path
    
    # Mark as configured
    config["first_run"] = False
    
    # Save config
    save_config(config)
    
    # Initialize database
    init_db()
    
    print("\n✅ 配置完成！")
    print(f"\n配置保存在: ~/.openclaw/workspace/skills/daily-journal/config.json")
    print(f"日记将保存在: {vault_path}/{config['journal_dir']}/")
    print(f"\n定时任务已创建:")
    print(f"  - 晨间问候: {config['morning_time']}")
    if interrupt_times:
        for t in times_list:
            print(f"  - Day Interrupt: {t}")
    print(f"  - 晚间归档: 23:59")
    print("\n💡 提示: 你可以随时修改配置文件或运行 `openclaw cron list` 查看任务。")
    print("\n明天早上我会主动问候你，开始第一天的记录。")
    print("你也可以随时说'开始今天'来启动。")


if __name__ == "__main__":
    setup_wizard()
