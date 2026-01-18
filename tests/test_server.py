import pytest
import respx
from httpx import Response

from fastmcp.client import Client

from mdnmcp.server import mcp

pytest_plugins = ("pytest_asyncio",)


MOCK_SEARCH_RESPONSE = {
    "documents": [
        {
            "title": "Fetch API",
            "slug": "web/api/fetch_api",
            "summary": "The Fetch API provides...",
        },
    ]
}

MOCK_DOC_RESPONSE = {
    "doc": {
        "title": "Fetch API",
        "summary": "The Fetch API provides an interface for fetching resources.",
        "body": [
            {
                "type": "prose",
                "value": {
                    "id": None,
                    "title": None,
                    "content": "<p>Introduction to Fetch.</p>",
                },
            },
            {
                "type": "prose",
                "value": {
                    "id": "syntax",
                    "title": "Syntax",
                    "content": "<p>fetch(url, options)</p>",
                },
            },
            {
                "type": "prose",
                "value": {
                    "id": "examples",
                    "title": "Examples",
                    "content": "<p>Here are examples.</p>",
                },
            },
        ],
    }
}


@pytest.fixture
async def mcp_client():
    async with Client(transport=mcp) as client:
        yield client


@pytest.mark.asyncio
async def test_list_tools(mcp_client: Client):
    tools = await mcp_client.list_tools()
    tool_names = [t.name for t in tools]

    assert "mdn_search" in tool_names
    assert "mdn_lookup" in tool_names
    assert "mdn_read" in tool_names


@pytest.mark.asyncio
@respx.mock
async def test_mdn_search(mcp_client: Client):
    respx.get("https://developer.mozilla.org/api/v1/search").mock(
        return_value=Response(200, json=MOCK_SEARCH_RESPONSE)
    )

    result = await mcp_client.call_tool("mdn_search", {"query": "fetch"})

    assert "Fetch API" in str(result.data)
    assert "web/api/fetch_api" in str(result.data)


@pytest.mark.asyncio
@respx.mock
async def test_mdn_search_no_results(mcp_client: Client):
    respx.get("https://developer.mozilla.org/api/v1/search").mock(
        return_value=Response(200, json={"documents": []})
    )

    result = await mcp_client.call_tool("mdn_search", {"query": "nonexistent"})

    assert "No results found" in str(result.data)


@pytest.mark.asyncio
@respx.mock
async def test_mdn_lookup(mcp_client: Client):
    respx.get(
        "https://developer.mozilla.org/en-US/docs/web/api/fetch_api/index.json"
    ).mock(return_value=Response(200, json=MOCK_DOC_RESPONSE))

    result = await mcp_client.call_tool(
        "mdn_lookup", {"identifier": "web/api/fetch_api"}
    )

    assert "Fetch API" in str(result.data)
    assert "syntax" in str(result.data)
    assert "examples" in str(result.data)


@pytest.mark.asyncio
@respx.mock
async def test_mdn_read_single(mcp_client: Client):
    respx.get(
        "https://developer.mozilla.org/en-US/docs/web/api/fetch_api/index.json"
    ).mock(return_value=Response(200, json=MOCK_DOC_RESPONSE))

    result = await mcp_client.call_tool(
        "mdn_read", {"identifier": "web/api/fetch_api", "section_ids": "syntax"}
    )

    assert "Syntax" in str(result.data)
    assert "fetch(url, options)" in str(result.data)


@pytest.mark.asyncio
@respx.mock
async def test_mdn_read_multiple(mcp_client: Client):
    respx.get(
        "https://developer.mozilla.org/en-US/docs/web/api/fetch_api/index.json"
    ).mock(return_value=Response(200, json=MOCK_DOC_RESPONSE))

    result = await mcp_client.call_tool(
        "mdn_read",
        {"identifier": "web/api/fetch_api", "section_ids": "syntax,examples"},
    )

    assert "Syntax" in str(result.data)
    assert "Examples" in str(result.data)


@pytest.mark.asyncio
@respx.mock
async def test_mdn_read_not_found(mcp_client: Client):
    respx.get(
        "https://developer.mozilla.org/en-US/docs/web/api/fetch_api/index.json"
    ).mock(return_value=Response(200, json=MOCK_DOC_RESPONSE))

    result = await mcp_client.call_tool(
        "mdn_read", {"identifier": "web/api/fetch_api", "section_ids": "nonexistent"}
    )

    assert "not_found" in str(result.data)
    assert "available_ids" in str(result.data)
