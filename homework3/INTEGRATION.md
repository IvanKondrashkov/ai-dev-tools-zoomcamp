# MCP Server Integration with Cursor

Instructions for integrating the MCP server with Cursor (Question 4):

## Method 1: Using mcp.json Configuration File

1. Open the Cursor configuration file: `C:\Users\<YourName>\.cursor\mcp.json`
2. Add the MCP server configuration:

```json
{
  "mcpServers": {
    "homework3": {
      "command": "uv",
      "args": [
        "--directory",
        "D:\\ai-dev-tools-zoomcamp\\homework3",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```
3. Restart Cursor

## Method 2: Using Cursor Settings UI

1. Open Cursor Settings
2. Find the MCP or Model Context Protocol section
3. Add a new MCP server with the following parameters:
   - **Name**: homework3 (or any name you prefer)
   - **Command**: `uv --directory D:\\ai-dev-tools-zoomcamp\\homework3 run python main.py`
     (Replace the path with your full project path)
   - **Transport**: STDIO

4. Restart Cursor

## Usage

After integration, you can ask Cursor:

```
Count how many times the word "data" appears on https://datatalks.club/
Use available MCP tools for that
```

Cursor will automatically use the available MCP tools (scrape_web, search_docs, add).