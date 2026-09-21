from ticket_assistant.graph.state import AssistantState
from ticket_assistant.graph.nodes.nodes import (
    evaluate_retrieval,
    MAX_ATTEMPTS,
)

# retry bound, given a state that has already used its attempts.

def test_retry_bound():
    state: AssistantState = {
        "question": "What is the weather?",
        "query": "What is the weather?",
        "chat_history": [],
        "documents": [],
        "attempts": MAX_ATTEMPTS,
    }

    assert evaluate_retrieval(state) == "refuse"