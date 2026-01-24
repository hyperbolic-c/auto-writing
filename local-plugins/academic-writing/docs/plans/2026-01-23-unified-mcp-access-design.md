# Unified MCP Access 设计方案

> **Date:** 2026-01-23
> **Branch:** feature/unified-mcp-access

## 1. 功能概述

在 `academic-writing` 插件中添加 MCP Provider 选择功能，允许用户配置使用 `zotero-mcp` 或 `zotero-mcp-plugin` 获取 PDF 内容。

## 2. 架构

```
academic-writing/
├── commands/
│   └── setup.md              # 交互式初始化命令（新增）
├── skills/
│   └── reference-manager/
│       └── SKILL.md          # 添加 Provider 选择逻辑（修改）
└── docs/
    └── plans/
        └── 2026-01-23-unified-mcp-access-design.md
```

## 3. 交互式初始化

### 命令

```bash
/academic-writing setup
```

### 执行流程

```
用户运行 /academic-writing setup
       ↓
显示选项让用户选择 MCP Provider
       ↓
保存选择到配置文件 ~/.config/auto-writing/config.json
       ↓
显示配置成功信息
```

### 选项

| 选项 | 说明 |
|------|------|
| [1] zotero-mcp | Python 实现，需要单独运行 MCP Server |
| [2] zotero-mcp-plugin | TypeScript/Zotero 插件实现，内置 PDF 提取 |

## 4. 配置

**配置文件:** `~/.config/auto-writing/config.json`

```json
{
  "mcp_provider": "zotero-mcp"  // 或 "zotero-mcp-plugin"
}
```

## 5. 工具映射

| 功能 | zotero-mcp | zotero-mcp-plugin |
|------|------------|-------------------|
| 获取 PDF 全文 | `zotero_get_item_fulltext` | `get_content` |
| 全文检索 | `zotero_search_fulltext` | `search_fulltext` |
| 获取摘要 | `zotero_get_item_abstract` | `get_item_abstract` |

## 6. 实现任务

1. 创建 `commands/setup.md` - 交互式初始化命令
2. 修改 `skills/reference-manager/SKILL.md` - 添加 Provider 选择逻辑
3. 创建配置文件工具函数
