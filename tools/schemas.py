"""
JSON Schemas for Native Function Calling (Week 4, Day 1)
Defines tool contracts for web_search, fetch_page, and execute_python.
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
    },  # <--- THIS IS THE COMMA THAT WAS MISSING!
    {
        "name": "execute_python",
        "description": (
            "Executes standalone Python code in an isolated subprocess. "
            "Use this tool for mathematical computations, data analysis, list sorting, algorithmic logic, "
            "or generating charts/plots. "
            "CRITICAL: Your code must be complete, include all necessary imports, and explicitly use "
            "print() to display results or outputs. "
            "For charts, do NOT use plt.show(); instead, save the chart to disk using plt.savefig('chart.png') "
            "and print a confirmation message."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Valid Python code to be executed."
                }
            },
            "required": ["code"]
        }
    }
]