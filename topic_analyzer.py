# topic_analysis/topic_analyzer.py
from typing import Dict, Any

def validate_input_state(state: Dict[str, Any]) -> None:
    """Ensures input parameters are present before proceeding."""
    required_fields = ["domain", "course", "topic", "level"]
    missing = [field for field in required_fields if not state.get(field)]
    if missing:
        raise ValueError(f"[BUG-004] Missing required state fields: {missing}")

def topic_analyzer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Topic Analysis node that guarantees input preservation across state transitions."""
    # Validate input fields exist
    validate_input_state(state)
    
    # Extract inputs safely
    domain = state["domain"]
    course = state["course"]
    topic = state["topic"]
    level = state["level"]
    
    # Generate search strategy based on topic analysis
    strategy = {
        "queries": [f"{course} {topic} {level} tutorial", f"learn {topic} {domain}"],
        "target_level": level
    }
    
    # Return inputs ALONG WITH new outputs to guarantee preservation
    return {
        "domain": domain,
        "course": course,
        "topic": topic,
        "level": level,
        "search_strategy": strategy
    }
