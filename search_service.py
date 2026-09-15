# search_service.py
from typing import Dict, Any, List

def execute_search_strategy(search_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Invokes search tools based on generated queries and normalizes results."""
    queries = search_strategy.get("queries", [])
    discovered_resources = []
    
    for query in queries:
        # 1. Invoke active search client (e.g., Tavily or Web Search)
        raw_results = run_search_query(query)  # Existing search function
        
        # 2. Normalize payload structure
        for item in raw_results:
            discovered_resources.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("content", ""),
                "source": item.get("source", "web"),
                "query_used": query
            })
            
    return discovered_resources


# Node function to embed directly inside agent_workflow.py
def resource_discovery_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph node executing BUG-002 requirements."""
    strategy = state.get("search_strategy", {})
    resources = execute_search_strategy(strategy)
    
    # Return state update for resource_discovery
    return {"discovered_resources": resources}