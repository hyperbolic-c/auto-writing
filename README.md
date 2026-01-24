# Auto-Writing

Automatic academic writing plugin for Claude Code.

## Overview

A monorepo for developing an **automatic academic writing plugin** that integrates:

- **Zotero MCP** - Reference management and PDF retrieval
- **MinerU** - PDF to Markdown conversion
- **Scientific Skills** - Academic writing capabilities
- **Superpowers** - Development workflow skills

## Project Structure

```
auto-writing/
├── .claude-plugin/
│   └── marketplace.json          # Auto-writing plugin marketplace
├── auto-academic-writing/        # Academic writing plugin
│   ├── commands/                 # /academic-write, /academic-writing setup
│   ├── skills/                   # requirement-parser, reference-manager, etc.
│   ├── agents/                   # academic-writer agent
│   ├── scripts/                  # Configuration utilities
│   └── README.md                 # Plugin documentation
├── superpowers/                  # Core skills library
├── claude-plugins-official/      # Official Claude plugins
├── claude-scientific-skills/     # Scientific research skills
├── zotero-mcp/                   # Zotero MCP server (Python)
├── cookjohn-zotero-mcp/          # Zotero MCP server (TypeScript/Zotero Plugin)
└── MinerU.py                     # PDF to Markdown conversion
```

## Plugins

### Auto-Academic-Writing

Academic writing assistant with Zotero integration.

**Commands:**
- `/academic-write <path>` - Start academic writing workflow
- `/academic-writing setup` - Configure MCP Provider

**Install:**
```bash
/plugin marketplace add hyperbolic-c/auto-writing
```

## Workflow

1. Use `/superpowers:brainstorm` to plan based on requirements
2. Use zotero-mcp for reference search and retrieval
3. Use MinerU API to parse references to markdown format
4. Read references as context for writing
5. Use `/scientific-skills` for academic writing

## License

MIT
