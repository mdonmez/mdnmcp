import re
from html import unescape

WHITESPACE = re.compile(r"\s+")
HTML_TAG = re.compile(r"<[^>]+>")


def clean_text(text: str | None) -> str:
    if not text:
        return ""
    text = unescape(text)
    text = HTML_TAG.sub("", text)
    return WHITESPACE.sub(" ", text).strip()


def convert_search_results(raw_data: dict) -> list[dict]:
    return [
        {
            "title": clean_text(doc.get("title")),
            "identifier": doc.get("slug", ""),
            "summary": clean_text(doc.get("summary")),
        }
        for doc in raw_data.get("documents", [])
    ]
