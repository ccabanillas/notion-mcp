# Notion MCP Server

A Model Context Protocol (MCP) server implementation for Notion integration, providing a standardized interface for interacting with Notion's API.

## Features

- List and query Notion databases
- Create and update pages
- Search across Notion workspace
- Full async/await support
- Type-safe with Pydantic models
- Proper error handling

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/notion-mcp.git
cd notion-mcp
```

2. Create a virtual environment and install dependencies:
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

1. Start the server:
```bash
python -m notion_mcp
```

2. The server exposes the following MCP tools:

- `list_databases`: List all accessible Notion databases
- `query_database`: Query items from a database with filtering and sorting
- `create_page`: Create new pages in databases
- `update_page`: Update existing pages
- `search`: Search across Notion content

## Development

### Project Structure

```
notion-mcp/
├── src/
│   └── notion_mcp/
│       ├── models/
│       │   ├── __init__.py
│       │   └── notion.py
│       ├── __init__.py
│       ├── __main__.py
│       ├── client.py
│       └── server.py
├── .env
├── .gitignore
├── pyproject.toml
└── README.md
```

### Running Tests

```bash
pytest
```

## Configuration

The server requires a Notion integration token. To set this up:

1. Go to https://www.notion.so/my-integrations
2. Create a new integration
3. Copy the integration token
4. Add it to your `.env` file

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - Use at your own risk

## Acknowledgments

- Built to work with Claude Desktop
- Uses Notion's API
- Special thanks to [danhilse], I referenced his [notion-mcp-server](https://github.com/danhilse/notion-mcp-server) project
This project is licensed under the MIT License - see the LICENSE file for details.
