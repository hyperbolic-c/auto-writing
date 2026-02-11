# Query Plan Template

Use this template to standardize tool invocation in Claude.

## Inputs
- `query`: `{{query}}`
- `top_n`: `{{top_n}}`
- `filters_json`: `{{filters_json}}`

## Execution Prompt

```text
Use Zotero MCP only. Do not use web search.

1. Run zotero_get_search_database_status.
2. If semantic DB is empty/uninitialized, stop and ask to run:
   - zotero-mcp update-db
   - zotero-mcp update-db --fulltext
3. Run zotero_semantic_search(query="{{query}}", limit={{top_n}}, filters={{filters_json}}).
4. For each top result, run:
   - zotero_get_item_metadata(item_key=<item_key>)
   - zotero_get_item_fulltext(item_key=<item_key>)
   - Extract 1-3 query-relevant snippets from fulltext output
   - If no fulltext is available, keep metadata-only evidence and state the limitation
5. Output ranked evidence with item_key and zotero_url.
```
