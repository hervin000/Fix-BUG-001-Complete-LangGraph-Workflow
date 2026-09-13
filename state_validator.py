# schema/state_validator.py
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger("StateValidator")

class HardenedAgentState(BaseModel):
    """Pydantic runtime validator for LangGraph AgentState."""
    domain: str = Field(min_length=1)
    course: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    level: str = Field(default="Beginner")
    
    search_strategy: Optional[Dict[str, Any]] = None
    discovered_resources: List[Dict[str, Any]] = Field(default_factory=list)
    extracted_metadata: List[Dict[str, Any]] = Field(default_factory=list)
    validated_resources: List[Dict[str, Any]] = Field(default_factory=list)
    deduped_resources: List[Dict[str, Any]] = Field(default_factory=list)
    evaluated_resources: List[Dict[str, Any]] = Field(default_factory=list)
    ranked_resources: List[Dict[str, Any]] = Field(default_factory=list)
    categorized_modules: List[Dict[str, Any]] = Field(default_factory=list)
    learning_path: Optional[Dict[str, Any]] = None
    
    is_persisted: bool = False
    persisted_path_id: Optional[str] = None

def validate_state_transition(state_dict: Dict[str, Any], node_name: str) -> Dict[str, Any]:
    """Validates full state against the runtime contract after node mutation."""
    try:
        validated = HardenedAgentState(**state_dict)
        return validated.model_dump()
    except ValidationError as e:
        logger.error(f"[BUG-014 State Violation] Schema corruption detected after node '{node_name}': {e}")
        raise ValueError(f"State validation failed at node '{node_name}': {e}")