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
1. Check semantic index status and retriever mode
2. Run semantic search
3. Use `matched_content` (advanced_rag) or retrieve fulltext (legacy) for evidence
4. Return traceable citations (item key and Zotero URL)

## When to Use

Use this skill for:
- Local literature review and evidence gathering
- Verifying claims against already curated papers
- Draft support where stable citations are required
- Finding methods, protocols, or technical details from saved papers
- Querying notes/annotations from local library context

Do not use this skill when:
- The request requires **very recent papers** not yet in the user's Zotero library
- Statistical data from current surveys/reports is needed (Zotero indexes what the user has saved, not the full web)
- Citation counts, journal impact factors, or h-index data are required (not available in Zotero metadata)

**Scope limitation**: This skill searches only the user's curated Zotero library. Coverage depends entirely on what the user has imported. If a topic returns few or no results, fall back to `claude-scientific-writer:semantic-scholar-lookup` to search the open Semantic Scholar corpus.

## Retriever Modes

The `retriever_mode` field in `zotero_get_search_database_status` determines search behavior:

| Mode | Index content | Evidence source | Quality |
|------|--------------|-----------------|---------|
| `legacy_metadata` | Title + abstract + authors | Call `zotero_get_item_fulltext` separately | Basic |
| `legacy_fulltext` | Metadata + extracted PDF text | Call `zotero_get_item_fulltext` separately | Moderate |
| `advanced_rag` | Markdown chunks (paragraph-level) with Rerank | `matched_content` in search result | Best |

**advanced_rag mode** (recommended) requires:
- `retriever_mode: "advanced_rag"` in `~/.config/zotero-mcp/config.json`
- `md_root` pointing to MinerU-converted Markdown files
- Index built with `zotero-mcp update-db --rebuild`

In advanced_rag, each result already contains `matched_content`—the exact chunk that matched the query, reranked by a cross-encoder. **Do not call `zotero_get_item_fulltext` for every item**; use `matched_content` directly and call fulltext only when deeper context is needed.

## Required MCP Tools

- `zotero_get_search_database_status`
- `zotero_semantic_search`
- `zotero_get_item_metadata`
- `zotero_get_item_fulltext` (legacy modes or when deeper context needed)
- `zotero_search_items` (keyword fallback)

## Default Parameters

- Semantic search `limit`: `5`
- `include_citation_references`: `true` (advanced_rag returns `resolved_citations` per item)
- `citation_max_items_per_result`: `8`
- Evidence snippets per item: `1-3` from `matched_content` (advanced_rag) or fulltext (legacy)
- Retrieval policy: semantic search first, keyword search fallback

## Deterministic Workflow

### Step 1: Check Index Health

Call `zotero_get_search_database_status`.

Inspect the response:
- `retriever_mode`: determines evidence strategy (see table above)
- `collection_info.document_count`: if `0`, the index is empty
- `advanced_rag.candidate_k`: number of candidates before reranking (default 30)
- `advanced_rag.meta_weight`: metadata blending weight (default 0.70)
- `reranker_status.enabled`: whether FlashRank reranking is active

If document count is `0` or not initialized:
- `advanced_rag` mode: run `zotero-mcp update-db --rebuild` (requires `md_root` configured)
- `legacy` modes: run `zotero-mcp update-db` (add `--fulltext` for PDF text extraction)

### Step 2: Semantic Retrieval

Call `zotero_semantic_search` with:
- `query`: user question
- `limit`: default `5` (or user override)
- `filters`: optional metadata filter dict (e.g. `{"year": "2023"}`)
- `include_citation_references`: `true` to get `resolved_citations` (advanced_rag only)
- `abstract_max_chars` / `matched_content_max_chars`: optional truncation controls

If semantic search errors or returns empty, fallback to `zotero_search_items` using the same query.

### Step 3: Evidence Collection Per Item

**advanced_rag mode** (preferred):
1. Extract `item_key`, `similarity_score`, `matched_content` directly from result
2. `matched_content` = the reranked chunk(s) that best matched the query—use as primary evidence
3. `resolved_citations` = reference list entries cited within this chunk (e.g. `[1] Author et al. 2020`)—use to surface additional relevant papers
4. Call `zotero_get_item_metadata(item_key)` for canonical citation fields
5. Call `zotero_get_item_fulltext` only if `matched_content` lacks sufficient context

**legacy modes**:
1. Extract `item_key` and `similarity_score` from result
2. Call `zotero_get_item_metadata(item_key)` for citation fields
3. Call `zotero_get_item_fulltext(item_key)` and extract `1-3` relevant snippets
4. If no fulltext available, keep metadata-only evidence and mark the limitation

## Query Construction

Zotero semantic search uses vector embeddings—query phrasing matters. Use these patterns:

**Structured format**: `[concept] + [aspect] + [context/field]`

| Query type | Example |
|-----------|---------|
| Literature review opening | `"theoretical frameworks for [topic] review"` |
| Empirical evidence | `"[intervention] effect on [outcome] [population]"` |
| Methods/protocols | `"[method name] procedure protocol [field]"` |
| Gap identification | `"limitations future research [sub-topic]"` |
| Comparative | `"[concept A] versus [concept B] [field]"` |
| Mechanism | `"mechanism [phenomenon] [field]"` |

**Tips:**
- Use field-specific terminology matching the papers in your library
- For broad topics, run **multiple targeted queries** per sub-theme rather than one vague query
- Apply `filters` (e.g. `{"year": "2022"}`) to scope searches by year or other metadata
- If results are poor, try synonyms or broader phrasing

## Step 4: Response Assembly (Expanded)

Return output in this order:
1. Query summary (1-2 lines)
2. Ranked evidence list
3. Synthesis across items
4. Gaps/uncertainty notes

Per item include:
- Rank
- Title, authors, year, journal/venue
- `item_key` and similarity score
- 1-3 evidence snippets (from `matched_content` or fulltext)
- `resolved_citations` if present (list notable cited references)
- Link: `zotero://select/items/<ITEM_KEY>`

**Synthesis** should cover:
- Research consensus: what do multiple sources agree on?
- Contradictions or debates across sources
- Methodological patterns (what methods dominate?)
- Identified research gaps explicitly mentioned in the papers
- Which sources are most directly relevant to the query

**Note**: Zotero metadata includes journal name and year but not citation counts or impact factors. When journal quality matters, report the journal name and let the user assess.

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
- resolved_citations: [1] Author et al. 2020 — <title snippet>
- zotero_url: zotero://select/items/<key>

## Synthesis
- ...

## Limitations
- ...
```

## Failure Handling

- Single-item failure: skip item, continue with remaining results, and report skipped key.
- No `matched_content` (advanced_rag): fall back to `zotero_get_item_fulltext`.
- No fulltext available: retain metadata result and report that only metadata-level evidence exists.
- Context budget exceeded: reduce `limit` first, then shorten snippet count per item.
- Semantic search returns empty or irrelevant results: fall back to `claude-scientific-writer:semantic-scholar-lookup` to search the open Semantic Scholar corpus with the same query.

## Quick Start

Use `scripts/run_lookup.sh` to generate a ready-to-paste execution prompt for Claude.

Examples are in `scripts/examples.md`.
