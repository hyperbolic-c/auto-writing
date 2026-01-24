# Academic Writing Plugin 设计方案

> **For Claude:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task.
>
> **使用指南:** 此插件需要配合以下工具使用:
> - zotero-mcp: 文献检索和 PDF 获取
> - claude-scientific-skills: scientific-writing 技能
> - superpowers: 工作流框架（brainstorming, writing-plans 等）

**Goal:** 创建一个 Claude Code 学术写作插件，集成 Zotero 文献管理、MinerU PDF 解析、scientific-skills 写作能力。

**Architecture:** 基于 superpowers 工作流框架，创建学术写作专用的技能和命令。用户通过需求文件启动写作流程，插件自动完成文献检索、解析、写作全流程。

**Tech Stack:**
- Claude Code Plugin System
- superpowers 技能框架
- zotero-mcp (MCP server)
- MinerU API (PDF 解析)
- scientific-skills (写作技能)

---

## 1. 插件概述

### 1.1 插件名称与定位

**插件名称:** `academic-writing`

**核心定位:** 基于 superpowers 工作流框架的学术写作插件

**设计原则:**
- 以 superpowers 为框架，复用其 planning、tool-calling 能力
- 创建专门的学术写作技能（skills）和代理（agents）
- 用户通过对话提供需求文件路径，插件自动执行完整写作流程
- 插件内嵌引用 superpowers 的技能作为子技能使用

### 1.2 与现有组件的关系

| 组件 | 关系 |
|------|------|
| superpowers | 引用作为子技能框架 |
| zotero-mcp | 通过 MCP tools 调用文献检索 |
| claude-scientific-skills | 引用 scientific-writing 技能 |
| MinerU | 通过 API 调用 PDF 解析 |

---

## 2. 数据流设计

### 2.1 完整工作流数据流

```
用户需求文件 (.md)
       ↓
需求解析技能 → 提取: title, topic, length, style, reference_titles
       ↓
superpowers:brainstorming → 生成写作大纲
       ↓
文献检索阶段:
├── zotero_semantic_search(topic) → 基于 topic 语义检索
├── 精确匹配 reference_titles → 获取 item_key 列表
├── 扩展检索 (expand_from_references) → 基于已匹配文献获取更多相关文献
       ↓
zotero_get_item_fulltext(item_key) → 下载 PDF → 转换为 MD
       ↓
MinerU API (可选) → 精调 PDF 解析质量
       ↓
读取解析后的文献 → 作为上下文
       ↓
scientific-skills:scientific-writing → 生成论文草稿
       ↓
输出: output.md
```

### 2.2 用户交互流程

1. 用户提供需求文件路径（如 `./writing-requirement.md`）
2. 插件确认文件存在，解析需求
3. 展示检索策略和大纲草案，用户确认/修改
4. 自动执行文献检索、解析、写作
5. 输出初稿，用户审阅反馈
6. 根据反馈迭代修改

---

## 3. 需求文件格式

### 3.1 完整格式规范

```markdown
---
title: 论文标题（英文）
topic: 研究主题简要描述（用于 Zotero 语义检索）
length: 3000
style: academic
references:
  - "Paper Title 1"
  - "Paper Title 2"
  - "Paper Title 3"
additional_references: 5    # 可选：额外检索数量（默认 5）
expand_from_references: true # 可选：是否基于参考文献扩展（默认 true）
---

# 研究背景
（可选）补充说明研究背景和动机

# 大纲要点
（可选）用户指定的章节结构提示
```

### 3.2 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | 是 | 论文标题 |
| `topic` | 是 | 研究主题描述，用于语义检索 |
| `length` | 是 | 预估字数（中文/英文均可） |
| `style` | 是 | 写作风格（academic, technical, review 等） |
| `references` | 是 | 参考文献标题列表（用于匹配 Zotero 中的文献） |
| `additional_references` | 否 | 额外检索数量，默认 5 |
| `expand_from_references` | 否 | 是否基于参考文献扩展，默认 true |
| `研究背景` | 否 | 补充说明 |
| `大纲要点` | 否 | 用户偏好的章节结构 |

### 3.3 内部数据结构

```python
@dataclass
class Requirement:
    title: str
    topic: str
    length: int
    style: str
    reference_titles: List[str]
    additional_references: int = 5
    expand_from_references: bool = True
    background: Optional[str] = None
    outline_hints: Optional[str] = None
```

---

## 4. 文献检索策略

### 4.1 多阶段检索流程

```
阶段 1: 精确匹配
├── 输入: reference_titles 列表
├── 操作: 在 Zotero 中搜索每个标题
└── 输出: 匹配的 item_key 列表

阶段 2: 语义检索
├── 输入: topic 描述
├── 操作: zotero_semantic_search(topic)
└── 输出: 按相似度排序的文献列表

阶段 3: 扩展检索
├── 输入: 已匹配的 item_key 列表
├── 操作:
│   ├── 获取文献的 tags/keywords
│   ├── 基于 tags 检索同主题文献
│   ├── 查找引用/被引用关系
│   └── 获取作者的其他著作
├── 输出: 扩展后的文献列表（去重）
└── 限制: additional_references 控制数量
```

### 4.2 文献匹配逻辑

```python
async def match_references(reference_titles: List[str], zotero_items: List) -> List[str]:
    """精确匹配用户提供的参考文献标题"""
    matched_keys = []
    for title in reference_titles:
        # 模糊匹配标题
        for item in zotero_items:
            if fuzzy_match(title, item.data.get("title", "")):
                matched_keys.append(item.key)
                break
    return matched_keys

async def expand_references(item_keys: List[str], limit: int = 5) -> List[str]:
    """基于已有文献扩展检索更多相关文献"""
    expanded = set()
    for key in item_keys:
        # 获取文献的 tags
        metadata = zotero_get_item_metadata(key)
        tags = extract_tags(metadata)

        # 基于 tags 检索（每 tag 最多 limit 篇）
        for tag in tags[:3]:  # 最多用 3 个 tag
            results = zotero_search_by_tag([tag], limit=limit)
            for item_key in extract_item_keys(results):
                expanded.add(item_key)

    return list(expanded)[:limit * len(item_keys)]
```

### 4.3 检索结果汇总

```markdown
**文献检索结果:**
- 精确匹配: {n} 篇
- 语义检索: {m} 篇
- 扩展检索: {k} 篇
- 解析成功: {p} 篇
- 跳过: {s} 篇（无 PDF）

**已解析文献列表:**
1. {title1} (key: xxx, 相似度: 0.95)
2. {title2} (key: xxx, 标签扩展)
```

---

## 5. 组件设计

### 5.1 目录结构

```
academic-writing/
├── .claude-plugin/
│   └── plugin.json              # 插件清单
├── commands/
│   └── academic-write.md        # /academic-write 命令
├── agents/
│   └── academic-writer.md       # 学术写作代理
├── skills/
│   ├── academic-writing-workflow/
│   │   └── SKILL.md             # 主工作流技能
│   ├── requirement-parser/
│   │   └── SKILL.md             # 需求解析技能
│   ├── reference-manager/
│   │   └── SKILL.md             # 参考文献管理技能
│   └── paper-writer/
│       └── SKILL.md             # 学术写作技能
├── hooks/
│   └── hooks.json               # 钩子配置（可选）
└── README.md                    # 插件说明文档
```

### 5.2 plugin.json

```json
{
  "name": "academic-writing",
  "version": "1.0.0",
  "description": "学术写作助手：集成 Zotero 文献检索、MinerU 解析、scientific-skills 写作",
  "author": {
    "name": "User",
    "email": "user@example.com"
  },
  "keywords": ["writing", "academic", "zotero", "research"]
}
```

### 5.3 技能设计

#### 5.3.1 academic-writing-workflow (主工作流技能)

**触发条件:** 用户启动学术写作流程时自动激活

**工作流程:**
```
1. 接收用户提供的需求文件路径
2. 调用 requirement-parser 解析需求
3. 使用 superpowers:brainstorming 生成大纲
4. 调用 reference-manager 检索和解析文献
5. 调用 paper-writer 生成论文
6. 返回输出文件路径
```

#### 5.3.2 requirement-parser (需求解析技能)

**功能:**
- 读取并解析 YAML frontmatter
- 验证必填字段
- 转换为内部数据结构

**输出格式:**
```markdown
**已解析需求:**
- 标题: {title}
- 主题: {topic}
- 字数: ~{length}
- 风格: {style}
- 参考文献: {n} 篇
- 额外检索: {additional_references} 篇
- 扩展检索: {expand_from_references}

**建议行动:**
- [确认] 开始生成写作大纲
- [修改] 返回修改需求
```

#### 5.3.3 reference-manager (参考文献管理技能)

**依赖工具:** zotero-mcp

**功能:**
- `zotero_semantic_search(topic)` - 语义检索
- 精确匹配 `reference_titles` 中的文献
- `zotero_get_item_fulltext(item_key)` - 获取全文并转换为 MD
- 扩展检索相关文献

**输出格式:**
```markdown
**文献检索结果:**
- 匹配文献: {n} 篇
- 解析成功: {m} 篇
- 跳过: {k} 篇（无 PDF）

**已解析文献列表:**
1. {title1} (key: xxx)
2. {title2} (key: xxx)
```

#### 5.3.4 paper-writer (学术写作技能)

**依赖:** scientific-skills 中的 `scientific-writing`

**功能:**
- 基于需求和大纲生成论文
- 注入解析后的文献作为上下文
- 引用格式: 保持原有引用或生成占位符

### 5.4 命令设计

**命令:** `/academic-write`

**文件:** `commands/academic-write.md`

**使用方式:** `/academic-write ./path/to/requirement.md`

**执行流程:**
```markdown
1. **确认需求文件**
   - 读取: {用户提供的路径}
   - 调用: requirement-parser 解析
   - 返回: 解析结果摘要

2. **用户确认**
   - 显示解析结果
   - 等待用户确认或修改
   - 用户确认后继续

3. **执行写作流程**
   - 调用: academic-writing-workflow 技能
   - 传递: 解析后的需求数据

4. **返回结果**
   - 输出文件路径
   - 显示摘要统计
```

### 5.5 代理设计

**代理:** `academic-writer`

**文件:** `agents/academic-writer.md`

**角色定义:**
```markdown
---
description: 专业的学术写作助手，负责根据需求撰写学术论文
model: opus
---

你是学术写作专家，负责:
1. 理解用户的研究需求
2. 规划和撰写结构清晰的学术论文
3. 正确引用和参考相关文献
4. 遵循学术写作规范

写作原则:
- 逻辑严谨，论证充分
- 语言专业，避免口语化
- 引用准确，格式规范
- 结构完整，符合学术惯例
```

---

## 6. 部署与测试

### 6.1 开发流程

1. **本地开发:** 创建 `academic-writing/` 目录，参照结构创建文件
2. **本地安装:** `/plugin local add ./academic-writing`
3. **测试:** 使用示例需求文件运行写作流程
4. **发布准备:** 添加完整 README、截图、使用示例

### 6.2 测试用例

**测试 1: 基础需求解析**
```markdown
---
title: "Deep Learning for Image Classification"
topic: "CNN architectures for image recognition"
length: 2000
style: "academic"
references:
  - "AlexNet"
  - "VGGNet"
---
```

**测试 2: 完整需求（含扩展检索）**
```markdown
---
title: "Transformer Models in NLP"
topic: "Attention mechanisms and BERT"
length: 5000
style: "academic"
references:
  - "Attention Is All You Need"
  - "BERT: Pre-training of Deep Bidirectional Transformers"
additional_references: 10
expand_from_references: true
---

# 研究背景
Transformers have revolutionized NLP...

# 大纲要点
1. Introduction
2. Related Work
3. Method
4. Experiments
5. Conclusion
```

---

## 7. 依赖关系

### 7.1 必需依赖

| 依赖 | 用途 | 安装方式 |
|------|------|----------|
| zotero-mcp | 文献检索和 PDF 获取 | MCP server |
| claude-scientific-skills | scientific-writing 技能 | 插件市场 |
| superpowers | 工作流框架 | 插件市场 |

### 7.2 可选依赖

| 依赖 | 用途 | 说明 |
|------|------|------|
| MinerU | PDF 解析质量提升 | 需要 API token |

---

## 8. 后续任务

实施计划详见各任务文档。核心任务包括：

1. 创建插件目录结构和基础文件
2. 实现 requirement-parser 技能
3. 实现 reference-manager 技能（集成 zotero-mcp）
4. 实现 academic-writing-workflow 技能
5. 实现 paper-writer 技能（集成 scientific-skills）
6. 创建 academic-write 命令
7. 创建 academic-writer 代理
8. 编写 README 和测试用例
