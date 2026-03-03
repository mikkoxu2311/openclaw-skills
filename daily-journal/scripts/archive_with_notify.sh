#!/bin/bash
# Archive daily journal and send Discord notification

cd ~/.openclaw/workspace

# Run archive
python3 ~/.openclaw/workspace/skills/daily-journal/scripts/archive.py

# Send Discord notification with announce
openclaw message send --channel discord --target 1470328409694539818 --announce "📓 今天的日记已自动归档完成！"
