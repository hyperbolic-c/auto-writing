---
name: requirement-parser
description: Parse and validate academic writing requirement files in YAML frontmatter format
---

# Requirement Parser

## Overview

Parse academic writing requirement files (YAML frontmatter + optional markdown body) and convert to structured data for downstream skills.

## When to Use

- User provides a requirement file path
- Need to extract: title, topic, length, style, references, additional_settings
- Validate required fields are present

## Input Format

The skill accepts a file path string pointing to a markdown file with YAML frontmatter:

```markdown
---
title: Paper Title
topic: Research topic description
length: 3000
style: academic
references:
  - "Reference Title 1"
  - "Reference Title 2"
additional_references: 5
expand_from_references: true
---

# 研究背景
Optional background text...

# 大纲要点
Optional outline hints...
```

## Parsing Logic

1. Read file content
2. Extract YAML frontmatter (between `---` markers)
3. Parse YAML to dictionary
4. Validate required fields
5. Extract optional body sections (研究背景, 大纲要点)

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Paper title |
| `topic` | string | Research topic for semantic search |
| `length` | integer | Target word count |
| `style` | string | Writing style (academic, technical, review) |
| `references` | list | List of reference titles |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `additional_references` | integer | 5 | Number of additional refs to search |
| `expand_from_references` | boolean | true | Whether to expand from matched refs |

## Output Format

```markdown
**已解析需求:**

- **标题:** {title}
- **主题:** {topic}
- **字数:** ~{length}
- **风格:** {style}
- **参考文献:** {n} 篇
- **额外检索:** {additional_references} 篇
- **扩展检索:** {expand_from_references}

**研究背景:**
{background_text or "未提供"}

**大纲要点:**
{outline_hints or "未提供"}

---

**建议行动:**
- [确认] 开始生成写作大纲
- [修改] 返回修改需求
```

## Error Handling

- **File not found:** Return error with path
- **Invalid YAML:** Return parsing error
- **Missing required field:** List missing fields
- **Invalid field type:** Return type error with expected type

## Example

```markdown
Input: "./requirements.md"

Output:
**已解析需求:**

- **标题:** Deep Learning for Image Classification
- **主题:** CNN architectures for image recognition
- **字数:** ~2000
- **风格:** academic
- **参考文献:** 2 篇
- **额外检索:** 5 篇
- **扩展检索:** true

**研究背景:**
未提供

**大纲要点:**
未提供

---

**建议行动:**
- [确认] 开始生成写作大纲
- [修改] 返回修改需求
```
