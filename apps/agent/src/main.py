from dotenv import load_dotenv
from graph_state import GraphMemoryState
from langchain.chat_models import init_chat_model
from langgraph.graph import END, START, StateGraph
from langgraph.store.memory import InMemoryStore
from langsmith import Client
from rich.console import Console

load_dotenv(override=True)

console = Console()
langsmith_client = Client()
MODEL_PROVIDER = "openai:gpt-4o-mini"
store = InMemoryStore()


def call_llm(state: GraphMemoryState):
    """Function to Call LLM"""
    llm = init_chat_model(MODEL_PROVIDER, store=store)

    response = llm.invoke(
        state["messages"],
    )

    return {"messages": [response]}



graph = StateGraph(GraphMemoryState)
graph.add_node("call_llm", call_llm)
graph.add_edge(START, "call_llm")
graph.add_edge("call_llm", END)
graph = graph.compile()
