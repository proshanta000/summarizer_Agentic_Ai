from typing import TypedDict, List, Optional, Any
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    input_type: str
    file_data: Optional[Any]
    web_url: Optional[str]
    selected_llm: str
    api_key: str
    model_name: str
    documents: List[Any]
    title: str
    summary: str
    messages: List[BaseMessage] # For chat-based display logic
    error: Optional[str]