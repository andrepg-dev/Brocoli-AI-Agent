from graph_state import GraphMemoryState, UserPreferences
from langgraph.runtime import Runtime
from rich.console import Console

console = Console()


def write_long_term_memory(
    content: UserPreferences, runtime: Runtime[GraphMemoryState]
):
    assert runtime.store is not None

    store = runtime.store
    user_id = runtime.context.user_id

    store.put("users", user_id, content)
    return "Succesfully saved user info"


def read_long_term_memory(_: GraphMemoryState, runtime: Runtime[GraphMemoryState]):
    """Reading long term memory"""
    print("[*] LONG TERM MEMORY NODE")

    store = runtime.store
    user_id = runtime.context.user_id
    user_preferences = store.get(("users",), user_id)
    return {"user_preferences": user_preferences.value if user_preferences else None}
