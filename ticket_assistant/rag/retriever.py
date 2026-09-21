""" create a retriever we can use as part of our chains """

from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever # a runnable
from langchain_core.vectorstores import InMemoryVectorStore # dont need if you are using AWS KB
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_aws import AmazonKnowledgeBasesRetriever, BedrockEmbeddings # this would be used for project

from functools import lru_cache
from pathlib import Path

from ..aws import config

RUNBOOK_DIR = Path(__file__).resolve().parent.parent.parent / "kb-documents"

# chunker
def load_policy_chunks() -> list[Document]:
    """ read runbooks/*.md and split each its "#" and "##" headers """

    splitter = MarkdownHeaderTextSplitter(
        [
            ("#", "title"),
            ("##", "sections")
        ],
        strip_headers=False # keep the header text inside of the chunks
    )

    chunks : list[Document] = []
    for path in sorted(RUNBOOK_DIR.glob("*.md")):
        for chunk in splitter.split_text(path.read_text(encoding="utf-8")):
            chunk.metadata["source"] = path.name
            chunks.append(chunk)

    return chunks

# retriever runnable
class ScoreThresholdRetriever(BaseRetriever):
    "Top - k & Top - p retrieval of documents"

    store : InMemoryVectorStore
    k : int = 4

    # InMemoryVectorStore is not a type Pydantic will recognize, so we need to tell pydantic to allow it

    model_config = {"arbitrary_types_allowed" : True}

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun) -> list[Document]:

        # find the K most relevent docs
        hits = self.store.similarity_search_with_score(query, k=self.k)

        # filter out only the docs that meet our threshold min
        return [doc for doc, score in hits]

@lru_cache(maxsize=1)
def build_local_retriever(k : int = 4) -> BaseRetriever:
    """ builds the in-memory vector store and creates the reliever for it

        cached so that chain doesn't have to spend time and money re-creating the embeddings
    """

    chunks = load_policy_chunks()
    embedding = BedrockEmbeddings(
        model_id=config.EMBED_MODEL_ID,
        region_name=config.AWS_REGION
    )

    store = InMemoryVectorStore.from_documents(chunks, embedding)

    return ScoreThresholdRetriever(
        store=store,
        k=k
    )


# only for when we using AWS KB

# def build_kd_retriever(k : int = 4, threshold : float = 0.4) -> BaseRetriever:
#     """grab a KB from AWS Bedrock and create a retriever for it"""
#     return AmazonKnowledgeBasesRetriever(
#         knowledge_base_id=config.BEDROCK_KB_ID,
#         region_name=config.AWS_REGION,
#         retrieval_config={"vectorSearchConfiguration" : {"numberOfResults" : k}},
#         min_score_confidence=threshold
#     )

# def get_retriever(k : int = 4) -> BaseRetriever:
#     if config.BEDROCK_KB_ID:
#         return build_kd_retriever(k=k)
#     return build_local_retriever(k=k)

