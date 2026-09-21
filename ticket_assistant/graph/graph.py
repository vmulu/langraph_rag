""" graph """

from .nodes.nodes import *
from .state import AssistantState

from langgraph.graph import StateGraph, START, END

def build_graph():
    builder = StateGraph(AssistantState)

    builder.add_node("retrieve", retrieve_node)
    builder.add_node("retry", retry_node)
    builder.add_node("answer", answer_node)
    builder.add_node("refuse", refuse_node)

    builder.add_edge(START, "retrieve")

    builder.add_conditional_edges(
        "retrieve",
        evaluate_retrieval,
        {
            "answer": "answer",
            "retry": "retry",
            "refuse": "refuse",
        },
    )

    builder.add_edge("retry", "retrieve")
    builder.add_edge("answer", END)
    builder.add_edge("refuse", END)


    return builder.compile()