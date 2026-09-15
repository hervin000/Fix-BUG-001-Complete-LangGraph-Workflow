# path_generator/path_generator_service.py
import logging
import uuid
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def generate_learning_path(
    domain: str,
    course: str,
    topic: str,
    level: str,
    categorized_modules: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Assembles final learning path payload from state and categorized modules."""
    if not categorized_modules:
        logger.warning("[BUG-011] No categorized modules found to generate path.")

    # Calculate total resources and estimated learning hours (e.g., 1.5 hrs per resource)
    total_resources = sum(len(mod.get("resources", [])) for mod in categorized_modules)
    estimated_hours = round(total_resources * 1.5, 1)

    # Build final learning path schema
    learning_path = {
        "path_id": str(uuid.uuid4()),
        "title": f"Mastering {topic}: From {level} to Advanced",
        "domain": domain,
        "course": course,
        "topic": topic,
        "target_level": level,
        "summary": f"A comprehensive {level}-level curriculum covering {topic} across {len(categorized_modules)} structured modules.",
        "estimated_hours": estimated_hours,
        "total_resources": total_resources,
        "modules": categorized_modules,
        "status": "generated"
    }

    logger.info(f"[BUG-011] Generated learning path '{learning_path['title']}' with {total_resources} resources.")
    return learning_path