# Academic Writing Plugin

学术写作助手：集成 Zotero 文献检索和内置写作能力

一个自包含的 Claude Code 学术写作插件，自动完成从需求解析、文献检索到论文生成的全流程。

## 功能特性

| 功能 | 描述 |
|------|------|
| **需求解析** | 解析 YAML 格式的需求文件，提取标题、主题、字数、风格、参考文献等 |
| **大纲生成** | 基于研究主题生成结构化的论文大纲 |
| **文献检索** | 三阶段检索：精确匹配 + 语义检索 + 扩展检索 |
| **全文获取** | 自动下载 Zotero 中的 PDF 附件并转换为 Markdown |
| **学术写作** | 基于参考文献生成 IMRAD 结构的学术论文 |

## 安装

### 前置依赖

安装本插件前，请确保已在 Claude Code 中安装 **Zotero MCP**（二选一）：

| 依赖 | 安装命令 | 说明 |
|------|----------|------|
| zotero-mcp (Python) | `/plugin marketplace add hyperbolic-c/zotero-mcp` | 功能完整，推荐使用 |
| cookjohn-zotero-mcp | `/plugin marketplace add cookjohn/zotero-mcp` | Zotero 插件形式 |

**注意:** v2.0.0 已内置写作技能，无需安装 scientific-skills 或 superpowers。

### 安装本插件

通过插件市场安装（推荐）：

```bash
/plugin marketplace add hyperbolic-c/auto-writing
```

或直接从源码安装：

```bash
/plugin local add ./auto-academic-writing
```

### 配置 MCP Provider

首次安装后，需要配置学术写作插件使用哪个 MCP Provider 获取 PDF 内容：

```bash
/academic-writing setup
```

此命令会交互式地让你选择：

| 选项 | 说明 |
|------|------|
| [1] zotero-mcp | Python 实现，功能完整 |
| [2] zotero-mcp-plugin | TypeScript/Zotero 插件形式 |

选择后配置会保存到 `~/.config/auto-writing/config.json`。

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
内置 brainstorming → 生成论文大纲
       ↓
文献检索阶段:
├── 精确匹配 reference_titles
├── 语义检索 topic
└── 扩展检索（基于 tags/作者/引用关系）
       ↓
获取全文 → PDF 下载 → Markdown 转换
       ↓
内置 paper-writer → 生成论文
       ↓
输出: output.md
```

## 文件结构

```
auto-academic-writing/
├── .claude-plugin/
│   └── plugin.json              # 插件清单
├── commands/
│   ├── academic-write.md        # /academic-write 命令
│   └── setup.md                 # /academic-writing setup 命令
├── agents/
│   └── academic-writer.md       # 学术写作代理
├── skills/
│   ├── requirement-parser/      # 需求解析技能
│   ├── reference-manager/       # 参考文献管理技能
│   ├── academic-writing-workflow/  # 主工作流技能
│   ├── brainstorming/           # 内置大纲生成技能
│   └── paper-writer/            # 内置学术写作技能
├── scripts/
│   └── config.py                # 配置脚本
├── examples/
│   └── sample-requirements.md   # 示例需求文件
├── hooks/
│   └── hooks.json               # 钩子配置
├── docs/
│   └── plans/                   # 设计文档
└── README.md                    # 本文件
```

## 内置技能

### brainstorming

基于研究主题生成结构化的论文大纲。采用两阶段流程：理解需求 → 生成大纲。

### paper-writer

核心学术写作技能，生成 IMRAD 结构的论文：
- **Two-Stage 写作**: 大纲 → 完整段落
- **IMRAD 结构**: Introduction, Related Work, Methods, Results, Discussion, Conclusion
- **引文格式**: APA, AMA, Vancouver, IEEE, Chicago
- **写作原则**: 清晰、简洁、准确、客观

## 依赖项

### Zotero MCP (二选一)

| 依赖 | 安装命令 | 仓库 |
|------|----------|------|
| zotero-mcp (Python) | `/plugin marketplace add hyperbolic-c/zotero-mcp` | [hyperbolic-c/zotero-mcp](https://github.com/hyperbolic-c/zotero-mcp) |
| cookjohn-zotero-mcp (TS) | `/plugin marketplace add cookjohn/zotero-mcp` | [cookjohn/zotero-mcp](https://github.com/cookjohn/zotero-mcp) |

**配置:** 安装后运行 `/academic-writing setup` 选择使用的 Provider。 |

**说明:** 插件会自动检测并适配两个版本的 Zotero MCP。

| 功能 | Python 版本 | TypeScript 版本 |
|------|-------------|-----------------|
| 语义检索 | ✅ | ✅ |
| PDF 全文提取 | ✅ | ⚠️ 有限支持 |
| 标签扩展检索 | ✅ | ⚠️ 有限支持 |
| 全文注释提取 | ✅ | ❌ |

### 可选依赖

| 依赖 | 用途 | 说明 |
|------|------|------|
| MinerU | PDF 解析质量提升 | 需要 API token，用于提升 PDF 转换质量 |

## 常见问题

### Q: 参考文献匹配失败怎么办？

A: 确保 Zotero 中的文献标题与需求文件中的一致。可以使用部分标题进行模糊匹配。

### Q: 没有 PDF 附件的文献会怎样？

A: 插件会跳过该文献，只使用 metadata（如摘要）作为参考。

### Q: 如何控制文献检索数量？

A: 使用 `additional_references` 字段设置额外检索数量。

### Q: MinerU 不是必须的吗？

A: MinerU 是可选的。插件使用 Zotero MCP 内置的 PDF 转换功能，MinerU 可用于提升解析质量。

## 更新日志

### v2.0.0

- **BREAKING**: 移除对 scientific-skills 和 superpowers 的依赖
- 新增内置 brainstorming 技能
- 合并 scientific-writing 到 paper-writer
- 插件现在自包含所有写作能力

## 许可证

MIT
