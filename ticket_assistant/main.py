
"""CLI for chat bot"""

from .graph.graph import build_graph

def main():

    print("Policy Assistant")
    print("Type 'quit' to exit.\n")

    graph = build_graph()

    chat_history = []

    while True:
        question = input("human> ").strip()

        if question.lower() in {"quit", "exit"}:
            print("chat closed")
            break

        if not question:
            continue

        result = graph.invoke(
            {
                "question": question,
                "query": question,
                "chat_history": chat_history,
                "documents": [],
                "attempts": 0,
            }
        )

        answer = result.get("answer", "I couldn't generate an answer.")

        print(f"\n bot> {answer}\n")

        chat_history = result.get("chat_history", chat_history)


if __name__ == "__main__":
    main()