from ..states.sales_agent_state import SalesAgentState
from logger import logger
def do_nothing_node(state: SalesAgentState):
    logger.info("do_nothing_node called.")
    return {}