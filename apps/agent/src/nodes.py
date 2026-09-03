from datetime import datetime

from constants import CALL_LLM, FOOD_PLANNER_LLM
from graph_state import GraphMemoryState
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage
from retrieve import get_prices_for_ingredients_batch
from rich.console import Console

console = Console()
MODEL_PROVIDER = "openai:gpt-4o-mini"


def food_planner(state: GraphMemoryState):
    llm = init_chat_model(MODEL_PROVIDER, temperature=0.5)
    user_preferences = state.get("user_preferences") or {}
    rules = user_preferences.get("rules")

    if not rules:
        rules = """- Solo desayuno, almuerzo y cena por día.
- Nada horneado.
- Ninguna comida debe tardar más de 75 minutos en prepararse.
- Comidas variadas, nutritivas y que ayuden a ganar/mantener peso de forma saludable.
- Para el desayuno siempre algo ligero pero enérgico y rápido de preparar."""

    sport = user_preferences.get("sport") or "Ninguno reportado"
    today_str = datetime.today().strftime("%Y-%m-%d")

    messages = [
        SystemMessage(
            """Eres un planificador nutricional experto en cocina tradicional y accesible de Honduras.
Tu tarea es diseñar un plan de alimentación saludable, realista y estructurado para 15 días continuos.

REGLAS OBLIGATORIAS:
1. IDIOMA: Todo el contenido debe ser exclusivamente en español.
2. CERO ALUCINACIONES Y TOTAL REALISMO: Utiliza platillos e ingredientes típicos, accesibles y comunes en Honduras (ej. frijoles, plátano, huevos, pollo, queso/mantequilla, arroz, tortillas de maíz/harina, verduras frescas). Nada de platos extravagantes o ingredientes difíciles de conseguir.
3. CERO TEXTO DE RELLENO: No incluyas introducciones, saludos, preámbulos ni despedidas (prohibido decir '¡Hola!', 'Aquí tienes tu plan', 'Espero te sirva'). Entrega directamente el plan estructurado.
4. FORMATO: Presenta el plan día por día (Día 1 al Día 15) indicando la fecha de cada día a partir de mañana. Para cada día incluye exactamente:
   - **Desayuno:** [Nombre del plato y breve descripción]
   - **Almuerzo:** [Nombre del plato y breve descripción]
   - **Cena:** [Nombre del plato y breve descripción]"""
        ),
        HumanMessage(
            f"""Crea el plan de comidas para 15 días a partir de mañana (Hoy es {today_str}).
Deporte practicado: {sport}.

Reglas del usuario:
{rules}"""
        ),
    ]

    response = llm.invoke(messages)
    console.print(response.content)

    return {"messages": [response], "food": response.content}


BUDGET = "3,500"


def ingredients_planner(state: GraphMemoryState):
    llm = init_chat_model(MODEL_PROVIDER, temperature=0.2)
    food = state.get("food") or ""

    assert food, "No se encontró el plan de comidas en el estado"

    messages = [
        SystemMessage(
            """Eres un planificador experto en cálculo de porciones e insumos para el hogar en Honduras.
Tu tarea es calcular y consolidar la lista completa y exacta de ingredientes necesarios para preparar el plan de comidas para exactamente 2 personas durante 15 días.

REGLAS OBLIGATORIAS:
1. CERO ALUCINACIONES: Extrae estrictamente los ingredientes requeridos para las comidas del plan. No inventes ingredientes que no se usen en el menú provisto.
2. REALISMO EN CANTIDADES: Calcula cantidades y pesos realistas para 2 personas adultas durante 15 días (ej. cantidad de libras de pollo/carne, cartones o unidades de huevos, libras de frijoles, plátanos, etc.). Recuerda incluir insumos básicos de cocina necesarios (aceite, sal, especias básicas) en cantidades moderadas.
3. CERO TEXTO DE RELLENO: No incluyas introducciones, frases de transición ni conclusiones (prohibido decir 'Aquí están los ingredientes'). Empieza directamente con la lista.
4. IDIOMA Y FORMATO: Todo en español. Organiza los ingredientes en formato Markdown clasificados por categorías claras:
   - 🥩 Carnes y Proteínas
   - 🥛 Lácteos y Huevos
   - 🌾 Granos, Abarrotes y Despensa
   - 🥦 Frutas y Verduras
   - 🧂 Aceites y Condimentos
   Cada elemento debe especificar: `- [Ingrediente]: [Cantidad y unidad de medida (ej. lbs, unidades, litros)]`."""
        ),
        HumanMessage(
            f"""Este es el plan de comidas para 15 días:
{food}

Calcula la lista consolidada de ingredientes con cantidades realistas para 2 personas."""
        ),
    ]

    response = llm.invoke(messages)
    return {"messages": [response], "ingredients": response.content}


def price_retriever(state: GraphMemoryState):
    """Nodo determinista: consulta precios reales de los ingredientes en SQLite."""
    ingredients_text = state.get("ingredients") or ""

    ingredient_names = []
    for line in ingredients_text.splitlines():
        clean_line = line.strip()
        if clean_line.startswith("-"):
            name = clean_line.lstrip("-").split(":")[0].strip()
            name = name.replace("[", "").replace("]", "").replace("*", "").strip()
            if name:
                ingredient_names.append(name)

    if not ingredient_names:
        ingredient_names = [
            l.strip()
            for l in ingredients_text.splitlines()
            if l.strip() and not l.strip().startswith("#")
        ]

    real_prices = get_prices_for_ingredients_batch(ingredient_names)

    console.print(real_prices)

    return {"real_prices": real_prices}


def shopping_list(state: GraphMemoryState):
    llm = init_chat_model(MODEL_PROVIDER, temperature=0.1)
    food = state.get("food") or ""
    ingredients = state.get("ingredients") or ""
    real_prices = state.get("real_prices") or []

    assert food and ingredients, (
        "Falta el plan de comida o los ingredientes en el estado"
    )

    # Formatear lista de opciones reales encontradas para el prompt
    prices_context = ""
    for item in real_prices:
        ing = item.get("ingredient")
        options = item.get("options", [])
        if options:
            prices_context += (
                f"\n🛒 Ingrediente: **{ing}** (Opciones disponibles en tienda):\n"
            )
            for idx, opt in enumerate(options, 1):
                prices_context += f"   - Opción {idx}: {opt['product_name']} | Marca: {opt.get('brand', 'N/A')} | Precio Real: **{opt['price_lps']} LPS**\n"
        else:
            prices_context += f"\n🛒 Ingrediente: **{ing}** -> Sin registro en catálogo (requiere estimación razonable)\n"

    messages = [
        SystemMessage(
            f"""Eres un asistente de compras experto en supermercados de Honduras (específicamente supermercados tipo Paiz en el Bulevar Morazán, Tegucigalpa).
Tu tarea es confeccionar la lista de compras óptima para 2 personas durante 15 días, ajustada estrictamente a un presupuesto de {BUDGET} LPS.

CÓMO ELEGIR LOS PRODUCTOS EN EL SUPERMERCADO:
1. SELECCIÓN INTELIGENTE DE OPCIONES: Para cada ingrediente requerido, dispones de las MEJORES OPCIONES reales encontradas en el catálogo de la tienda con sus precios exactos en LPS.
   - Actúa como si estuvieras recorriendo los pasillos del supermercado: evalúa el presupuesto global de {BUDGET} LPS y selecciona la opción que mejor balancee costo y practicidad.
   - Si el presupuesto es ajustado, prioriza las opciones más económicas (marcas accesibles o presentaciones estándar).
2. RESPETO OBLIGATORIO DE PRECIOS REALES: Cuando selecciones una opción del catálogo, ES OBLIGATORIO usar su precio real en LPS para el cálculo de los subtotales. Prohibido alterar o inventar precios de productos del catálogo.
3. INGREDIENTES SIN REGISTRO: Solo si un ingrediente indica 'Sin registro en catálogo', proporciona una estimación realista acorde a los precios promedio de Honduras.
4. CERO TEXTO DE RELLENO: No escribas saludos, introducciones ni despedidas (prohibido decir 'Ya está lista la lista de compras', 'Aquí tienes la lista'). Comienza inmediatamente con las tablas de pasillo.
5. FORMATO DE SALIDA: Presenta cada pasillo/sección con una tabla Markdown clara:
   | Producto Seleccionado | Cantidad / Presentación | Precio Unitario (LPS) | Subtotal (LPS) |
   Al final de la lista, incluye un resumen matemático exacto:
   - **Total Estimado de Compras:** [Total] LPS
   - **Presupuesto Asignado:** {BUDGET} LPS
   - **Diferencia / Balance:** [Diferencia] LPS"""
        ),
        HumanMessage(
            f"""Genera la lista de compras seleccionando las mejores opciones para los ingredientes del menú y respetando los precios reales provistos:

INGREDIENTES REQUERIDOS:
{ingredients}

CATÁLOGO DE OPCIONES REALES ENCONTRADAS EN EL SUPERMERCADO:
{prices_context}"""
        ),
    ]

    response = llm.invoke(messages)
    return {"messages": [response], "shopping_list": response.content}


def evaluator(state: GraphMemoryState):
    llm = init_chat_model(MODEL_PROVIDER, temperature=0.0)
    food = state.get("food") or ""
    ingredients = state.get("ingredients") or ""
    shopping_list_content = state.get("shopping_list") or ""

    assert food and shopping_list_content and ingredients, (
        "Faltan datos para ejecutar el evaluador"
    )

    messages = [
        SystemMessage(
            f"""Eres un auditor y evaluador financiero-nutricional crítico, estricto y objetivo para compras en Honduras.
Tu trabajo es auditar la coherencia y viabilidad real entre: el plan de comidas, la lista de ingredientes y la lista de compras con presupuesto de {BUDGET} LPS.

CRITERIOS DE AUDITORÍA:
1. Coherencia (Comidas vs. Ingredientes): ¿Todos los ingredientes necesarios para cocinar el menú están en la lista? ¿Hay ingredientes que se compran pero nunca se usan?
2. Realismo en Cantidades: ¿Las cantidades son suficientes y lógicas para alimentar a 2 personas durante 15 días?
3. Realismo de Precios y Matemática: Verifica que la suma matemática de la lista de compras sea correcta y que los precios unitarios estimados en Lempiras sean creíbles en el mercado hondureño. ¿El presupuesto de {BUDGET} LPS es realmente viable o queda muy corto/excedido?

REGLAS OBLIGATORIAS:
- IDIOMA: Todo exclusivamente en español.
- CERO COMPLACENCIA NI ALUCINACIONES: Sé sumamente crítico. Si la matemática no suma bien, señálalo. Si faltan ingredientes o las porciones son insuficientes para 15 días, indícalo claramente con números.
- CERO TEXTO DE RELLENO: No pongas introducciones ni saludos. Ve directo al reporte estructurado en Markdown.
- FORMATO:
  - 📋 **Veredicto General:** [Aprobado / Ajustes Necesarios / Inviable]
  - 📊 **Auditoría por Criterio:** Usa viñetas con ✅ (Correcto), ⚠️ (Advertencia) o ❌ (Falla/Error).
  - 💡 **Ajustes y Recomendaciones Concretas:** Si hay fallas en presupuesto o ingredientes, indica exactamente qué ajustar."""
        ),
        HumanMessage(
            f"""Audita los siguientes datos:

PLAN DE COMIDAS:
{food}

INGREDIENTES:
{ingredients}

LISTA DE COMPRAS:
{shopping_list_content}"""
        ),
    ]

    response = llm.invoke(messages)
    return {"messages": [response]}


def call_llm(state: GraphMemoryState):
    llm = init_chat_model(
        MODEL_PROVIDER,
        temperature=0.7,
        max_tokens=1000,
    )
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


def direct_talk(state: GraphMemoryState):
    print("TALKING DIRECTLY TO DIRECT TALK NODE")

    if state.get("shopping_list"):
        console.print("Redirecting to calling LLM")
        return CALL_LLM
    else:
        print("Food planner List NODE")
        return FOOD_PLANNER_LLM
