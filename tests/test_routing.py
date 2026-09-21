from langchain_core.documents import Document

from ticket_assistant.graph.state import AssistantState
from ticket_assistant.graph.nodes.nodes import (
    evaluate_retrieval,
    MAX_ATTEMPTS,
)

# routing decision, given a state you construct by hand,

def test_routing_to_answer_when_documents_exist():
    state: AssistantState = {
        "question": "What is the refund policy?",
        "query": "What is the refund policy?",
        "chat_history": [],
        "documents": [
            Document(page_content="Refunds are allowed.")
        ],
        "attempts": 1,
    }

    assert evaluate_retrieval(state) == "answer"


def test_routing_to_retry_when_no_documents():
    state: AssistantState = {
        "question": "What is the refund policy?",
        "query": "What is the refund policy?",
        "chat_history": [],
        "documents": [],
        "attempts": 1,
    }

    assert evaluate_retrieval(state) == "retry"