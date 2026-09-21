"""nodes for LangGraph"""

from ..state import AssistantState
from ...rag.retriever import build_local_retriever
from ...converse import converse, format_user_message, text_of

MAX_ATTEMPTS = 2

# retriever runnable
retriever = build_local_retriever()

def retrieve_node(state: AssistantState) -> dict:

    documents = retriever.invoke(state["query"])

    return {
        "documents": documents,
        "attempts": state["attempts"] + 1,
    }


def evaluate_retrieval(state: AssistantState) -> str:

    if state["documents"]:
        return "answer"

    if state["attempts"] < MAX_ATTEMPTS:
        return "retry"

    return "refuse"


def retry_node(state: AssistantState) -> dict:

    return {
        "query": f"policy information about {state['question']}"
    }


def answer_node(state: AssistantState) -> dict:

    context = "\n\n".join(
        f"Source: {document.metadata.get('source', 'Unknown')}\n"
        f"{document.page_content}"
        for document in state["documents"]
    )

    prompt = f"""
            Answer the user's question using ONLY the policy documents below.

            If the documents do not contain enough information to answer the
            question, do not make up an answer.

            Question:
            {state["question"]}

            Policy documents:
            {context}

            When answering, name the source document that supports the answer.
            """

    response = converse(
        messages=[format_user_message(prompt)],
        system=(
            "You are a policy assistant. "
            "Answer only from the provided policy documents."
        ),
    )

    return {
        "answer": text_of(response)
    }


def refuse_node(state: AssistantState) -> dict:
    """Refuse when the documents do not support the question."""

    return {
        "answer": (
            "I can't answer that based on the policy documents "
            "available to me."
        )
    }