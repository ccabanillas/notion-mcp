"""MCP server implementation for Notion integration."""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent, EmbeddedResource
from typing import Any, Dict, List, Optional, Sequence, Union
import os
import json
from datetime import datetime
import logging
from pathlib import Path
from dotenv import load_dotenv
import rich
from rich.logging import RichHandler

from .client import NotionClient
from .models.notion import Database, Page, SearchResults, Block

# Set up enhanced logging with rich - directing logs to stderr to avoid breaking MCP
import sys
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, console=rich.console.Console(file=sys.stderr))]
)
logger = logging.getLogger('notion_mcp')

# Find and load .env file from project root
project_root = Path(__file__).parent.parent.parent
env_path = project_root / '.env'
if not env_path.exists():
    raise FileNotFoundError(f"No .env file found at {env_path}")
load_dotenv(env_path)

# Configuration with validation
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
if not NOTION_API_KEY:
    raise ValueError("NOTION_API_KEY not found in .env file")

# Initialize server with name only (MCP 1.6.0 compatible)
server = Server("notion-mcp")

# Initialize Notion client
notion_client = NotionClient(NOTION_API_KEY)

# Roots functionality not supported in MCP 1.6.0
# Leaving a comment to indicate future enhancement when MCP is upgraded

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available Notion tools."""
    return [
        Tool(
            name="list_databases",
            description="List all accessible Notion databases",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_database",
            description="Get details about a specific Notion database",
            inputSchema={
                "type": "object",
                "properties": {
                    "database_id": {
                        "type": "string",
                        "description": "ID of the database to retrieve"
                    }
                },
                "required": ["database_id"]
            }
        ),
        Tool(
            name="query_database",
            description="Query items from a Notion database",
            inputSchema={
                "type": "object",
                "properties": {
                    "database_id": {
                        "type": "string",
                        "description": "ID of the database to query"
                    },
                    "filter": {
                        "type": "object",
                        "description": "Optional filter criteria"
                    },
                    "sorts": {
                        "type": "array",
                        "description": "Optional sort criteria"
                    },
                    "start_cursor": {
                        "type": "string",
                        "description": "Cursor for pagination"
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of results per page",
                        "default": 100
                    }
                },
                "required": ["database_id"]
            }
        ),
        Tool(
            name="create_page",
            description="Create a new page in a database",
            inputSchema={
                "type": "object",
                "properties": {
                    "database_id": {
                        "type": "string",
                        "description": "ID of the database to create the page in"
                    },
                    "properties": {
                        "type": "object",
                        "description": "Page properties matching the database schema"
                    },
                    "children": {
                        "type": "array",
                        "description": "Optional page content blocks"
                    }
                },
                "required": ["database_id", "properties"]
            }
        ),
        Tool(
            name="update_page",
            description="Update an existing page",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_id": {
                        "type": "string",
                        "description": "ID of the page to update"
                    },
                    "properties": {
                        "type": "object",
                        "description": "Updated page properties"
                    },
                    "archived": {
                        "type": "boolean",
                        "description": "Whether to archive the page"
                    }
                },
                "required": ["page_id", "properties"]
            }
        ),
        Tool(
            name="get_block_children",
            description="Get the children blocks of a block",
            inputSchema={
                "type": "object",
                "properties": {
                    "block_id": {
                        "type": "string",
                        "description": "ID of the block to get children for"
                    },
                    "start_cursor": {
                        "type": "string",
                        "description": "Cursor for pagination"
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of results per page",
                        "default": 100
                    }
                },
                "required": ["block_id"]
            }
        ),
        Tool(
            name="search",
            description="Search Notion content",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string"
                    },
                    "filter": {
                        "type": "object",
                        "description": "Filter criteria for search results"
                    },
                    "sort": {
                        "type": "object",
                        "description": "Sort criteria for search results"
                    },
                    "start_cursor": {
                        "type": "string",
                        "description": "Cursor for pagination"
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of results per page",
                        "default": 100
                    }
                },
                "required": []
            }
        )
    ]

# Resources functionality not supported in MCP 1.6.0
# Leaving a comment to indicate future enhancement when MCP is upgraded

@server.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[Union[TextContent, EmbeddedResource]]:
    """Handle tool calls for Notion operations."""
    try:
        if name == "list_databases":
            databases = await notion_client.list_databases()
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "databases": [db.model_dump() for db in databases]
                    }, indent=2, default=str)
                )
            ]
            
        elif name == "get_database":
            if not isinstance(arguments, dict):
                raise ValueError("Invalid arguments")
                
            database_id = arguments.get("database_id")
            if not database_id:
                raise ValueError("database_id is required")
                
            database = await notion_client.get_database(database_id)
            return [
                TextContent(
                    type="text",
                    text=database.model_dump_json(indent=2)
                )
            ]
            
        elif name == "query_database":
            if not isinstance(arguments, dict):
                raise ValueError("Invalid arguments")
                
            database_id = arguments.get("database_id")
            if not database_id:
                raise ValueError("database_id is required")
                
            results = await notion_client.query_database(
                database_id=database_id,
                filter=arguments.get("filter"),
                sorts=arguments.get("sorts"),
                start_cursor=arguments.get("start_cursor"),
                page_size=arguments.get("page_size", 100)
            )
            return [
                TextContent(
                    type="text",
                    text=json.dumps(results, indent=2, default=str)
                )
            ]
            
        elif name == "create_page":
            if not isinstance(arguments, dict):
                raise ValueError("Invalid arguments")
                
            database_id = arguments.get("database_id")
            properties = arguments.get("properties")
            if not database_id or not properties:
                raise ValueError("database_id and properties are required")
                
            page = await notion_client.create_page(
                parent_id=database_id,
                properties=properties,
                children=arguments.get("children")
            )
            return [
                TextContent(
                    type="text",
                    text=page.model_dump_json(indent=2)
                )
            ]
            
        elif name == "update_page":
            if not isinstance(arguments, dict):
                raise ValueError("Invalid arguments")
                
            page_id = arguments.get("page_id")
            properties = arguments.get("properties")
            if not page_id or not properties:
                raise ValueError("page_id and properties are required")
                
            page = await notion_client.update_page(
                page_id=page_id,
                properties=properties,
                archived=arguments.get("archived")
            )
            return [
                TextContent(
                    type="text",
                    text=page.model_dump_json(indent=2)
                )
            ]
            
        elif name == "get_block_children":
            if not isinstance(arguments, dict):
                raise ValueError("Invalid arguments")
                
            block_id = arguments.get("block_id")
            if not block_id:
                raise ValueError("block_id is required")
                
            results = await notion_client.get_block_children(
                block_id=block_id,
                start_cursor=arguments.get("start_cursor"),
                page_size=arguments.get("page_size", 100)
            )
            return [
                TextContent(
                    type="text",
                    text=json.dumps(results, indent=2, default=str)
                )
            ]
            
        elif name == "search":
            if not isinstance(arguments, dict):
                raise ValueError("Invalid arguments")
                
            query = arguments.get("query", "")
            results = await notion_client.search(
                query=query,
                filter=arguments.get("filter"),
                sort=arguments.get("sort"),
                start_cursor=arguments.get("start_cursor"),
                page_size=arguments.get("page_size", 100)
            )
            return [
                TextContent(
                    type="text",
                    text=results.model_dump_json(indent=2)
                )
            ]
            
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}")
        return [
            TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )
        ]

async def main():
    """Run the server."""
    if not NOTION_API_KEY:
        raise ValueError("NOTION_API_KEY environment variable is required")
    
    logger.info("Starting Notion MCP Server v0.2.0")
    logger.info(f"Using Notion API with key: {NOTION_API_KEY[:4]}...")
    
    try:
        # Test connection to Notion API
        databases = await notion_client.list_databases()
        logger.info(f"Successfully connected to Notion API. Found {len(databases)} accessible databases.")
    except Exception as e:
        logger.error(f"Failed to connect to Notion API: {str(e)}")
        raise
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
