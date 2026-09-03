"""Smart price retrieval with local SQLite caching, on-demand VTEX scraping, and multi-option selection."""

import os
import re
import unicodedata

from ingestion import fetch_vtex_products, parse_and_store_products
from models import ProductPrice
from sqlmodel import Session, create_engine, select

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(CURRENT_DIR, "prices.db")
DB_PATH = os.getenv("PRICE_DB_PATH", DEFAULT_DB_PATH)
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False)


def strip_accents(text: str) -> str:
    """Remove diacritics/accents from text (e.g. 'plátano' -> 'platano')."""
    return "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )


def extract_core_search_term(ingredient_raw: str) -> str:
    """Extract clean, searchable keyword from ingredient string.
    Example: 'Atún enlatado' -> 'atun'
             'Carne de res' -> 'res'
             'Tortillas de maíz' -> 'tortilla'
             'Especias varias (pimienta, orégano)' -> 'pimienta'
    """
    cleaned = re.sub(r"\(.*?\)", "", ingredient_raw)
    cleaned = re.sub(r"[^\w\s]", "", cleaned).strip().lower()

    special_mappings = {
        "atun enlatado": "atun",
        "carne de res": "res",
        "chuletas de cerdo": "chuleta",
        "tortillas de maiz": "tortilla",
        "tortillas": "tortilla",
        "frijoles negros": "frijol",
        "frijoles rojos": "frijol",
        "aceite vegetal": "aceite",
        "yogur natural": "yogur",
        "pan de banano": "pan",
        "pan de maiz": "pan",
        "cereal integral": "cereal",
        "especias varias": "especias",
    }

    norm = strip_accents(cleaned)
    for k, v in special_mappings.items():
        if k in norm:
            return v

    stop_words = {
        "de",
        "en",
        "con",
        "para",
        "y",
        "el",
        "la",
        "los",
        "las",
        "un",
        "una",
        "fresco",
        "fresca",
        "natural",
        "enlatado",
        "enlatada",
        "varias",
        "varios",
        "picado",
        "molido",
    }
    words = [w for w in norm.split() if w not in stop_words]

    return words[0] if words else norm


def query_db_for_options(term: str, limit: int = 6) -> list[ProductPrice]:
    """Search SQLite DB for matching products strictly by product_name."""
    if not os.path.exists(DB_PATH):
        return []

    norm_term = strip_accents(term).lower()
    title_term = norm_term.capitalize()

    with Session(engine) as session:
        stmt = (
            select(ProductPrice)
            .where(
                (ProductPrice.product_name.contains(term))
                | (ProductPrice.product_name.contains(norm_term))
                | (ProductPrice.product_name.contains(title_term))
            )
            .order_by(ProductPrice.price_lps.asc())
            .limit(limit)
        )
        return list(session.exec(stmt).all())


def get_prices_for_ingredients_smart(
    ingredients_list: list[str], max_options_per_item: int = 6
) -> list[dict]:
    """Smart price retrieval:
    1. Checks local SQLite DB for matching options.
    2. If missing in DB, fetches live from VTEX API, saves to DB, and re-queries.
    3. Returns top 2-3 best options per ingredient for the model to choose.
    """
    results = []
    missing_for_vtex = []

    # First pass: Check DB
    for ing in ingredients_list:
        clean_name = ing.strip()
        if not clean_name:
            continue

        search_term = extract_core_search_term(clean_name)
        options = query_db_for_options(search_term, limit=max_options_per_item)

        if options:
            results.append(
                {
                    "ingredient": clean_name,
                    "options": [
                        {"product": opt.product_name, "price": opt.price_lps}
                        for opt in options
                    ],
                }
            )
        else:
            missing_for_vtex.append((clean_name, search_term))

    # Second pass: For missing items, search VTEX on the fly & cache in DB!
    if missing_for_vtex:
        print(
            f"[*] Buscando {len(missing_for_vtex)} ingredientes faltantes en VTEX en vivo..."
        )
        for clean_name, search_term in missing_for_vtex:
            raw_products = fetch_vtex_products(search_term)
            if raw_products:
                parse_and_store_products(raw_products)
                options = query_db_for_options(search_term, limit=max_options_per_item)
                if options:
                    results.append(
                        {
                            "ingredient": clean_name,
                            "options": [
                                {"product": opt.product_name, "price": opt.price_lps}
                                for opt in options
                            ],
                        }
                    )
                    continue

            results.append(
                {
                    "ingredient": clean_name,
                    "options": [],
                }
            )

    return results


def get_prices_for_ingredients_batch(ingredients_list: list[str]) -> list[dict]:
    """Compatibility alias returning smart options."""
    return get_prices_for_ingredients_smart(ingredients_list, max_options_per_item=6)
