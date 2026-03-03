# LLM Tagging Guide

Guidelines for auto-generating tags from journal content using LLM.

## Tag Categories

### 1. Insight Tags (#insight)
**Use when:** User expresses realization, understanding, or learning about themselves/life/work.

**Triggers:**
- "我意识到..."
- "突然明白..."
- "原来..."
- "感悟到..."
- "发现..." + personal realization
- "should have..." / "could have..."

**Examples:**
- "我意识到我总是拖延是因为害怕失败" → #insight
- "今天发现我对批评特别敏感" → #insight

### 2. Content Ideas (#idea/content)
**Use when:** Idea could become blog post, article, video, or social media content.

**Triggers:**
- "可以写一篇..."
- "这个可以分享..."
- "值得记录..."
- "内容选题..."
- Mentions: blog, article, post, content, video, 文章, 博客

**Examples:**
- "这个想法可以写一篇关于ADHD的博客" → #idea/content
- "记录下这个观察，可能做成视频" → #idea/content

### 3. Product Ideas (#idea/product)
**Use when:** Idea relates to products, features, apps, or business.

**Triggers:**
- "可以做个app..."
- "这个功能..."
- "产品化..."
- "创业想法..."
- Mentions: app, feature, product, 功能, 产品

**Examples:**
- "可以做个自动整理笔记的工具" → #idea/product
- "这个功能应该加入到现有产品里" → #idea/product

### 4. Story Seeds (#seed/story)
**Use when:** Personal experience that could become a narrative/story.

**Triggers:**
- Personal anecdotes
- Memorable encounters
- "那天..."
- "有一次..."
- "今天发生了一件事..."

**Examples:**
- "今天和孩子对话让我想到..." → #seed/story
- "上次那个项目失败的经历..." → #seed/story

### 5. Observation Seeds (#seed/observation)
**Use when:** Noticing something interesting about people, behavior, or patterns.

**Triggers:**
- "我发现..." + observation
- "有趣的是..."
- "注意到..."
- "pattern..."
- "trend..."

**Examples:**
- "发现大家在开会时都会看手机" → #seed/observation
- "注意到我每次焦虑时都会整理桌面" → #seed/observation

### 6. Fleeting Notes (#fleeting)
**Use when:** Raw thought that needs more processing.

**Triggers:**
- Incomplete thoughts
- Questions without answers
- "有个想法..." without elaboration
- "待思考..."
- "需要研究..."

**Examples:**
- "不知道AI会不会改变写作" → #fleeting
- "有个关于时间管理的问题" → #fleeting

### 7. Method Tags (#method)
**Use when:** Describing a process, technique, or approach that worked.

**Triggers:**
- "我发现一个方法..."
- "步骤是..."
- "workflow..."
- "process..."
- "技巧..."

**Examples:**
- "用番茄工作法提高了专注度" → #method
- "发现先写大纲再写内容更快" → #method

### 8. Principle Tags (#principle)
**Use when:** Generalizing a lesson into a guiding rule.

**Triggers:**
- "原则..."
- "重要的是..."
- "关键是..."
- "always..." / "never..." statements
- "should..." as general advice

**Examples:**
- "重要的是开始，不是完美" → #principle
- "不要在工作前查看邮件" → #principle

## Tagging Process

```
Input: User's raw journal content

Step 1: Analyze content type
- Is this a realization? → #insight
- Is this a creative idea? → #idea/content or #idea/product
- Is this an experience/observation? → #seed/story or #seed/observation
- Is this a raw/unprocessed thought? → #fleeting

Step 2: Extract secondary tags if applicable
- Does the insight include a method? → #insight #method
- Does the story contain an observation? → #seed/story #seed/observation

Step 3: Generate domain/context tags
- Work-related → #work
- Parenting-related → #parenting
- Health-related → #health
- Relationship-related → #relationship
- Creative-related → #creative

Step 4: Format output
[primary-tag] [secondary-tags] [domain-tags]
```

## Examples

### Input 1
"今天开会时突然意识到，我总是在担心别人的看法，这导致我不敢表达真实想法。可能是因为小时候被批评太多了。"

**Analysis:**
- Personal realization about behavior pattern
- Root cause analysis (childhood)
- Self-awareness moment

**Tags:** #insight #psychology #work

---

### Input 2
"有个想法，可以写一篇关于'如何用Notion管理ADHD'的文章，分享我的系统。可能很多人需要这个。"

**Analysis:**
- Content idea (article)
- Specific topic (Notion + ADHD)
- Value proposition (helping others)

**Tags:** #idea/content #adhd #productivity

---

### Input 3
"发现每次我想开始工作时，都会先整理桌面、倒杯水、检查邮件——其实都是在拖延。真正的开始应该是直接打开文档写第一个字。"

**Analysis:**
- Observation of personal behavior
- Identified procrastination pattern
- Proposed solution/method

**Tags:** #seed/observation #insight #method #procrastination

---

### Input 4
"不知道未来的AI助手会是什么样子，会不会真的能理解上下文和情绪？"

**Analysis:**
- Open question
- No clear direction
- Needs more thinking

**Tags:** #fleeting #ai #future

## Output Format

For each captured item, return:

```json
{
  "primary_tag": "#insight",
  "secondary_tags": ["#method"],
  "domain_tags": ["#work", "#productivity"],
  "confidence": 0.9,
  "reasoning": "User described a personal realization about their workflow"
}
```

## Multi-Tag Rules

1. **Always include primary tag** - most specific category
2. **Add secondary tags** - if content spans multiple types
3. **Include domain tags** - contextual area (work/parenting/health)
4. **Maximum 4-5 tags** - avoid over-tagging
5. **Be specific** - prefer #procrastination over #psychology

## Tag Priority

When content could fit multiple categories:

1. **#insight** > #fleeting (if there's realization)
2. **#method** > #insight (if it's about process)
3. **#seed/story** > #seed/observation (if it's personal experience)
4. **#idea/product** > #idea/content (if it's product-related)
