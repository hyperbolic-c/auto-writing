# Auto-Writing

Automatic academic writing plugin for Claude Code.

## Overview

A monorepo for developing an **automatic academic writing plugin** that integrates:

- **Zotero MCP** - Reference management and PDF retrieval
- **Built-in skills** - Academic writing and brainstorming capabilities

## Project Structure

```
auto-writing/
├── .claude-plugin/
│   └── marketplace.json          # Auto-writing plugin marketplace
├── auto-academic-writing/        # Academic writing plugin
│   ├── commands/                 # /academic-write, /academic-writing-setup
│   ├── skills/                   # Built-in skills (brainstorming, paper-writer, etc.)
│   ├── agents/                   # academic-writer agent
│   ├── scripts/                  # Configuration utilities
│   └── README.md                 # Plugin documentation
├── superpowers/                  # Core skills library (for reference)
├── claude-plugins-official/      # Official Claude plugins
├── claude-scientific-skills/     # Scientific research skills (for reference)
├── zotero-mcp/                   # Zotero MCP server (Python)
├── cookjohn-zotero-mcp/          # Zotero MCP server (TypeScript/Zotero Plugin)
└── MinerU.py                     # PDF to Markdown conversion (optional)
```

## Plugins

### Claude Scientific Writer

Deep research and writing tool with AI-driven research and well-formatted outputs. Generate publication-ready scientific papers, reports, posters, grant proposals, literature reviews, and more—all backed by real-time literature search and verified citations.

**Install:**
```bash
/plugin marketplace add hyperbolic-c/auto-writing
/plugin install claude-scientific-writer@hyperbolic-c/auto-writing
```

**Initialize:**
```bash
/scientific-writer:init
```

**Requirements:**
- [zotero-mcp](https://github.com/54yyyu/zotero-mcp) - Reference management and PDF retrieval
- [cookjohn-zotero-mcp](https://github.com/cookjohn/zotero-mcp) (TypeScript) - Zotero plugin alternative

**Available Skills:** 20+ including scientific-schematics, research-lookup, peer-review, citation-management, clinical-reports, research-grants, latex-posters, scientific-slides, and more.

## License

MIT
