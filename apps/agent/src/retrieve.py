"""Retrieve price information from local SQLite database in batch using SQLModel."""

import os

from models import ProductPrice
from sqlmodel import Session, create_engine, or_, select

DB_PATH = os.getenv("PRICE_DB_PATH", "prices.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False)


def search_product_price(ingredient_name: str) -> ProductPrice | None:
    """Search for the best matching ProductPrice in local DB for a single ingredient."""
    if not os.path.exists(DB_PATH):
        return None

    with Session(engine) as session:
        statement = (
            select(ProductPrice)
            .where(
                (ProductPrice.product_name.contains(ingredient_name))
                | (ProductPrice.category.contains(ingredient_name))
            )
            .order_by(ProductPrice.price_lps.asc())
            .limit(1)
        )
        return session.exec(statement).first()


def get_prices_for_ingredients_batch(ingredients_list: list[str]) -> list[dict]:
    """Retrieve prices for a list of ingredients in a SINGLE batch SQL query."""
    if not ingredients_list or not os.path.exists(DB_PATH):
        return [
            {
                "ingredient": ing,
                "matched_product": None,
                "price_lps": None,
                "note": "Sin registro",
            }
            for ing in ingredients_list
        ]

    # Build dynamic OR conditions for all ingredients
    conditions = []
    for ing in ingredients_list:
        clean_ing = ing.strip()
        if clean_ing:
            conditions.append(ProductPrice.product_name.contains(clean_ing))
            conditions.append(ProductPrice.category.contains(clean_ing))

    if not conditions:
        return []

    # Execute ONE single SQL query for all ingredients
    with Session(engine) as session:
        statement = select(ProductPrice).where(or_(*conditions))
        matched_products = session.exec(statement).all()

    # Map each ingredient to its best matching product
    results = []
    for ing in ingredients_list:
        clean_ing = ing.strip().lower()
        matched = next(
            (
                p
                for p in matched_products
                if clean_ing in p.product_name.lower()
                or (p.category and clean_ing in p.category.lower())
            ),
            None,
        )

        if matched:
            results.append(
                {
                    "ingredient": ing,
                    "matched_product": matched.product_name,
                    "price_lps": matched.price_lps,
                    "category": matched.category,
                    "supermarket": matched.supermarket,
                }
            )
        else:
            results.append(
                {
                    "ingredient": ing,
                    "matched_product": None,
                    "price_lps": None,
                    "note": "Sin registro en BD",
                }
            )

    return results
