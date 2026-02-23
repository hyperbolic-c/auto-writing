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
/plugin marketplace add https://github.com/K-Dense-AI/claude-scientific-writer
/plugin install claude-scientific-writer
```

**Initialize:**
```bash
/scientific-writer:init
```

**Requirements:**
- ANTHROPIC_API_KEY (required)
- OPENROUTER_API_KEY (optional, for research lookup)

**Available Skills:** 20+ including scientific-schematics, research-lookup, peer-review, citation-management, clinical-reports, research-grants, latex-posters, scientific-slides, and more.

### Auto-Academic-Writing

Self-contained academic writing assistant with Zotero integration.

**Commands:**
- `/academic-write <path>` - Start academic writing workflow
- `/academic-writing-setup` - Configure MCP Provider

**Install:**
```bash
# Register the marketplace
/plugin marketplace add hyperbolic-c/auto-writing

# Install the academic-writing plugin from this marketplace
/plugin install academic-writing@hyperbolic-c/auto-writing
```

**Requirements:**
- [zotero-mcp](/zotero-mcp/) (Python) - Reference management and PDF retrieval
- [cookjohn-zotero-mcp](/cookjohn-zotero-mcp/) (TypeScript) - Zotero plugin alternative

## License

MIT
