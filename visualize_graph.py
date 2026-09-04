from agent_workflow import app

# Generate ASCII diagram of node connections
try:
    print(app.get_graph().draw_ascii())
except Exception:
    # Print list of nodes and edges directly if ASCII drawing dependencies are missing
    print("Nodes in Graph:", list(app.get_graph().nodes.keys()))
    