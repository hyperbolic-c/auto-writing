# Academic Writing Plugin

学术写作助手：集成 Zotero 文献检索、MinerU 解析、scientific-skills 写作

一个基于 Claude Code 的学术写作插件，自动完成从需求解析、文献检索到论文生成的全流程。

## 功能特性

| 功能 | 描述 |
|------|------|
| **需求解析** | 解析 YAML 格式的需求文件，提取标题、主题、字数、风格、参考文献等 |
| **文献检索** | 三阶段检索：精确匹配 + 语义检索 + 扩展检索 |
| **全文获取** | 自动下载 Zotero 中的 PDF 附件并转换为 Markdown |
| **学术写作** | 基于参考文献生成结构化的学术论文 |

## 安装

### 前置依赖

安装本插件前，请确保已安装以下依赖：

```bash
# 安装 zotero-mcp
/plugin marketplace add hyperbolic-c/zotero-mcp

# 安装 scientific-skills
/plugin marketplace add K-Dense-AI/claude-scientific-skills

# 安装 superpowers
/plugin marketplace add obra/superpowers
```

### 安装本插件

```bash
/plugin local add ./features/academic-writing
```

### Zotero MCP 配置

确保 Zotero MCP 已正确配置并能访问你的 Zotero 库：

```bash
zotero-mcp setup
```

## 使用方法

### 1. 创建需求文件

创建一个 Markdown 文件，包含 YAML frontmatter：

```markdown
---
title: "论文标题（英文）"
topic: 研究主题简要描述（用于 Zotero 语义检索）
length: 3000
style: academic
references:
  - "参考文献标题 1"
  - "参考文献标题 2"
  - "参考文献标题 3"
additional_references: 5    # 可选：额外检索数量，默认 5
expand_from_references: true # 可选：是否扩展检索，默认 true
---

# 研究背景
（可选）补充说明研究背景和动机

# 大纲要点
（可选）用户指定的章节结构提示
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | 是 | 论文标题 |
| `topic` | 是 | 研究主题描述，用于语义检索 |
| `length` | 是 | 预估字数 |
| `style` | 是 | 写作风格（academic, technical, review） |
| `references` | 是 | Zotero 中的参考文献标题列表 |
| `additional_references` | 否 | 额外检索数量，默认 5 |
| `expand_from_references` | 否 | 是否基于参考文献扩展，默认 true |

### 2. 启动写作流程

在 Claude Code 中执行：

```
/academic-write ./path/to/requirements.md
```

### 3. 确认与审阅

1. 插件解析需求文件，显示摘要
2. 确认后自动执行文献检索和论文生成
3. 查看生成的论文，提出修改意见
4. 根据反馈迭代修改

## 工作流程

```
用户需求文件 (.md)
       ↓
需求解析 → 提取: title, topic, length, style, references
       ↓
文献检索阶段:
├── 精确匹配 reference_titles
├── 语义检索 topic
└── 扩展检索（基于 tags/作者/引用关系）
       ↓
获取全文 → PDF 下载 → Markdown 转换
       ↓
scientific-skills → 生成论文
       ↓
输出: output.md
```

## 文件结构

```
academic-writing/
├── .claude-plugin/
│   └── plugin.json              # 插件清单
├── commands/
│   └── academic-write.md        # /academic-write 命令
├── agents/
│   └── academic-writer.md       # 学术写作代理
├── skills/
│   ├── requirement-parser/      # 需求解析技能
│   ├── reference-manager/       # 参考文献管理技能
│   ├── academic-writing-workflow/  # 主工作流技能
│   └── paper-writer/            # 学术写作技能
├── examples/
│   └── sample-requirements.md   # 示例需求文件
├── hooks/
│   └── hooks.json               # 钩子配置
└── README.md                    # 本文件
```

## 示例

### 示例需求文件

参考 `examples/sample-requirements.md`：

```markdown
---
title: "Deep Learning for Image Classification"
topic: "CNN architectures for image recognition with deep neural networks"
length: 2000
style: "academic"
references:
  - "ImageNet Classification with Deep Convolutional Neural Networks"
  - "Very Deep Convolutional Networks for Large-Scale Image Recognition"
additional_references: 5
expand_from_references: true
---

# 研究背景
Deep learning has revolutionized computer vision...

# 大纲要点
1. Introduction
2. Related Work
3. Methodology
4. Experiments
5. Conclusion
```

## 依赖项

### Zotero MCP (二选一)

| 依赖 | 用途 | 仓库 |
|------|------|------|
| zotero-mcp (Python) | 文献检索和 PDF 获取 | [hyperbolic-c/zotero-mcp](https://github.com/hyperbolic-c/zotero-mcp) |
| cookjohn-zotero-mcp (TypeScript) | 文献检索（Zotero 插件集成） | [cookjohn/zotero-mcp](https://github.com/cookjohn/zotero-mcp) |

**说明:** 插件会自动检测并适配两个版本的 Zotero MCP。

| 功能 | Python 版本 | TypeScript 版本 |
|------|-------------|-----------------|
| 语义检索 | ✅ | ✅ |
| PDF 全文提取 | ✅ | ⚠️ 有限支持 |
| 标签扩展检索 | ✅ | ⚠️ 有限支持 |
| 全文注释提取 | ✅ | ❌ |

### 其他依赖

| 依赖 | 用途 | 仓库 |
|------|------|------|
| claude-scientific-skills | scientific-writing 技能 | [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) |
| superpowers | 工作流框架 | [obra/superpowers](https://github.com/obra/superpowers) |

## 常见问题

### Q: 参考文献匹配失败怎么办？

A: 确保 Zotero 中的文献标题与需求文件中的一致。可以使用部分标题进行模糊匹配。

### Q: 没有 PDF 附件的文献会怎样？

A: 插件会跳过该文献，只使用 metadata（如摘要）作为参考。

### Q: 如何控制文献检索数量？

A: 使用 `additional_references` 字段设置额外检索数量。

### Q: MinerU 不是必须的吗？

A: MinerU 是可选的。插件使用 Zotero MCP 内置的 PDF 转换功能，MinerU 可用于提升解析质量。

## 许可证

MIT
