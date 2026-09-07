from langchain_core.messages import HumanMessage

from backend.agent.graph import agent_graph


config = {
    "configurable": {
        "thread_id": "persistent-test-001"
    }
}


result = agent_graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="Can I return it?"
            )
        ]
    },
    config=config,
)


print(result["messages"][-1].content)