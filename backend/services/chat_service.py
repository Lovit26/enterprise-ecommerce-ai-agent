from langchain_core.messages import HumanMessage

from backend.agent.graph import agent_graph


class ChatService:

    def chat(
        self,
        message: str,
        thread_id: str,
    ) -> str:

        config = {
            "configurable": {
                "thread_id": thread_id,
            }
        }

        result = agent_graph.invoke(
            {
                "messages": [
                    HumanMessage(content=message)
                ]
            },
            config=config,
        )

        final_message = result["messages"][-1]

        return str(final_message.content)