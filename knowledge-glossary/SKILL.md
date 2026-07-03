---
name: knowledge-glossary
description: Create a project-specific knowledge glossary from messy notes, strategy docs, meeting transcripts, product discussions, or founder language. Use when the user wants to turn ambiguous project language into a reusable concept map, align team vocabulary, clarify strategic terms, distinguish commonly confused concepts, or give future AI agents durable domain context before writing strategy, product, research, or fundraising materials.
---

# Knowledge Glossary

## Purpose

Turn scattered project language into a durable concept system that future humans and AI agents can reuse. The output is not a generic dictionary; it is a project-specific map of terms, definitions, aliases, confusions, relationships, ambiguities, and analogies.

Use this skill to help a team agree on what its own words mean before producing strategy docs, pitch decks, PRDs, research reports, positioning, or other high-context artifacts.

## Core Workflow

1. **Collect source context**
   - Read the user-provided notes, docs, meeting summaries, transcripts, or existing glossary.
   - If the project has durable instructions or background docs, read those first.
   - Preserve source-specific meaning. Do not replace project language with generic industry definitions.

2. **Extract candidate terms**
   - Prioritize terms that affect strategy, product direction, technical architecture, business model, or team alignment.
   - Include terms that the team repeats, argues about, uses inconsistently, or treats as obvious.
   - Exclude ordinary nouns unless they carry a project-specific meaning.

3. **Classify term importance**
   - `🟢` Core: must be understood by anyone working on the project.
   - `🟡` Supporting: important for interpreting the project, but not the main positioning.
   - `🔴` Complex or high-leverage: nuanced, strategic, cross-domain, or often misunderstood.

4. **Define terms in project context**
   - Write definitions as "what this means in this project," not as encyclopedia entries.
   - Include cross-domain aliases when helpful, such as business, technical, academic, or investor-language equivalents.
   - Capture "confused with" distinctions whenever a wrong interpretation would change decisions.

5. **Map relationships**
   - Explain how key concepts depend on, contrast with, or reinforce each other.
   - Focus on causal or strategic relationships, not superficial associations.
   - Prefer concise bullets that future agents can reuse as context.

6. **Flag ambiguities**
   - Identify terms with multiple meanings inside the team.
   - Explain why the ambiguity matters.
   - Suggest the clearest wording to use going forward.

7. **Add examples and analogies**
   - Include short example dialogue when it reveals how the concept is used in real decisions.
   - Add analogies only when they make a complex distinction easier to explain.

## Output Format

Default to a single Markdown document named or titled `Knowledge Glossary - <Project Name>`.

Use the schema in `references/output-format.md` when the user asks for a full deliverable or when the source material is complex.

For lightweight requests, return only:
- `Core Terms`
- `Key Confusions`
- `Relationships`
- `Recommended Language`

## Quality Bar

- Make the glossary decision-useful, not comprehensive for its own sake.
- Prefer 15-40 high-value terms over a bloated list.
- Keep definitions short enough to scan.
- Use the user's language when it is precise; improve it when it is ambiguous.
- Mark uncertain definitions as "needs validation" instead of inventing certainty.
- Avoid exposing private source excerpts unless the user asks for traceability.

## Common Use Cases

- "Turn these founder notes into a project glossary."
- "Create a vocabulary map for this pitch deck."
- "Help future AI agents understand our product strategy."
- "Clarify which concepts we keep mixing up."
- "Create a knowledge glossary before rewriting this BP."
- "Update an existing glossary with new meeting notes."

## Update Existing Glossaries

When updating an existing glossary:
- Preserve its structure unless the user asks for a redesign.
- Add new terms in the most relevant section.
- Update definitions only when new source material clearly changes meaning.
- Add a "Last updated" line if the existing file uses one.
- Call out major changes in a short summary before or after the glossary.

