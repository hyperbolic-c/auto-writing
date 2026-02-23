# Zotero Deep Research Skill Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a new `zotero-deep-research` skill that implements iterative deep research workflow using Zotero library through MCP, adapted from gemini-fullstack-langgraph-quickstart's deep research agent.

**Architecture:** Single skill with integrated prompts. The workflow follows: generate_query → parallel zotero_search → reflection → evaluate_research → finalize_answer. Iteration controlled by max_research_loops and is_sufficient flag.

**Tech Stack:** Claude Code skills, Zotero MCP tools (zotero_semantic_search, zotero_get_item_metadata, zotero_get_item_fulltext), prompt-based LLM interactions

---

## Task 1: Create Skill Directory Structure

**Files:**
- Create: `claude-scientific-writer/skills/zotero-deep-research/SKILL.md`
- Create: `claude-scientific-writer/skills/zotero-deep-research/prompts/query_writer.txt`
- Create: `claude-scientific-writer/skills/zotero-deep-research/prompts/reflection.txt`
- Create: `claude-scientific-writer/skills/zotero-deep-research/prompts/answer.txt`
- Create: `claude-scientific-writer/skills/zotero-deep-research/scripts/run_lookup.sh`

**Step 1: Create directories**

```bash
mkdir -p claude-scientific-writer/skills/zotero-deep-research/prompts
mkdir -p claude-scientific-writer/skills/zotero-deep-research/scripts
```

**Step 2: Commit**

```bash
git add claude-scientific-writer/skills/zotero-deep-research/
git commit -m "feat: create zotero-deep-research skill directory structure"
```

---

## Task 2: Create query_writer.txt Prompt

**Files:**
- Create: `claude-scientific-writer/skills/zotero-deep-research/prompts/query_writer.txt`

**Step 1: Write prompt file**

```txt
Your goal is to generate sophisticated and diverse search queries for academic literature research. These queries are intended for searching a local Zotero library containing scholarly papers, books, and research documents.

Instructions:
- Generate {number_queries} distinct queries that cover different aspects of the research topic.
- Each query should focus on one specific aspect: background/theory, methodology, applications, recent developments, or related works.
- Queries should be specific enough to match relevant academic papers in a semantic search system.
- Prefer academic terminology and key concepts from the research topic.
- Don't generate similar queries - each should represent a different angle.

Format:
- Format your response as a JSON object with these exact keys:
   - "rationale": Brief explanation of why these queries are relevant
   - "query": A list of search queries

Example:
Topic: "What are the latest advances in mRNA vaccine technology"
```json
{{
    "rationale": "To comprehensively cover mRNA vaccine advances, we need queries covering different aspects: mechanism of action, delivery systems, clinical trials, and manufacturing challenges.",
    "query": [
        "mRNA vaccine mechanism of action lipid nanoparticles",
        "mRNA vaccine clinical trials 2024 2025",
        "mRNA vaccine manufacturing scale-up challenges",
        "self-amplifying mRNA vaccine technology advances"
    ]
}}
```

Context: {research_topic}
```

**Step 2: Commit**

```bash
git add claude-scientific-writer/skills/zotero-deep-research/prompts/query_writer.txt
git commit -m "feat: add query_writer prompt for generating optimized queries"
```

---

## Task 3: Create reflection.txt Prompt

**Files:**
- Create: `claude-scientific-writer/skills/zotero-deep-research/prompts/reflection.txt`

**Step 1: Write prompt file**

```txt
You are an expert research assistant analyzing search results from a Zotero library about "{research_topic}".

Instructions:
- Review the collected academic papers and their evidence snippets.
- Identify knowledge gaps or areas that need deeper exploration.
- If the collected papers are sufficient to answer the user's question, indicate that no follow-up is needed.
- If there are knowledge gaps, generate specific follow-up queries that would help fill those gaps.
- Focus on missing theoretical frameworks, methodological approaches, empirical evidence, or recent developments.

Requirements:
- Follow-up queries must be self-contained and specific for semantic search.
- Consider the hierarchy of the research topic: foundational theory, methodology, results, implications.

Output Format:
- Format your response as a JSON object with these exact keys:
   - "is_sufficient": true or false
   - "knowledge_gap": Description of missing information (empty if is_sufficient is true)
   - "follow_up_queries": List of queries to address the gap (empty if is_sufficient is true)

Example:
```json
{{
    "is_sufficient": false,
    "knowledge_gap": "The results lack papers on recent clinical trials and real-world effectiveness data",
    "follow_up_queries": [
        "mRNA vaccine effectiveness real-world data 2024",
        "COVID-19 vaccine clinical trials phase 3 results"
    ]
}}
```

Research Topic: {research_topic}

Search Results Summary:
{summaries}
```

**Step 2: Commit**

```bash
git add claude-scientific-writer/skills/zotero-deep-research/prompts/reflection.txt
git commit -m "feat: add reflection prompt for analyzing search results"
```

---

## Task 4: Create answer.txt Prompt

**Files:**
- Create: `claude-scientific-writer/skills/zotero-deep-research/prompts/answer.txt`

**Step 1: Write prompt file**

```txt
Generate a high-quality academic research summary answering the user's question based on the provided literature from their Zotero library.

Instructions:
- Synthesize findings from multiple academic papers.
- Use academic tone and terminology.
- Include proper citations using Zotero item keys.
- The current date is {current_date} - consider this for any time-sensitive claims.
- Organize the answer logically: background, main findings, synthesis, limitations.

User Question: {research_topic}

Literature Summary:
{summaries}

Output Format:
- Provide a comprehensive but focused answer
- Use bullet points for key findings
- Include citations in format: [Author, Year] with item_key
- Highlight consensus and disagreements across studies if applicable
```

**Step 2: Commit**

```bash
git add claude-scientific-writer/skills/zotero-deep-research/prompts/answer.txt
git commit -m "feat: add answer prompt for finalizing research summary"
```

---

## Task 5: Create SKILL.md

**Files:**
- Create: `claude-scientific-writer/skills/zotero-deep-research/SKILL.md`

**Step 1: Write SKILL.md**

```markdown
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
```

**Step 2: Commit**

```bash
git add claude-scientific-writer/skills/zotero-deep-research/SKILL.md
git commit -m "feat: add zotero-deep-research SKILL.md"
```

---

## Task 6: Create run_lookup.sh Script

**Files:**
- Create: `claude-scientific-writer/skills/zotero-deep-research/scripts/run_lookup.sh`

**Step 1: Write script**

```bash
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
```

**Step 2: Make executable and commit**

```bash
chmod +x claude-scientific-writer/skills/zotero-deep-research/scripts/run_lookup.sh
git add claude-scientific-writer/skills/zotero-deep-research/scripts/run_lookup.sh
git commit -m "feat: add run_lookup.sh execution script"
```

---

## Task 7: Verify and Final Commit

**Step 1: Verify structure**

```bash
find claude-scientific-writer/skills/zotero-deep-research -type f | sort
```

Expected output:
```
claude-scientific-writer/skills/zotero-deep-research/SKILL.md
claude-scientific-writer/skills/zotero-deep-research/prompts/answer.txt
claude-scientific-writer/skills/zotero-deep-research/prompts/query_writer.txt
claude-scientific-writer/skills/zotero-deep-research/prompts/reflection.txt
claude-scientific-writer/skills/zotero-deep-research/scripts/run_lookup.sh
```

**Step 2: Final commit**

```bash
git add -A
git commit -m "feat: complete zotero-deep-research skill implementation"
```

---

**Plan complete and saved to `docs/plans/2026-02-23-zotero-deep-research-implementation-plan.md`.**

Two execution options:

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing_plans, batch execution with checkpoints

Which approach?
