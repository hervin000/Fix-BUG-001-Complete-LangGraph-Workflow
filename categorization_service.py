# categorization/categorization_service.py
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def categorize_and_group_resources(
    ranked_resources: List[Dict[str, Any]], 
    topic: str, 
    level: str
) -> List[Dict[str, Any]]:
    """Groups ranked resources into chronological/pedagogical learning modules."""
    if not ranked_resources:
        logger.warning("[BUG-010] No ranked resources available to categorize.")
        return []

    # Initialize standard 3-stage learning module structure
    modules = {
        "Foundations": [],
        "Core Concepts": [],
        "Practical Applications": []
    }

    # Categorize based on difficulty and index placement
    total_items = len(ranked_resources)
    for idx, resource in enumerate(ranked_resources):
        # Assign module based on target difficulty or relative rank
        diff = resource.get("difficulty", level).capitalize()
        
        if diff == "Beginner" or idx < total_items * 0.33:
            modules["Foundations"].append(resource)
        elif diff == "Intermediate" or idx < total_items * 0.66:
            modules["Core Concepts"].append(resource)
        else:
            modules["Practical Applications"].append(resource)

    # Format into structured module output payload
    categorized_modules = [
        {"module_name": "Module 1: Foundations", "topic": topic, "resources": modules["Foundations"]},
        {"module_name": "Module 2: Core Concepts", "topic": topic, "resources": modules["Core Concepts"]},
        {"module_name": "Module 3: Practical Applications", "topic": topic, "resources": modules["Practical Applications"]}
    ]

    # Filter out empty modules
    result = [m for m in categorized_modules if len(m["resources"]) > 0]
    logger.info(f"[BUG-010] Categorized {len(ranked_resources)} items into {len(result)} modules.")
    return result
