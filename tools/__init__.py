"""
Tools package initialization.
Centralizes tool imports, schemas, and execution registry.
"""

from tools.web_search import web_search
from tools.fetch_page import fetch_page
from tools.code_executor import execute_python
from tools.schemas import TOOL_SCHEMAS

# Central mapping for dynamic tool invocation
TOOL_REGISTRY = {
    "web_search": web_search,
    "fetch_page": fetch_page,
    "execute_python": execute_python,
}

__all__ = ["web_search", "fetch_page", "execute_python", "TOOL_SCHEMAS", "TOOL_REGISTRY"]