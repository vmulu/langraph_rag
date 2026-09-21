#  RAG Assistant as a LangGraph Agent

## Setup

Clone the repository and move into the project:

`git clone <repository-url>`

`cd <repository-name>`

Create and activate a virtual environment:

`python -m venv .venv`

`source .venv/bin/activate`

Install the project:

`pip install -e .`

Create your .env file from the .env.example

Add your AWS configuration to your .env.

## Run

From the repository root:

`python -m ticket_assistant.main`

For testing run:

`python -m pytest`

This will start up the chat bot.

## Requirement 5 — Compiled LangGraph

The assistant uses a compiled `LangGraph StateGraph.`

The graph contains these nodes:

**retrieve** — searches the policy documents

**retry** — changes the search query and tries again

**answer** — generates an answer using the retrieved documents

**refuse** — refuses when the documents do not support the question

## Requirement 9 — Bounded Retry

The assistant allows a maximum of 2 retrieval attempts.

If the first search does not find documents, the graph changes the query and tries again.

If the second attempt also fails, the graph routes to refuse.

This prevents the graph from retrying forever.

## Graph :
```mermaid
graph TD;
        __start__([<p>__start__</p>]):::first
        retrieve(retrieve)
        retry(retry)
        answer(answer)
        refuse(refuse)
        __end__([<p>__end__</p>]):::last
        __start__ --> retrieve;
        retrieve -.-> answer;
        retrieve -.-> refuse;
        retrieve -.-> retry;
        retry --> retrieve;
        answer --> __end__;
        refuse --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
```
