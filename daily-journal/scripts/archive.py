#!/usr/bin/env python3
"""
Archive daily entries into Obsidian journal file.
Combines cached data with existing manual entries.
"""

import sys
import argparse
import re
import json
from datetime import datetime
from pathlib import Path

scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from config import load_config, is_configured, get_entry_path
from db import (
    get_morning_setup, get_day_interrupts, get_captures, 
    get_conversations, clear_date
)

def parse_existing_entry(file_path: Path) -> dict:
    """Parse an existing journal file into sections."""
    if not file_path.exists():
        return None
    
    content = file_path.read_text(encoding='utf-8')
    
    # Split by major sections (## headings)
    sections = {}
    current_section = None
    current_content = []
    
    for line in content.split('\n'):
        if line.startswith('## '):
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = line[3:].strip()
            current_content = []
        else:
            current_content.append(line)
    
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections

def generate_tags_with_llm(content: str) -> list:
    """
    Generate tags based on content analysis.
    In actual use, this calls LLM. Here we return placeholder.
    """
    # This is a placeholder - actual implementation would use LLM
    tags = []
    
    # Simple keyword matching as fallback
    content_lower = content.lower()
    
    if any(w in content_lower for w in ['感悟', '明白', '意识到', '发现', 'insight', 'realize']):
        tags.append('#insight')
    
    if any(w in content_lower for w in ['文章', '博客', '内容', 'content', 'article', 'blog']):
        tags.append('#idea/content')
    
    if any(w in content_lower for w in ['产品', '功能', 'app', 'product', 'feature']):
        tags.append('#idea/product')
    
    if any(w in content_lower for w in ['故事', '经历', 'story', 'experience']):
        tags.append('#seed/story')
    
    if any(w in content_lower for w in ['观察', '发现', 'observation', 'notice']):
        tags.append('#seed/observation')
    
    if any(w in content_lower for w in ['想法', '考虑', 'think', 'idea', 'wonder']):
        tags.append('#fleeting')
    
    return tags if tags else ['#daily']

def build_journal_content(date: str, template: str, existing_sections: dict = None) -> str:
    """Build complete journal content from cached data."""
    
    # Get all cached data
    morning = get_morning_setup(date)
    interrupts = get_day_interrupts(date)
    captures = get_captures(date)
    conversations = get_conversations(date)
    
    # Parse captures by type
    insights = [c for c in captures if c[0] == 'insight']
    ideas = [c for c in captures if c[0] == 'idea']
    seeds = [c for c in captures if c[0] == 'seed']
    fleeting = [c for c in captures if c[0] == 'fleeting']
    
    # Format date display
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    date_display = date_obj.strftime("%Y-%m-%d %A")
    
    lines = [f"# {date_display}\n"]
    
    # Morning Setup Section
    lines.append("## 🌅 早晨设定\n")
    if morning:
        energy, focus, template_used, context = morning
        lines.append(f"- 今天的状态：{energy}/10")
        lines.append(f"- 今天想 focus 的一件事：{focus}")
        if context:
            lines.append(f"- 今天的背景：{context}")
    else:
        lines.append("- 今天的状态：")
        lines.append("- 今天想 focus 的一件事：")
    lines.append("")
    
    # Today's Records Section
    lines.append("## 📝 今日记录\n")
    
    # Day Interrupts
    if interrupts:
        lines.append("### 日间记录")
        for time_slot, doing, reflection, insight in interrupts:
            lines.append(f"\n**{time_slot}**")
            lines.append(f"- 在做什么：{doing}")
            if reflection:
                lines.append(f"- 反思：{reflection}")
            if insight:
                lines.append(f"- 发现：{insight}")
        lines.append("")
    
    # Merge any manual records from existing sections
    if existing_sections:
        for section_name, content in existing_sections.items():
            if section_name not in ["🌅 早晨设定", "💡 知识捕获", "🌙 晚间反思"] and content.strip():
                lines.append(f"### {section_name}")
                lines.append(content)
                lines.append("")
    
    # Knowledge Capture Section
    lines.append("## 💡 知识捕获\n")
    
    # Insights
    if insights:
        lines.append("### 🔥 Insights")
        for _, content, tags, context in insights:
            tag_str = ' '.join(tags) if tags else '#insight'
            lines.append(f"\n- [ ] {tag_str}")
            lines.append(f"  > **感悟：** {content}")
            if context:
                lines.append(f"  > **触发场景：** {context}")
        lines.append("")
    
    # Ideas
    if ideas:
        lines.append("### 💭 Ideas")
        for _, content, tags, context in ideas:
            tag_str = ' '.join(tags) if tags else '#idea'
            lines.append(f"\n- [ ] {tag_str}")
            lines.append(f"  > **想法：** {content}")
            if context:
                lines.append(f"  > **可能的形式：** {context}")
        lines.append("")
    
    # Seeds
    if seeds:
        lines.append("### 🎬 Content Seeds")
        for _, content, tags, context in seeds:
            tag_str = ' '.join(tags) if tags else '#seed'
            lines.append(f"\n- [ ] {tag_str}")
            lines.append(f"  > **素材：** {content}")
            if context:
                lines.append(f"  > **有趣的点：** {context}")
        lines.append("")
    
    # Fleeting Notes
    if fleeting:
        lines.append("### 🔗 Fleeting Notes")
        for _, content, tags, context in fleeting:
            tag_str = ' '.join(tags) if tags else '#fleeting'
            lines.append(f"\n- [ ] {tag_str}")
            lines.append(f"  > {content}")
        lines.append("")
    
    # Conversational Retrospectives and Reflections
    if conversations:
        project_convs = [c for c in conversations if c[0] == 'project']
        reflection_convs = [c for c in conversations if c[0] == 'reflection']
        
        if project_convs:
            lines.append("### 📊 项目复盘")
            for conv_type, topic, summary, raw_content, tags in project_convs:
                lines.append(f"\n**{topic or '项目复盘'}**")
                if summary:
                    lines.append(f"{summary}")
                if raw_content:
                    lines.append(f"\n详细记录：")
                    lines.append(f"> {raw_content.replace(chr(10), chr(10)+'> ')}")
                if tags:
                    tag_list = json.loads(tags) if isinstance(tags, str) else tags
                    lines.append(f"\n标签：{' '.join(tag_list)}")
            lines.append("")
        
        if reflection_convs:
            lines.append("### 🤔 反思与洞察")
            for conv_type, topic, summary, raw_content, tags in reflection_convs:
                lines.append(f"\n**{topic or '反思'}**")
                if summary:
                    lines.append(f"{summary}")
                if raw_content:
                    lines.append(f"\n思考过程：")
                    lines.append(f"> {raw_content.replace(chr(10), chr(10)+'> ')}")
                if tags:
                    tag_list = json.loads(tags) if isinstance(tags, str) else tags
                    lines.append(f"\n标签：{' '.join(tag_list)}")
            lines.append("")
    
    # Evening Reflection
    lines.append("## 🌙 晚间反思\n")
    lines.append("- 今天最有成就感的时刻：")
    lines.append("- 今天最消耗能量的事：")
    lines.append("- 明天想调整的一件事：")
    lines.append("")
    
    # Auto-generated tags
    all_content = ' '.join([c[1] for c in captures if c[1]])
    auto_tags = generate_tags_with_llm(all_content)
    
    lines.append("---")
    lines.append(f"\n**标签：** {' '.join(auto_tags)}")
    lines.append(f"**模板：** {template or 'Daily Journal'}")
    lines.append(f"**归档时间：** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    return '\n'.join(lines)

def archive_date(date: str = None, dry_run: bool = False):
    """Archive entries for a specific date."""
    if not is_configured():
        print("❌ 请先运行 setup.py 完成首次配置")
        sys.exit(1)
    
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    config = load_config()
    
    # Check if there's any data to archive
    from db import has_data
    has_cached = has_data(date)
    
    # Check for existing manual entry
    entry_path = get_entry_path(date)
    existing_sections = parse_existing_entry(entry_path) if entry_path.exists() else None
    
    if not has_cached and not existing_sections:
        print(f"ℹ️  {date} 没有需要归档的内容")
        return
    
    # Get template from morning setup
    morning = get_morning_setup(date)
    template = morning[2] if morning else "daily"
    
    # Build content
    content = build_journal_content(date, template, existing_sections)
    
    if dry_run:
        print("📋 预览归档内容：")
        print("-" * 40)
        print(content)
        print("-" * 40)
        return
    
    # Ensure directory exists
    entry_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write file
    entry_path.write_text(content, encoding='utf-8')
    
    # Clear cache
    clear_date(date)
    
    # Generate summary
    summary_tags = []
    if morning:
        summary_tags.append(f"状态: {morning[0]}/10")
        summary_tags.append(f"Focus: {morning[1]}")
    
    captures_data = get_captures(date)
    if captures_data:
        capture_types = set(c[0] for c in captures_data)
        summary_tags.append(f"记录: {', '.join(capture_types)}")
    
    summary = f"状态: {morning[0]}/10 | Focus: {morning[1]}" if morning else "今日记录"
    
    print(f"✅ 已归档到: {entry_path}")
    print(f"   {summary}")
    
    # Also output Discord notification message
    discord_msg = f"📓 今天的记录已归档！\n{summary}\n文件: {entry_path.name}"
    print(f"\n[DISCORD] {discord_msg}")
    
    return str(entry_path)

def main():
    parser = argparse.ArgumentParser(description="Archive daily journal entries")
    parser.add_argument("--date", help="Date to archive (YYYY-MM-DD, default: today)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    
    args = parser.parse_args()
    
    archive_date(args.date, args.dry_run)

if __name__ == "__main__":
    main()
