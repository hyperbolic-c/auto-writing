---
name: brainstorming
description: "Generate structured outline for academic writing based on research topic and requirements. Uses collaborative dialogue to develop paper structure."
---

# Brainstorming for Academic Writing

## Overview

Help generate a well-structured outline for academic papers through collaborative dialogue. Start by understanding the research topic and requirements, then develop a logical paper structure following academic conventions.

## The Process

**Understanding the research:**
- Review the requirement file (title, topic, length, style, references)
- Ask clarifying questions about the research focus and objectives
- Identify the target venue/journal and its typical structure requirements

**Exploring structure approaches:**
- Propose 2-3 different outline structures with trade-offs
- Consider IMRAD (Introduction, Methods, Results, Discussion) or alternative formats
- Present options conversationally with recommendations

**Presenting the outline:**
- Once the topic is understood, present the structured outline
- Break it into sections with key points for each section
- Include suggested subsections and content hints
- Ask whether the structure looks appropriate

## Key Principles

- **Academic structure** - Follow IMRAD or discipline-specific conventions
- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary sections from the outline
- **Incremental validation** - Present outline in sections, validate each
- **Be flexible** - Go back and adjust when structure doesn't fit

## Output Format

```markdown
# Paper Outline

## 1. Introduction
- Context and background
- Research problem statement
- Gap in current knowledge
- Study objectives/research questions

## 2. Related Work
- Key prior studies
- Current approaches and limitations
- How this work advances the field

## 3. Methods
- Study design
- Data collection
- Analysis approach
- Rationale for chosen methods

## 4. Results
- Primary findings
- Secondary outcomes
- Statistical significance

## 5. Discussion
- Interpretation of results
- Comparison with prior work
- Limitations
- Implications and future directions

## 6. Conclusion
- Key contributions summary
- Broader impact

## References
- Primary citations
```

## Integration

### Uses Sub-Skills
- None (standalone skill for outline generation)

### Input Format

```markdown
{
  "requirement": {
    "title": "Paper Title",
    "topic": "Research topic description",
    "length": 3000,
    "style": "academic",
    "background": "Optional background context",
    "outline_hints": "Optional structural preferences"
  }
}
```

### Output Format

```markdown
{
  "outline": {
    "sections": [
      {
        "title": "Section Title",
        "key_points": ["Point 1", "Point 2", ...],
        "content_hints": "Optional guidance for writing"
      }
    ],
    "total_sections": 5,
    "estimated_words": 3000
  }
}
```

## Example

```markdown
Input:
{
  "requirement": {
    "title": "Deep Learning for Image Classification",
    "topic": "CNN architectures for medical image diagnosis",
    "length": 2500,
    "style": "academic"
  }
}

Output:
# Paper Outline: Deep Learning for Image Classification

## 1. Introduction
- Medical imaging challenges
- Deep learning potential for diagnosis
- Research objectives

## 2. Related Work
- CNN evolution (LeNet, AlexNet, VGG)
- Medical imaging applications
- Diagnostic accuracy studies

## 3. Methods
- Dataset description
- Architecture choices
- Training procedure
- Evaluation metrics

## 4. Results
- Classification accuracy
- Comparison with baselines
- Sensitivity analysis

## 5. Discussion
- Clinical implications
- Limitations
- Future directions
```
