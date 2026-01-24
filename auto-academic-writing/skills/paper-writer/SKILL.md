---
name: paper-writer
description: "Generate academic paper content section-by-section using semantic matching with reference paragraphs. Full scientific writing capabilities: IMRAD structure, citation styles, reporting guidelines, figures/tables, and professional formatting."
allowed-tools: [Read, Write, Edit, Bash]
---

# Paper Writer

## Overview

**Section-by-section academic writing skill** that generates publication-quality content by matching section content points with relevant reference paragraphs through semantic similarity, then writing in fluent academic prose.

**Core scientific writing skill** combining semantic matching with full academic manuscript capabilities: IMRAD structure, citation styles (APA/AMA/Vancouver/IEEE/Chicago), reporting guidelines (CONSORT/STROBE/PRISMA), figures/tables, and venue-specific formatting.

**Critical Principle: Always write in full paragraphs with flowing prose. Never submit bullet points in scientific papers.**

## When to Use

- Requirements document parsed with references by section
- Reference fulltext content available
- Need to generate paper content section-by-section
- Need semantic matching between content points and reference paragraphs
- Need full academic manuscript capabilities (journal submission, reporting guidelines, etc.)

## Writing Principles

### 1. Section-by-Section Writing Process

**For each section in order:**

1. **Review section structure** - Title, subsections, content points
2. **Review reference content** - Read fulltext paragraphs for each reference
3. **Semantic matching** - Identify which reference paragraphs match each content point
4. **Template selection** - Use **first reference as primary template** for structure
5. **Write prose** - Expand content points using matched reference paragraphs as template
6. **Add supporting citations** - Use semantic search results for additional support
7. **Format appropriately** - Apply venue-specific or standard academic formatting

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
- Use active voice when appropriate for clarity

**Conciseness:**
- Eliminate redundant words and phrases
- Favor shorter sentences (15-20 words average)
- Remove unnecessary qualifiers
- Respect word limits strictly

**Accuracy:**
- Report exact values with appropriate precision
- Use consistent terminology throughout
- Distinguish between observations and interpretations
- Acknowledge uncertainty appropriately

**Objectivity:**
- Present results without bias
- Avoid overstating findings or implications
- Acknowledge conflicting evidence
- Maintain professional, neutral tone

### 5. Citation Management

**Major Citation Styles:**
- **APA** (Author, Year): Common in social sciences, natural sciences
- **AMA**: Numbered superscript citations, common in medicine
- **Vancouver**: Numbered citations in square brackets [1], biomedical standard
- **IEEE**: Numbered square brackets [1], engineering and computer science
- **Chicago**: Notes-bibliography or author-date, humanities and sciences

**Best Practices:**
- Cite primary sources when possible
- Include recent literature (last 5-10 years for active fields)
- Balance citation distribution across introduction and discussion
- Integrate citations naturally within sentences, not as lists
- Verify all citations against original sources

### 6. Manuscript Structure (IMRAD)

**Standard Sections:**
- **Introduction**: Establish research context, identify gaps, state objectives
- **Related Work**: Review relevant literature systematically
- **Methods**: Detail study design, populations, procedures, and analysis
- **Results**: Present findings objectively without interpretation
- **Discussion**: Interpret results, acknowledge limitations, propose future directions
- **Conclusion**: Summarize key contributions and implications

**For Chinese academic papers:**
- **摘要** (Abstract): Concise summary in Chinese
- **关键词** (Keywords): 3-5 terms
- **第X章** structure following Chinese thesis standards

### 7. Reporting Guidelines by Study Type

Ensure completeness and transparency by following established reporting standards:

| Guideline | Study Type |
|-----------|------------|
| **CONSORT** | Randomized controlled trials |
| **STROBE** | Observational studies (cohort, case-control, cross-sectional) |
| **PRISMA** | Systematic reviews and meta-analyses |
| **STARD** | Diagnostic accuracy studies |
| **TRIPOD** | Prediction model studies |
| **ARRIVE** | Animal research |
| **CARE** | Case reports |
| **SPIRIT** | Study protocols for clinical trials |

### 8. Figures and Tables

**When to Use Tables vs. Figures:**
- **Tables**: Precise numerical data, complex datasets, multiple variables requiring exact values
- **Figures**: Trends, patterns, relationships, comparisons best understood visually

**Design Principles:**
- Make each table/figure self-explanatory with complete captions
- Use consistent formatting and terminology across all display items
- Label all axes, columns, and rows with units
- Include sample sizes (n) and statistical annotations
- Follow the "one table/figure per 1000 words" guideline
- Avoid duplicating information between text, tables, and figures

**Common Figure Types:**
- Bar graphs: Comparing discrete categories
- Line graphs: Showing trends over time
- Scatterplots: Displaying correlations
- Box plots: Showing distributions and outliers
- Heatmaps: Visualizing matrices and patterns

### 9. Field-Specific Terminology

**Biomedical and Clinical Sciences:**
- Use precise anatomical and clinical terminology
- Use "patients" for clinical studies, "participants" for community-based research
- Report lab values with standard SI units
- Follow standardized disease nomenclature (ICD, DSM, SNOMED-CT)

**Molecular Biology and Genetics:**
- Use italics for gene symbols (e.g., *TP53*), regular font for proteins (e.g., p53)
- Follow species-specific gene nomenclature
- Specify organism names in full at first mention

**Chemistry and Pharmaceutical Sciences:**
- Follow IUPAC nomenclature for chemical compounds
- Report concentrations with appropriate units (mM, μM, nM, or % w/v, v/v)
- Use terms like "bioavailability," "pharmacokinetics," "IC50" consistently

**Physics and Engineering:**
- Follow SI units consistently
- Specify equipment with model numbers and manufacturers when relevant
- Use standard notation for physical quantities

**General Principles:**
- Define abbreviations at first use: "messenger RNA (mRNA)"
- Maintain consistency throughout the document
- Match terminology to audience expertise

### 10. Journal-Specific Formatting

Adapt manuscripts to journal requirements:
- Follow author guidelines for structure, length, and format
- Apply journal-specific citation styles
- Meet figure/table specifications (resolution, file formats, dimensions)
- Include required statements (funding, conflicts of interest, data availability, ethical approval)
- Adhere to word limits for each section

---

## Input Format

```markdown
{
  "paper_title": "Paper Title",
  "language": "zh-CN | en-US",
  "citation_style": "APA | AMA | Vancouver | IEEE | Chicago",
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
  "supplementary_references": [],
  "journal_format": "standard | nature | science | cell | ieee | ...",
  "reporting_guideline": "CONSORT | STROBE | PRISMA | ..."
}
```

---

## Processing Steps

1. **Process sections in order** - Start from first chapter to last
2. **For each section:**
   a. **Review content points** - Understand what needs to be written
   b. **Fetch reference fulltexts** - Call `zotero_get_item_fulltext` for each reference key
   c. **Parse and split fulltext** - Split into paragraphs, ignore headings
   d. **Semantic match** - Match each content point to relevant paragraphs
   e. **Select template** - Use first reference as primary template
   f. **Write prose** - Convert content points to full paragraphs using two-stage process
   g. **Add citations** - Reference [1], [2] based on matched sources
   h. **Apply formatting** - Use venue-specific or standard academic formatting
3. **Compile output** - Combine all sections into complete paper

---

## Two-Stage Writing Process

**Stage 1: Create Section Outlines with Key Points**

When starting a new section:
1. Review the provided content points
2. Organize the main arguments or findings to present
3. Identify key studies to cite from matched references
4. Plan logical flow and organization

**Stage 2: Convert Key Points to Full Paragraphs**

Once the outline is complete, expand each point into proper prose:

1. **Transform bullet points into complete sentences** with subjects, verbs, and objects
2. **Add transitions** between sentences and ideas (however, moreover, in contrast, subsequently)
3. **Integrate citations naturally** within sentences
4. **Expand with context and explanation** that bullet points omit
5. **Ensure logical flow** from one sentence to the next within each paragraph
6. **Vary sentence structure** to maintain reader engagement

---

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

本文设计了一种p-MQWs-n（p型层-多量子阱-n型层）结构的AlGaN日盲紫外探测器[1]。该结构利用多量子阱有源区增强光电转换效率，同时通过p型和n型掺杂实现载流子的有效注入。AlGaN外延片采用金属有机化学气相沉积（MOCVD）技术在蓝宝石衬底上生长[1]。外延片结构包括n型AlGaN层、多层量子阱有源区和p型AlGaN层。生长过程中需要严格控制温度、压强和源流量，以获得高质量的晶体结构和光电特性[1]。

器件制备采用标准的光刻工艺定义电极图案，然后通过电子束蒸镀在器件表面沉积Cr/Au电极[2]。蒸镀完成后进行快速热退火处理以形成良好的欧姆接触[2]。
```

---

## Output Format

### Chinese Academic Paper Format

```markdown
# {paper_title}

## 摘要

{concise 200-300 word summary in Chinese covering purpose, methods, results, conclusions}

**关键词:** {keyword1}; {keyword2}; {keyword3}; {keyword4}; {keyword5}

---

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

## 参考文献

1. {Reference 1 with full citation}
2. {Reference 2 with full citation}
...
```

### English Journal Manuscript Format

```markdown
# {paper_title}

## Abstract

{concise 100-250 word summary covering purpose, methods, results, conclusions}

**Keywords:** keyword1; keyword2; keyword3; keyword4; keyword5

## 1. Introduction

{full prose content with citations}

## 2. Related Work

{full prose content with citations}

## 3. Methods

{full prose content with procedural details}

## 4. Results

{full prose content with data presentation and statistics}

## 5. Discussion

{full prose content with interpretation, limitations, future directions}

## 6. Conclusion

{full prose content summarizing contributions}

---

## References

1. {Reference 1}
2. {Reference 2}
...
```

---

## Writing Notes

```markdown
**参考文献使用统计:**
- Section 2.1: [1], [2]
- Section 2.2: [1], [2]

**主要模板文献:**
- Section 2.1: "High-performance AlGaN UV detector" [1]
- Section 2.2: "High-performance AlGaN UV detector" [1]

**格式信息:**
- 语言: zh-CN
- 引文格式: APA
- 期刊格式: 标准中文学术论文
```

---

## Integration

### Workflow

```
reference-manager 输出 (需求文档解析)
    ↓
paper-writer 输入 (结构化章节 + 引用)
    ↓
遍历每个章节:
    ├── 语义匹配内容要点与文献段落
    ├── 调用 zotero_get_item_fulltext 获取全文
    ├── 以第一篇为主要模板仿写
    ├── 应用学术写作规范
    └── 添加引用
    ↓
输出完整论文
```

### Uses Sub-Skills
- None (standalone writing capability, integrates scientific writing principles)

---

## Error Handling

- **No matching paragraphs found:** Use abstract/metadata, warn in output
- **Insufficient references:** Proceed with available sources, suggest additional references
- **Length constraint violated:** Adjust content to match target length
- **Citation format error:** Use fallback format (APA by default)
- **Writing blocked:** Return error with suggestions
- **Missing reference fulltext:** Call `zotero_get_item_fulltext` to fetch, report if failed

---

## Example

**Input:**
```markdown
{
  "paper_title": "p-MQWs-n型AlGaN日盲紫外探测器研究",
  "language": "zh-CN",
  "citation_style": "APA",
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
  ]
}
```

**Output:**
```
# p-MQWs-n型AlGaN日盲紫外探测器研究

## 摘要

本文针对日盲紫外探测应用，设计并制备了一种p-MQWs-n型AlGaN日盲紫外探测器。通过优化多量子阱结构参数，实现了高响应度和高探测率的器件性能。研究表明，该器件在254 nm波长处具有峰值响应，响应度达到... mA/W，探测率... Jones。与传统结构相比，p-MQWs-n结构具有...

**关键词:** AlGaN; 日盲紫外探测器; 多量子阱; 光电探测

---

## 第2章 器件研究

### 2.1 引言

日盲紫外探测器（波长200-280 nm）在导弹尾焰探测、臭氧层监测、医疗消毒等领域具有重要应用价值[1]。相比于可见光和红外探测器，日盲紫外探测器具有背景噪声低、定位精度高、抗干扰能力强等优势[1]。

然而，传统日盲紫外探测器面临以下挑战：响应度不足、响应速度较慢、以及稳定性有待提高等问题[1]。为解决这些问题，研究人员开展了大量关于新型结构设计的探索...

---

## 参考文献

[1] Author, A. A., & Author, B. B. (2023). High-performance AlGaN UV detector. *Journal Name*, volume(issue), pages. DOI
```

---

## Common Mistakes to Avoid

- ❌ **Never** leave bullet points in the final manuscript
- ❌ **Never** use numbered or bulleted lists in Results or Discussion sections
- ❌ **Don't** write sentence fragments or incomplete thoughts
- ✅ **Do** use occasional lists only in Methods (e.g., inclusion/exclusion criteria, materials lists)
- ✅ **Do** ensure every section flows as connected prose
- ✅ **Do** read paragraphs aloud to check for natural flow
- ✅ **Do** define abbreviations at first use
- ✅ **Do** maintain consistent terminology throughout
