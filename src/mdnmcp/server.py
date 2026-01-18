import orjson
import httpx
from fastmcp import FastMCP

from mdnmcp.config import MDN_API_BASE
from mdnmcp.utils import convert_search_results, get_doc_metadata, get_sections_content

mcp = FastMCP("mdnmcp")


@mcp.tool()
async def mdn_search(query: str) -> str:
    """
    Step 1: Search MDN Web Docs for documentation.

    Use this tool FIRST to find relevant documentation.
    After getting results, you MUST call mdn_lookup with the identifier to see available sections.

    Args:
        query: Search terms (e.g., 'fetch API', 'CSS grid', 'JavaScript promises')

    Returns:
        List of documents with title, identifier, and summary.

    Next step: Call mdn_lookup(identifier) with a result's identifier.
    """
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(
            f"{MDN_API_BASE}/search",
            params={"q": query, "locale": "en-US"},
        )
        response.raise_for_status()

        results = convert_search_results(response.json())

        if not results:
            return "No results found."

        return orjson.dumps(results, option=orjson.OPT_INDENT_2).decode()


@mcp.tool()
async def mdn_lookup(identifier: str) -> str:
    """
    Step 2: Get the list of sections in a document.

    Use this AFTER mdn_search to see what sections are available.
    Then call mdn_read with the section ids you need.

    Args:
        identifier: Document path from search results (e.g., 'web/api/fetch_api')

    Returns:
        Document title, summary, and list of sections (id + title).

    Next step: Call mdn_read(identifier, section_ids) with the sections you need.
    """
    async with httpx.AsyncClient(follow_redirects=True) as client:
        url = f"https://developer.mozilla.org/en-US/docs/{identifier}/index.json"
        response = await client.get(url)
        response.raise_for_status()

        metadata = get_doc_metadata(response.json())

        if not metadata["sections"]:
            return "No sections found."

        return orjson.dumps(metadata, option=orjson.OPT_INDENT_2).decode()


@mcp.tool()
async def mdn_read(identifier: str, section_ids: str) -> str:
    """
    Step 3: Read the content of one or more sections.

    Use this AFTER mdn_lookup to get actual documentation content.
    You can request multiple sections in one call by separating ids with commas.

    Args:
        identifier: Document path (e.g., 'web/api/fetch_api')
        section_ids: Comma-separated section ids from mdn_lookup.
                     Example: "intro,syntax,examples" for multiple sections.
                     Example: "intro" for single section.
                     MUST use exact ids from mdn_lookup. Do not invent ids.

    Returns:
        Markdown content for each requested section.
    """
    ids = [s.strip() for s in section_ids.split(",") if s.strip()]

    async with httpx.AsyncClient(follow_redirects=True) as client:
        url = f"https://developer.mozilla.org/en-US/docs/{identifier}/index.json"
        response = await client.get(url)
        response.raise_for_status()

        result = get_sections_content(response.json(), ids)

        return orjson.dumps(result, option=orjson.OPT_INDENT_2).decode()


if __name__ == "__main__":
    mcp.run()
