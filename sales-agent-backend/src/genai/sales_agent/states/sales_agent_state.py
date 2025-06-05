from typing import TypedDict, Annotated
from langgraph.graph.message import AnyMessage, add_messages
from langchain_core.messages import AIMessage
from ..schemas.topic import TopicSchema

class SalesAgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages] = None
    human_input: str = ""
    topic: TopicSchema = None
    selected_flow: str = None
    ai_reply: AIMessage = None