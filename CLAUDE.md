# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Monorepo for an **automatic academic writing plugin** for Claude Code. Integrates multiple components:

- **zotero-mcp** (Python): MCP server for Zotero library access
- **cookjohn-zotero-mcp** (TypeScript): Alternative Zotero MCP as a Zotero plugin
- **auto-academic-writing/**: Academic writing plugin with commands, skills, and agents
- **superpowers/**: Core skills library (TDD, debugging, brainstorming, collaboration patterns)
- **claude-scientific-skills/**: 139 scientific research and writing skills

### Two Zotero MCP Variants

| Feature | zotero-mcp (Python) | cookjohn-zotero-mcp (TS) |
|---------|---------------------|--------------------------|
| Semantic search | Yes | Yes |
| PDF full-text extraction | Yes | Limited |
| Tag-based expansion | Yes | Limited |
| Annotation extraction | Yes | No |
| Local SQLite access | Yes | No |

The auto-academic-writing plugin auto-detects and uses whichever is available.

## Commands

### Zotero MCP (Python)
```bash
cd zotero-mcp
pip install -e .                    # Dev install
pip install pre-commit && pre-commit install
pre-commit run --all-files          # Linting (black, isort, pyupgrade)
pytest                              # Testing
python -m build                     # Build distribution
```

### Superpowers
```bash
cd superpowers
./hooks/run-hook.cmd session-start.sh  # Session initialization
```

## Architecture

### Zotero MCP (`zotero-mcp/`)
- **CLI** (`src/zotero_mcp/cli.py`): `zotero-mcp` command with `serve`, `setup`, `update-db`, `db-status` subcommands
- **Server** (`src/zotero_mcp/server.py`): FastMCP-based server with 20+ tools
- **Key modules**: `client.py` (Zotero API), `local_db.py` (SQLite), `semantic_search.py` (ChromaDB)

### Auto-Academic-Writing Plugin (`auto-academic-writing/`)
- **Commands** (`commands/`): `/academic-write <path>` and `/academic-writing setup`
- **Skills** (`skills/`): `requirement-parser`, `reference-manager`, `academic-writing-workflow`, `paper-writer`
- **Agents** (`agents/`): `academic-writer` agent

### Scientific Skills (`claude-scientific-skills/`)
Each skill is a directory with `SKILL.md`, `references/`, and `scripts/`. Categories include bioinformatics, cheminformatics, clinical research, ML, and scientific writing.

### Superpowers (`superpowers/skills/`)
Process-oriented skills: `brainstorming/`, `test-driven-development/`, `systematic-debugging/`, `writing-plans/`.

## Workflow

1. Use `/superpowers:brainstorm` to plan based on requirements
2. Use Zotero MCP for reference search and retrieval
3. Parse references (PDF → Markdown via Zotero MCP's markitdown integration)
4. Read references as context for writing
5. Use `/scientific-skills` for academic writing assistance

## Configuration

- Zotero MCP config: `~/.config/zotero-mcp/config.json`
- Auto-writing config: `~/.config/auto-writing/config.json`
- Local marketplace: Add `"allowedMarkets": ["local"]` to Claude Desktop config