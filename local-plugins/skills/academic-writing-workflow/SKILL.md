---
name: academic-writing-workflow
description: Main workflow skill that orchestrates the complete academic writing process
---

# Academic Writing Workflow

## Overview

Main workflow skill that orchestrates the complete academic writing process: parse requirements, search references, parse papers, and generate academic writing output.

## When to Use

- User confirms requirement file and wants to proceed with writing
- This is the main entry point for the academic writing process

## Workflow Steps

```
1. Parse Requirements
   └── requirement-parser skill

2. Generate Outline
   └── superpowers:brainstorming (optional)
   └── Create structured outline based on topic

3. Search References
   └── reference-manager skill
   └── Multi-phase retrieval + PDF parsing

4. Generate Paper
   └── paper-writer skill
   └── scientific-skills:scientific-writing

5. Output Result
   └── Return output file path
```

## Input Format

```markdown
{
  "requirement_file_path": "./path/to/requirement.md",
  "skip_outline_confirmation": false,
  "skip_reference_confirmation": true
}
```

## Output Format

```markdown
**学术写作流程完成**

**输出文件:** {output_path}

**写作统计:**
- 标题: {title}
- 目标字数: ~{length}
- 风格: {style}
- 参考文献: {n} 篇
- 生成字数: ~{actual_length}

**建议下一步:**
- [审阅] 查看生成的论文
- [修改] 提出修改意见
- [导出] 导出为其他格式
```

## Integration Points

### Requires Sub-Skills

- `@superpowers:brainstorming` - For outline generation
- `requirement-parser` - For parsing requirements
- `reference-manager` - For reference management
- `paper-writer` - For paper generation
- `@scientific-skills:scientific-writing` - For actual writing

### Output Format for Next Steps

This skill passes structured data to downstream skills:

```python
{
  "requirement": Requirement,
  "outline": Outline,
  "references": List[Reference],
  "output_path": str
}
```

## Error Handling

- **Requirement parse error:** Return error details
- **Reference search failed:** Report and suggest alternatives
- **Paper generation failed:** Return partial results + error
- **File write error:** Report and suggest retry

## Example

```markdown
Input: {"requirement_file_path": "./requirements.md"}

Output:
**学术写作流程完成**

**输出文件:** ./output/deep-learning-paper.md

**写作统计:**
- 标题: Deep Learning for Image Classification
- 目标字数: ~2000
- 风格: academic
- 参考文献: 15 篇
- 生成字数: ~2150

**建议下一步:**
- [审阅] 查看生成的论文
- [修改] 提出修改意见
- [导出] 导出为其他格式
```
