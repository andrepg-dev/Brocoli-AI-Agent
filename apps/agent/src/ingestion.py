"""Ingest products and prices from VTEX supermarket API into SQLite in controlled batches."""

import os
import time
from datetime import datetime

import httpx
from dotenv import load_dotenv
from models import ProductPrice
from sqlmodel import Session, SQLModel, create_engine, select

load_dotenv(override=True)

SUPERMARKET_BASE_URL = os.getenv("SUPERMARKET_BASE_URL", "https://www.paiz.com.hn")
DB_PATH = os.getenv("PRICE_DB_PATH", "prices.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    """Initialize database tables using SQLModel metadata."""
    SQLModel.metadata.create_all(engine)


def fetch_vtex_products(
    query: str,
    base_url: str = SUPERMARKET_BASE_URL,
    from_idx: int = 0,
    to_idx: int = 49,
) -> list[dict]:
    """Fetch products from VTEX catalog search API."""
    endpoint = f"{base_url.rstrip('/')}/api/catalog_system/pub/products/search"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
    }
    params = {"ft": query, "_from": from_idx, "_to": to_idx}

    try:
        response = httpx.get(endpoint, headers=headers, params=params, timeout=10.0)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"[!] Error fetching VTEX data for query '{query}': {e}")
    return []


def chunk_list(items: list, chunk_size: int = 5):
    """Split a list into smaller chunks for batch processing."""
    for i in range(0, len(items), chunk_size):
        yield items[i : i + chunk_size]


def parse_and_store_products(
    raw_products: list[dict], supermarket_name: str = "Paiz"
) -> int:
    """Parse raw VTEX JSON response and upsert into SQLite using SQLModel Session."""
    saved_count = 0

    with Session(engine) as session:
        for prod in raw_products:
            try:
                prod_id = str(prod.get("productId"))
                name = prod.get("productName", "")
                brand = prod.get("brand", "")
                categories = prod.get("categories", ["Desconocido"])
                category = categories[0].strip("/") if categories else "General"

                items = prod.get("items", [])
                if not items:
                    continue

                sellers = items[0].get("sellers", [])
                if not sellers:
                    continue

                offer = sellers[0].get("commertialOffer", {})
                price = float(offer.get("Price", 0.0))
                list_price = float(offer.get("ListPrice", price))
                available_qty = int(offer.get("AvailableQuantity", 0))

                if price <= 0:
                    continue

                statement = select(ProductPrice).where(
                    ProductPrice.product_id == prod_id
                )
                existing = session.exec(statement).first()

                if existing:
                    existing.product_name = name
                    existing.brand = brand
                    existing.category = category
                    existing.price_lps = price
                    existing.list_price_lps = list_price
                    existing.available_quantity = available_qty
                    existing.updated_at = datetime.now().isoformat()
                    session.add(existing)
                else:
                    new_item = ProductPrice(
                        product_id=prod_id,
                        product_name=name,
                        brand=brand,
                        category=category,
                        price_lps=price,
                        list_price_lps=list_price,
                        available_quantity=available_qty,
                        supermarket=supermarket_name,
                        updated_at=datetime.now().isoformat(),
                    )
                    session.add(new_item)

                saved_count += 1
            except Exception as err:
                print(f"[!] Error processing product item: {err}")

        session.commit()

    return saved_count


def run_ingestion_batch(
    keywords: list[str] | None = None,
    batch_size: int = 5,
    delay_between_batches: float = 1.0,
    base_url: str = SUPERMARKET_BASE_URL,
) -> None:
    """Run ingestion pipeline splitting keywords into small controlled batches to avoid rate limits."""
    init_db()

    if not keywords:
        keywords = [
            "frijoles",
            "arroz",
            "leche",
            "huevos",
            "queso",
            "mantequilla",
            "pollo",
            "carne",
            "cerdo",
            "platano",
            "tomate",
            "cebolla",
            "papa",
            "aceite",
            "harina",
            "pan",
            "café",
            "azucar",
            "sal",
        ]

    total_ingested = 0
    keyword_batches = list(chunk_list(keywords, chunk_size=batch_size))
    print(
        f"[*] Starting ingestion of {len(keywords)} keywords in {len(keyword_batches)} batches (Batch size: {batch_size})..."
    )

    for idx, batch in enumerate(keyword_batches, start=1):
        print(f"\n[📦 Lote {idx}/{len(keyword_batches)}] Procesando palabras: {batch}")

        for kw in batch:
            products = fetch_vtex_products(kw, base_url=base_url)
            count = parse_and_store_products(products)
            total_ingested += count

        # Small pause between batches to prevent rate limiting / blocking
        if idx < len(keyword_batches):
            time.sleep(delay_between_batches)

    print(
        f"\n[+] Ingestion batch process completed! {total_ingested} total products synced into database."
    )


if __name__ == "__main__":
    run_ingestion_batch()
