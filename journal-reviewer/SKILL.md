---
name: journal-reviewer
description: Automated and on-demand journal review system for Obsidian vault with deduplication. Auto-runs weekly via cron, supports manual arbitrary date ranges with conflict resolution. Use when user mentions reviewing journals, running /journal-review, processing diary entries, or weekly/monthly reviews.
metadata:
  openclaw:
    emoji: "📓"
    requires:
      bins: ["obsidian-cli"]
---

# Journal Reviewer

智能日记回顾系统。自动每周运行，支持手动触发任意时间周期的分析。

**核心特性**: 内置去重机制，自动/手动模式无缝协调。

---

## When to Use

- **自动回顾**: 每周日 21:00 自动运行，回顾上周日记
- **手动回顾**: 用户输入 `/journal-review` 分析任意日期范围
- **去重协调**: 自动检测已处理日期，避免重复
- **源文件归档**: 整理后将原始日记移动到归档文件夹

---

## First-time Setup

首次使用前，配置日记文件夹位置：

### 方式 1: 交互式设置（推荐）

```
用户: /journal-review --setup
系统: "首次使用，请配置日记位置："
       "1. Obsidian Vault 路径:"
用户: "/Users/username/Obsidian Vault"
系统: "2. 日记文件夹名称（默认: 4.0 Journal）:"
用户: [回车使用默认] 或输入自定义名称
系统: "配置已保存到 USER.md，可以开始使用了！"
```

### 方式 2: 手动配置

在 `USER.md` 中添加：

```yaml
journal_review:
  vault_path: "/path/to/your/obsidian/vault"
  journal_folder: "4.0 Journal"  # 你的日记文件夹名称
```

### 验证配置

```
用户: /journal-review --check
系统: "配置检查："
       "✓ Vault 路径: /Users/username/Obsidian Vault"
       "✓ 日记文件夹: 4.0 Journal"
       "✓ 发现 15 篇日记文件"
       "✓ 已准备好使用"
```

---

## Quick Start

### 自动模式

无需操作，每周日 21:00 自动运行：
1. 确定"上周"日期范围（周一到周日）
2. 跳过已处理日期 → 处理新日期
3. 生成 Weekly Review

### 手动模式

```
用户: /journal-review
系统: "请提供日期范围："
用户: "2026-02-01 to 2026-02-28"
系统: [显示已处理/未处理日期]
用户: 选择"仅处理未处理"或"重新处理全部"
系统: [执行并输出]
```

---

## Core Workflow

### Step 1: 读取状态

读取 `4.0 Journal/.jr-state.json`：
- 检查请求日期范围内哪些已处理
- 显示已处理/未处理统计
- 询问处理方式

详见: [references/state-management.md](references/state-management.md)

### Step 2: 处理日记

对每个未处理的日记文件：

**Task 1: Raw Record**
- 读取日记文件
- 清理并格式化
- 追加到 `Raw2026-MM.md`（按月）
- 标记 `rawRecord: true`

**Task 2: 三池提取**
- 提取 Ideas → `Journal2Content/Ideas Backlog.md`
- 提取 Seeds → `Journal2Content/Content Seeds.md`
- 提取 Insights → `Journal2Content/Insights Pool.md`
- 每个项生成唯一 ID，标记 `pools: true`

**支持自由格式日记** - 无论是否使用模板，都可通过语义分析提取内容。

提取规则: [references/content-extraction.md](references/content-extraction.md)  
去重机制: [references/deduplication.md](references/deduplication.md)

### Step 3: 生成回顾

**自动模式**: `Weekly Review - 2026-W06.md`
- 仅包含当周实际处理的日期

**手动模式**:
- 整月: `Monthly Review - 2026-02.md`
- 任意周期: `Journal Review - 2026-02-20 to 2026-02-26.md`

### Step 4: 更新状态

更新 `.jr-state.json`：
```json
{
  "processedDates": {
    "2026-02-26": {
      "rawRecord": true,
      "pools": true,
      "review": "W09"
    }
  },
  "extractedItems": {
    "ideas": ["idea-20260226-a3f7b2"],
    "seeds": [],
    "insights": ["insight-20260226-f2a9e3"]
  }
}
```

### Step 5: 源文件归档（可选）

询问用户是否归档已处理的源文件：
```
是否将 2026-02-01.md ~ 2026-02-26.md 移动到 Archive/raw_record/2026/?
[归档全部] [保留原样] [选择性归档]
```

---

## File Structure

```
4.0 Journal/
├── 2026-02-28.md                    # 当前日记
├── Raw2026-02.md                    # 月度整理（按月累积）
├── Weekly Review - 2026-W09.md      # 周回顾
├── Monthly Review - 2026-02.md      # 月回顾（手动生成）
├── Journal2Content/
│   ├── Ideas Backlog.md
│   ├── Content Seeds.md
│   └── Insights Pool.md
├── Archive/
│   └── raw_record/                  # 归档的源文件
│       └── 2026/
│           ├── 2026-02-01.md
│           └── ...
├── .jr-state.json                   # 活跃状态（3个月窗口）
└── .jr-state-archive.json           # 历史归档
```

---

## Core Principles

- **绝不删除任何文件**
- **绝不覆盖已有内容**
- **智能去重**: 同一条日记不会重复进入 Raw Record 或 Pool
- **状态追踪**: 记录已处理日期，自动跳过重复

---

## Common Scenarios

### 场景 1: 月初手动整月 + 后续自动周

```
[2月28日] 用户手动: /journal-review 2026-02-01 to 2026-02-28
  → 处理全部28天，生成 Monthly Review
  → 状态文件标记全部日期为 processed

[3月2日] 系统自动: 处理上周 (2月24日-3月2日)
  → 跳过 2月24-28（已处理）
  → 只处理 3月1-2（新日期）
```

### 场景 2: 重复手动触发

```
用户再次: /journal-review 2026-02-01 to 2026-02-28
系统提示: "检测到全部28天已处理，是否：
  1. 跳过（推荐）
  2. 强制重新处理（会检查重复）
  3. 查看现有回顾"
```

### 场景 3: 跨月日期范围

```
用户: /journal-review 2026-02-25 to 2026-03-02
系统: 
  - 处理 02-25 至 02-28 → Raw2026-02.md
  - 处理 03-01 至 03-02 → Raw2026-03.md
  - 分别记录状态
```

---

## Resources

- [references/content-extraction.md](references/content-extraction.md) - 三池提取规则、支持自由格式日记
- [references/state-management.md](references/state-management.md) - 状态文件结构、归档机制、跨时间查询
- [references/deduplication.md](references/deduplication.md) - 去重逻辑、ID生成、冲突解决
- [references/configuration.md](references/configuration.md) - 完整配置选项、YAML示例

---

## Error Handling

| 场景 | 处理方式 |
|------|----------|
| 状态文件损坏 | 自动重建，扫描现有 Raw 文件和 Pool 文件恢复 |
| 日记文件被删除 | 标记为 `missing`，保留状态记录 |
| Pool 文件手动编辑后 ID 丢失 | 重新扫描生成 ID，合并重复项 |
| 跨月日期 | 分别处理到对应月度文件，状态分别记录 |

---

## Configuration

基础配置（USER.md）：

```yaml
journal_review:
  vault_path: "/path/to/vault"
  journal_folder: "4.0 Journal"
  cron_day: "sunday"
  cron_time: "21:00"
  
  deduplication:
    strict: true
    state_file: ".jr-state.json"
  
  archiving:
    enabled: true
    keep_months: 3
```

完整配置: [references/configuration.md](references/configuration.md)
