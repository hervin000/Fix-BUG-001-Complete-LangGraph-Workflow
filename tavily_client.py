# search_config/tavily_client.py
import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# DO NOT initialize the client at the top level:
# client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))  <-- THIS CRASHES ON IMPORT

def get_tavily_client():
    """Lazily initializes Tavily client only when called."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        logger.warning("[SearchConfig] TAVILY_API_KEY is missing. Search will return empty results.")
        return None
    
    try:
        from tavily import TavilyClient
        return TavilyClient(api_key=api_key)
    except Exception as e:
        logger.error(f"[SearchConfig] Failed to initialize TavilyClient: {e}")
        return None

def run_tavily_search(query: str) -> List[Dict[str, Any]]:
    """Executes search safely with graceful error handling."""
    client = get_tavily_client()
    
    # Graceful fallback if key is missing or client creation failed
    if client is None:
        return []

    try:
        response = client.search(query=query)
        return response.get("results", [])
    except Exception as e:
        logger.error(f"[SearchConfig] Tavily search failed for query '{query}': {e}")
        return []