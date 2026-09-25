# Project Context

## What this is
A learning project from Anthropic's **Introduction to MCP** course.
Goal: understand how to build MCP (Model Context Protocol) servers that extend Claude's capabilities.

## Key MCP concepts covered here

| Concept | What it does |
|---------|-------------|
| **Tool** | A function Claude can call to take an action (read, edit, search...) |
| **Resource** | A data source Claude can read (like a file or DB row) — _TODO_ |
| **Prompt** | A reusable prompt template Claude can invoke — _TODO_ |

## Files
- `mcp_server.py` — the MCP server, built with FastMCP

## TODOs (from the course)
- [ ] Resource: return contents of a specific doc
- [ ] Prompt: rewrite a doc in markdown format
- [ ] Prompt: summarize a doc

## Useful commands
```bash
# Run the server directly (for testing)
python mcp_server.py
```
