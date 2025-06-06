from langgraph.graph import StateGraph, END
from ..nodes.subgraph.off_topic_nodes import off_topic_node
from ..nodes.reset_topic import reset_topic_node
from ..states.sales_agent_state import SalesAgentState

def build_off_topic_subgraph():
    graph = StateGraph(SalesAgentState)
    graph.add_node("off_topic_node", off_topic_node)
    graph.add_node("reset_topic_node", reset_topic_node)

    graph.set_entry_point("off_topic_node") # START -> off_topic_node
    graph.add_edge("off_topic_node", "reset_topic_node") # off_topic_node -> reset_topic_node
    graph.add_edge("reset_topic_node", END) # reset_topic_node -> END

    return graph.compile()