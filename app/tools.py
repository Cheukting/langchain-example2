from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

import httpx
from bs4 import BeautifulSoup
from langchain.tools import tool


BASE_URL = "https://docs.python.org/3/whatsnew/"


@dataclass
class WhatsNewEntry:
    version: str
    url: str
    title: str


def _fetch(url: str, timeout: float = 20.0) -> str:
    with httpx.Client(
        follow_redirects=True,
        timeout=timeout,
        headers={"User-Agent": "LangChainExample2/1.0 (+https://python.org)"},
    ) as client:
        r = client.get(url)
        r.raise_for_status()
        return r.text


def _find_latest_entry(index_html: str) -> Optional[WhatsNewEntry]:
    soup = BeautifulSoup(index_html, "html.parser")
    # The "What's New" index lists links under main content
    candidates = []
    for a in soup.select("main a[href]"):
        text = (a.get_text() or "").strip()
        href = a.get("href")
        # Look for entries like "What's New In Python 3.x"
        if text.lower().startswith("what's new in python 3") and href:
            # Normalize URL
            url = href if href.startswith("http") else BASE_URL + href
            m = re.search(r"3\.(\d+)", text)
            minor = int(m.group(1)) if m else -1
            candidates.append((minor, text, url))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    minor, title, url = candidates[0]
    return WhatsNewEntry(version=f"3.{minor}", url=url, title=title)


def _extract_highlights(article_html: str) -> str:
    soup = BeautifulSoup(article_html, "html.parser")
    # Remove navigation and sidebar if any
    for selector in ["nav", "header", "footer", "aside"]:
        for node in soup.select(selector):
            node.decompose()
    main = soup.select_one("main") or soup

    # Collect top-level sections (h2 + following content)
    lines: list[str] = []
    title = main.find(["h1"]) or soup.find("title")
    if title:
        lines.append(f"TITLE: {title.get_text(strip=True)}")

    for h2 in main.find_all("h2"):
        section_title = h2.get_text(strip=True)
        # Skip housekeeping sections
        skip = any(
            k in section_title.lower()
            for k in [
                "acknowledgements",
                "credits",
                "porting",
                "deprecated",
                "removed",
                "documentation",
                "security",
                "contributors",
            ]
        )
        if skip:
            continue
        # Gather the first paragraph and bullet list under the section
        content_parts = []
        for sib in h2.find_all_next():
            if sib.name == "h2":
                break
            if sib.name in {"p", "ul", "ol"}:
                text = sib.get_text(" ", strip=True)
                if text:
                    content_parts.append(text)
            # Limit per section to keep output concise
            if len("\n".join(content_parts)) > 1600:
                break
        if content_parts:
            lines.append(f"\n## {section_title}\n" + "\n".join(content_parts))

    extracted = "\n".join(lines)
    # Trim to reasonable size for the LLM
    if len(extracted) > 8000:
        extracted = extracted[:8000] + "\n...[truncated]"
    return extracted


@tool("fetch_python_whatsnew", return_direct=False)
def fetch_python_whatsnew(_) -> str:
    """
    Fetch the latest "What's New in Python" article and return a concise, cleaned
    text payload including the URL and extracted section highlights.

    The tool ignores the input argument.
    """
    index_html = _fetch(BASE_URL)
    latest = _find_latest_entry(index_html)
    if not latest:
        return "Could not determine latest What's New entry from the index page."
    article_html = _fetch(latest.url)
    highlights = _extract_highlights(article_html)
    return f"URL: {latest.url}\nVERSION: {latest.version}\n\n{highlights}"
