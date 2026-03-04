---
name: thesis-writing
description: Use when writing academic theses or dissertations (Master's, PhD, undergraduate honors). Covers chapter-by-chapter structure, literature review chapters, methodology, results, discussion, conclusion, front matter, and thesis-specific conventions including abstract, acknowledgements, appendices, and institutional formatting requirements.
allowed-tools: [Read, Write, Edit, Bash]
---

# Thesis Writing

## Overview

This skill guides the writing of academic theses and dissertations—Master's (MSc/MA), doctoral (PhD/DPhil), and undergraduate honors—combining rigorous structure with depth of argumentation appropriate for degree-level assessment.

**Core principle:** A thesis is an extended argument. Every chapter, section, and paragraph must advance the central thesis statement. Use a two-stage process: first build section outlines informed by Zotero literature search, then convert to flowing scholarly prose.

**Critical:** Write in full paragraphs with flowing academic prose. Never submit bullet points in the final document. Use `claude-scientific-writer:zotero-research-lookup` for all literature-based evidence gathering—it uses the advanced_rag semantic search mode for high-quality chunk-level retrieval from your Zotero library.

---

## Thesis vs. Journal Paper: Key Differences

| Dimension | Journal Paper | Thesis/Dissertation |
|-----------|--------------|---------------------|
| Length | 4,000–10,000 words | 20,000–100,000+ words |
| Audience | Field specialists | Examining committee + future researchers |
| Literature review | Focused, selective | Comprehensive, critically synthesized |
| Methods | Summarized | Fully reproducible detail |
| Original contribution | One contribution | Multiple or one substantial contribution |
| Voice | Impersonal | Often first-person acceptable |
| Chapter structure | IMRAD | Extended multi-chapter format |

---

## Standard Thesis Chapter Structure

### Front Matter
1. **Title page** — title, author, institution, degree, date
2. **Abstract** — 200–500 words (standalone summary; state gap, approach, findings, contribution)
3. **Acknowledgements** — brief personal and funding acknowledgements
4. **Table of contents**, list of figures, list of tables, list of abbreviations
5. **Declaration / statement of originality**

### Core Chapters

#### Chapter 1 — Introduction
- Research context and significance
- Problem statement and research gap (use zotero-research-lookup to document gap)
- Research questions or hypotheses (numbered, specific)
- Scope and delimitations
- Thesis structure overview (roadmap paragraph)

#### Chapter 2 — Literature Review
See [Literature Review Chapter](#chapter-2-in-depth-literature-review) below.

#### Chapter 3 — Methodology
- Research paradigm and philosophical stance (positivist, interpretivist, etc.)
- Research design (experimental, quasi-experimental, case study, survey, etc.)
- Participants/data sources and sampling rationale
- Data collection instruments and procedures
- Data analysis strategy
- Validity, reliability, trustworthiness considerations
- Ethical approval and consent

#### Chapter 4 — Results / Findings
- Present findings objectively and systematically
- Organize by research question, not by data collection order
- Tables and figures with full captions (self-explanatory)
- No interpretation here (save for Discussion)

#### Chapter 5 — Discussion
- Interpret findings in light of research questions
- Compare with existing literature (use zotero-research-lookup to find relevant papers)
- Theoretical and practical implications
- Limitations and their impact
- Unexpected findings

#### Chapter 6 — Conclusion
- Restate contribution(s) to knowledge
- Answer each research question directly
- Recommendations for practice and future research
- Final reflective statement on significance

### Back Matter
- **References / Bibliography** (use institutional or field-standard style)
- **Appendices** (instruments, raw data summaries, ethics approval, supplementary analyses)

---

## Chapter 2 In-Depth: Literature Review

The literature review chapter is the most research-intensive part of the thesis. It demonstrates mastery of the field and justifies the research gap.

### Structure Options

**Thematic structure** (most common): Group literature by theme, concept, or theoretical strand—not chronologically.

**Funnel structure**: Move from broad field → sub-field → specific gap → your study.

**Conceptual framework section**: End the chapter with a conceptual or theoretical framework diagram (text-based description) that organizes the key constructs your study will examine.

### Two-Stage Writing Process for Literature Review

**Stage 1 — Build evidence outline using zotero-research-lookup:**

For each thematic section:
1. Invoke `claude-scientific-writer:zotero-research-lookup` with a targeted semantic query
2. The skill uses **advanced_rag mode**: it retrieves chunk-level matches with reranking, returning matched text passages alongside metadata—ideal for extracting specific claims from PDFs
3. Collect: key claims, methodological approaches, conflicting findings, seminal authors, date ranges
4. Organize as a bullet-point evidence scaffold per theme

**Stage 2 — Convert to critical synthesis prose:**

Transform evidence scaffold into paragraphs that:
- Integrate multiple sources per paragraph (not one paragraph per paper)
- Show critical engagement: compare, contrast, evaluate methodologies
- Use attribution verbs with nuance: "argued," "demonstrated," "challenged," "replicated," "failed to replicate"
- Identify patterns across studies (consensus, debate, evolution of understanding)
- Explicitly state the gap your thesis addresses

### Advanced_RAG Semantic Search Usage

The `zotero-research-lookup` skill activates the **advanced_rag retriever** when configured (retriever_mode = "advanced_rag"). This mode:

- Indexes PDF content as **semantic chunks** (paragraph-level), not just metadata
- Returns `matched_content` — the actual chunk that matched your query
- Applies a **reranker** (cross-encoder) to score chunks against the query
- Uses `candidate_k` (default 30) for initial retrieval, then reranks to top `limit`
- Supports `filters` (e.g., `{"year": "2020"}`) for scoping searches

**Effective query strategies for thesis literature:**

```
# Broad conceptual query (Chapter 2 opening)
"theoretical frameworks for [your topic]"

# Methods-focused query (Chapter 3 justification)
"[method name] validity reliability [your field]"

# Gap identification query
"limitations future research [sub-topic]"

# Conceptual comparison query
"[concept A] versus [concept B] [field]"

# Empirical evidence query
"[intervention/factor] effect on [outcome] [population]"
```

**Check index health before writing any chapter:**
```
Step 1: zotero_get_search_database_status
  - If retriever_mode = "advanced_rag" → full chunk search available
  - If retriever_mode = "legacy_metadata" → metadata-only search (less precise)
  - If doc count = 0 (advanced_rag) → run: zotero-mcp update-db --rebuild
  - If doc count = 0 (legacy)        → run: zotero-mcp update-db [--fulltext]
  - If topic returns few/irrelevant results → fall back to semantic-scholar-lookup
```

---

## Writing Principles for Thesis Prose

### Academic Register
- Use hedging language appropriately: "suggests," "indicates," "appears to," "may be attributed to"
- Distinguish empirical claims from interpretations: "the data show" vs. "this suggests"
- First-person is acceptable in most modern theses (check institutional guidelines): "I argue," "this study investigated"
- Avoid informal contractions, colloquialisms, and rhetorical questions

### Citation Integration
- **Integral citations**: "Smith (2020) demonstrated that..."
- **Non-integral citations**: "...as demonstrated in recent meta-analyses (Jones, 2019; Lee, 2021)."
- Cite primary sources; avoid secondary citations where primary is accessible
- In literature review, cite multiple studies per claim to show breadth

### Paragraph Architecture
Each paragraph should follow:
1. **Topic sentence** — states the paragraph's argument
2. **Evidence** — 2–4 cited pieces of support
3. **Analysis** — your interpretation connecting evidence to the argument
4. **Transition** — links to the next paragraph or signals conclusion

### Transitions Between Chapters
Every chapter should end with a brief **chapter summary** (3–5 sentences) and a **transition sentence** pointing to the next chapter's purpose.

---

## Citation Styles by Discipline

| Discipline | Style |
|-----------|-------|
| Sciences (biology, chemistry, physics) | Vancouver or APA 7 |
| Social sciences, psychology, education | APA 7 |
| Humanities (history, literature) | Chicago Notes-Bibliography |
| Engineering, computer science | IEEE |
| Law | Jurisdiction-specific (Bluebook, OSCOLA) |
| Business, economics | Harvard / APA |

Always verify the exact style required by your institution and department.

---

## Common Thesis Writing Mistakes

| Mistake | Fix |
|---------|-----|
| Literature review as annotated bibliography | Synthesize across sources; organize thematically |
| Methodology without philosophical grounding | State research paradigm before design choices |
| Results mixed with interpretation | Keep results objective; interpretation belongs in Discussion |
| Weak conclusion that just summarizes | State explicit contribution to knowledge; answer each RQ |
| Inconsistent tense | Methods/results: past tense; established facts: present tense |
| Single-source paragraphs | Integrate 2–4 sources per paragraph in lit review |
| Thesis statement buried or absent | State research gap + approach + contribution in Introduction clearly |
| Ignoring counter-evidence | Engage with contradictory findings; show critical thinking |

---

## Workflow: Writing a Thesis Chapter

```
1. PLAN
   - Identify chapter purpose and its argument
   - List research questions this chapter addresses

2. SEARCH (for each thematic section)
   - Invoke zotero-research-lookup with targeted query
   - If results are empty or irrelevant → fall back to semantic-scholar-lookup
   - Collect evidence scaffold as bullet points

3. OUTLINE
   - Arrange bullet points into logical paragraph groups
   - Identify gaps → run additional searches

4. DRAFT
   - Convert each bullet group to a full paragraph (topic + evidence + analysis + transition)
   - Write in full prose; no bullet points in final output

5. REVIEW
   - Does each paragraph advance the chapter argument?
   - Are citations integrated (not listed)?
   - Is tense consistent?
   - Does the chapter end with a summary and transition?
```

---

## Integration with Other Skills

- **`claude-scientific-writer:zotero-research-lookup`** — REQUIRED for all literature-based sections; use advanced_rag for chunk-level precision
- **`claude-scientific-writer:semantic-scholar-lookup`** — fallback when Zotero returns empty or insufficient results; searches the open Semantic Scholar corpus
- **`claude-scientific-writer:zotero-deep-research`** — use for iterative multi-round research on complex topics requiring gap analysis
- **`claude-scientific-writer:literature-review`** — complements Chapter 2 with systematic search protocols and PRISMA-style documentation
- **`claude-scientific-writer:venue-templates`** — for formatting theses to institutional LaTeX templates
- **`claude-scientific-writer:citation-management`** — for verifying and generating accurate BibTeX entries

Do **not** use image generation skills (scientific-schematics, generate-image) unless the thesis specifically requires custom diagrams—most theses use data-generated figures produced by the researcher's own analysis tools.
