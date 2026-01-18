from mdnmcp.utils.search import convert_search_results


def test_convert_search_results_basic():
    raw = {
        "documents": [
            {
                "title": "Fetch API",
                "slug": "web/api/fetch_api",
                "summary": "The Fetch API provides...",
            },
            {
                "title": "Array.map()",
                "slug": "web/javascript/reference/global_objects/array/map",
                "summary": "Creates a new array...",
            },
        ]
    }

    result = convert_search_results(raw)

    assert len(result) == 2
    assert result[0]["title"] == "Fetch API"
    assert result[0]["identifier"] == "web/api/fetch_api"
    assert result[0]["summary"] == "The Fetch API provides..."


def test_convert_search_results_empty():
    raw = {"documents": []}
    result = convert_search_results(raw)
    assert result == []


def test_convert_search_results_missing_documents():
    raw = {}
    result = convert_search_results(raw)
    assert result == []


def test_convert_search_results_cleans_html():
    raw = {
        "documents": [
            {
                "title": "<mark>Fetch</mark> API",
                "slug": "test",
                "summary": "Text with &amp; entity",
            },
        ]
    }

    result = convert_search_results(raw)

    assert result[0]["title"] == "Fetch API"
    assert result[0]["summary"] == "Text with & entity"
