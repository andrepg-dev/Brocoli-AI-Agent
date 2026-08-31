from langgraph.graph import END, START, MessagesState, StateGraph


def call_llm(state: MessagesState):
    return {
        "messages": [{"role": "assistant", "content": "I'm great, what about you?"}]
    }


graph = StateGraph(MessagesState)
graph.add_node("call_llm", call_llm)

graph.add_edge(START, "call_llm")
graph.add_edge("call_llm", END)

graph = graph.compile()

graph.invoke({"messages": [{"role": "user", "content": "Hi, how are you?"}]})
