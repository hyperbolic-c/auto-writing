---
name: paper-writer
description: "Generate academic paper content in full paragraphs with IMRAD structure, citations, and professional formatting. Two-stage process: outline then prose."
allowed-tools: [Read, Write, Edit, Bash]
---

# Paper Writer

## Overview

**Core academic writing skill** for generating publication-quality scientific manuscripts. Combines requirements, outline, and reference materials into complete, well-structured academic papers.

**Critical Principle: Always write in full paragraphs with flowing prose. Never submit bullet points in scientific papers.** Use a two-stage process: first create section outlines with key points, then convert those outlines into complete paragraphs.

## When to Use

- Requirements parsed and confirmed
- References retrieved and parsed
- Ready to generate paper content
- Need publication-quality academic writing

## Writing Principles

### 1. Two-Stage Writing Process

**Stage 1: Create Section Outlines with Key Points**

When starting a new section:
1. Review the provided outline with key points
2. Organize the main arguments or findings to present
3. Identify key studies to cite
4. Plan logical flow and organization

**Stage 2: Convert Key Points to Full Paragraphs**

Once the outline is complete, expand each point into proper prose:

1. **Transform bullet points into complete sentences** with subjects, verbs, and objects
2. **Add transitions** between sentences and ideas (however, moreover, in contrast)
3. **Integrate citations naturally** within sentences
4. **Ensure logical flow** from one sentence to the next
5. **Vary sentence structure** to maintain reader engagement

### 2. Core Writing Principles

**Clarity**:
- Use precise, unambiguous language
- Define technical terms and abbreviations at first use
- Maintain logical flow within and between paragraphs

**Conciseness**:
- Eliminate redundant words and phrases
- Favor shorter sentences (15-20 words average)
- Respect word limits strictly

**Accuracy**:
- Report exact values with appropriate precision
- Use consistent terminology throughout
- Distinguish between observations and interpretations

**Objectivity**:
- Present results without bias
- Avoid overstating findings or implications
- Maintain professional, neutral tone

### 3. Manuscript Structure (IMRAD)

**Standard Sections:**
- **Introduction**: Establish research context, identify gaps, state objectives
- **Related Work**: Review relevant literature systematically
- **Methods**: Detail study design, populations, procedures, and analysis
- **Results**: Present findings objectively without interpretation
- **Discussion**: Interpret results, acknowledge limitations, propose future directions
- **Conclusion**: Summarize key contributions and implications

**Alternative Structures:**
- Review articles (narrative, systematic, scoping)
- Case reports and case series
- Theoretical/modeling papers

### 4. Citation Management

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

### 5. Field-Specific Terminology

**Biomedical and Clinical Sciences:**
- Use precise anatomical and clinical terminology
- Use "patients" for clinical studies, "participants" for community-based research
- Report lab values with standard SI units

**Molecular Biology and Genetics:**
- Use italics for gene symbols (e.g., *TP53*), regular font for proteins (e.g., p53)
- Follow species-specific gene nomenclature

**General Principles:**
- Match terminology to audience expertise
- Define abbreviations at first use: "messenger RNA (mRNA)"
- Maintain consistency throughout

## Input Format

```markdown
{
  "requirement": {
    "title": "Paper Title",
    "topic": "Research topic",
    "length": 3000,
    "style": "academic",
    "citation_style": "APA",
    "background": "Optional background text",
    "outline_hints": "Optional outline hints"
  },
  "outline": {
    "sections": [
      {
        "title": "Introduction",
        "key_points": ["Point 1", "Point 2", "Point 3"],
        "content_hints": "Optional guidance"
      }
    ]
  },
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
  ],
  "output_path": "./output/paper.md"
}
```

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

## Output Format

```markdown
# {title}

## Abstract
{concise 100-250 word summary covering purpose, methods, results, conclusions}

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

1. {Reference 1 with full citation}
2. {Reference 2 with full citation}
...
```

## Integration

### Uses Sub-Skills
- None (standalone writing capability)

### Output Structure

```python
@dataclass
class PaperOutput:
    content: str          # Full paper markdown
    word_count: int       # Actual word count
    reference_count: int  # Number of references used
    output_path: str      # File path
```

## Workflow

**Stage 1: Planning**
1. Review requirement and outline
2. Identify target structure (IMRAD or alternative)
3. Plan section sequence

**Stage 2: Drafting** (Use two-stage process for each section)
1. Create outline with key points for each section
2. Convert outline to full paragraphs with flowing prose
3. Write Methods first (often easiest)
4. Draft Results, Discussion, Introduction in order
5. Craft Abstract last

**Stage 3: Revision**
1. Check logical flow and "red thread" throughout
2. Verify consistency in terminology
3. Ensure proper citation formatting
4. Proofread for grammar and clarity

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

## Error Handling

- **Insufficient references:** Warn and proceed with available sources
- **Length constraint violated:** Adjust content to match target length
- **Citation format error:** Use fallback format (APA by default)
- **Writing blocked:** Return error with suggestions

## Example

```markdown
Input:
{
  "requirement": {
    "title": "Deep Learning for Image Classification",
    "topic": "CNN architectures for medical diagnosis",
    "length": 2000,
    "style": "academic",
    "citation_style": "APA"
  },
  "references": [...]
}

Output:
# Deep Learning for Image Classification

## Abstract
Deep learning approaches have gained significant traction in medical imaging...

## 1. Introduction
Image classification is a fundamental task in computer vision...

## 2. Related Work
Convolutional neural networks have evolved significantly...

## 3. Methods
We employed a novel architecture combining...

## 4. Results
Our model achieved 98.5% accuracy on the test set...

## 5. Discussion
These results suggest that deep learning can effectively...

## 6. Conclusion
In this study, we demonstrated the effectiveness of...

## References
[Formatted references]
```
