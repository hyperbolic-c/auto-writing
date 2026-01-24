---
name: paper-writer
description: Generate academic paper content based on requirements, outline, and reference materials
---

# Paper Writer

## Overview

Generate academic paper content by combining requirements, outline, and parsed reference materials. Uses scientific-writing skills for quality output.

## When to Use

- Requirements parsed and confirmed
- References retrieved and parsed
- Ready to generate paper content

## Input Format

```markdown
{
  "requirement": {
    "title": "Paper Title",
    "topic": "Research topic",
    "length": 3000,
    "style": "academic",
    "background": "Optional background text",
    "outline_hints": "Optional outline hints"
  },
  "outline": {
    "sections": ["Introduction", "Method", "Results", "Discussion"]
  },
  "references": [
    {
      "title": "Reference Title",
      "authors": ["Author 1", "Author 2"],
      "content": "Parsed markdown content",
      "key": "ZoteroKey"
    }
  ],
  "output_path": "./output/paper.md"
}
```

## Writing Process

1. **Analyze requirements** - Understand topic, style, length
2. **Review references** - Extract key points, citations
3. **Structure content** - Organize based on outline
4. **Generate sections** - Write each section with proper citations
5. **Review and polish** - Check consistency, flow, length

## Citation Handling

- **Inline citations:** Use (Author, Year) format
- **Reference list:** Generate from reference materials
- **Direct quotes:** Cite with page numbers if available
- **Paraphrasing:** Cite without page numbers

## Output Format

```markdown
# {title}

## Abstract
{auto-generated abstract}

## 1. Introduction
{content}

## 2. Related Work
{content with citations}

## 3. Method
{content}

## 4. Experiments/Results
{content}

## 5. Discussion
{content}

## 6. Conclusion
{content}

---

## References

1. {Reference 1}
2. {Reference 2}
...
```

## Integration

### Uses Sub-Skills

- `@scientific-skills:scientific-writing` - Core writing capability

### Output Structure

```python
@dataclass
class PaperOutput:
    content: str          # Full paper markdown
    word_count: int       # Actual word count
    reference_count: int  # Number of references used
    output_path: str      # File path
```

## Error Handling

- **Insufficient references:** Warn and proceed
- **Length constraint violated:** Adjust content
- **Citation format error:** Use fallback format
- **Writing blocked:** Return error with suggestions

## Example

```markdown
Input:
{
  "requirement": {
    "title": "Deep Learning for Image Classification",
    "topic": "CNN architectures for image recognition",
    "length": 2000,
    "style": "academic"
  },
  "references": [...]
}

Output:
# Deep Learning for Image Classification

## Abstract
Deep learning has revolutionized image classification...

## 1. Introduction
Image classification is a fundamental task...

## References
1. Krizhevsky, A., et al. (2012). ImageNet Classification...
2. Simonyan, K., & Zisserman, A. (2014). Very Deep Convolutional...
```
