# Zotero Deep Research Skill Design

**Date:** 2026-02-23
**Status:** Approved

## Overview

Create a new `zotero-deep-research` skill that implements iterative deep research workflow using Zotero library through MCP. The workflow combines query generation, semantic search, reflection, and answer synthesis - adapted from gemini-fullstack-langgraph-quickstart's deep research agent, with web search replaced by Zotero semantic search.

## Architecture

### Skill Location
```
claude-scientific-writer/skills/zotero-deep-research/
├── SKILL.md
├── prompts/
│   ├── query_writer.txt
│   ├── reflection.txt
│   └── answer.txt
└── scripts/
    └── run_lookup.sh
```

### Workflow

```
User Question
    │
    ▼
generate_query (LLM)
    │ Generate 3-5 optimized queries
    ▼
Parallel zotero_search × N
    │ • zotero_semantic_search(query)
    │ • zotero_get_item_metadata(key)
    │ • zotero_get_item_fulltext(key)
    │ • Extract evidence snippets
    ▼
reflection (LLM)
    │ • Analyze results
    │ • Identify knowledge_gap
    │ • Determine is_sufficient
    │ • Generate follow_up_queries
    ▼
evaluate_research
    │ • is_sufficient == true → finalize
    │ • is_sufficient == false + under limit → continue search
    ▼
finalize_answer (LLM)
    • Deduplicate sources
    • Generate structured answer
    • Include Zotero citations
```

## Core Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| max_research_loops | 2 | Maximum iteration rounds |
| number_of_initial_queries | 3 | Initial query count |
| top_n_per_query | 5 | Results per query |

## MCP Tool Dependencies

- `zotero_get_search_database_status` - Check index status
- `zotero_semantic_search` - Semantic search
- `zotero_get_item_metadata` - Get metadata
- `zotero_get_item_fulltext` - Get fulltext
- `zotero_search_items` - Keyword search (fallback)

## Output Format

```markdown
## Research Topic
<User question>

## Search Results (Round X)

### 1) <Title>
- item_key: <key>
- authors: <authors>
- year: <year>
- relevance: <score>
- source_query: <which query returned this>
- evidence:
  - "..."
  - "..."
- zotero_url: zotero://select/items/<key>

...

## Reflection
- knowledge_gap: <gap>
- is_sufficient: <true/false>
- follow_up_queries: <if needed>

## Final Answer
<Comprehensive answer based on all evidence>

## Citations
- [1] <title> - zotero://select/items/<key>
- [2] ...
```

## Failure Handling

| Scenario | Handling |
|----------|----------|
| Index not initialized | Prompt to run `zotero-mcp update-db` |
| Single item fetch failure | Skip, record skipped key |
| No fulltext available | Use metadata only, mark limitation |
| Context overflow | Reduce top_n, reduce snippets |

## Prompt Adaptation

### Query Writer
Adapted from `gemini-fullstack-langgraph-quickstart/prompts.py`:
- Generate diverse queries covering different aspects
- Ensure queries are specific for academic literature search
- Output: JSON with rationale + query list

### Reflection
Adapted from `reflection_instructions`:
- Analyze search results
- Identify knowledge gaps
- Determine if sufficient for answering question
- Generate follow-up queries if needed

### Answer
Adapted from `answer_instructions`:
- Synthesize findings
- Include Zotero citations
- Format as markdown
