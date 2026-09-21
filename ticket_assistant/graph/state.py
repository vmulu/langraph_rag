""" state used by the policy assistant """

from typing import TypedDict, Annotated, NotRequired

from langchain_core.documents import Document
from langgraph.graph.message import add_messages
from operator import add


class AssistantState(TypedDict):
    """ state passed along nodes """

    question: str
    query: str
    chat_history: Annotated[list[dict], add_messages]
    documents: Annotated[list[Document], add]
    attempts: int
    answer: NotRequired[str]