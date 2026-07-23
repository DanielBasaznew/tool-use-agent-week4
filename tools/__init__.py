from .web_search import web_search
from .fetch_page import fetch_page

TOOL_REGISTRY = {
    "web_search": web_search,
    "fetch_page": fetch_page,
}

__all__ = ["web_search", "fetch_page", "TOOL_REGISTRY"]