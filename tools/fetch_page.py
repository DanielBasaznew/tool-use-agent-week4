import requests
from bs4 import BeautifulSoup

def fetch_page(url: str) -> str:
    """
    Fetches and extracts clean body text from a webpage URL.
    Strips navigation clutter and preserves natural reading order.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove scripts, styles, headers, footers, and navigation
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()

        # Extract clean text line by line
        text = soup.get_text(separator="\n", strip=True)

        if not text.strip():
            return f"Warning: No readable text could be extracted from '{url}'."

        # Cap output to protect context window safely
        if len(text) > 2500:
            text = text[:2500] + "\n\n... [TRUNCATED: Content exceeds 2500 characters.]"

        return text

    except Exception as e:
        return f"Error fetching {url}: {str(e)}"