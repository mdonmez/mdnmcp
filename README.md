# mdnmcp

A lightweight MCP server that provides real-time access to [MDN Web Docs](https://developer.mozilla.org/) for LLMs and AI coding assistants.

## Why?

LLMs often hallucinate outdated or incorrect web API information. This MCP server gives them direct access to MDN's official documentation with a token-efficient, layered approach.

## Features

- **Real-time data:** Fetches directly from MDN's API, always up-to-date
- **Pinpoint content:** Search → List sections → Read specific content
- **Token efficient:** Only fetch what you need, not entire documents
- **Small model friendly:** Designed for local LLMs

## Tools

This MCP server provides three tools:

| Tool         | Description                     |
| ------------ | ------------------------------- |
| `mdn_search` | Search MDN documentation        |
| `mdn_lookup` | Get document sections list      |
| `mdn_read`   | Read specific section's content |

### Example Flow

```mermaid
sequenceDiagram
    participant User
    participant LLM
    participant mdnmcp
    participant MDN API

    User->>LLM: How does fetch() work?
    LLM->>mdnmcp: mdn_search("fetch API")
    mdnmcp->>MDN API: GET /api/v1/search?q=fetch+API
    MDN API-->>mdnmcp: [{title, identifier, summary}, ...]
    mdnmcp-->>LLM: Search results

    LLM->>mdnmcp: mdn_lookup("web/api/fetch_api")
    mdnmcp->>MDN API: GET /docs/web/api/fetch_api/index.json
    MDN API-->>mdnmcp: {doc: {body, title, ...}}
    mdnmcp-->>LLM: {title, summary, sections: [{id, title}, ...]}

    LLM->>mdnmcp: mdn_read("web/api/fetch_api", "syntax,examples")
    mdnmcp->>MDN API: GET /docs/web/api/fetch_api/index.json
    MDN API-->>mdnmcp: {doc: {body, ...}}
    mdnmcp-->>LLM: {sections: [{id, title, content}, ...]}

    LLM->>User: Here's how fetch() works...
```

## Installation

This is remote MCP server, add this to your MCP configuration:

```json
{
  "mdnmcp": {
    "url": "https://mdnmcp.fastmcp.app/mcp"
  }
}
```

## Development

### Install dev dependencies

```bash
uv sync --group dev
```

### Run tests

```bash
uv run pytest
```

## License

MIT
