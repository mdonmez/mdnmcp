from mdnmcp.utils.doc import get_doc_metadata, get_sections_content, extract_sections


MOCK_RAW_DATA = {
    "doc": {
        "title": "Test API",
        "summary": "This is a test API.",
        "body": [
            {
                "type": "prose",
                "value": {
                    "id": None,
                    "title": None,
                    "content": "<p><strong>Test API</strong> is for testing.</p>",
                },
            },
            {
                "type": "prose",
                "value": {
                    "id": "usage",
                    "title": "Usage",
                    "content": "<p>Here is how to use it.</p><code>example()</code>",
                },
            },
            {
                "type": "prose",
                "value": {
                    "id": "examples",
                    "title": "Examples",
                    "content": "<p>Some <a href='/docs/test'>examples</a> here.</p>",
                },
            },
        ],
    }
}


def test_extract_sections():
    sections = extract_sections(MOCK_RAW_DATA)

    assert len(sections) == 3
    assert sections[0]["id"] == "intro"
    assert sections[1]["id"] == "usage"
    assert sections[2]["id"] == "examples"


def test_get_doc_metadata():
    metadata = get_doc_metadata(MOCK_RAW_DATA)

    assert metadata["title"] == "Test API"
    assert metadata["summary"] == "This is a test API."
    assert len(metadata["sections"]) == 3
    assert metadata["sections"][0] == {"id": "intro", "title": "Test API"}
    assert metadata["sections"][1] == {"id": "usage", "title": "Usage"}


def test_get_sections_content_single():
    result = get_sections_content(MOCK_RAW_DATA, ["usage"])

    assert len(result["sections"]) == 1
    assert result["sections"][0]["id"] == "usage"
    assert "how to use it" in result["sections"][0]["content"]


def test_get_sections_content_multiple():
    result = get_sections_content(MOCK_RAW_DATA, ["intro", "examples"])

    assert len(result["sections"]) == 2
    assert result["sections"][0]["id"] == "intro"
    assert result["sections"][1]["id"] == "examples"


def test_get_sections_content_not_found():
    result = get_sections_content(MOCK_RAW_DATA, ["nonexistent"])

    assert len(result["sections"]) == 0
    assert "nonexistent" in result["not_found"]
    assert "intro" in result["available_ids"]


def test_get_sections_content_partial_match():
    result = get_sections_content(MOCK_RAW_DATA, ["usage", "nonexistent"])

    assert len(result["sections"]) == 1
    assert result["sections"][0]["id"] == "usage"
    assert "nonexistent" in result["not_found"]
