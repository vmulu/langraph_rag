from langchain_core.documents import Document

from ticket_assistant.graph.graph import build_graph

# graph has the nodes and edges you think it has

def test_graph_has_expected_nodes_and_edges():
    graph = build_graph()

    nodes = graph.get_graph().nodes
    edges = graph.get_graph().edges

    assert "retrieve" in nodes
    assert "retry" in nodes
    assert "answer" in nodes
    assert "refuse" in nodes

    edge_pairs = {(edge.source, edge.target) for edge in edges}

    assert ("__start__", "retrieve") in edge_pairs
    assert ("retry", "retrieve") in edge_pairs
    assert ("answer", "__end__") in edge_pairs
    assert ("refuse", "__end__") in edge_pairs