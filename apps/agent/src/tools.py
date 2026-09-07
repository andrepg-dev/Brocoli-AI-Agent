from constants import MODEL_PROVIDER
from graph_state import GraphMemoryState
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from rich.console import Console

console = Console()


@tool
def shopping_list_correction(state: GraphMemoryState):
    """Tool to correct shopping list if provided"""
    llm = init_chat_model(MODEL_PROVIDER, temperature=0.1)
    food = state.get("food") or ""
    real_prices = state.get("real_prices") or []

    assert food, "Falta el plan de comida o los ingredientes en el estado"

    # Formatear catálogo limpio de opciones reales para el prompt
    prices_context = ""
    for item in real_prices:
        ing = item.get("ingredient")
        options = item.get("options", [])
        if options:
            prices_context += f"\n🛒 **{ing}**:\n"
            for opt in options:
                prices_context += f"   - {opt['product']} -> {opt['price']} LPS\n"
        else:
            prices_context += f"\n🛒 **{ing}** -> Sin opciones en catálogo (estimar)\n"

    print("\n" + "=" * 70)
    console.print(prices_context)
    print("\n" + "=" * 70)

    messages = [
        SystemMessage(
            """Eres un asistente que corrige una lista de shopping, se te proveera la lista de shopping y las correciones que se deben de hacer, sigue las instrucciones correctamente."""
        ),
        HumanMessage(
            f"""
            Shopping List
            {state.get("shopping_list")}

            Precios:
            {prices_context}

            Correciones:
            {state.get("corrections")}
            """
        ),
    ]

    response = llm.invoke(messages)
    return {"messages": [response], "shopping_list": response.content}
