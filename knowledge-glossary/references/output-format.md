# Knowledge Glossary Output Format

Use this structure for a full project glossary or ubiquitous language. Adapt section names to the project domain.

## Header

```markdown
# Knowledge Glossary - <Project Name>

> Domain: <domain / market / product area>
> Last updated: YYYY-MM-DD
```

## Term Tables

Group terms by strategic category. Use this table schema:

```markdown
## <Category>

| Term | Definition | Use instead of / aliases to avoid | Confused with |
| ---- | ---------- | --------------------------------- | ------------- |
| **Term** | Project-specific definition | Alias 1, Alias 2 | Similar term - concise distinction |
```

Suggested categories:
- Product and positioning
- Business model
- Technical architecture
- Customer and market
- Workflow and operations
- Strategy and narrative
- Domain-specific concepts

## Relationships

Capture concept links as concise bullets. Express cardinality or direction when obvious:

```markdown
## Relationships

- A **Customer** can have many **Users**.
- An **Order** produces one or more **Invoices** after fulfillment.
- **Concept C** is the user-facing entry point; **Concept D** is the paid delivery layer.
- **Concept E** should not be confused with **Concept F**: E means ..., F means ...
```

Good relationships are causal, directional, or decision-relevant. Avoid vague links such as "A is related to B."

## Example Dialogue

Use this section when terminology has caused confusion in team conversations. Keep it short, practical, and precise:

```markdown
## Example Dialogue

> **Founder:** "When I say X, I do not mean Y. I mean ..."
>
> **Product:** "So the public wording should be ..."
>
> **Founder:** "Exactly."
```

Keep dialogue short. Its job is to show usage, not dramatize the meeting.

## Flagged Ambiguities

```markdown
## Flagged Ambiguities

- **"Term A" vs "Term B"**: Explain the ambiguity, why it matters, and recommended wording.
- **"Old positioning" vs "new positioning"**: Explain which term to use now and which term is deprecated.
```

Each ambiguity should include a clear recommendation and one of:
- recommended wording
- deprecated wording
- decision needed
- needs validation

## Analogies

```markdown
## Analogies

- **Concept A vs Concept B** is like ...
```

Use analogies sparingly. Prefer analogies that help explain the project to investors, teammates, customers, or future AI agents.

## Final Metadata

```markdown
> Last updated: YYYY-MM-DD
```

## Mini Example

```markdown
# Knowledge Glossary - Example AI Research Tool

> Domain: AI research workflow / knowledge infrastructure
> Last updated: 2026-01-15

## Product and Positioning

| Term | Definition | Use instead of / aliases to avoid | Confused with |
| ---- | ---------- | --------------------------------- | ------------- |
| **Trusted Research Context** | The product's core promise: convert scattered research sources into traceable context that an AI agent can use with lower hallucination risk. | Evidence layer, source-grounded context | AI search - search returns links; trusted context organizes evidence for downstream decisions. |
| **Source Graph** | A structured map of papers, patents, datasets, claims, and citations used to show where an answer came from. | Folder of sources, citation dump | Knowledge graph - a source graph can be simpler and focused on evidence provenance. |
| **Agent Workflow** | The model-led process that plans steps, calls tools, and produces outputs using the trusted context. | Magic AI flow, automation | Data preparation - data preparation creates inputs; agent workflow decides what to do with them. |

## Relationships

- **Trusted Research Context** is the input layer; **Agent Workflow** is the execution layer.
- **Source Graph** makes **Trusted Research Context** auditable by preserving relationships among evidence.
- The product should sell **decision confidence**, not just faster search.

## Flagged Ambiguities

- **"Research assistant" vs "research infrastructure"**: The first sounds like an application; the second supports the broader strategy. Use **research infrastructure** for investor-facing copy unless the audience is non-technical; treat "research assistant" as an alias to avoid in strategic docs.
```

