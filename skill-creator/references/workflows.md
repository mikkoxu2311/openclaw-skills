# Workflow Patterns

Multi-step process patterns for complex skills.

## When to Use This Reference

- Designing multi-step skills
- Handling conditional logic
- Managing state across steps

## Sequential Workflow

For processes with clear, linear steps:

```markdown
## Workflow

### Step 1: [Action Name]
[Clear instruction]

### Step 2: [Action Name]
[Clear instruction]

### Step 3: [Action Name]
[Clear instruction]
```

**When to use:** File processing, setup procedures, document creation

## Decision Tree Workflow

For processes with significant branching:

```markdown
## Workflow

1. **Assess [condition]**
   - If A → Go to step 2A
   - If B → Go to step 2B
   - If C → Go to step 2C

2A. **[Action for A]**
    [Instructions]
    → Go to step 3

2B. **[Action for B]**
    [Instructions]
    → Go to step 3

2C. **[Action for C]**
    [Instructions]
    → Go to step 3

3. **[Common final step]**
```

**When to use:** Troubleshooting, deployment choices, format conversions

## Iterative Workflow

For processes that loop until completion:

```markdown
## Workflow

Initialize: [Starting state]

Loop:
1. [Process item]
2. [Update state]
3. Check: [Completion condition]
   - If complete → Exit
   - If not → Continue loop

Finalize: [Cleanup actions]
```

**When to use:** Batch processing, review all items, pagination

## State-Machine Workflow

For complex processes with distinct states:

```markdown
## States

- `idle` - Initial state
- `processing` - Active work
- `review` - Pending verification
- `complete` - Finished
- `error` - Issue encountered

## Transitions

| From | Event | To | Action |
|------|-------|-----|--------|
| idle | start | processing | [Action] |
| processing | success | review | [Action] |
| processing | fail | error | [Action] |
| review | approve | complete | [Action] |
| review | reject | processing | [Action] |
| error | retry | processing | [Action] |
| error | abort | idle | [Action] |
```

**When to use:** Complex automation, approval workflows, error recovery

## User-Checkpoint Workflow

For processes requiring user confirmation:

```markdown
## Workflow

### Phase 1: [Automated work]
[Actions OpenClaw performs]

### Checkpoint 1
Present to user:
- [Summary of work done]
- [Preview of next steps]

Wait for user input:
- "continue" → Proceed to Phase 2
- "modify" → Adjust based on feedback
- "abort" → Stop with cleanup

### Phase 2: [Conditional on continue]
[Next actions]
```

**When to use:** Destructive operations, significant changes, multi-stage approvals

## Error Handling Patterns

### Fail-Fast

Stop immediately on any error:

```markdown
## Error Handling

If any step fails:
1. Stop workflow immediately
2. Report specific error
3. Suggest fix or rollback
```

**When to use:** Setup procedures, data migrations

### Continue-with-Logging

Log errors but continue:

```markdown
## Error Handling

For each item:
1. Try processing
2. If success → Continue
3. If fail → Log error, mark as failed, continue to next

Final report includes:
- Success count
- Failed items with specific errors
```

**When to use:** Batch processing, review tasks

### Retry-with-Backoff

Retry failed operations:

```markdown
## Error Handling

On failure:
1. Log attempt
2. Wait [delay] seconds
3. Retry (max [N] attempts)
4. If all fail → Escalate to user
```

**When to use:** API calls, network operations

## Best Practices

1. **Always define exit conditions** - How does the workflow end?
2. **Prefer early validation** - Check prerequisites first
3. **Make state explicit** - What is the current status?
4. **Plan for interruption** - Can the workflow resume?
5. **Clean up on failure** - Leave system in known state
