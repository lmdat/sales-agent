from langgraph.graph import StateGraph, END
from ..nodes.subgraph.greeting_nodes import greeting_node
from ..nodes.reset_topic import reset_topic_node
from ..states.sales_agent_state import SalesAgentState

def build_greeting_subgraph():
    graph = StateGraph(SalesAgentState)
    graph.add_node("greeting_node", greeting_node)
    graph.add_node("reset_topic_node", reset_topic_node)

    graph.set_entry_point("greeting_node") # START -> greeting_node
    graph.add_edge("greeting_node", "reset_topic_node") # greeting_node -> reset_topic_node
    graph.add_edge("reset_topic_node", END) # reset_topic_node -> END

    return graph.compile()