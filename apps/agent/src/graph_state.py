from typing import Literal, TypedDict

from langgraph.graph import MessagesState
from pydantic import Field


class UserPreferences(TypedDict):
    goal: Literal["gain_energy", "weight_loss", "gain_weight"] = Field(
        "User goal, gain energy, weigh loss, gain weight"
    )
    sport: str | None = Field("If the user is involucred in some sport.")
    rules: str | None = Field("Any user preference")
    location: str | None = Field("User location")
    budget: int | None = Field("User budget")
    persons_included: int | None = Field("Default 1")


class GraphMemoryState(MessagesState):
    user_preferences: UserPreferences
    food: str = Field("This is the food that you have planned for the user")
    ingredients: str = Field("This are the ingredients of the food")
    real_prices: list[dict] = Field(default_factory=list, description="Precios reales de la BD")
    shopping_list: str = Field("Shopping list")

