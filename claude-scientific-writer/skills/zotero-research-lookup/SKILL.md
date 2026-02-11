---
name: zotero-research-lookup
description: Research from a local Zotero library through MCP. Use a deterministic workflow: check search DB status, run semantic search, retrieve metadata + fulltext for top items, and fall back to keyword search when needed.
allowed-tools: [Read, Bash]
license: MIT license
---

# Zotero Research Lookup

## Overview

Use this skill when the source of truth should be the user's local Zotero library instead of web search APIs.

Primary workflow:
1. Check semantic index status
2. Run semantic search
3. Retrieve metadata and fulltext from top items
4. Extract query-relevant evidence snippets from returned fulltext
5. Return traceable citations (item key and Zotero URL)

## When to Use

Use this skill for:
- Local literature review and evidence gathering
- Verifying claims against already curated papers
- Draft support where stable citations are required
- Querying notes/annotations from local library context

Do not use this skill when the request requires latest web-only sources outside the local Zotero library.

## Required MCP Tools

- `zotero_get_search_database_status`
- `zotero_semantic_search`
- `zotero_get_item_metadata`
- `zotero_get_item_fulltext`
- `zotero_search_items` (fallback)

## Default Parameters

- Semantic search `limit`: `5`
- Evidence snippets per item: `1-3` concise quotes from returned fulltext
- Retrieval policy: semantic search first, keyword search fallback

## Deterministic Workflow

### Step 1: Check Index Health

Call `zotero_get_search_database_status`.

If document count is `0` or tool reports not initialized, return this action:
- Run `zotero-mcp update-db`
- For better semantic quality with local PDFs: `zotero-mcp update-db --fulltext`

### Step 2: Semantic Retrieval

Call `zotero_semantic_search` with:
- `query`: user question
- `limit`: default `5` (or user override)
- `filters`: optional dictionary

If semantic search errors or returns empty, fallback to `zotero_search_items` using the same query.

### Step 3: Evidence Collection Per Item

For each top result (ranked order):
1. Extract `item_key`
2. Call `zotero_get_item_metadata(item_key=<item_key>)` to capture canonical citation fields
3. Call `zotero_get_item_fulltext(item_key=<item_key>)`
4. From returned fulltext markdown/text, extract `1-3` short snippets most relevant to the original query
5. If no fulltext is available, keep metadata-only evidence and mark the limitation

### Step 4: Response Assembly

Return output in this order:
1. Query summary (1-2 lines)
2. Ranked evidence list
3. Concise synthesis across items
4. Gaps/uncertainty notes

Per item include:
- Rank
- Title
- Authors
- Year/date if available
- `item_key`
- Similarity score (if available)
- 1-3 evidence snippets
- Link: `zotero://select/items/<ITEM_KEY>`

## Output Contract

Use this structure:

```markdown
## Query
<user query>

## Top Evidence
### 1) <title>
- item_key: <key>
- authors: <authors>
- year: <year>
- relevance: <score>
- evidence:
  - "..."
  - "..."
- zotero_url: zotero://select/items/<key>

## Synthesis
- ...

## Limitations
- ...
```

## Failure Handling

- Single-item failure: skip item, continue with remaining results, and report skipped key.
- No fulltext available: retain metadata result and report that only metadata-level evidence exists.
- Context budget exceeded: reduce `limit` first, then shorten snippet count per item.

## Quick Start

Use `scripts/run_lookup.sh` to generate a ready-to-paste execution prompt for Claude.

Examples are in `scripts/examples.md`.
