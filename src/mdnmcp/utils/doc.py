import re
from markdownify import markdownify as md

MULTI_NEWLINE = re.compile(r"\n{3,}")
MULTI_SPACE = re.compile(r" {2,}")


def html_to_markdown(html: str | None) -> str:
    if not html:
        return ""
    text = md(html, heading_style="ATX", strip=["script", "style"])
    text = MULTI_NEWLINE.sub("\n\n", text)
    text = MULTI_SPACE.sub(" ", text)
    return text.strip()


def extract_sections(raw_data: dict) -> list[dict]:
    doc = raw_data.get("doc", {})
    sections = []

    for item in doc.get("body", []):
        if item.get("type") != "prose":
            continue

        value = item.get("value", {})
        content = html_to_markdown(value.get("content"))

        if not content:
            continue

        sections.append(
            {
                "id": value.get("id") or "intro",
                "title": value.get("title") or doc.get("title", ""),
                "content": content,
            }
        )

    return sections


def get_doc_metadata(raw_data: dict) -> dict:
    doc = raw_data.get("doc", {})
    sections = extract_sections(raw_data)

    return {
        "title": doc.get("title", ""),
        "summary": doc.get("summary", ""),
        "sections": [{"id": s["id"], "title": s["title"]} for s in sections],
    }


def get_sections_content(raw_data: dict, section_ids: list[str]) -> dict:
    sections = extract_sections(raw_data)
    available_ids = [s["id"] for s in sections]

    results = []
    not_found = []

    for section_id in section_ids:
        found = False
        for section in sections:
            if section["id"] == section_id:
                results.append(
                    {
                        "id": section["id"],
                        "title": section["title"],
                        "content": section["content"],
                    }
                )
                found = True
                break
        if not found:
            not_found.append(section_id)

    output = {"sections": results}

    if not_found:
        output["not_found"] = not_found
        output["available_ids"] = available_ids

    return output
