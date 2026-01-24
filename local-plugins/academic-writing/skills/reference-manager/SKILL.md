---
name: reference-manager
description: Manage academic references: search, match, expand, and parse PDF fulltext from Zotero library (supports both zotero-mcp and zotero-mcp-plugin)
---

# Reference Manager

## Overview

Manage academic references through Zotero MCP: search by semantic query, match user-provided references, expand to related literature, and parse fulltext content.

**Supports two Zotero MCP providers:**
- `zotero-mcp` (Python version) - see [hyperbolic-c/zotero-mcp](https://github.com/hyperbolic-c/zotero-mcp)
- `zotero-mcp-plugin` (TypeScript/Zotero Plugin version) - see [cookjohn/zotero-mcp](https://github.com/cookjohn/zotero-mcp)

**Configuration:**
- Run `/academic-writing setup` to select your preferred MCP provider
- Config stored in `~/.config/auto-writing/config.json`

## When to Use

- Need to find references in Zotero library
- Need to match user-provided reference titles with Zotero items
- Need to expand search to related literature
- Need to get fulltext content from PDF attachments

## Multi-Phase Retrieval Strategy

### Phase 1: Exact Matching

Match user-provided reference titles with Zotero items:

```
Input: List[str] of reference titles
Action: Search each title, fuzzy match results
Output: List of matched item keys
```

### Phase 2: Semantic Search

Search by research topic:

```
Input: Research topic description
Action: semantic_search(topic) or zotero_semantic_search(topic)
Output: List of items sorted by similarity
```

### Phase 3: Expansion

Expand to related literature:

```
Input: List of matched item keys
Actions:
  - Get item tags/keywords
  - Search by tags
  - Find related items
Output: Expanded list of item keys
```

## Tool Mapping (Based on Configuration)

### zotero-mcp (Python Version)

| Function | Description |
|----------|-------------|
| `zotero_search_items` | Keyword/title search |
| `zotero_semantic_search` | AI-powered semantic search |
| `zotero_get_item_metadata` | Get item details |
| `zotero_get_item_fulltext` | Get PDF fulltext as markdown |
| `zotero_search_by_tag` | Search by tags |

### zotero-mcp-plugin (TypeScript Version)

| Function | Description |
|----------|-------------|
| `search_library` | Keyword/title search |
| `semantic_search` | AI-powered semantic search |
| `get_item_details` | Get item details |
| `get_content` | Get PDF fulltext content |
| `search_fulltext` | Fulltext search |

## Configuration-Based Selection

The skill uses the configured MCP provider:

1. Read `mcp_provider` from `~/.config/auto-writing/config.json`
2. Use the corresponding tool set for the selected provider
3. Report selected provider in output

## Input Format

```markdown
{
  "topic": "Research topic description",
  "reference_titles": ["Title 1", "Title 2"],
  "additional_references": 5,
  "expand_from_references": true
}
```

## Processing Steps

1. **Read configuration** - Get `mcp_provider` from config file
2. **Fetch items** - Get items for matching (using selected provider's tools)
3. **Exact match** each reference title
4. **Semantic search** by topic if needed
5. **Expand** from matched items (if tools available for selected provider)
6. **Fetch fulltext** for matched items with PDF (using selected provider's tool)
7. **Return** parsed content + metadata

## Output Format

```markdown
**文献检索结果:**

- **MCP Provider:** {zotero-mcp | zotero-mcp-plugin}
- **精确匹配:** {n} 篇
- **语义检索:** {m} 篇
- **扩展检索:** {k} 篇
- **解析成功:** {p} 篇
- **跳过:** {s} 篇（无 PDF）

---

**已解析文献:**

### 1. {title1}
- **Key:** {key}
- **Authors:** {authors}
- **Date:** {date}
- **相似度/来源:** {similarity_score or "精确匹配"}

**内容摘要:**
{abstract or "无摘要"}

---

**全文内容:**
{fulltext_markdown}
```

## Error Handling

- **No items found:** Report zero results
- **Missing PDF attachment:** Skip and report
- **PDF conversion failed:** Report error, continue with abstract
- **Network/API errors:** Report and suggest retry
- **Configuration missing:** Prompt user to run `/academic-writing setup`

## Example

```markdown
Input:
{
  "topic": "CNN architectures for image recognition",
  "reference_titles": ["AlexNet", "VGGNet"],
  "additional_references": 5,
  "expand_from_references": true
}

Output:
**文献检索结果:**

- **MCP Provider:** zotero-mcp
- **精确匹配:** 2 篇
- **语义检索:** 8 篇
- **扩展检索:** 10 篇
- **解析成功:** 15 篇
- **跳过:** 5 篇（无 PDF）

---

**已解析文献:**

### 1. ImageNet Classification with Deep Convolutional Neural Networks
- **Key:** ABC123DEF
- **Authors:** Krizhevsky, A., et al.
- **Date:** 2012
- **相似度/来源:** 精确匹配

**内容摘要:**
We propose a deep convolutional neural network architecture for image classification...

---

**全文内容:**
[Markdown converted from PDF]
```

## Limitations by Provider

### zotero-mcp (Python Version)

- ✅ Full PDF text extraction via `zotero_get_item_fulltext`
- ✅ Tag-based expansion via `zotero_search_by_tag`
- ✅ Rich metadata and annotations

### zotero-mcp-plugin (TypeScript Version)

- ✅ Full PDF text extraction via `get_content`
- ⚠️ Limited tag-based expansion
- ✅ Semantic search with embedding vectors
- ✅ Streamable HTTP for real-time communication
