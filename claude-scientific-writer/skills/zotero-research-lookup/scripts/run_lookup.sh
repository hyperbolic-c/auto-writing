#!/usr/bin/env bash
set -euo pipefail

QUERY="${1:-}"
TOP_N="${2:-5}"
FILTERS_JSON="${3:-null}"

if [[ -z "$QUERY" ]]; then
  echo "Usage: $0 \"query\" [top_n=5] [filters_json=null]"
  exit 1
fi

cat <<PROMPT
You are using Zotero MCP only (no web search). Execute this workflow exactly:

1) Call zotero_get_search_database_status.
- If DB is empty or uninitialized, stop and tell me to run:
  - zotero-mcp update-db
  - or zotero-mcp update-db --fulltext (preferred for richer evidence)

2) Call zotero_semantic_search with:
- query: "$QUERY"
- limit: $TOP_N
- filters: $FILTERS_JSON

3) For each returned item in rank order:
- Read item_key
- Call zotero_get_item_metadata with:
  - item_key: <item_key>
- Call zotero_get_item_fulltext with:
  - item_key: <item_key>
- Extract 1-3 short snippets from returned fulltext that best answer "$QUERY".
- If fulltext is unavailable, keep metadata-only evidence and note the limitation.

4) Produce final output sections:
- Query
- Top Evidence (ranked)
- Synthesis
- Limitations

5) Per evidence item include:
- title, authors, year/date, item_key, similarity score (if available)
- 1-3 quotes/snippets
- zotero_url: zotero://select/items/<item_key>
PROMPT
