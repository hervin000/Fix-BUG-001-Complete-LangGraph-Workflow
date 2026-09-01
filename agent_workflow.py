from langgraph.graph import StateGraph, END
from .schema import AgentState
from .nodes import (
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
initial_state = {
    "domain": "Languages",
    "course": "French",
    "topic": "Greetings",
    "level": "A1"
}

result = app.invoke(initial_state)
print("Execution finished successfully!")
# FIXED CODE EXAMPLE
workflow = StateGraph(AgentState)

# 1. Add all 14 nodes
workflow.add_node("topic_analysis", topic_analysis_node)
workflow.add_node("search_strategy", search_strategy_node)
workflow.add_node("resource_discovery", resource_discovery_node)
workflow.add_node("metadata_extraction", metadata_extraction_node)
workflow.add_node("validation", validation_node)
workflow.add_node("deduplication", deduplication_node)
workflow.add_node("evaluation", evaluation_node)
workflow.add_node("ranking", ranking_node)
workflow.add_node("categorization", categorization_node)
workflow.add_node("learning_sequence", sequence_node)
workflow.add_node("database_persistence", persistence_node)
workflow.add_node("embedding", embedding_node)

# 2. Connect the nodes sequentially from START to END
workflow.set_entry_point("topic_analysis")

workflow.add_edge("topic_analysis", "search_strategy")
workflow.add_edge("search_strategy", "resource_discovery")
workflow.add_edge("resource_discovery", "metadata_extraction")
workflow.add_edge("metadata_extraction", "validation")
workflow.add_edge("validation", "deduplication")
workflow.add_edge("deduplication", "evaluation")
workflow.add_edge("evaluation", "ranking")
workflow.add_edge("ranking", "categorization")
workflow.add_edge("categorization", "learning_sequence")
workflow.add_edge("learning_sequence", "database_persistence")
workflow.add_edge("database_persistence", "embedding")
workflow.add_edge("embedding", END)

# 3. Compile the graph
app = workflow.compile()