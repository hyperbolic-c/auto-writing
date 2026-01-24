---
name: academic-writing-setup
description: Configure academic-writing plugin MCP Provider
---

# Academic Writing Setup Command

## Usage

`/academic-writing setup`

## Function

Interactively configure the MCP Provider used by academic-writing plugin to get PDF content from Zotero.

## Execution Steps

### Step 1: Show Welcome Message

Display the welcome message and current configuration status.

### Step 2: Display Options

Show the two available MCP providers:

```
┌─ Select MCP Provider ─────────────────────────────────┐
│                                                        │
│  [1] zotero-mcp                                        │
│      - Python implementation                           │
│      - Requires running separate MCP Server            │
│      - Tool: zotero_get_item_fulltext                  │
│                                                        │
│  [2] zotero-mcp-plugin                                 │
│      - TypeScript/Zotero Plugin implementation         │
│      - Built-in PDF extraction                         │
│      - Tool: get_content                               │
│                                                        │
└────────────────────────────────────────────────────────┘

Enter 1 or 2:
```

### Step 3: Get User Input

- Validate input is "1" or "2"
- If invalid, prompt again with clear error message

### Step 4: Save Configuration

Execute terminal commands to save the selection:

```bash
# Create config directory
mkdir -p ~/.config/auto-writing

# Write config (replace with your choice)
echo '{"mcp_provider": "zotero-mcp"}' > ~/.config/auto-writing/config.json

# Verify
cat ~/.config/auto-writing/config.json
```

### Step 5: Display Result

```
**Configuration Complete**

Selected: zotero-mcp

Please ensure the selected MCP Server is configured in Claude Desktop.

Current Configuration:
- Provider: zotero-mcp
- Config File: ~/.config/auto-writing/config.json
```

## Implementation for Claude

When executing this command, Claude should:

1. Display the welcome message and options
2. Ask user for input (1 or 2)
3. Validate input and retry if invalid
4. Execute terminal commands to write config file
5. Display confirmation message

## Notes

- User needs to have the selected MCP Server configured in Claude Desktop
- Config file location: `~/.config/auto-writing/config.json`
- Can re-run this command to change configuration anytime
- Check current provider: `cat ~/.config/auto-writing/config.json`
