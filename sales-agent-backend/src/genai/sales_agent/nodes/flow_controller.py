from ..states.sales_agent_state import SalesAgentState
from logger import logger

TOPIC_FLOW_MAPPING = {
    "greeting": "greeting",
    "off_topic": "off_topic",
    "company_info": "company_info",
    "product_consulting": "product_consulting",
    "make_order": "make_order",
    "wanna_exit": "wanna_exit"
}

def flow_controller_node(state: SalesAgentState):
    selected_flow = TOPIC_FLOW_MAPPING[state['topic'].name]
    logger.info(f"Selected Flow: {selected_flow}")

    return {
        "selected_flow": selected_flow
    }

def get_selected_flow(state: SalesAgentState):
    return state.get('selected_flow', TOPIC_FLOW_MAPPING['off_topic'])