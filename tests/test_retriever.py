from ticket_assistant.rag.retriever import load_policy_chunks

# documents load and split as expected

def test_policy_documents_load_and_split():
    chunks = load_policy_chunks()

    assert len(chunks) > 0

    for chunk in chunks:
        assert chunk.page_content.strip()
        assert "source" in chunk.metadata
        assert chunk.metadata["source"].endswith(".md")