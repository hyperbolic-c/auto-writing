---
name: reference-manager
description: Parse requirements document, extract references by section, and fetch fulltext from Zotero library (supports both zotero-mcp and zotero-mcp-plugin)
---

# Reference Manager

## Overview

Parse academic paper requirements document, extract references by section, and fetch fulltext content from Zotero library.

**Supports two Zotero MCP providers:**
- `zotero-mcp` (Python version) - see [hyperbolic-c/zotero-mcp](https://github.com/hyperbolic-c/zotero-mcp)
- `zotero-mcp-plugin` (TypeScript/Zotero Plugin version) - see [cookjohn/zotero-mcp](https://github.com/cookjohn/zotero-mcp)

**Configuration:**
- Run `/academic-write-setup` to select your preferred MCP provider
- Config stored in `~/.config/auto-writing/config.json`

## When to Use

- Need to parse requirements document for section structure
- Need to extract references listed under each section
- Need to fetch fulltext content for referenced papers
- Need semantic matching between section content and reference paragraphs

## Input Format

```markdown
{
  "requirements_doc": "完整的需求文档内容（Markdown格式）"
}
```

### 支持的需求文档格式

#### 格式1：固定模板（结构化）
```markdown
论文题目：p-MQWs-n型AlGaN日盲紫外探测器研究

# 第1章 绪论
## 1.1 研究背景与意义
- 研究背景描述
- 研究意义

### 参考文献
- "Reference Title 1"
- "Reference Title 2"

# 第2章 器件研究
## 2.1 引言
- 内容要点1
- 内容要点2

### 参考文献
- "Reference Title 3"
```

#### 格式2：自由格式（行内标注）
```markdown
论文题目：AlGaN日盲紫外探测器研究

# 第2章 器件研究
## 2.1 引言
日盲紫外探测器在导弹尾焰探测中具有重要应用。参考文献：ZnO基日盲紫外探测器研究进展。当前技术面临的主要挑战包括噪声控制问题。
- 材料生长工艺复杂
```

### 参考文献识别规则

| 格式 | 识别方式 | 示例 |
|------|----------|------|
| 模板格式 | `### 参考文献` + `- "标题"` | `### 参考文献\n- "Title1"` |
| 行内格式 | `参考文献：...。` 或 `参考文献：...` | `参考文献：ZnO日盲探测器研究进展。` |

## Processing Steps

1. **Parse requirements document** - Extract paper title, section structure (H1 → H2 → content points)
2. **Extract references by section** - Identify references under each section
3. **Search references in Zotero** - Match reference titles with Zotero items
4. **Fetch fulltext for all references** - REQUIRED: Call `zotero_get_item_fulltext` or `get_content` for each referenced paper
5. **Analyze reference content** - Split fulltext into paragraphs, ignoring headings
6. **Return structured output** - Sections with content points + fulltext content

## Tool Mapping (Based on Configuration)

### zotero-mcp (Python Version)

| Function | Description |
|----------|-------------|
| `zotero_search_items` | Keyword/title search |
| `zotero_semantic_search` | AI-powered semantic search |
| `zotero_get_item_metadata` | Get item details |
| `zotero_get_item_fulltext` | **REQUIRED** - Get PDF fulltext as markdown |
| `zotero_search_by_tag` | Search by tags |

### zotero-mcp-plugin (TypeScript Version)

| Function | Description |
|----------|-------------|
| `search_library` | Keyword/title search |
| `semantic_search` | AI-powered semantic search |
| `get_item_details` | Get item details |
| `get_content` | **REQUIRED** - Get PDF fulltext content |
| `search_fulltext` | Fulltext search |

## Output Format

```markdown
**需求文档解析结果:**

- **论文题目:** {title}
- **章节数量:** {n} 个

---

## 全文获取日志:

```
[FETCH_FULLTEXT] Section 2.1: "High-performance AlGaN UV detector" → zotero_get_item_fulltext ✓
[FETCH_FULLTEXT] Section 2.1: "ZnO-based photodetector..." → zotero_get_item_fulltext ✓
[FETCH_FULLTEXT] Section 2.2: "MQWs structure design..." → zotero_get_item_fulltext ✓
```

---

## 章节结构与引用:

### 第1章 绪论

#### 1.1 研究背景与意义

**内容要点:**
- 研究背景描述
- 研究意义

**参考文献:**
| # | 标题 | Key |
|---|------|-----|
| 1 | "Reference Title 1" | ABC123 |
| 2 | "Reference Title 2" | DEF456 |

---

### 第2章 器件研究

#### 2.1 引言

**内容要点:**
- 日盲紫外探测器的重要性
- 研究进展与存在的问题

**参考文献:**
| # | 标题 | Key |
|---|------|-----|
| 1 | "High-performance AlGaN UV detector" | GHI789 |
| 2 | "ZnO-based photodetector..." | JKL012 |

---

## 章节写作输入:

```json
{
  "paper_title": "{title}",
  "sections": [
    {
      "title": "第1章 绪论",
      "subsections": [
        {
          "title": "1.1 研究背景与意义",
          "content_points": ["研究背景描述", "研究意义"],
          "references": [
            {"title": "Reference Title 1", "key": "ABC123"},
            {"title": "Reference Title 2", "key": "DEF456"}
          ]
        }
      ]
    }
  ],
  "citation_style": "APA"
}
```

---

## Error Handling

- **No items found:** Report zero results for each reference
- **Missing PDF attachment:** Report error for that specific reference, continue with others
- **PDF conversion failed:** Report error, continue with abstract
- **Network/API errors:** Report and suggest retry
- **Configuration missing:** Prompt user to run `/academic-write-setup`
- **No references found in section:** Report section has no references

## Example

**Input:**
```markdown
论文题目：AlGaN日盲紫外探测器研究

# 第2章 器件研究
## 2.1 引言
- 日盲紫外探测器的重要性
- 研究进展与存在的问题

### 参考文献
- "High-performance AlGaN UV detector"
```

**Output:**
```
**需求文档解析结果:**

- **论文题目:** AlGaN日盲紫外探测器研究
- **章节数量:** 1 个

---

## 全文获取日志:

[FETCH_FULLTEXT] Section 2.1: "High-performance AlGaN UV detector" → zotero_get_item_fulltext ✓

---

## 章节结构与引用:

### 第2章 器件研究

#### 2.1 引言

**内容要点:**
- 日盲紫外探测器的重要性
- 研究进展与存在的问题

**参考文献:**
| # | 标题 | Key |
|---|------|-----|
| 1 | "High-performance AlGaN UV detector" | ABC123 |

---

## 章节写作输入:

```json
{
  "paper_title": "AlGaN日盲紫外探测器研究",
  "sections": [
    {
      "title": "第2章 器件研究",
      "subsections": [
        {
          "title": "2.1 引言",
          "content_points": ["日盲紫外探测器的重要性", "研究进展与存在的问题"],
          "references": [
            {"title": "High-performance AlGaN UV detector", "key": "ABC123"}
          ]
        }
      ]
    }
  ],
  "citation_style": "APA"
}
```
```

## Limitations by Provider

### zotero-mcp (Python Version)

- ✅ Full PDF text extraction via `zotero_get_item_fulltext` (**REQUIRED** for all references)
- ✅ Tag-based expansion via `zotero_search_by_tag`
- ✅ Rich metadata and annotations

### zotero-mcp-plugin (TypeScript Version)

- ✅ Full PDF text extraction via `get_content` (**REQUIRED** for all references)
- ⚠️ Limited tag-based expansion
- ✅ Semantic search with embedding vectors
- ✅ Streamable HTTP for real-time communication
