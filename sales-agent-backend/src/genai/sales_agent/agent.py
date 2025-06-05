import os
from dotenv import load_dotenv, find_dotenv
from langgraph.graph import StateGraph, END
from .states.sales_agent_state import SalesAgentState
from .nodes.router import router_node
from .nodes.flow_controller import flow_controller_node


load_dotenv(find_dotenv())

def build_graph():
    graph = StateGraph(SalesAgentState)
    graph.add_node("router_node", router_node)
    graph.add_node("flow_controller_node", flow_controller_node)

    graph.set_entry_point("router_node") # START -> router_node
    graph.add_edge("router_node", "flow_controller_node") # router_node -> flow_controller_node
    graph.add_edge("flow_controller_node", END) # router_node -> END

    return graph.compile()

    