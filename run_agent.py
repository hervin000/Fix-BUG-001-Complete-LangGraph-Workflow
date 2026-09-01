import json
from langgraph.graph import StateGraph, END

def main():
    # Define a sample test request
    sample_input = {
        "domain": "Languages",
        "course": "French",
        "topic": "French A1 Greetings",
        "level": "Beginner"
    }

    print("🚀 Starting LangGraph Workflow Execution...\n")

    try:
        # Stream output node by node to observe full 14-step execution
        for event in app.stream(sample_input):
            for node_name, state_update in event.items():
                print(f"✅ Completed Node: [{node_name}]")
                # Print keys modified/added by this node
                print(f"   Updated State Keys: {list(state_update.keys())}\n")

        print("🎉 Workflow reached END node successfully!")

    except Exception as e:
        print(f"❌ Workflow failed with error: {e}")

if __name__ == "__main__":
    main()