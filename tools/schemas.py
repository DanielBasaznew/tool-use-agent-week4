"""
JSON Schemas for Native Function Calling (Week 4, Day 1)
Defines tool contracts for web_search and fetch_page.
"""

TOOL_SCHEMAS = [
    {
        "name": "web_search",
        "description": (
            "Searches DuckDuckGo for live web information. Returns numbered search results "
            "with titles, URLs, and short 200-character snippets. "
            "Use specific queries rather than broad single words. "
            "Good query example: 'GPT-4 vs Claude 3 differences 2024'. "
            "Bad query example: 'GPT'."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Specific search query terms."
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "fetch_page",
        "description": (
            "Fetches and extracts clean, full body text from a specific webpage URL. "
            "Use this tool after web_search when you need deeper details, full article text, "
            "or precise facts beyond what a short 200-character snippet provides."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The exact target webpage URL to fetch (must start with http:// or https://)."
                }
            },
            "required": ["url"]
        }
    }
]