---
name: lookup
description: Unified literature search with Zotero-first strategy. Search your local Zotero library with automatic fallback to external search when configured.
allowed-tools: [Read, Write, Edit, Bash]
---

# Unified Literature Lookup

Search literature from your personal Zotero library with intelligent fallback to external search.

## Overview

This module provides a unified interface for literature search:
- **Primary**: Zotero local library via zotero-mcp (default)
- **Fallback**: External search via research-lookup (requires OPENROUTER_API_KEY)

## Key Features

1. **Local-First Search**
   - Default to searching your Zotero library
   - Semantic search for better relevance
   - Sort by year (newest first)

2. **Automatic Fallback**
   - Falls back to external search only when 0 local results
   - Requires OPENROUTER_API_KEY environment variable
   - Falls back gracefully without API key

3. **Unified Output**
   - Consistent result format across sources
   - BibTeX citations included
   - Deduplication support

## Usage

```python
from scientific_writer import UnifiedLiteratureLookup, LookupConfig

# Default config (Zotero first)
lookup = UnifiedLiteratureLookup()

# Search local library
result = lookup.search("transformer attention mechanism")

# Check results
for paper in result.papers:
    print(f"{paper.title} ({paper.year})")
    print(paper.bibtex)
```

## Search Flow

```
1. Search Zotero library (semantic by default)
   ↓
2. If 0 results and OPENROUTER_API_KEY set:
   Search external databases
   ↓
3. Return unified results
```

## Fallback Behavior

| Condition | Behavior |
|-----------|----------|
| Local 0 + API key | Fallback to external search |
| Local 0 + no API | Continue with 0 results, log warning |
| Local >=1 | Use local, no fallback |

## Output Format

```python
StandardLiteratureResult:
  - query: str           # Original search query
  - source: str          # "zotero", "research-lookup", or "none"
  - papers: list[PaperEntry]  # Found papers
  - total_count: int     # Number of papers
  - search_performed: str  # "local_only" or "local_with_fallback"
  - fallback_info: dict  # Fallback status if triggered
```

## Configuration

Create `lookup.yaml` in your project root:

```yaml
zotero:
  prefer_semantic_search: true

research_lookup:
  fallback_on_empty: true  # Only fallback on 0 results
```

Or use environment variables:
- `OPENROUTER_API_KEY`: Enable external search fallback

## Integration

Use with writing workflow:

```python
from scientific_writer import UnifiedLiteratureLookup

lookup = UnifiedLiteratureLookup()

# Get papers for writing
papers = lookup.get_citations_for_writing([
    "deep learning foundations",
    "attention mechanism",
    "transformer architecture"
])

# Papers are deduplicated and sorted by year
```
