#!/bin/bash

# Zotero Deep Research - Execution Prompt Generator
# Usage: ./run_lookup.sh "research topic" [max_loops] [initial_queries] [top_n]

TOPIC="${1:-}"
MAX_LOOPS="${2:-2}"
INITIAL_QUERIES="${3:-3}"
TOP_N="${4:-5}"

if [ -z "$TOPIC" ]; then
    echo "Usage: $0 \"research topic\" [max_loops] [initial_queries] [top_n]"
    echo "Example: $0 \"mRNA vaccine advances\" 2 3 5"
    exit 1
fi

cat << EOF
## Zotero Deep Research Execution

### Research Topic
$TOPIC

### Parameters
- max_research_loops: $MAX_LOOPS
- number_of_initial_queries: $INITIAL_QUERIES
- top_n_per_query: $TOP_N

### Step 1: Check Index Status
Run: zotero_get_search_database_status

If document count is 0 or reports not initialized, return this action:
- Run: zotero-mcp update-db
- Or: zotero-mcp update-db --fulltext (preferred for richer evidence)

### Step 2: Query Generation (Round 1)
Read prompts/query_writer.txt and generate $INITIAL_QUERIES queries for: "$TOPIC"

### Step 3: Parallel Zotero Search
For each generated query, execute:
- zotero_semantic_search(query="<query>", limit=$TOP_N)
- For each result: zotero_get_item_metadata(item_key=<key>)
- For each result: zotero_get_item_fulltext(item_key=<key>)

### Step 4: Reflection
Read prompts/reflection.txt and analyze the collected papers.
Output JSON with is_sufficient, knowledge_gap, and follow_up_queries.

### Step 5: Evaluate
- If is_sufficient == true → Step 6
- If is_sufficient == false and loop < $MAX_LOOPS → Step 3 with follow-up queries
- If is_sufficient == false and loop >= $MAX_LOOPS → Step 6

### Step 6: Finalize Answer
Read prompts/answer.txt and synthesize all collected evidence into final answer.
Include proper Zotero citations with item_key.

EOF
