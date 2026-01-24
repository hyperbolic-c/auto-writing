# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a monorepo for developing an **automatic academic writing plugin** for Claude Code. The project integrates multiple existing components:

- **superpowers**: Core skills library (TDD, debugging, brainstorming, collaboration patterns)
- **claude-plugins-official**: Official Claude plugins (code-simplifier, code-review, etc.)
- **claude-scientific-skills**: 139 scientific skills for research and writing
- **zotero-mcp**: MCP server for Zotero reference management
- **local-plugins/**: Local plugin marketplace for custom plugins

### Local Plugins

| Plugin | Description |
|--------|-------------|
| `academic-writing` | Academic writing assistant with Zotero integration |

**Install local plugins:**
```bash
/plugin local add ./local-plugins/academic-writing
```

**Or configure local marketplace:**
Add `"allowedMarkets": ["local"]` to Claude Desktop config under `cli` section.

### Workflow (from workflow.md)

1. Use `/superpowers:brainstorm` to plan based on requirements
2. Use zotero-mcp for reference search and retrieval
3. Use MinerU API to parse references to markdown format
4. Read references as context for writing
5. Use `/scientific-skills` for academic writing

## Commands

### Zotero MCP
```bash
cd zotero-mcp
pip install -e .                    # Dev install
pip install pre-commit && pre-commit install
pre-commit run --all-files          # Linting
pytest                              # Testing
```

### Superpowers
```bash
cd superpowers
./hooks/run-hook.cmd session-start.sh  # Session initialization hook
```

## Architecture

### Zotero MCP (`zotero-mcp/`)
- **CLI** (`src/zotero_mcp/cli.py`): `zotero-mcp` command with `serve`, `setup`, `update-db` subcommands
- **Server** (`src/zotero_mcp/server.py`): FastMCP-based server with 20+ tools
- **Key modules**: `client.py` (Zotero API), `local_db.py` (SQLite), `semantic_search.py` (ChromaDB)

### Scientific Skills (`claude-scientific-skills/`)
Each skill is a directory with:
- `SKILL.md` - Skill documentation
- `references/` - Additional documentation and examples
- `scripts/` - Example Python scripts

Common skill categories: bioinformatics, cheminformatics, clinical research, machine learning, scientific writing.

### Superpowers (`superpowers/skills/`)
Process-oriented skills for development workflow:
- `brainstorming/` - Planning and ideation
- `test-driven-development/` - TDD workflows
- `systematic-debugging/` - Debugging techniques
- `writing-plans/` - Plan documentation

### Academic Writing Plugin (`features/academic-writing/` or `local-plugins/academic-writing/`)

**Commands:**
- `/academic-write <path>` - Start academic writing workflow
- `/academic-writing setup` - Configure MCP Provider

**Skills:**
- `requirement-parser` - Parse writing requirements from markdown
- `reference-manager` - Manage Zotero references (supports both zotero-mcp and zotero-mcp-plugin)
- `academic-writing-workflow` - Main workflow orchestration
- `paper-writer` - Academic paper writing skill

**Configuration:**
- Run `/academic-writing setup` to select MCP Provider (zotero-mcp or zotero-mcp-plugin)
- Config stored in: `~/.config/auto-writing/config.json`

