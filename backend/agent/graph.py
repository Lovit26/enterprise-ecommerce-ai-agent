from langchain_core.messages import SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from backend.agent.state import AgentState
from backend.llm.provider import get_chat_model
from backend.tools.registry import TOOLS

from backend.agent.checkpoint import checkpointer




SYSTEM_PROMPT = """
You are an e-commerce customer support AI agent.

You help the current authenticated user with:
- order information
- shipping and tracking
- return eligibility

Rules:
1. Never invent order, shipping, or return information.
2. Use the available tools whenever business data is required.
3. Never claim access to an order if a tool returns access_denied.
4. Never bypass tool or service authorization.
5. If a tool returns an error, explain it clearly without inventing data.
6. Keep responses concise and helpful.
"""


model = get_chat_model().bind_tools(TOOLS)

tool_node = ToolNode(TOOLS)


def call_model(state: AgentState):
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"],
    ]

    response = model.invoke(messages)

    return {
        "messages": [response]
    }


def should_continue(state: AgentState):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END


builder = StateGraph(AgentState)

builder.add_node(
    "agent",
    call_model,
)

builder.add_node(
    "tools",
    tool_node,
)

builder.add_edge(
    START,
    "agent",
)

builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END,
    },
)

builder.add_edge(
    "tools",
    "agent",
)




agent_graph = builder.compile(
    checkpointer=checkpointer
)