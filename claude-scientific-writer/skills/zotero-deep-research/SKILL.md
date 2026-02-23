---
name: zotero-deep-research
description: Iterative deep research workflow using Zotero library through MCP. Combines query generation, semantic search, reflection, and answer synthesis for comprehensive literature research.
allowed-tools: [Read, Bash]
license: MIT license
---

# Zotero Deep Research

## Overview

Implements iterative deep research workflow using Zotero library. Based on gemini-fullstack-langgraph-quickstart's research agent pattern, with web search replaced by Zotero semantic search.

## When to Use

Use this skill for:
- Comprehensive literature reviews requiring multiple search angles
- In-depth research on academic topics
- Identifying knowledge gaps in existing research
- Building comprehensive evidence base for academic writing

Do not use this skill when:
- Quick single-query lookups are sufficient (use zotero-research-lookup)
- The Zotero library is not populated with relevant papers

## Required MCP Tools

- `zotero_get_search_database_status` - Check index status
- `zotero_semantic_search` - Semantic search
- `zotero_get_item_metadata` - Get item metadata
- `zotero_get_item_fulltext` - Get fulltext content
- `zotero_search_items` - Keyword search (fallback)

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| max_research_loops | 2 | Maximum iteration rounds |
| number_of_initial_queries | 3 | Initial query count |
| top_n_per_query | 5 | Results per query |

## Workflow

### Step 1: Query Generation
Read `prompts/query_writer.txt` and invoke LLM to generate 3-5 optimized queries based on user's research topic.

### Step 2: Parallel Zotero Search
For each generated query:
1. Call `zotero_semantic_search(query=query, limit=top_n_per_query)`
2. For each result, call `zotero_get_item_metadata(item_key=key)`
3. Call `zotero_get_item_fulltext(item_key=key)`
4. Extract 1-3 evidence snippets relevant to the research topic

### Step 3: Reflection
Read `prompts/reflection.txt` and invoke LLM to:
- Analyze collected papers and evidence
- Determine if sufficient to answer the question
- Identify knowledge gaps
- Generate follow-up queries if needed

### Step 4: Evaluate Research
- If is_sufficient == true → proceed to finalize
- If is_sufficient == false and research_loop_count < max_research_loops → return to Step 2 with follow-up queries
- If is_sufficient == false and research_loop_count >= max_research_loops → proceed to finalize

### Step 5: Finalize Answer
Read `prompts/answer.txt` and invoke LLM to:
- Synthesize all collected evidence
- Generate comprehensive answer
- Include proper Zotero citations

## Output Format

```markdown
## Research Topic
<user question>

## Search Results (Round X)
### 1) <title>
- item_key: <key>
- authors: <authors>
- year: <year>
- relevance: <score>
- source_query: <query that returned this>
- evidence:
  - "..."
- zotero_url: zotero://select/items/<key>

## Reflection
- knowledge_gap: <gap description or "none">
- is_sufficient: <true/false>
- follow_up_queries: <queries or []>

## Final Answer
<comprehensive answer>

## Citations
- [1] <title> [Author, Year] - zotero://select/items/<key>
```

## Failure Handling

| Scenario | Handling |
|----------|----------|
| Index not initialized | Prompt to run `zotero-mcp update-db` |
| Single item fetch failure | Skip item, continue, log skipped key |
| No fulltext available | Use metadata only, mark limitation |
| Context overflow | Reduce top_n_per_query, reduce snippets |

## Prompt Files

- `prompts/query_writer.txt` - Query generation prompt
- `prompts/reflection.txt` - Reflection analysis prompt
- `prompts/answer.txt` - Final answer synthesis prompt

## Example Usage

Use `scripts/run_lookup.sh` to generate a ready-to-paste execution prompt for Claude.
