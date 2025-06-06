from ..states.sales_agent_state import SalesAgentState

def reset_topic_node(state: SalesAgentState):
    return {
        "topic": None
    }