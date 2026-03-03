---
name: daily-journal
description: ADHD-friendly structured journaling for Obsidian. Use when user wants to start their day, capture thoughts/ideas, do day check-ins, or archive daily entries. Activates on keywords like "开始今天", "记一下", "capture", "整理今天".
metadata:
  openclaw:
    emoji: "📝"
    requires:
      bins: ["sqlite3"]
---

# Daily Journal

Structured journaling system for ADHD users with guided conversations, automatic archiving, and smart tagging.

## When to Use

| User Says | Trigger |
|-----------|---------|
| "开始今天" / "morning" / 当天首次对话 | 晨间启动 (Phase 2) |
| "记一下" / "capture" / "有个想法" | 随时记录 (Phase 4) |
| "有点乱" / "需要理清" | 对话式反思模式 |
| "做完了 XX" / "项目完成" | 项目复盘模式 |
| "整理今天" / "archive today" | 手动归档 (Phase 6) |
| 其他时间 | 正常对话 |

## Core Principles

**ADHD-First Design:**
- Ask ONE question at a time
- Give specific options, not open-ended
- Break tasks into minimum actionable steps
- Recognize energy states (Low Energy template)

## Quick Commands

```bash
# First-time setup (auto-triggered)
python ~/.openclaw/workspace/skills/daily-journal/scripts/setup.py

# Morning setup
python ~/.openclaw/workspace/skills/daily-journal/scripts/morning_setup.py

# Capture an entry
python ~/.openclaw/workspace/skills/daily-journal/scripts/capture.py --type insight --content "..."

# Day interrupt check-in
python ~/.openclaw/workspace/skills/daily-journal/scripts/day_interrupt.py --time afternoon

# Archive today's entries
python ~/.openclaw/workspace/skills/daily-journal/scripts/archive.py --date 2026-03-02
```

## Phase 1: Onboarding (First Time)

**Triggered automatically on first use.**

Ask one question at a time:

1. **Obsidian Vault path**: "你的 Obsidian Vault 路径是什么？"
2. **Journal directory**: "日记想存在哪个文件夹？（不指定则创建 journal 文件夹）"
3. **Day Interrupt times**: "每天想被提醒几次？什么时间？（如：14:00, 20:00）"
4. **Morning greeting time**: "如果没有主动对话，几点主动问候？（如：08:00）"
5. **Optional paths**: "Idea Backlog 和项目追踪文件的路径？（可选）"

Store config in `~/.openclaw/workspace/skills/daily-journal/config.json`.

## Phase 2: Morning Setup

**Trigger conditions:**
- User says "开始今天" / "morning"
- First conversation of the day (auto-detect)
- Configured morning time reached (cron/heartbeat)

**Workflow:**

1. **State check**: "早上好！给今天的状态打个分（1-10）"
2. **Intention**: "今天有什么特别安排？比如：带娃 / 重要会议 / 轻松的一天"
3. **Auto-select template** (no user prompt):
   - Score ≤4 → Low Energy
   - Mentions parenting → Parenting Day  
   - Mentions confusion → Reflection
   - Mentions project completion → Project Day
   - Default → Daily Journal
4. **Recommend tasks**: "根据你的记录，今天可以推进这3件事：
   - [Task A] - 来源：Next Actions
   - [Task B] - 来源：Idea Backlog
   - [Task C] - 来源：项目X
   
   我建议 focus 在【Task A】，第一步：{最小可行动步骤}"
5. **Confirm**: "这个方向 OK 吗？"

Store in DB: `morning_setup` table.

## Phase 3: Day Interrupt (Cron)

**Run via OpenClaw cron at configured times.**

Setup automatically creates cron jobs when user configures interrupt times.
Each job sends a message to Discord #playground with `--announce` for mobile push.

**Trigger Message by Time Slot:**
- Morning (default 10:00): "🎯 你在干啥？别光想不干哦"
- Afternoon (default 15:00): "👀 进展如何？别总看手机"
- Evening (default 20:00): "🌙 晚上检查时间！今天有什么想改变/保持的？"

**Agent Flow:**
1. Agent receives day interrupt trigger message
2. Sends greeting to Discord #playground
3. Asks "现在手上在忙什么？"
4. Follow-up by time slot:
   - Morning: "现在在做的事，是'想成为的我'会做的吗？"
   - Afternoon: "过去2小时，在推进还是消耗？"
   - Evening: "今天有什么想改变/保持的？"
5. Capture any insight/fleeting note
6. Store in `day_interrupts` table

**Cron Jobs Created by Setup:**
```bash
# Day Interrupt - Morning (10:00)
openclaw cron add --name day-interrupt-morning --cron "0 10 * * *" --announce --channel discord --to 1470328409694539818

# Day Interrupt - Afternoon (15:00)
openclaw cron add --name day-interrupt-afternoon --cron "0 15 * * *" --announce --channel discord --to 1470328409694539818
```

## Phase 4: On-Demand Capture

**Intent recognition:**

| Pattern | Mode | Agent Action |
|---------|------|--------------|
| "记一下" / "capture" | Quick | Record as fleeting, no follow-up |
| "有个想法" / "idea" | Idea | **Auto-judge**: 分析内容判断 `#idea/content` 还是 `#idea/product`，确认后保存 |
| "突然想到" / "fleeting" | Fleeting | Quick record, tag as #fleeting |
| "做完了 XX" | Project | Switch to **对话式复盘** (Phase 5) |
| "有点乱" / "理清" | Reflection | Switch to **对话式反思** (Phase 5) |

### Idea Capture Flow

1. User: "有个想法"
2. Agent: "说说看是什么想法？"
3. User describes the idea
4. **Agent analyzes and judges:**
   - Mentions article/blog/video/post/content → `#idea/content`
   - Mentions app/feature/product/tool/business → `#idea/product`
5. Agent confirms: "这是关于 [内容/产品] 的想法对吧？"
6. Save to `captures` table with appropriate tag

**No form-filling, natural conversation only.**

### Insight/Seed/Fleeting Capture

Store directly to `captures` table with auto-generated tags.

## Phase 5: Conversational Modes (Project & Reflection)

**NO fixed question lists. Agent acts as a guide through natural conversation.**

### Project Retrospective Mode

**Trigger:** User mentions completing a project ("做完了 XX", "搞定了", "ship 了")

**Agent Role:** Curious facilitator, not interviewer

**Example Flow:**
```
User: 今天把登录功能做完了
Agent: 恭喜！具体完成了什么？花了多久？
User: 做了 Google 和微信登录，大概 3 小时
Agent: 比预期快还是慢？
User: 比预期快，因为用了现成的 OAuth 库
Agent: 学到什么了？
User: 发现 Auth0 其实挺简单的，文档很清晰
Agent: 遇到什么坑了吗？
User: 微信登录的回调 URL 配置搞了半天
→ Agent synthesizes key points, marks #insight #method, stores to DB
```

**Key areas to explore (naturally, not as checklist):**
- What was completed and time spent
- Surprises (harder/easier than expected)
- Learnings and new skills
- Problems encountered and solutions
- Improvements for next time

Store synthesized summary to `conversations` table with type: project.

### Reflection Mode

**Trigger:** User says "有点乱", "需要理清", "想不通", "纠结"

**Agent Role:** Socratic guide, helping user think through

**Example Flow:**
```
User: 有点乱，不知道该不该接那个外包项目
Agent: 说说看，什么情况让你纠结？
User: 钱不错但时间很紧
Agent: 不接的话最坏会怎样？
User: 可能错过一个长期客户
Agent: 接了的话，现在的生活会受到什么影响？
User: 可能要牺牲周末陪孩子的时间
Agent: 对你来说，周末陪孩子和这个项目，哪个更接近你想要的生活？
→ Agent captures the insight/decision, stores to DB
```

**Guiding principles (not questions):**
- Surface the real concern
- Explore worst-case scenarios
- Connect to values and long-term goals
- Help clarify decision criteria

Store synthesized insight to `conversations` table with type: reflection.

## Phase 6: Evening Archive

**Trigger:** Daily at 23:59 via cron, or manual "整理今天".

**Process:**

1. Load config
2. Query DB for today's entries:
   - morning_setup
   - day_interrupts
   - captures (insights, ideas, seeds, fleeting)
   - conversations (project retrospectives and reflections)
3. Check for existing manual entry: `{journal-dir}/{YYYY-MM-DD} Daily Journal.md`
4. **If exists:** Read → parse sections → merge with cached data
5. **Apply template structure:** Reorganize all content into appropriate sections
6. **Auto-tag with LLM:** Analyze merged content, generate tags (#insight, #idea/content, etc.)
7. **Write file:** Overwrite with organized content
8. **Clear cache:** Delete today's entries from DB

**Archive path:** `{journal-dir}/{YYYY-MM-DD} Daily Journal.md`

## Tagging System

**Auto-generate based on content analysis:**

| Tag | Meaning |
|-----|---------|
| #insight | 对自己/生活/工作的感悟 |
| #idea/content | 可能写成内容的想法 |
| #idea/product | 产品/项目想法 |
| #seed/story | 可以讲的故事 |
| #seed/observation | 有趣的观察 |
| #fleeting | 需要进一步思考的闪念 |
| #method | 学到的方法/流程 |
| #principle | 总结的原则 |

## Database Schema

SQLite at `~/.openclaw/workspace/skills/daily-journal/cache/journal.db`:

```sql
-- Daily conversation entries
CREATE TABLE entries (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,  -- YYYY-MM-DD
    phase TEXT,          -- morning, interrupt, capture, archive
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Captured items (insights, ideas, seeds, fleeting)
CREATE TABLE captures (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    type TEXT NOT NULL,  -- insight, idea, seed, fleeting
    content TEXT,
    tags TEXT,           -- JSON array
    context TEXT,        -- trigger context
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Day interrupt check-ins
CREATE TABLE day_interrupts (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    time_slot TEXT,      -- morning, afternoon, evening
    doing TEXT,
    reflection TEXT,
    insight TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Morning setup
CREATE TABLE morning_setup (
    id INTEGER PRIMARY KEY,
    date TEXT PRIMARY KEY,
    energy_score INTEGER,
    focus_task TEXT,
    template TEXT,       -- daily, low-energy, parenting, project, reflection
    context TEXT,        -- user context (parenting, meeting, etc.)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Project retrospectives
CREATE TABLE project_retrospectives (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    project_name TEXT,
    completion TEXT,
    time_spent TEXT,
    difficulties TEXT,
    successes TEXT,
    learnings TEXT,
    solutions TEXT,
    improvements TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Resources

- `scripts/setup.py` - First-time configuration
- `scripts/morning_setup.py` - Morning routine
- `scripts/capture.py` - Record insights/ideas/seeds
- `scripts/day_interrupt.py` - Day check-in prompts
- `scripts/archive.py` - Generate daily journal file
- `scripts/db.py` - Database operations
- `references/templates.md` - All journal templates
- `references/tagging-guide.md` - LLM tagging prompts

## Cron Setup

Daily Journal uses **OpenClaw internal cron** instead of system crontab. This ensures tasks run even if the machine was sleeping (they execute on wake).

### Auto-Created Cron Jobs (by setup.py)

```bash
# Morning Greeting (configurable, default 08:00)
openclaw cron add --name daily-journal-morning \
  --cron "0 8 * * *" --tz Asia/Shanghai \
  --session isolated --announce \
  --channel discord --to 1470328409694539818 \
  --message "🌅 早上好！开始今天的记录吗？给今天的状态打个分（1-10）"

# Day Interrupts (configurable by user)
openclaw cron add --name day-interrupt-morning \
  --cron "0 10 * * *" --tz Asia/Shanghai \
  --session isolated --announce \
  --channel discord --to 1470328409694539818 \
  --message "【Day Interrupt - Morning】..."

# Evening Archive (23:59)
openclaw cron add --name daily-journal-archive \
  --cron "59 23 * * *" --tz Asia/Shanghai \
  --session isolated --announce \
  --channel discord --to 1470328409694539818 \
  --message "📓 归档今天的日记"
```

### Why OpenClaw Cron > System Crontab

| Feature | System Crontab | OpenClaw Cron |
|---------|---------------|---------------|
| Sleep handling | ❌ Task skipped | ✅ Executes on wake |
| Cross-platform | ⚠️ macOS/Linux differ | ✅ Unified |
| Management | Manual crontab -e | `openclaw cron list/rm` |
| Delivery | Manual message send | Built-in `--announce` |

**Note:** Always use `--channel discord --target 1470328409694539818 --announce` for mobile push notifications.

## Example Usage

### Morning Setup
```
User: 开始今天
Agent: 早上好！给今天的状态打个分（1-10）
User: 6
Agent: 今天有什么特别安排？比如：带娃 / 重要会议 / 轻松的一天
User: 今天要开一个重要会议
Agent: [Selects Daily Journal template]
       根据你的记录，今天可以推进这3件事：
       1. 完成项目方案 - 来源：Next Actions
       2. 联系设计师讨论UI - 来源：项目A
       3. 写周报 - 来源：历史Journal
       
       我建议今天 focus 在【完成项目方案】
       第一步：打开 Obsidian，列出3个核心论点
       
       这个方向 OK 吗？
```

### Capture
```
User: 有个想法
Agent: 说说看是什么想法？
User: 觉得现在的 journaling workflow 可以改进
Agent: 这个想法很好！可能是什么形式分享？文章/视频/帖子？
User: 可以写一篇博客
Agent: [Tagged as #idea/content] 已记录！
```

### Archive
```
User: 整理今天
Agent: 今天的记录已整理完成！
       状态：6/10 | Focus：完成项目方案 | 标签：#work #insight
       已保存到：journal/2026-03-02 Daily Journal.md
```
