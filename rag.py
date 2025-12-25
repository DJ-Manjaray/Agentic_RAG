from typing import Literal
from langgraph.graph import StateGraph,MessagesState, START, END
from openai import OpenAI
from typing_extensions import TypedDict
from typing import List
from results_openai import get_llm_response
from chromaDB import collection1, collection2
import os

# === Define workflow node functions ===
def retrieve_context(state):
    """Retrieve top documents from ChromaDB based on query."""
    print("---RETRIEVING CONTEXT---")
    query = state["query"] # last user message

    results = collection1.query(query_texts=[query], n_results=3)
    context = "\n".join(results["documents"][0])

    #state["query"] = query
    state["context"] = context
    print(context)
    # Save context in the state for later nodes
    return state

def build_prompt(state):
    """Construct the RAG-style prompt."""
    print("---AUGMENT (BUILDING PROMPT)---")
    query = state["query"]
    context = state["context"]

    prompt = f"""
            Answer the following question using the context below.

            Context:
            {context}

            Question: {query}

            please limit your answer in 50 words.
            """
    
    state["prompt"] = prompt
    print(prompt)
    return state

def call_llm(state):
    """Call your existing LLM function."""
    print("---GENERATE (CALLING LLM)---")
    prompt = state["prompt"]
    answer = get_llm_response(prompt)
    state["response"] = answer
    return state

# === Build the workflow ===

## Define the state structure
class GraphState(TypedDict):
    query : str
    prompt : str
    context : List[str]
    response : str

    
workflow = StateGraph(GraphState)

# Add nodes
workflow.add_node("Retriever", retrieve_context)
workflow.add_node("Augment", build_prompt)
workflow.add_node("Generate", call_llm)

# Define edges
workflow.add_edge(START, "Retriever")
workflow.add_edge("Retriever", "Augment")
workflow.add_edge("Augment", "Generate")
workflow.add_edge("Generate", END)

# Compile agent
rag_agent = workflow.compile()

# === Run it ===
graph_path = os.path.join(os.getcwd(), "rag_graph.png")
with open(graph_path, "wb") as graph_file:
    graph_file.write(rag_agent.get_graph().draw_mermaid_png())
print(f"Workflow graph saved to {graph_path}")

input_state = {"query": "What are the treatments for Kawasaki disease ?"}

from pprint import pprint

final_response = None
for step in rag_agent.stream(input_state):
    for key, value in step.items():
        pprint(f"Finished running: {key}:")
        if "response" in value:
            final_response = value["response"]
            pprint(final_response)

if final_response:
    response_path = os.path.join(os.getcwd(), "rag_response.txt")
    with open(response_path, "w", encoding="utf-8") as response_file:
        response_file.write(final_response)
    print(f"Response saved to {response_path}")
else:
    print("No response generated to save.")