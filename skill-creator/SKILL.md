---
name: skill-creator
description: Create or update OpenClaw skills. Use when designing, structuring, or packaging skills with scripts, references, and assets. Triggers when user wants to create a new skill, modify existing skill, or needs guidance on skill best practices.
---

# Skill Creator

This skill provides guidance for creating effective OpenClaw skills.

## About Skills

Skills are modular, self-contained packages that extend OpenClaw's capabilities by providing specialized knowledge, workflows, and tools. They transform OpenClaw from a general-purpose agent into a specialized agent equipped with procedural knowledge.

### What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific CLIs or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, and assets for complex tasks

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with system prompt, conversation history, other skills' metadata, and the user request.

**Default assumption: OpenClaw is already very smart.** Only add context it doesn't already have. Challenge each piece: "Does OpenClaw really need this?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

| Level | Use When | Form |
|-------|----------|------|
| **High** | Multiple approaches valid, context-dependent decisions | Text-based instructions |
| **Medium** | Preferred pattern exists, some variation acceptable | Pseudocode or scripts with parameters |
| **Low** | Fragile/error-prone operations, consistency critical | Specific scripts, few parameters |

### Anatomy of a Skill

```
skill-name/
├── SKILL.md              # Required - instructions and metadata
├── scripts/              # Optional - executable code
├── references/           # Optional - documentation, schemas
└── assets/               # Optional - templates, boilerplate
```

#### SKILL.md Structure

**Frontmatter (YAML):**
```yaml
---
name: skill-name
description: Clear description including what the skill does AND when to use it.
metadata:
  openclaw:
    emoji: "🔧"
    requires:
      bins: ["cli-tool"]
---
```

**Body (Markdown):** Instructions for using the skill and its resources.

### OpenClaw-Specific Metadata

Under `metadata.openclaw`:

- `emoji` - Visual identifier for the skill
- `requires.bins` - Array of required CLI tools
- `requires.env` - Required environment variables

## Skill Creation Process

Follow these steps in order. Skip only if clearly not applicable.

### Step 1: Understand with Concrete Examples

Ask the user:
- "What functionality should this skill support?"
- "Can you give examples of how this skill would be used?"
- "What would trigger this skill?"

Conclude when you have clear sense of supported functionality.

### Step 2: Plan Reusable Contents

Analyze each example:
1. How to execute from scratch?
2. What scripts/references/assets would help when repeating?

**Examples:**
- PDF rotation → `scripts/rotate_pdf.py`
- Webapp boilerplate → `assets/hello-world/` template
- Database queries → `references/schema.md`

### Step 3: Initialize the Skill

Create directory structure:

```bash
mkdir -p ~/.openclaw/workspace/skills/{skill-name}/{scripts,references,assets}
```

Generate SKILL.md template:

```markdown
---
name: {skill-name}
description: {description}
metadata:
  openclaw:
    emoji: "🔧"
---

# {Skill Name}

Brief description of what this skill does.

## When to Use

Specific triggers and contexts.

## Workflow

1. Step one
2. Step two
3. Step three

## Resources

- `scripts/example.py` - Description
- `references/guide.md` - Description

## Examples

### Example 1: Common use case

```
User: "Do X"
Response: Do Y then Z
```
```

### Step 4: Implement Resources

Start with reusable resources (scripts, references, assets).

**Scripts:**
- Must be tested by actually running
- Handle errors gracefully
- Include shebang and executable permissions if needed

**References:**
- Keep SKILL.md lean
- Load only when needed
- For files >100 lines, include table of contents

**Assets:**
- Not loaded into context
- Used in final output (templates, images)

### Step 5: Write SKILL.md Body

**Use imperative/infinitive form.**

Structure:
1. Brief overview
2. When to use (triggers)
3. Workflow/procedure
4. Resource references
5. Examples

**Progressive Disclosure Patterns:**

```markdown
# API Integration

## Quick Start

Basic usage example here.

## Advanced

- **Auth patterns**: See [AUTH.md](references/AUTH.md)
- **Error handling**: See [ERRORS.md](references/ERRORS.md)
```

### Step 6: Test and Iterate

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Update SKILL.md or resources
4. Test again

## Naming Conventions

- **Skill name**: lowercase, hyphens only, max 64 chars, verb-led
  - Good: `gh-address-comments`, `pdf-processor`, `obsidian-sync`
  - Bad: `PDF_Processor`, `my skill`, `github_stuff`
- **Folder name**: exactly matches skill name
- **Script names**: descriptive, hyphen-case, include extension

## What NOT to Include

Do NOT create:
- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- Any auxiliary documentation

The skill should only contain information needed for OpenClaw to do the job.

## Progressive Disclosure Best Practices

**Keep SKILL.md under 500 lines.**

**Pattern 1: High-level with references**
```markdown
## Quick start
Basic example

## Advanced features
- **Feature A**: See [A.md](references/A.md)
- **Feature B**: See [B.md](references/B.md)
```

**Pattern 2: Domain-specific organization**
```
cloud-deploy/
├── SKILL.md
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

**Avoid deeply nested references** - Keep references one level deep from SKILL.md.

## Example: Complete Skill

```
obsidian-sync/
├── SKILL.md
├── scripts/
│   └── daily-note.py
└── references/
    └── templates.md
```

**SKILL.md:**
```markdown
---
name: obsidian-sync
description: Sync and manage Obsidian vault notes. Use when working with Obsidian markdown files, daily notes, or vault organization.
metadata:
  openclaw:
    emoji: "📝"
    requires:
      bins: ["obsidian-cli"]
---

# Obsidian Sync

Manage Obsidian vault content efficiently.

## When to Use

- Creating daily notes
- Searching vault content
- Organizing notes

## Quick Start

Create daily note:
```bash
obsidian-cli daily
```

## Resources

- `scripts/daily-note.py` - Custom daily note generator
- `references/templates.md` - Note templates and formats
```

## Common Pitfalls

1. **Too verbose** - Trust OpenClaw's intelligence
2. **Missing triggers** - Description must include when to use
3. **Duplicate info** - Info in SKILL.md OR references, not both
4. **Wrong freedom level** - Simple tasks don't need scripts
5. **Untested scripts** - Always run scripts to verify

## Quick Reference

| Task | Action |
|------|--------|
| Create new skill | Follow 6-step process |
| Add script | Create in `scripts/`, test, reference in SKILL.md |
| Add reference | Create in `references/`, link from SKILL.md |
| Update skill | Edit → Test → Iterate |
| Name skill | lowercase-hyphens, verb-led, <64 chars |

## Resources in This Skill

- `references/output-patterns.md` - Templates and quality standards
- `references/workflows.md` - Multi-step process patterns
