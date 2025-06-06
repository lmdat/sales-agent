import os
from dotenv import load_dotenv, find_dotenv
from langgraph.graph import StateGraph, END
from .states.sales_agent_state import SalesAgentState
from .nodes.router import router_node
from .nodes.flow_controller import flow_controller_node, get_selected_flow
from .nodes.do_nothing import do_nothing_node
from .subgraphs.greeting_subgraph import build_greeting_subgraph
from .subgraphs.off_topic_subgraph import build_off_topic_subgraph
from langgraph.checkpoint.memory import MemorySaver


load_dotenv(find_dotenv())

SUBGRAPH_PATH_MAP = {
    'greeting': 'greeting_subgraph',
    'off_topic': 'off_topic_subgraph'
}

def build_graph():
    graph = StateGraph(SalesAgentState)
    graph.add_node("router_node", router_node)
    graph.add_node("flow_controller_node", flow_controller_node)
    graph.add_node("greeting_subgraph", build_greeting_subgraph())
    graph.add_node("off_topic_subgraph", build_off_topic_subgraph())
    # graph.add_node("do_nothing_node", do_nothing_node)

    graph.set_entry_point("router_node") # START -> router_node
    graph.add_edge("router_node", "flow_controller_node") # router_node -> flow_controller_node

    graph.add_conditional_edges(
        "flow_controller_node",
        get_selected_flow,
        SUBGRAPH_PATH_MAP
    )

    # Memory
    memory = MemorySaver()
    return graph.compile(checkpointer=memory)

    