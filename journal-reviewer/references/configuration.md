# Configuration

完整配置选项、首次设置指南和故障排除。

---

## 首次设置指南

### Step 1: 确定 Obsidian Vault 路径

**macOS:**
```bash
# 默认 iCloud 路径
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/YourVault

# 或自定义路径
~/Documents/Obsidian Vault
~/Obsidian/YourVault
```

**Windows:**
```
C:\Users\Username\Documents\Obsidian Vault
```

**常见路径检测:**
```
系统会自动检测以下位置的 Vault：
- ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/*
- ~/Documents/*Vault*/
- ~/Obsidian/*/
- ~/Notes/*/
```

### Step 2: 确定日记文件夹名称

**常见日记文件夹命名:**

| 命名模式 | 示例 |
|----------|------|
| PARA 方法 | `4.0 Journal`, `1. Inbox` |
| 日记专用 | `Journal`, `Daily Notes`, `Diary` |
| 日期前缀 | `2026-Journal`, `Daily` |
| 中文命名 | `日记`, `每日笔记` |

**自动检测逻辑:**
```
系统会在 Vault 中查找包含日记文件的文件夹：
1. 搜索 YYYY-MM-DD.md 格式的文件
2. 找出包含最多日记文件的文件夹
3. 提示用户确认或修改
```

### Step 3: 交互式配置流程

```
用户: /journal-review --setup

系统: "📓 Journal Reviewer 首次设置"
       ""
       "步骤 1/3: 选择 Obsidian Vault"
       "检测到以下 Vault："
       "  1. Personal Vault (/Users/name/Documents/Personal)"
       "  2. Work Vault (/Users/name/Documents/Work)"
       "  3. 手动输入路径"
       ""
       "请选择 [1-3]: "

用户: 1

系统: "步骤 2/3: 确认日记文件夹"
       "检测到 '4.0 Journal' 文件夹中有 45 篇日记"
       ""
       "确认使用该文件夹？"
       "  1. 是的，使用 '4.0 Journal'"
       "  2. 选择其他文件夹"
       "  3. 手动输入名称"
       ""
       "请选择 [1-3]: "

用户: 1

系统: "步骤 3/3: 配置选项"
       "自动回顾时间: 每周日 21:00"
       "  - 修改请按 'e'"
       "  - 保持默认请按回车"

用户: [回车]

系统: "✅ 配置完成！"
       ""
       "Vault: /Users/name/Documents/Personal"
       "日记文件夹: 4.0 Journal"
       "发现日记: 45 篇"
       ""
       "可以开始使用：/journal-review"
```

### Step 4: 验证配置

```
用户: /journal-review --check

系统: "📋 配置检查报告"
       ""
       "✓ Vault 路径: /Users/name/Documents/Personal"
       "✓ 日记文件夹: 4.0 Journal"
       "✓ 日记文件: 45 篇"
       "✓ 状态文件: 不存在（将自动创建）"
       "✓ 已准备好使用"
       ""
       "下次自动回顾: 2026-03-08 (周日) 21:00"
```

---

## 基础配置

在 `USER.md` 中添加：

```yaml
journal_review:
  vault_path: "/path/to/vault"
  journal_folder: "4.0 Journal"
  cron_day: "sunday"
  cron_time: "21:00"
  
  deduplication:
    strict: true
    check_content_hash: true
    state_file: ".jr-state.json"
  
  archiving:
    enabled: true
    keep_months: 3
    max_size_kb: 100
    auto_archive_day: 1
    archive_file: ".jr-state-archive.json"
```

## 完整配置选项

### 路径配置

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `vault_path` | `""` | Obsidian vault 根路径 |
| `journal_folder` | `"4.0 Journal"` | 日记文件夹名称 |

### 自动模式配置

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `cron_day` | `"sunday"` | 自动运行星期（sunday/monday/...） |
| `cron_time` | `"21:00"` | 自动运行时间（24小时制） |

### 文件模式配置

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `raw_file_mode` | `"monthly"` | Raw Record 分片方式（monthly/weekly） |

### 去重策略配置

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `deduplication.strict` | `true` | true=严格去重, false=允许重复 |
| `deduplication.check_content_hash` | `true` | 内容哈希去重 |
| `deduplication.state_file` | `".jr-state.json"` | 状态文件名 |

### 状态文件归档配置

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `archiving.enabled` | `true` | 启用自动归档 |
| `archiving.keep_months` | `3` | 活跃窗口保留月数 |
| `archiving.max_size_kb` | `100` | 触发归档的大小阈值 |
| `archiving.auto_archive_day` | `1` | 每月归档日期（1=每月1日） |
| `archiving.archive_file` | `".jr-state-archive.json"` | 归档文件名 |

### 源文件归档配置

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `source_archiving.enabled` | `true` | 启用源文件归档 |
| `source_archiving.auto_archive` | `false` | 自动归档（false=每次询问） |
| `source_archiving.archive_folder` | `"Archive/raw_record"` | 归档文件夹 |
| `source_archiving.group_by_year` | `true` | 按年份分组存储 |
| `source_archiving.keep_recent_days` | `7` | 保留最近N天的源文件不归档 |
| `source_archiving.confirm_before_move` | `true` | 移动前确认 |

## 完整配置示例

```yaml
journal_review:
  # 路径
  vault_path: "/Users/username/Obsidian Vault"
  journal_folder: "4.0 Journal"

  # 自动模式
  cron_day: "sunday"
  cron_time: "21:00"

  # 文件模式
  raw_file_mode: "monthly"

  # 去重策略
  deduplication:
    strict: true
    check_content_hash: true
    state_file: ".jr-state.json"

  # 状态文件归档
  archiving:
    enabled: true
    keep_months: 3
    max_size_kb: 100
    auto_archive_day: 1
    archive_file: ".jr-state-archive.json"

  # 源文件归档
  source_archiving:
    enabled: true
    auto_archive: false
    archive_folder: "Archive/raw_record"
    group_by_year: true
    keep_recent_days: 7
    confirm_before_move: true
```

## 配置优先级

1. 运行时参数（如 `--archive`）
2. USER.md 配置
3. 默认值

## 恢复配置

如需从 Archive 恢复源文件：

```yaml
# 在 USER.md 中添加快捷命令
commands:
  restore-journal: "mv '4.0 Journal/Archive/raw_record/2026/{date}.md' '4.0 Journal/{date}.md'"
```

或使用交互式：
```
/journal-review --restore-source 2026-02-26
```

---

## 故障排除

### 问题 1: 未检测到 Vault

**现象:**
```
系统: "未检测到 Obsidian Vault"
```

**解决:**
1. 确认 Obsidian 已安装并创建过 Vault
2. 手动输入 Vault 完整路径：
   ```
   用户: /journal-review --setup
   系统: "请输入 Vault 完整路径:"
   用户: "/Users/username/Documents/My Vault"
   ```

### 问题 2: 未检测到日记文件夹

**现象:**
```
系统: "未在 Vault 中找到日记文件夹"
```

**可能原因:**
- 日记文件命名格式不是 YYYY-MM-DD.md
- 日记散落在多个文件夹中
- 日记文件夹使用非标准命名

**解决:**
```
系统: "请手动指定日记文件夹名称:"
       "常见选项:"
       "  1. Journal"
       "  2. Daily Notes"
       "  3. 日记"
       "  4. 手动输入"
用户: 4
系统: "请输入文件夹名称:"
用户: "My Daily Notes"
```

### 问题 3: 配置后找不到日记

**检查清单:**

```
用户: /journal-review --check

系统: "⚠️ 配置检查报告"
       ""
       "✓ Vault 路径: /Users/name/Documents/Personal"
       "✗ 日记文件夹: 'Journal' 不存在"
       "  在 Vault 中发现以下文件夹:"
       "    - 4.0 Journal"
       "    - Projects"
       "    - Resources"
       ""
       "建议修改为: '4.0 Journal'"
```

### 问题 4: 权限问题

**现象:** 无法读取日记文件或写入状态文件

**解决:**
```bash
# 检查文件夹权限
ls -la "path/to/journal/folder"

# 修复权限（macOS/Linux）
chmod -R 755 "path/to/vault"
```

### 问题 5: iCloud 同步延迟

**现象:** 新写的日记没有被检测到

**说明:** iCloud 可能有同步延迟，特别是刚创建的日记文件。

**解决:**
1. 等待 iCloud 同步完成（通常几秒钟到几分钟）
2. 或手动触发同步：在 Obsidian 中重新打开文件
3. 使用本地 Vault 而非 iCloud 路径以避免延迟

### 重置配置

如需重新配置：

```
用户: /journal-review --reset-config
系统: "确定要重置配置吗？这将清除："
       "  - Vault 路径设置"
       "  - 日记文件夹设置"
       "  - 自定义选项"
       ""
       "状态文件和已生成的回顾不会被删除。"
       ""
       "确认重置? [y/N]"

用户: y
系统: "配置已重置，请重新运行 /journal-review --setup"
```

---

## 分享 Skill 给他人使用

### 快速上手指南（给新用户）

```markdown
## Journal Reviewer 快速上手

### 1. 首次配置（只需一次）
```
/journal-review --setup
```
按提示选择你的 Obsidian Vault 和日记文件夹。

### 2. 验证配置
```
/journal-review --check
```

### 3. 开始使用
- **手动回顾**: `/journal-review`
- **自动回顾**: 每周日 21:00 自动运行

### 文件结构要求
你的日记文件应该使用 `YYYY-MM-DD.md` 命名格式，
放在配置的日记文件夹中。

### 需要帮助？
- 检查配置: `/journal-review --check`
- 重新配置: `/journal-review --reset-config`
- 查看文档: 询问我 "journal-reviewer 如何使用"
```

### 导出配置

如需备份或迁移配置：

```
用户: /journal-review --export-config
系统: "配置已导出到:"
       "~/.openclaw/workspace/journal-reviewer-config.yaml"
       ""
       "内容:"
       "  vault_path: /Users/name/Documents/Personal"
       "  journal_folder: 4.0 Journal"
       "  ..."
```

在新设备上导入：

```
用户: /journal-review --import-config journal-reviewer-config.yaml
系统: "配置已导入"
```
