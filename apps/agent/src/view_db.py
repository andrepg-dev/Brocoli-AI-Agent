"""Helper script to visualize ProductPrice table data formatted with rich."""

import argparse

from models import ProductPrice
from retrieve import engine
from rich.console import Console
from rich.table import Table
from sqlmodel import Session, select


def view_prices(limit: int = 50, search: str | None = None) -> None:
    """Print database records in a rich formatted table."""
    console = Console()
    table = Table(title="🛒 Tabla de Precios de Supermercado (prices.db)")

    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Producto", style="bold white")
    table.add_column("Precio (LPS)", justify="right", style="bold green")
    table.add_column("Categoría", style="magenta")
    table.add_column("Supermercado", style="yellow")
    table.add_column("Actualizado", style="dim")

    with Session(engine) as session:
        statement = select(ProductPrice)
        if search:
            statement = statement.where(
                (ProductPrice.product_name.contains(search))
                | (ProductPrice.category.contains(search))
            )
        statement = statement.limit(limit)
        products = session.exec(statement).all()

        if not products:
            console.print(
                "[yellow]No se encontraron registros en la base de datos.[/yellow]"
            )
            return

        for p in products:
            table.add_row(
                str(p.id),
                p.product_name,
                f"LPS {p.price_lps:.2f}",
                p.category or "N/A",
                p.supermarket,
                p.updated_at[:19] if p.updated_at else "",
            )

    console.print(table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Visualizar tabla de precios de supermercado."
    )
    parser.add_argument(
        "--limit", type=int, default=50, help="Límite de registros a mostrar"
    )
    parser.add_argument(
        "--search", type=str, default=None, help="Filtrar por producto o categoría"
    )
    args = parser.parse_args()

    view_prices(limit=args.limit, search=args.search)
