# Daily Journal

An ADHD-friendly structured journaling system for Obsidian with guided conversations, automatic archiving, and smart tagging.

## Features

- **🌅 Morning Setup**: Daily intention setting with template auto-selection
- **🎯 Day Interrupts**: Scheduled check-ins via OpenClaw cron (configurable times)
- **📝 Capture Mode**: Quick idea/insight logging with auto-tagging
- **🤖 Conversational Modes**: Project retrospectives and reflection sessions
- **📦 Auto Archive**: Evening compilation into your Obsidian vault

## Installation

1. Copy this skill to your OpenClaw workspace:
   ```bash
   cp -r daily-journal ~/.openclaw/workspace/skills/
   ```

2. Run the setup wizard:
   ```bash
   python3 ~/.openclaw/workspace/skills/daily-journal/scripts/setup.py
   ```

3. The setup will automatically create OpenClaw cron jobs for:
   - Morning greeting
   - Day interrupt check-ins
   - Evening archive

## Configuration

Copy `config.example.json` to `config.json` and customize:

```json
{
  "vault_path": "/path/to/your/obsidian/vault",
  "journal_dir": "journal",
  "archive_dir": "journal",
  "day_interrupt_times": ["10:00", "15:00"],
  "morning_time": "08:00"
}
```

## Usage

| Trigger | Action |
|---------|--------|
| "开始今天" / "morning" | Morning setup flow |
| "记一下" / "capture" | Quick capture |
| "有个想法" | Idea logging with auto-classification |
| "整理今天" / "archive today" | Manual archive |
| "做完了 XX" | Project retrospective |
| "有点乱" | Reflection mode |

## File Structure

```
daily-journal/
├── SKILL.md                 # Main skill documentation
├── README.md               # This file
├── config.example.json     # Configuration template
├── scripts/                # Python automation scripts
│   ├── setup.py           # First-time setup wizard
│   ├── morning_setup.py   # Morning routine
│   ├── capture.py         # Quick capture
│   ├── day_interrupt.py   # Check-in prompts
│   ├── archive.py         # Daily archive generation
│   ├── db.py              # Database operations
│   └── config.py          # Configuration management
└── references/            # Additional documentation
    ├── templates.md       # Journal templates
    ├── tagging-guide.md   # Auto-tagging rules
    └── db-schema.md       # Database schema
```

## Requirements

- OpenClaw with Discord channel configured
- Obsidian vault
- Python 3.8+
- SQLite3

## License

MIT
