# evaluation_engine/evaluation_service.py
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def evaluate_single_resource(resource: Dict[str, Any], level: str) -> Dict[str, Any]:
    """Calculates composite quality score (0-100) for a resource."""
    # 1. Base score calculations (or LLM scoring call)
    summary_length = len(resource.get("summary", ""))
    has_keywords = len(resource.get("keywords", [])) > 0
    
    # Example heuristic quality calculation (replace with your engine's logic/LLM call)
    completeness_score = min(40, (summary_length // 5))
    relevance_score = 30 if has_keywords else 10
    authority_score = 30 if "github.com" in resource.get("url", "") or "edu" in resource.get("url", "") else 20
    
    quality_score = min(100, completeness_score + relevance_score + authority_score)
    
    # 2. Attach score and breakdown evaluation metadata
    evaluated_resource = resource.copy()
    evaluated_resource["qualityScore"] = quality_score
    evaluated_resource["evaluationBreakdown"] = {
        "completeness": completeness_score,
        "relevance": relevance_score,
        "authority": authority_score,
        "targetLevel": level
    }
    return evaluated_resource

def evaluate_resources_batch(resources: List[Dict[str, Any]], level: str) -> List[Dict[str, Any]]:
    """Evaluates a batch of deduplicated resources."""
    evaluated_list = []
    for res in resources:
        try:
            scored_res = evaluate_single_resource(res, level)
            evaluated_list.append(scored_res)
        except Exception as e:
            logger.error(f"[BUG-008 Evaluation Error] Failed to evaluate {res.get('url')}: {e}")
    return evaluated_list