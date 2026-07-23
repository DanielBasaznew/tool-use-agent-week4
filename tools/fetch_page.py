"""
Fetch Page Tool for ReAct Agent (Week 4)
Retrieves and extracts clean main-body text from a given web URL.
"""

import requests
from bs4 import BeautifulSoup

def fetch_page(url: str, max_chars: int = 2000) -> str:
    """
    Fetches the HTML from a URL, strips non-content tags,
    and returns up to max_chars of cleaned visible text.
    """
    if not url or not url.strip():
        return "Error: URL cannot be empty."

    # User-Agent header so websites treat us like a regular browser
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url.strip(), headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Strip out clutter tags that don't contain article body text
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        # Extract remaining visible text
        text = soup.get_text(separator=" ", strip=True)

        if not text:
            return f"Warning: Could not extract readable text from {url}"

        # Truncate to protect context window
        if len(text) > max_chars:
            text = text[:max_chars] + f"\n\n[... Truncated at {max_chars} characters ...]"

        return f"Source URL: {url}\n\nContent:\n{text}"

    except requests.exceptions.Timeout:
        return f"Error: Request timed out while attempting to fetch {url}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching page {url}: {str(e)}"
    except Exception as e:
        return f"Error parsing page content: {str(e)}"