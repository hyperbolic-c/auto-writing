---
name: paper-writer
description: "Generate academic paper content section-by-section using semantic matching with reference paragraphs. Output full prose with citations and professional formatting."
allowed-tools: [Read, Write, Edit, Bash]
---

# Paper Writer

## Overview

**Section-by-section academic writing skill** that generates publication-quality content by matching section content points with relevant reference paragraphs through semantic similarity, then writing in fluent academic prose.

**Critical Principle: Always write in full paragraphs with flowing prose. Never submit bullet points in scientific papers.**

## When to Use

- Requirements document parsed with references by section
- Reference fulltext content available
- Need to generate paper content section-by-section
- Need semantic matching between content points and reference paragraphs

## Writing Principles

### 1. Section-by-Section Writing Process

**For each section in order:**

1. **Review section structure** - Title, subsections, content points
2. **Review reference content** - Read fulltext paragraphs for each reference
3. **Semantic matching** - Identify which reference paragraphs match each content point
4. **Template selection** - Use **first reference as primary template** for structure
5. **Write prose** - Expand content points using matched reference paragraphs as template
6. **Add supporting citations** - Use semantic search results for additional support

### 2. Semantic Matching Rules

**Matching Process:**

| Step | Action |
|------|--------|
| 1 | Read content points under the section |
| 2 | Read reference fulltext (split into paragraphs, ignore headings) |
| 3 | For each content point, find semantically similar paragraphs |
| 4 | Mark matched paragraphs as template source |

**Key Insight:** Reference headings often don't contain topic information. Match by **paragraph content**, not section titles.

### 3. Template Selection Rules

- **Primary template:** First listed reference for the section
- **Secondary references:** All other listed references (used for comparison/supplement)
- **Supplementary support:** Semantic search results for additional citations

### 4. Core Writing Principles

**Clarity:**
- Use precise, unambiguous language
- Define technical terms and abbreviations at first use
- Maintain logical flow within and between paragraphs

**Conciseness:**
- Eliminate redundant words and phrases
- Favor shorter sentences (15-20 words average)
- Respect word limits strictly

**Accuracy:**
- Report exact values with appropriate precision
- Use consistent terminology throughout
- Distinguish between observations and interpretations

**Objectivity:**
- Present results without bias
- Avoid overstating findings or implications
- Maintain professional, neutral tone

### 5. Citation Management

**Major Citation Styles:**
- **APA**: Author-date in-text citations (Author, Year)
- **AMA**: Numbered superscript citations
- **Vancouver**: Numbered citations in square brackets [1]
- **IEEE**: Numbered square brackets [1]
- **Chicago**: Notes-bibliography or author-date

**Best Practices:**
- Cite primary sources when possible
- Include recent literature (last 5-10 years)
- Balance citation distribution across sections
- Integrate citations naturally within sentences

## Input Format

```markdown
{
  "paper_title": "Paper Title",
  "sections": [
    {
      "title": "第1章 绪论",
      "subsections": [
        {
          "title": "1.1 研究背景与意义",
          "content_points": [
            "日盲紫外探测在军事和民用领域的重要应用",
            "现有技术的局限性"
          ],
          "references": [
            {"title": "Reference Title 1", "key": "ZoteroKey1"},
            {"title": "Reference Title 2", "key": "ZoteroKey2"}
          ]
        }
      ]
    }
  ],
  "citation_style": "APA",
  "supplementary_references": []  // Optional: semantic search results for additional citations
}
```

## Processing Steps

1. **Process sections in order** - Start from first chapter to last
2. **For each section:**
   a. **Review content points** - Understand what needs to be written
   b. **Fetch reference fulltexts** - Call `zotero_get_item_fulltext` for each reference key to get full content
   c. **Parse and split fulltext** - Split into paragraphs, ignore headings
   d. **Semantic match** - Match each content point to relevant paragraphs
   e. **Select template** - Use first reference as primary template
   f. **Write prose** - Convert content points to full paragraphs
   g. **Add citations** - Reference [1], [2] based on matched sources
3. **Compile output** - Combine all sections into complete paper

## Semantic Matching Example

**Input Section:**
```markdown
## 2.2 器件设计与制备

**内容要点:**
- p-MQWs-n结构的设计原理
- AlGaN外延片的外延生长
- 光刻与蒸镀电极工艺

**参考文献:**
- "High-performance AlGaN UV detector"
- "MQWs structure design for UV photodetectors"
```

**Reference Fulltext Paragraphs:**
```
段落1: 我们设计了一种p-MQWs-n结构的AlGaN日盲紫外探测器。首先，通过金属有机化学气相沉积（MOCVD）技术在蓝宝石衬底上生长了多层量子阱结构的外延片。

段落2: 外延片结构包括n型AlGaN层、多层量子阱有源区和p型AlGaN层。生长过程中需要严格控制温度、压强和源流量。

段落3: 制备完成后，我们采用标准的光刻工艺定义电极图案，然后通过电子束蒸镀在器件表面沉积Cr/Au电极。
```

**Matching Result:**
| Content Point | Matched Paragraph |
|---------------|-------------------|
| p-MQWs-n结构的设计原理 | 段落1, 段落2 |
| AlGaN外延片的外延生长 | 段落1, 段落2 |
| 光刻与蒸镀电极工艺 | 段落3 |

**Output:**
```markdown
## 2.2 器件设计与制备

本文设计了一种p-MQWs-n（p型层-多量子阱-n型层）结构的AlGaN日盲紫外探测器。该结构利用多量子阱有源区增强光电转换效率，同时通过p型和n型掺杂实现载流子的有效注入[1]。

AlGaN外延片采用金属有机化学气相沉积（MOCVD）技术在蓝宝石衬底上生长[1]。外延片结构包括n型AlGaN层、多层量子阱有源区和p型AlGaN层。生长过程中需要严格控制温度、压强和源流量，以获得高质量的晶体结构和光电特性[1]。

器件制备采用标准的光刻工艺定义电极图案，然后通过电子束蒸镀在器件表面沉积Cr/Au电极[2]。蒸镀完成后进行快速热退火处理以形成良好的欧姆接触[2]。
```

## Output Format

```markdown
# {paper_title}

## 第1章 绪论

### 1.1 研究背景与意义

{full prose content with citations}

### 1.2 国内外研究现状

{full prose content with citations}

---

## 第2章 器件研究

### 2.1 引言

{full prose content with citations}

### 2.2 器件设计与制备

{full prose content with citations}

---

## 第3章 实验结果与讨论

### 3.1 器件结构表征

{full prose content with citations}

---

## Writing Notes

**参考文献使用统计:**
- Section 2.1: [1], [2]
- Section 2.2: [1], [2]
- Section 3.1: [1]

**主要模板文献:**
- Section 2.1: "High-performance AlGaN UV detector" [1]
- Section 2.2: "High-performance AlGaN UV detector" [1]
```

## Integration

### Workflow

```
reference-manager 输出
    ↓
paper-writer 输入
    ↓
遍历每个章节:
    ├── 语义匹配内容要点与文献段落
    ├── 以第一篇为主要模板仿写
    └── 添加引用
    ↓
输出完整论文
```

### Uses Sub-Skills
- None (standalone writing capability)

## Error Handling

- **No matching paragraphs found:** Use abstract/metadata, warn in output
- **Insufficient references:** Proceed with available sources, suggest additional references
- **Length constraint violated:** Adjust content to match target length
- **Citation format error:** Use fallback format (APA by default)
- **Writing blocked:** Return error with suggestions

## Example

**Input:**
```markdown
{
  "paper_title": "p-MQWs-n型AlGaN日盲紫外探测器研究",
  "sections": [
    {
      "title": "第2章 器件研究",
      "subsections": [
        {
          "title": "2.1 引言",
          "content_points": [
            "日盲紫外探测器的重要性",
            "研究进展与存在的问题"
          ],
          "references": [
            {
              "title": "High-performance AlGaN UV detector",
              "key": "ABC123",
              "fulltext": "日盲紫外探测器（波长200-280 nm）在导弹尾焰探测、臭氧层监测等领域具有重要应用价值。相比于可见光和红外探测器，日盲紫外探测器具有背景噪声低、定位精度高、抗干扰能力强等优势。然而，传统日盲紫外探测器面临以下挑战：..."
            }
          ]
        }
      ]
    }
  ],
  "citation_style": "APA"
}
```

**Output:**
```
# p-MQWs-n型AlGaN日盲紫外探测器研究

## 第2章 器件研究

### 2.1 引言

日盲紫外探测器（波长200-280 nm）在导弹尾焰探测、臭氧层监测等领域具有重要应用价值[1]。相比于可见光和红外探测器，日盲紫外探测器具有背景噪声低、定位精度高、抗干扰能力强等优势[1]。

然而，传统日盲紫外探测器面临以下挑战：...

---

## Writing Notes

**参考文献使用统计:**
- Section 2.1: [1]

**主要模板文献:**
- Section 2.1: "High-performance AlGaN UV detector" [1]
```
