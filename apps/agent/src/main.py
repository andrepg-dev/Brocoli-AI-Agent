from dataclasses import dataclass
from datetime import datetime

from dotenv import load_dotenv
from graph_state import GraphMemoryState
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.store.memory import InMemoryStore
from langsmith import Client
from long_term_memory import read_long_term_memory
from rich.console import Console

load_dotenv(override=True)

console = Console()
langsmith_client = Client()
MODEL_PROVIDER = "openai:gpt-4o-mini"
store = InMemoryStore()

store.put(
    ("users",),
    "0b954782-8cff-44cf-bec3-efd7998300d6",
    {"preferences": "This user wants food using peras"},
)

item = store.get(("users",), "0b954782-8cff-44cf-bec3-efd7998300d6")

FOOD_PLANNER_LLM = "food_planner_llm"
READ_LONG_TERM_MEMORY = "read_long_term_memory"
INGREDIENTS_PLANNER = "ingredients_planner"
SHOPPING_LIST = "shopping_list"
EVALUATOR = "evaluator"
CALL_LLM = "call_llm"


@dataclass
class RuntimeContext:
    user_name: str
    user_id: str


def food_planner(state: GraphMemoryState):
    llm = init_chat_model(MODEL_PROVIDER)
    user_preferences = state.get("user_preferences") or {}
    rules = user_preferences.get("rules")

    if not rules:
        rules = """- Give me only breakfast, lunch and dinner each day.
                    - **Nothing baked.**
                    - No meal should take **more than 75 minutes** to prepare.
                    - Delicious, varied foods that help you gain weight.
                    - For breakfast always something light and energetic, quick to make
                    """

    messages = [
        SystemMessage("You're a food planner"),
        HumanMessage(
            f"""
            Make me a biweekly healthy food plan (15 days). I want to have **energy every day**.
            I'm doing this sport **{user_preferences.get("sport") if user_preferences.get("sport") else "None"}**, keep that in mind.
            I'm from Honduras, then make good food from here.

            Rules:
            {rules}

            Start from tomorrow and give me the dates of each day. Today is: {datetime.today()}
            """  # noqa: E501
        ),
    ]

    response = llm.invoke(messages)

    console.print(response)

    return {"messages": [response], "food": response}


BUDGET = "500"


def ingredients_planner(state: GraphMemoryState):
    llm = init_chat_model(MODEL_PROVIDER)
    food = state.get("food") or {}

    assert food

    HUMAN_PROMPT = f"""
    Great, now for every meal you suggested, give me the ingredients.
    Make sure the ingredients on your shopping list are well distributed for 15 days.
    We are two people who will eat the food. We're in Honduras. We have a budget of {BUDGET} LPS.

    This is the food that you balance ingredients
    {food}
    """

    messages = [
        SystemMessage("You're an ingredient balanced based on food"),
        HumanMessage(
            f"""
            {HUMAN_PROMPT}
            """  # noqa: E501
        ),
    ]

    response = llm.invoke(messages)
    return {"messages": [response], "ingredients": response}


def shopping_list(state: GraphMemoryState):
    llm = init_chat_model(MODEL_PROVIDER)
    food = state.get("food") or {}
    ingredients = state.get("ingredients") or {}

    assert food and ingredients

    HUMAN_PROMPT = f"""
    Great, now make me a shopping list to buy it in Paiz, on Morazán Boulevard.

    I have a budget of {BUDGET} lempiras. Give me the shopping list in copyable markdown for checking.

    give me the list of ingredients based on the aisles of Paiz. Do the list in Spanish, and put the prices and quantity at the side

    FOOD:
    {food}

    INGREDIENTS:
    {ingredients}
    """

    messages = [
        SystemMessage(
            "You're creating a shopping list based on food and ingredients but based on a budget, food and country."
        ),
        HumanMessage(
            f"""
            {HUMAN_PROMPT}
            """  # noqa: E501
        ),
    ]

    response = llm.invoke(messages)
    return {"messages": [response], "shopping_list": response}


def evaluator(state: GraphMemoryState):
    llm = init_chat_model("openai:gpt-5.6-terra")
    food = state.get("food") or {}
    ingredients = state.get("ingredients") or {}
    shopping_list = state.get("shopping_list") or {}

    assert food and shopping_list and ingredients

    HUMAN_PROMPT = f"""
    Please evaluate if each item of the shopping list and food are well related, that I won't need something else more than this. If I need something else that are in the food and not in the gradient, 
    show the product and tell me how much, and if the ingredient is too much based on the food, then suggest change, is everything is OK then do not do anything, and say that everything is okey, well balanced and
    all the ingredients will be used based on the food. Use emojis to check each category to see the result in a easy way
    
    BE SUPER CRITIQUE, NO TE DEJES LLEVAR POR LOS MENSJAES DE VERIFICACION FALSA DE LA IA, ES POR ESO MISMO QUE TU ERES EL EVALUADOR, SI VES QUE NADA TIENE SENTIDO, MENCIONALO, SI VES QUE TODO ESTA CORRECTO, MENCIONALO.

    FOOD:
    {food}

    SHOPPING LIST:
    {shopping_list}

    INGREDIENTS:
    {ingredients}
    """

    messages = [
        SystemMessage(
            "Be precise while evaluating the food, shopping list and also evaluate if the shopping list is the same that the ingredients required but its more important the food and shopping list evaluation, to know if we have everything needed, also evaluate if the shopping list makes sense based on the budget: {BUDGET} LPS . Evalute if the PRICES and QUANTITY of each element of the shopping list makes sense, evalute BOTH, that's important."
        ),
        HumanMessage(
            f"""
            {HUMAN_PROMPT}
            """  # noqa: E501
        ),
    ]

    response = llm.invoke(messages)
    return {"messages": [response]}


def call_llm(state: GraphMemoryState):
    llm = init_chat_model("openai:gpt-5.6-terra")
    return llm.invoke(state["messages"])


def direct_talk(state: GraphMemoryState):
    print("TALKING DIRECTLY TO DIRECT TALK NODE")

    if state.get("shopping_list"):
        console.print("Redirecting to calling LLM")
        return CALL_LLM
    else:
        print("Food planner List NODE")
        return FOOD_PLANNER_LLM


graph = StateGraph(GraphMemoryState, context_schema=RuntimeContext)
graph.add_node(FOOD_PLANNER_LLM, food_planner)
graph.add_node(READ_LONG_TERM_MEMORY, read_long_term_memory)
graph.add_node(INGREDIENTS_PLANNER, ingredients_planner)
graph.add_node(SHOPPING_LIST, shopping_list)
graph.add_node(EVALUATOR, evaluator)
graph.add_node(CALL_LLM, call_llm)

graph.add_conditional_edges(
    READ_LONG_TERM_MEMORY,
    direct_talk,
    {CALL_LLM: CALL_LLM, FOOD_PLANNER_LLM: FOOD_PLANNER_LLM},
)

graph.add_edge(START, READ_LONG_TERM_MEMORY)
graph.add_edge(FOOD_PLANNER_LLM, INGREDIENTS_PLANNER)
graph.add_edge(INGREDIENTS_PLANNER, SHOPPING_LIST)
graph.add_edge(SHOPPING_LIST, EVALUATOR)
graph.add_edge(EVALUATOR, END)
graph.add_edge(CALL_LLM, END)

graph = graph.compile()

# response = graph.invoke(
#     {"messages": [HumanMessage("Hi, do you know my preferences?")]},
#     context=RuntimeContext("andre_ponce", "0b954782-8cff-44cf-bec3-efd7998300d6"),
# )

# console.print(response)
