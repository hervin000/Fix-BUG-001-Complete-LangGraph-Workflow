# metadata_extractor/metadata_service.py
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, HttpUrl, ValidationError
import logging

logger = logging.getLogger(__name__)

class ResourceMetadata(BaseModel):
    title: str
    url: HttpUrl
    type: str
    source: str
    language: str
    difficulty: str
    summary: str
    keywords: List[str]

def extract_and_validate_metadata(raw_resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extracts metadata and validates required fields. Returns None if invalid."""
    try:
        # Construct metadata dictionary from raw resource payload
        metadata = {
            "title": raw_resource.get("title", "").strip(),
            "url": raw_resource.get("url", "").strip(),
            "type": raw_resource.get("type", "article"),
            "source": raw_resource.get("source", "web"),
            "language": raw_resource.get("language", "en"),
            "difficulty": raw_resource.get("difficulty", "Beginner"),
            "summary": raw_resource.get("summary", raw_resource.get("snippet", "")).strip(),
            "keywords": raw_resource.get("keywords", [])
        }
        
        # Pydantic validation: raises ValidationError if fields are missing/malformed
        validated = ResourceMetadata(**metadata)
        
        # Return serializable dict
        result = validated.model_dump()
        result["url"] = str(result["url"])  # Convert HttpUrl to string
        return result

    except (ValidationError, Exception) as e:
        logger.warning(f"[BUG-005 Rejection] Resource rejected due to incomplete metadata: {raw_resource.get('url')}. Error: {e}")
        return None