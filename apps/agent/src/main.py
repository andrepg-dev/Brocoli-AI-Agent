from dataclasses import dataclass

from constants import (
    CALL_LLM,
    EVALUATOR,
    FOOD_PLANNER_LLM,
    INGREDIENTS_PLANNER,
    PRICE_RETRIEVER,
    READ_LONG_TERM_MEMORY,
    SHOPPING_LIST,
)
from dotenv import load_dotenv
from graph_state import GraphMemoryState
from langgraph.graph import END, START, StateGraph
from langgraph.store.memory import InMemoryStore
from langsmith import Client
from long_term_memory import read_long_term_memory
from nodes import (
    call_llm,
    direct_talk,
    evaluator,
    food_planner,
    ingredients_planner,
    price_retriever,
    shopping_list,
)

load_dotenv(override=True)


langsmith_client = Client()
MODEL_PROVIDER = "openai:gpt-4o-mini"
store = InMemoryStore()

store.put(
    ("users",),
    "0b954782-8cff-44cf-bec3-efd7998300d6",
    {"preferences": "This user wants food using peras"},
)

item = store.get(("users",), "0b954782-8cff-44cf-bec3-efd7998300d6")


@dataclass
class RuntimeContext:
    user_name: str
    user_id: str


graph = StateGraph(GraphMemoryState, context_schema=RuntimeContext)
graph.add_node(READ_LONG_TERM_MEMORY, read_long_term_memory)
graph.add_node(FOOD_PLANNER_LLM, food_planner)
graph.add_node(INGREDIENTS_PLANNER, ingredients_planner)
graph.add_node(PRICE_RETRIEVER, price_retriever)
graph.add_node(SHOPPING_LIST, shopping_list)
graph.add_node(EVALUATOR, evaluator)
graph.add_node(CALL_LLM, call_llm)

graph.add_conditional_edges(
    START,
    direct_talk,
    {CALL_LLM: CALL_LLM, FOOD_PLANNER_LLM: FOOD_PLANNER_LLM},
)

graph.add_edge(START, READ_LONG_TERM_MEMORY)
graph.add_edge(FOOD_PLANNER_LLM, INGREDIENTS_PLANNER)
graph.add_edge(INGREDIENTS_PLANNER, PRICE_RETRIEVER)
graph.add_edge(PRICE_RETRIEVER, SHOPPING_LIST)
graph.add_edge(SHOPPING_LIST, EVALUATOR)
graph.add_edge(EVALUATOR, END)
graph.add_edge(CALL_LLM, END)

graph = graph.compile()
