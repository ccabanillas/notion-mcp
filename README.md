# Notion MCP Server
[![smithery badge](https://smithery.ai/badge/@ccabanillas/notion-mcp)](https://smithery.ai/server/@ccabanillas/notion-mcp)

A Model Context Protocol (MCP) server implementation for Notion integration, providing a standardized interface for interacting with Notion's API. Compatible with Claude Desktop and other MCP clients.

## Features

- List and query Notion databases
- Create and update pages
- Search across Notion workspace
- Get database details and block children
- Full async/await support with httpx
- Type-safe with Pydantic v2 models
- Proper error handling with detailed logging
- Compatibility with MCP 1.6.0

## Installation

### Installing via Smithery

To install Notion Integration Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@ccabanillas/notion-mcp):

```bash
npx -y @smithery/cli install @ccabanillas/notion-mcp --client claude
```

### Manual Installation
1. Clone the repository:
```bash
git clone https://github.com/ccabanillas/notion-mcp.git
cd notion-mcp
```

2. Create a virtual environment and install dependencies (using uv):
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

Alternatively, using standard venv:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

3. Create a `.env` file in the project root:
```bash
NOTION_API_KEY=your_notion_integration_token
```

## Usage

1. Test the server (it should run without errors):
```bash
python -m notion_mcp
```

2. To use it with Claude Desktop, adjust your `claude_desktop_config.json` file (located at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "servers": {
    "notion-mcp": {
      "command": "/Users/username/Projects/notion-mcp/.venv/bin/python",
      "args": ["-m", "notion_mcp"],
      "cwd": "/Users/username/Projects/notion-mcp"
    }
  }
}
```

Be sure to replace `/Users/username/` with your actual home directory path.

## Development

### Project Structure

```
notion-mcp/
├── src/
│   └── notion_mcp/
│       ├── models/
│       │   ├── __init__.py
│       │   └── notion.py      # Pydantic models for Notion objects
│       ├── __init__.py        
│       ├── __main__.py        # Entry point
│       ├── client.py          # Notion API client
│       └── server.py          # MCP server implementation
├── .env                       # Environment variables (add your Notion API key here)
├── .gitignore
├── pyproject.toml             # Project dependencies
└── README.md
```

### Running Tests

```bash
pytest
```

## Configuration

The server requires a Notion integration token. To set this up:

1. Go to https://www.notion.so/my-integrations
2. Create a new integration with appropriate capabilities (read/write as needed)
3. Copy the integration token
4. Add it to your `.env` file in the project root directory:

```
NOTION_API_KEY=your_notion_integration_token
```

5. Share your Notion databases with the integration (from the database's "Share" menu)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - Use at your own risk

## Troubleshooting

### Common Issues

- **Connection Errors**: Make sure your Notion API key is correct and you have internet access
- **Permission Errors**: Ensure your integration has been given access to the databases you're trying to access
- **Claude Desktop Integration**: If Claude Desktop isn't connecting, check that your config path is correct and that the server is running without logging to stdout

## Acknowledgments

- Built to work with Claude Desktop and other MCP clients
- Uses Notion's API (latest compatible version 2022-02-22)
- MCP 1.6.0 compatibility maintained
- Special thanks to [danhilse](https://github.com/danhilse), I referenced his [notion-mcp-server](https://github.com/danhilse/notion-mcp-server) project
