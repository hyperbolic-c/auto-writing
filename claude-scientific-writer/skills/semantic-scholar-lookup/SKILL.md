---
name: semantic-scholar-lookup
description: Use when user needs to find papers from the open web (not local Zotero library) to support a writing argument, fill a citation gap, or discover literature in a field. Triggers include: "find papers on X", "I need references for this claim", "what's been published about Y", Zotero returns empty results, or topic is outside local library.
allowed-tools: [Bash]
compatibility: Semantic Scholar API key optional (recommended for stable throughput)
---

# Semantic Scholar Lookup

Search the open Semantic Scholar corpus and return citation-ready evidence packs for scientific writing. Use when Zotero is unavailable or insufficient.

## When to Use

- Finding papers on a topic not in the local Zotero library
- Supporting a specific argument or claim with external citations
- Discovering recent literature in a field
- Zotero semantic search returns empty or irrelevant results
- User explicitly asks to search Semantic Scholar or the web for papers

**Do NOT use** when the user wants citations from their own curated library — use `zotero-research-lookup` instead.

## API Key Setup

The script works anonymously but an API key gives stable 1 req/s throughput. Before running, check if the user has configured their API key:

1. Look for a `.env` file in the project directory or parent directories
2. Check for `SEMANTIC_SCHOLAR_API_KEY=<key>` in the `.env` file
3. If not found, inform the user they can:
   - Create a `.env` file with `SEMANTIC_SCHOLAR_API_KEY=your-api-key-here`
   - Or set the environment variable: `export SEMANTIC_SCHOLAR_API_KEY=your-api-key-here`
   - Get a free API key from: https://www.semanticscholar.org/product/api#api-key-form

The script automatically detects the `.env` file and warns if the key is missing (anonymous mode proceeds with rate limits).

## Deterministic Workflow

### Step 1: Translate argument/topic to search query

If input is a natural-language argument or claim, extract 3–5 focused English keywords before searching. See **Argument-to-Query** section below.

### Step 2: Search papers

```bash
python scripts/semantic_scholar_lookup.py "<query>" --year-from <YYYY>
```

Default returns top 12 papers ranked by relevance + recency + citation impact + venue quality.

### Step 3: Expand with recommendations (optional)

Omit `--no-recommendations` (default ON) to let the script fetch related papers from top seed results. Disable for speed:

```bash
python scripts/semantic_scholar_lookup.py "<query>" --no-recommendations --limit 10
```

### Step 4: Return evidence pack

Report results using the **Output Format** below. Always include traceability status per citation.

## Argument-to-Query Translation

When the user provides a claim or section topic rather than keywords, decompose it before searching:

| Input type | Example | Query to use |
|------------|---------|-------------|
| Broad claim | "gut microbiome affects mental health" | `gut microbiome depression mechanism` |
| Section topic | "research background on AlGaN UV detectors" | `AlGaN UV photodetector performance` |
| Hypothesis | "sleep deprivation causes insulin resistance" | `sleep deprivation insulin resistance causal` |
| Comparison argument | "mRNA vaccines vs traditional for cancer" | `mRNA cancer vaccine clinical trial efficacy` |

Rules:
- Use 3–5 English keywords (Semantic Scholar indexes English abstracts globally)
- Include mechanism/outcome words when the claim is causal
- Add year range when recency matters: `--year-from 2020`
- Run 2–3 query variants if first result set is weak

## Output Format

```markdown
## Query
<query used>

## Top Evidence
### 1) <title>
- paperId: <id>
- authors: <names>
- year: <year>
- venue: <venue>
- citationCount: <n>
- traceable: true/false
- claim: <tldr or abstract excerpt>
- url: <semanticscholar.org/paper/...>

## Synthesis
<1–3 sentences connecting top papers to the original argument>

## Limitations
- <e.g., N papers lack abstracts>
- <e.g., N papers lack DOI>

## Rate Limit Status
- total_requests: <n>
- retry_429_count: <n>
```

## Guardrails

- All API calls throttled at 0.8 req/s via built-in `GlobalRateLimiter`
- 429 → respect `Retry-After`; fallback exponential backoff 2s→4s→8s
- Prefer `/paper/batch` over per-paper detail calls
- Exclude non-traceable papers by default (no paperId, DOI, or URL)

## Script Reference

```bash
# Basic search with year range
python scripts/semantic_scholar_lookup.py "QUERY" --year-from 2019 --year-to 2026

# JSON output to file
python scripts/semantic_scholar_lookup.py "QUERY" --json -o evidence.json

# Fast mode, no recommendation expansion
python scripts/semantic_scholar_lookup.py "QUERY" --no-recommendations --limit 10
```

Run `python scripts/semantic_scholar_lookup.py --help` for all flags.

## Failure Handling

- Search returns empty: rephrase query with broader or different keywords, try 1–2 variants
- All results non-traceable: add `--non-strict-traceability` and flag in output
- 429 exhausted after retries: report rate limit hit, suggest retry in 60s
- No API key set: script proceeds anonymously and warns on stderr; direct user to **API Key Setup** section above

## References

- API endpoint details: `references/api_usage.md`
