from LangGraph.agent_workflow import app

# Define initial user input state
initial_state = {
    "domain": "Languages",
    "course": "French",
    "topic": "Greetings",
    "level": "A1"
}

# Execute the graph
print("--- STARTING WORKFLOW EXECUTION ---")
final_state = app.invoke(initial_state)

print("\n--- WORKFLOW COMPLETED SUCCESSFULLY ---")
print("Keys present in final state:", list(final_state.keys()))
