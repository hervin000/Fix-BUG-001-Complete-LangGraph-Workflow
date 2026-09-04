from agent_workflow import app, initial_state

# Run the workflow
try:
    result = app.invoke(initial_state)
    print("Workflow completed successfully!")
    print("Result:", result)
except Exception as e:
    print(f"Error: {e}")