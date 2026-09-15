# ranking_engine/ranking_service.py
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Core thresholds
MIN_QUALITY_THRESHOLD = 50  # Filter out items below 50/100
MAX_TOP_RESOURCES = 10      # Select top 10 best items

def rank_and_select_resources(
    evaluated_resources: List[Dict[str, Any]], 
    min_score: int = MIN_QUALITY_THRESHOLD, 
    top_n: int = MAX_TOP_RESOURCES
) -> List[Dict[str, Any]]:
    """Filters resources below quality threshold and selects top N by quality score."""
    if not evaluated_resources:
        logger.warning("[BUG-009 Ranking] No evaluated resources provided.")
        return []

    # 1. Filter out resources below quality score threshold
    qualified = [
        r for r in evaluated_resources 
        if r.get("qualityScore", 0) >= min_score
    ]
    
    # Fallback: If strict threshold yields too few results, lower threshold gracefully
    if not qualified and evaluated_resources:
        logger.warning(f"[BUG-009 Ranking] No resources met threshold {min_score}. Falling back to top overall.")
        qualified = evaluated_resources

    # 2. Sort descending by qualityScore
    ranked = sorted(qualified, key=lambda x: x.get("qualityScore", 0), reverse=True)

    # 3. Slice top N resources
    selected = ranked[:top_n]
    logger.info(f"[BUG-009 Ranking] Input: {len(evaluated_resources)}, Qualified: {len(qualified)}, Selected Top: {len(selected)}")
    
    return selected