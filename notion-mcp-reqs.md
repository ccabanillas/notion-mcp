# MCP Notion Server Development Prompt

Help me expand an existing Model Context Protocol server that will integrate with Notion's API. The server should:

## Core Functionality
- Modify existing server exposing Notion operations as MCP resources and tools
- Add Notion operations including:
  - Listing databases
  - Querying databases
  - Creating and updating pages
  - Handling blocks and content
  - Search functionality

## Technical Requirements
- Use Python 3.10+ with async/await
- Implement proper error handling and status codes
- Include type hints and validation
- Follow MCP protocol specifications for:
  - Resource definitions
  - Tool schemas
  - Response formats
  - Error handling

## Project Structure
Base the implementation on the MCP weather server example, but adapt for Notion:
- Use `notion-mcp` as project name
- Include configuration for Notion API authentication
- Structure handlers for different Notion object types

## Code Style
Generate code that is:
- Fully typed with pydantic models
- Well-documented with docstrings
- Includes unit tests
- Uses async patterns consistently
- Implements proper error handling

## Expected Functionality
First phase should include:
1. List databases
2. Query database items
3. Create/update pages
5. Search functionality

## Specific Requirements
- Use the official Notion Python SDK
- Implement caching where appropriate
- Add proper logging
- Include progress notifications for long operations
- Handle rate limiting

Please help me implement this server step by step, starting with the basic structure and building up to a complete implementation.