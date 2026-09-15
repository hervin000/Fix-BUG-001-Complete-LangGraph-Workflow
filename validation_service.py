# resource_validator/validation_service.py
import urllib.parse
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)

def validate_resource(resource: Dict[str, Any], topic: str) -> Tuple[bool, str]:
    """Validates resource URL, domain, and basic topic relevance."""
    url = resource.get("url", "")
    title = resource.get("title", "").lower()
    summary = resource.get("summary", "").lower()
    
    # 1. Check URL Structure
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme in ["http", "https"] or not parsed.netloc:
        return False, "Invalid URL scheme or missing domain"
        
    # 2. Basic Topic Relevance Check
    topic_words = [w.lower() for w in topic.split() if len(w) > 2]
    is_relevant = any(w in title or w in summary for w in topic_words)
    
    if topic_words and not is_relevant:
        return False, f"Resource content failed relevance match for topic: '{topic}'"
        
    return True, "Valid"