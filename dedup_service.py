# deduplication/dedup_service.py
import urllib.parse
import logging
from typing import List, Dict, Any, Set

logger = logging.getLogger(__name__)

def normalize_url(url: str) -> str:
    """Normalizes URL by stripping tracking parameters, trailing slashes, and lowercasing host."""
    try:
        parsed = urllib.parse.urlparse(url.strip())
        
        # Standardize scheme and lowercase hostname
        scheme = "https"  # Normalize scheme to https where applicable
        netloc = parsed.netloc.lower().replace("www.", "")
        path = parsed.path.rstrip("/")
        
        # Filter out common tracking parameters
        query_params = urllib.parse.parse_qs(parsed.query)
        clean_params = {
            k: v for k, v in query_params.items() 
            if not k.startswith("utm_") and k not in ["ref", "fbclid", "gclid", "source"]
        }
        clean_query = urllib.parse.urlencode(clean_params, doseq=True)
        
        # Reconstruct canonical URL
        clean_url = urllib.parse.urlunparse((scheme, netloc, path, "", clean_query, ""))
        return clean_url
    except Exception as e:
        logger.warning(f"[BUG-007] URL normalization failed for {url}: {e}")
        return url.strip().rstrip("/")

def deduplicate_resources(resources: List[Dict[str, Any]], existing_db_urls: Set[str] = None) -> List[Dict[str, Any]]:
    """Filters duplicate resources using normalized URLs."""
    existing_db_urls = existing_db_urls or set()
    seen_urls: Set[str] = set(existing_db_urls)
    unique_resources = []

    for res in resources:
        raw_url = res.get("url", "")
        norm_url = normalize_url(raw_url)
        
        if norm_url not in seen_urls:
            seen_urls.add(norm_url)
            res["url"] = norm_url  # Replace with canonical URL
            unique_resources.append(res)
        else:
            logger.info(f"[BUG-007 Dedup] Filtered duplicate resource: {raw_url}")

    return unique_resources