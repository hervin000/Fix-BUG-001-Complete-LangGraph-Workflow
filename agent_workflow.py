from agent_workflow import app
import nodes
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from langgraph.graph import StateGraph, END
from schema import AgentState
from nodes import (
    topic_analysis_node,
    search_strategy_node,
    resource_discovery_node,
    metadata_extraction_node,
    validation_node,
    deduplication_node,
    evaluation_node,
    ranking_node,
    categorization_node,
    sequence_node,
    persistence_node,
    embedding_node,
)

# 1. Initialize StateGraph with schema
workflow = StateGraph(AgentState)

# 2. Add all 14 nodes to the graph
workflow.add_node("topic_analysis", topic_analysis_node)
workflow.add_node("search_strategy", search_strategy_node)
workflow.add_node("resource_discovery", resource_discovery_node)
workflow.add_node("metadata_extraction", metadata_extraction_node)
workflow.add_node("validation", validation_node)
workflow.add_node("deduplication", deduplication_node)
workflow.add_node("evaluation", evaluation_node)
workflow.add_node("ranking", ranking_node)
workflow.add_node("categorization", categorization_node)
workflow.add_node("sequence", sequence_node)
workflow.add_node("persistence", persistence_node)
workflow.add_node("embedding", embedding_node)

# 3. Define the entry point
workflow.set_entry_point("topic_analysis")

# 4. Connect nodes sequentially (BUG-001 Fix)
workflow.add_edge("topic_analysis", "search_strategy")
workflow.add_edge("search_strategy", "resource_discovery")
workflow.add_edge("resource_discovery", "metadata_extraction")
workflow.add_edge("metadata_extraction", "validation")
workflow.add_edge("validation", "deduplication")
workflow.add_edge("deduplication", "evaluation")
workflow.add_edge("evaluation", "ranking")
workflow.add_edge("ranking", "categorization")
workflow.add_edge("categorization", "sequence")
workflow.add_edge("sequence", "persistence")
workflow.add_edge("persistence", "embedding")

# 5. Connect final node to END
workflow.add_edge("embedding", END)

# 6. Compile the graph into runnable app
app = workflow.compile()