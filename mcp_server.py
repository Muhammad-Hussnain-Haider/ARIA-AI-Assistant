"""
ARIA MCP Server — Model Context Protocol Server
Exposes ARIA tools as MCP resources for Antigravity IDE integration.
"""

import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types as mcp_types
from tools import (
    get_tasks, add_task, complete_task, delete_task,
    get_medicines, add_medicine, mark_medicine_taken,
    get_budget, add_expense, set_budget_limit,
    get_goals, add_goal, update_goal_progress,
    get_daily_summary
)

# Initialize MCP Server
server = Server("aria-mcp-server")

@server.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    """List all available ARIA tools via MCP."""
    return [
        mcp_types.Tool(
            name="aria_get_tasks",
            description="Get all tasks for today from ARIA",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        mcp_types.Tool(
            name="aria_add_task",
            description="Add a new task to ARIA",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "time": {"type": "string"},
                    "priority": {"type": "string", "enum": ["high", "medium", "low"]}
                },
                "required": ["title"]
            }
        ),
        mcp_types.Tool(
            name="aria_get_medicines",
            description="Get all medicine reminders from ARIA",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        mcp_types.Tool(
            name="aria_get_budget",
            description="Get budget summary from ARIA",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        mcp_types.Tool(
            name="aria_get_goals",
            description="Get all goals from ARIA",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        mcp_types.Tool(
            name="aria_daily_summary",
            description="Get full daily summary from ARIA",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[mcp_types.TextContent]:
    """Handle tool calls from MCP clients."""
    result = ""

    if name == "aria_get_tasks":
        result = get_tasks()
    elif name == "aria_add_task":
        result = add_task(**arguments)
    elif name == "aria_get_medicines":
        result = get_medicines()
    elif name == "aria_get_budget":
        result = get_budget()
    elif name == "aria_get_goals":
        result = get_goals()
    elif name == "aria_daily_summary":
        result = get_daily_summary()
    else:
        result = f"Unknown tool: {name}"

    return [mcp_types.TextContent(type="text", text=result)]

async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
