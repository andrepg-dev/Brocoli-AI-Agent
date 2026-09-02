from langgraph.graph import MessagesState
from pydantic import Field


class GraphMemoryState(MessagesState):
    search: str | None = Field("This is used for searching in the web")
