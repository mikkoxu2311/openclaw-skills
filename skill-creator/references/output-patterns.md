# Output Patterns

Templates and quality standards for skill outputs.

## When to Use This Reference

- Defining consistent output formats
- Establishing quality checklists
- Creating templates for skill outputs

## Template Patterns

### Pattern 1: Simple Output Format

For skills with consistent, simple output:

```markdown
## Output Format

```
[Field 1]: [Value]
[Field 2]: [Value]

[Main content]
```
```

### Pattern 2: Structured Report

For analytical or review skills:

```markdown
## Output Structure

### Summary
One-paragraph overview.

### Details
| Item | Status | Notes |
|------|--------|-------|
| A | ✅ | ... |
| B | ⚠️ | ... |

### Recommendations
1. First recommendation
2. Second recommendation
```

### Pattern 3: Code-Heavy Output

For skills generating code or configs:

```markdown
## Output Structure

**Files created:**
- `path/to/file1` - Purpose
- `path/to/file2` - Purpose

**Usage:**
```bash
command to run
```

**Next steps:**
1. Step one
2. Step two
```

## Quality Checklists

### Pre-Output Checklist

Before delivering output, verify:

- [ ] Output matches user's implicit or explicit format request
- [ ] All requested information is included
- [ ] No hallucinated information
- [ ] Technical details verified (if applicable)

### Code Output Checklist

- [ ] Code is syntactically correct
- [ ] Error handling included
- [ ] Comments for non-obvious logic
- [ ] Tested or clearly marked as untested

### Document Output Checklist

- [ ] Clear structure with headers
- [ ] Consistent formatting
- [ ] No placeholder text remaining
- [ ] Appropriate detail level for audience

## Example-Driven Quality

When possible, provide examples rather than specifications:

**Instead of:**
```markdown
The output should include all relevant fields from the input.
```

**Prefer:**
```markdown
## Example

Input:
```
name: John, age: 30
```

Output:
```
User Profile: John (30 years old)
```
```

## Progressive Detail

Start with the minimal viable format, then expand:

1. **Basic** - Core information only
2. **Standard** - Core + common optional fields
3. **Complete** - All possible fields

Document all three levels so OpenClaw can match the user's need.
