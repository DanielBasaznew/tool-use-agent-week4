"""
JSON Schemas for Native Function Calling (Week 4)
Defines tool contracts for search, code execution, and PDF reading.
"""

TOOL_SCHEMAS = [
    {
        "name": "web_search",
        "description": "Searches DuckDuckGo for live web information. Returns numbered search results with titles, URLs, and short 200-character snippets.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Specific search query terms."}
            },
            "required": ["query"]
        }
    },
    {
        "name": "fetch_page",
        "description": "Fetches and extracts clean, full body text from a specific webpage URL.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The exact target webpage URL to fetch."}
            },
            "required": ["url"]
        }
    },
    {
        "name": "execute_python",
        "description": "Executes standalone Python code in an isolated subprocess. Use explicitly for math, logic, sorting, or charts. Must use print() or plt.savefig().",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Valid Python code to be executed."}
            },
            "required": ["code"]
        }
    },
    {
        "name": "read_pdf",
        "description": (
            "Extracts document metadata and the first 3000 characters of text from a local PDF file. "
            "Use this tool FIRST to get an overview of what a document contains, its length, and its general topics. "
            "If the output says it was truncated, use read_pdf_page to fetch specific pages."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The local file path to the PDF document."
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "read_pdf_page",
        "description": (
            "Extracts the complete text from a single, specific page of a local PDF file. "
            "Use this tool ONLY AFTER using read_pdf, when you need the full detail of a specific page "
            "that was mentioned in the overview or truncated."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The local file path to the PDF document."
                },
                "page_number": {
                    "type": "integer",
                    "description": "The 1-indexed page number to extract (e.g., 1 for the first page)."
                }
            },
            "required": ["file_path", "page_number"]
        }
    }
]