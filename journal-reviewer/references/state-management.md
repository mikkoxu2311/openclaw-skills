# State Management

状态文件的结构、归档机制和跨时间查询。

## 状态文件结构

### 活跃状态文件: `.jr-state.json`

保留最近 **3个月** 的详细状态，用于日常去重和冲突检测。

```json
{
  "version": "1.0",
  "activeWindow": {
    "startDate": "2026-02-01",
    "endDate": "2026-04-30"
  },
  "stats": {
    "totalProcessedDays": 60,
    "totalIdeas": 25,
    "totalSeeds": 12,
    "totalInsights": 40
  },
  "processedDates": {
    "2026-02-26": {
      "rawRecord": true,
      "pools": true,
      "review": "W09",
      "sourceFile": {
        "archived": true,
        "archivedAt": "2026-02-28T11:30:00Z",
        "originalPath": "4.0 Journal/2026-02-26.md",
        "archivePath": "4.0 Journal/Archive/raw_record/2026/2026-02-26.md"
      }
    }
  },
  "extractedItems": {
    "ideas": ["idea-20260226-a3f7b2"],
    "seeds": ["seed-20260207-b8c2d1"],
    "insights": ["insight-20260226-f2a9e3"]
  }
}
```

### 字段说明

| 字段 | 说明 |
|------|------|
| `activeWindow` | 当前活跃时间窗口（自动维护） |
| `stats` | 统计信息（快速概览） |
| `processedDates` | 已处理日期（仅活跃窗口内） |
| `processedDates.{date}.rawRecord` | 是否已进入 Raw Record |
| `processedDates.{date}.pools` | 是否已提取到 Pool |
| `processedDates.{date}.review` | 关联的回顾文件（`Wxx`或`manual-YYYYMMDD`） |
| `processedDates.{date}.sourceFile` | 源文件归档状态 |
| `extractedItems` | 已提取内容的唯一标识 |

## 归档状态文件: `.jr-state-archive.json`

历史状态的压缩存储，按年份/月份索引。

```json
{
  "version": "1.0",
  "archives": {
    "2026-01": {
      "dateRange": "2026-01-01 to 2026-01-31",
      "processedDays": 25,
      "extractedItems": {
        "ideas": ["idea-20260105-001"],
        "seeds": ["seed-20260107-001"],
        "insights": ["insight-20260105-001"]
      },
      "archivedAt": "2026-02-01T00:00:00Z"
    }
  },
  "yearlySummary": {
    "2026": {
      "totalProcessedDays": 60,
      "totalIdeas": 25,
      "totalSeeds": 12,
      "totalInsights": 40
    }
  }
}
```

## 自动归档机制

### 触发条件

- 每月1日凌晨自动归档上月数据
- 状态文件大小超过 100KB 时触发
- 手动运行 `/journal-review --archive`

### 归档逻辑

1. 将超过3个月的日期记录移到归档文件
2. 压缩 `extractedItems`（仅保留ID列表）
3. 保留活跃窗口的完整信息
4. 生成归档摘要

## 跨时间查询

### 场景

查询 2025年12月 的某日期是否已处理。

### 处理流程

```
1. 检查活跃状态文件（3个月窗口）
2. 未找到 → 查询归档文件的索引
3. 返回结果（是/否/未记录）
4. 如需详细内容，从归档文件中提取
```

### 性能

- **活跃文件**: < 50KB，内存加载快速查询
- **归档文件**: 按年份索引，延迟加载

## 文件大小估算

假设每天写日记，持续1年：

| 数据类型 | 每天 | 每月 | 每年 |
|----------|------|------|------|
| Processed Dates | 1条 | ~30条 | ~365条 |
| Ideas | 0.5条 | ~15条 | ~180条 |
| Seeds | 0.3条 | ~9条 | ~110条 |
| Insights | 0.5条 | ~15条 | ~180条 |

**活跃窗口 (3个月)**: ~20KB  
**全年归档**: ~50KB  
**5年总计**: < 500KB

## 状态维护

### 自动维护

- 活跃窗口自动滑动
- 每月自动归档
- 文件大小触发归档

### 手动维护

```bash
# 手动触发归档
/journal-review --archive

# 重建状态文件（从现有文件扫描）
/journal-review --rebuild-state
```

### 备份建议

定期备份 `.jr-state-archive.json`（历史记录）。
