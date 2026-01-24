# 分层全文获取策略实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 修改 `reference-manager/SKILL.md` 和 `paper-writer/SKILL.md`，实现分层全文获取策略

**Architecture:** 通过明确 Skill 描述强制 LLM 调用 `zotero_get_item_fulltext`，区分精确匹配文献（强制全文）和语义检索文献（按章节分配优先级）

**Tech Stack:** Claude Code Skills (SKILL.md), Zotero MCP (zotero-mcp)

---

## 实现步骤

### 任务 1: 修改 reference-manager SKILL.md - 新增输入字段和分层策略

**文件:**
- 修改: `auto-academic-writing/skills/reference-manager/SKILL.md`

**步骤 1: 添加 sections_for_fulltext 输入字段**

在 "Input Format" 部分新增 `sections_for_fulltext` 字段：

```markdown
## Input Format

```markdown
{
  "topic": "Research topic description",
  "reference_titles": ["Title 1", "Title 2"],
  "additional_references": 5,
  "expand_from_references": true,
  "sections_for_fulltext": ["Methods", "Results"]
}
```

**步骤 2: 修改 Processing Steps**

将步骤6改为明确强制调用 fulltext：

```markdown
## Processing Steps

1. **Read configuration** - Get `mcp_provider` from config file
2. **Fetch items** - Get items for matching (using selected provider's tools)
3. **Exact match** each reference title
4. **Semantic search** by topic if needed
5. **Expand** from matched items (if tools available for selected provider)
6. **Fetch fulltext** for exact-matched items (REQUIRED - ALWAYS call `zotero_get_item_fulltext`)
7. **Fetch fulltext** for semantic-matched items by section priority (Methods/Results=required, Related Work=optional)
8. **Return** parsed content + metadata with fulltext_status
```

**步骤 3: 修改 Output Format**

添加 fulltext_status 标签和统计信息：

```markdown
## Output Format

```markdown
**文献检索结果:**

- **MCP Provider:** {zotero-mcp | zotero-mcp-plugin}
- **精确匹配:** {n} 篇 (强制全文: {nf} 篇, 摘要: {na} 篇)
- **语义检索:** {m} 篇 (强制全文: {mf} 篇, 可选全文: {mo} 篇, 摘要: {ms} 篇)
- **扩展检索:** {k} 篇（摘要）

---

**已解析文献:**

### 1. {title} [强制全文]
- **Key:** {key}
- **Authors:** {authors}
- **Date:** {date}
- **相似度/来源:** {similarity_score or "精确匹配"}

**内容摘要:**
{abstract or "无摘要"}

---

**全文内容:**
{fulltext_markdown}

### 2. {title} [可选全文]
- **Key:** {key}
- **Authors:** {authors}
- **Date:** {date}
- **相似度/来源:** {similarity_score}

**内容摘要:**
{abstract}
（全文预载: {fulltext_preview}）

### 3. {title} [摘要]
- **Key:** {key}
- **Authors:** {authors}
- **Date:** {date}
- **相似度/来源:** {similarity_score}

**内容摘要:**
{abstract}
```
```

**步骤 4: 修改 Limitations by Provider 部分**

确保明确列出 fulltext 工具：

```markdown
## Limitations by Provider

### zotero-mcp (Python Version)

- ✅ Full PDF text extraction via `zotero_get_item_fulltext` (REQUIRED for exact-matched items)
- ✅ Tag-based expansion via `zotero_search_by_tag`
- ✅ Rich metadata and annotations

### zotero-mcp-plugin (TypeScript Version)

- ✅ Full PDF text extraction via `get_content` (REQUIRED for exact-matched items)
- ⚠️ Limited tag-based expansion
- ✅ Semantic search with embedding vectors
- ✅ Streamable HTTP for real-time communication
```

**步骤 5: 提交变更**

```bash
cd /Users/liam/projects/auto-writing/.worktrees/fulltext-strategy
git add auto-academic-writing/skills/reference-manager/SKILL.md
git commit -m "feat(reference-manager): add tiered fulltext retrieval strategy"
```

---

### 任务 2: 修改 paper-writer SKILL.md - 添加全文触发逻辑

**文件:**
- 修改: `auto-academic-writing/skills/paper-writer/SKILL.md`

**步骤 1: 在 Input Format 中添加 fulltext_status 字段**

```markdown
"references": [
  {
    "title": "Reference Title",
    "authors": ["Author 1", "Author 2"],
    "year": 2023,
    "content": "Parsed markdown content",
    "key": "ZoteroKey",
    "fulltext_status": "required" | "optional" | "abstract",
    "sections_cited": ["Methods"]
  }
]
```

**步骤 2: 在 Writing Process 中添加全文获取触发逻辑**

```markdown
## Writing Process

1. **Analyze requirements** - Understand topic, style, length, citation format
2. **Review references** - Extract key points, citations, methodology
3. **Structure content** - Organize based on outline sections
4. **Generate sections** - Write each section using two-stage process
   - **For Methods/Results sections:** Check `fulltext_status=required` references
     - If content lacks details → Call `zotero_get_item_fulltext` to get full paper
   - **For Related Work section:** Check `fulltext_status=optional` references
     - Evaluate if detailed comparison needed → Call `zotero_get_item_fulltext` if necessary
   - **For other sections:** Use available abstract/metadata
5. **Review and polish** - Check consistency, flow, length, citations
```

**步骤 3: 添加 Fulltext Trigger Rules**

```markdown
### Fulltext Trigger Rules

When writing specific sections:

| Section Type | Trigger Condition | Action |
|--------------|-------------------|--------|
| Methods | Need experimental parameters/details | Get fulltext for `required` references |
| Results | Need specific data/figures | Get fulltext for `required` references |
| Related Work | Need detailed comparison | Evaluate `optional` references, get fulltext if high relevance |
| Introduction | General background | Use abstract only |
| Discussion | Interpretation | Use abstract, fallback to fulltext if needed |

**IMPORTANT:** For exact-matched references (user-provided), ALWAYS have fulltext available.
```

**步骤 4: 提交变更**

```bash
cd /Users/liam/projects/auto-writing/.worktrees/fulltext-strategy
git add auto-academic-writing/skills/paper-writer/SKILL.md
git commit -m "feat(paper-writer): add fulltext trigger logic for sections"
```

---

### 任务 3: 合并到 main 分支

**步骤 1: 切换到 main 分支**

```bash
cd /Users/liam/projects/auto-writing
git worktree remove /Users/liam/projects/auto-writing/.worktrees/fulltext-strategy
git checkout main
```

**步骤 2: 合并 worktree 变更**

```bash
git merge .worktrees/fulltext-strategy/main
```

**步骤 3: 推送到远程**

```bash
git push origin main
```

---

## 验证步骤

1. **检查 SKILL.md 格式正确**: 确保 markdown 语法正确
2. **检查工具名称正确**: `zotero_get_item_fulltext` vs `get_content` (根据 provider)
3. **检查步骤逻辑清晰**: LLM 能理解何时必须调用 fulltext 工具

---

## 计划完成

**文件:** `auto-academic-writing/docs/plans/2026-01-24-fulltext-retrieval-impl.md`

**执行选项:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?**
