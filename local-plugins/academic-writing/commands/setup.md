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

#### Step 4a: Generate Config Based on Input

| User Input | Config Content |
|------------|----------------|
| 1 | `{"mcp_provider": "zotero-mcp"}` |
| 2 | `{"mcp_provider": "zotero-mcp-plugin"}` |

#### Step 4b: Execute Terminal Commands

Generate and execute the following commands with the selected config:

```bash
# Create config directory
mkdir -p ~/.config/auto-writing

# Write config (use config content from Step 4a)
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

1. Display the welcome message and current configuration
2. Show the options table with both providers
3. Ask user for input (1 or 2)
4. Validate input, prompt again if invalid
5. Based on input:
   - If "1": Set `config_content='{"mcp_provider": "zotero-mcp"}'`
   - If "2": Set `config_content='{"mcp_provider": "zotero-mcp-plugin"}'`
6. Execute terminal commands with the generated config:
   ```bash
   mkdir -p ~/.config/auto-writing
   echo "$config_content" > ~/.config/auto-writing/config.json
   ```
7. Display confirmation message with selected provider

## Notes

- User needs to have the selected MCP Server configured in Claude Desktop
- Config file location: `~/.config/auto-writing/config.json`
- Can re-run this command to change configuration anytime
- Check current provider: `cat ~/.config/auto-writing/config.json`
