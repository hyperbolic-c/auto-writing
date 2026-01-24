# Local Plugin Marketplace

This directory serves as a local plugin marketplace for the auto-writing project.

## Usage

### Method 1: Configure CLAUDE_ORIGINS

Add the following to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    // ... your MCP servers ...
  },
  "cli": {
    "allowedMarkets": ["local"]
  }
}
```

### Method 2: Install from Local Path

Use the direct path installation:

```bash
/plugin local add ./local-plugins/academic-writing
```

## Marketplace Structure

```
local-plugins/
├── marketplace.json           # Marketplace manifest
└── academic-writing/          # Plugin directory
    ├── .claude-plugin/
    │   └── plugin.json
    ├── commands/
    ├── skills/
    ├── agents/
    └── README.md
```

## Plugins

### academic-writing

Academic writing assistant with Zotero integration.

**Commands:**
- `/academic-write <path>` - Start academic writing workflow
- `/academic-writing setup` - Configure MCP Provider

**Dependencies:**
- zotero-mcp (Python version) or zotero-mcp-plugin (TypeScript version)
- claude-scientific-skills
- superpowers

## Adding New Plugins

1. Create plugin directory under `local-plugins/`
2. Add plugin entry to `marketplace.json`
3. Install with: `/plugin local add ./local-plugins/<plugin-name>`
