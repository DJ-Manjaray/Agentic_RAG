from __future__ import annotations

from typing import Literal
from langgraph.graph import StateGraph,MessagesState, START, END
from openai import OpenAI
from typing_extensions import TypedDict
from results_openai import get_llm_response
from chromaDB import collection1, collection2
from typing import List
import os
from langchain_community.utilities import GoogleSerperAPIWrapper

search = GoogleSerperAPIWrapper()

# === Define workflow node functions ===
def retrieve_context_q_n_a(state):
    """Retrieve top documents from ChromaDB Collection 1 (Medical Q&A Data) based on query."""
    print("---RETRIEVING CONTEXT---")
    query = state["query"] # last user message

    results = collection1.query(query_texts=[query], n_results=3)
    context = "\n".join(results["documents"][0])
    state["context"] = context
    state["source"] = "Medical Q&A Collection"
    print(context)
    # Save context in the state for later nodes
    return state

# === Define workflow node functions ===
def retrieve_context_medical_device(state):
    """Retrieve top documents from ChromaDB Collection 2 (Medical Device Manuals Data) based on query."""
    print("---RETRIEVING CONTEXT---")
    query = state["query"] # last user message

    results = collection2.query(query_texts=[query], n_results=3)
    context = "\n".join(results["documents"][0])
    state["context"] = context
    state["source"] = "Medical Device Manual"
    print(context)
    # Save context in the state for later nodes
    return state

def web_search(state):
    """Perform web search using Google Serper API."""
    print("---PERFORMING WEB SEARCH---")
    query = state["query"]
    search_results = search.run(query=query)
    state["context"] = search_results
    state["source"] = "Web Search"
    print(search_results)
    return state

def router(state: GraphState) -> Literal[
    "Retrieve_QnA", "Retrieve_Device", "Web_Search"
]:
    """Agentic router: decides which retrieval method to use."""
    query = state["query"]

    # A lightweight decision LLM — you can replace this with GPT-4o-mini, etc.
    decision_prompt = f"""
    You are a routing agent. Based on the user query, decide where to look for information.

    Options:
    - Retrieve_QnA: if it's about general medical knowledge, symptoms, or treatment.
    - Retrieve_Device: if it's about medical devices, manuals, or instructions.
    - Web_Search: if it's about recent news, brand names, or external data.

    Query: "{query}"

    Respond ONLY with one of: Retrieve_QnA, Retrieve_Device, Web_Search
    """

    router_decision = get_llm_response(decision_prompt).strip()
    print(f"---ROUTER DECISION: {router_decision}---")

    print(router_decision)

    updated_state = dict(state)
    updated_state["route"] = router_decision
    updated_state["source"] = router_decision
    return updated_state

# Define the routing function for the conditional edge
def route_decision(state: GraphState) -> str:
    route_choice = state.get("route")
    if route_choice not in {"Retrieve_QnA", "Retrieve_Device", "Web_Search"}:
        raise ValueError(
            f"Router did not set a valid route. Received: {route_choice!r}"
        )
    return route_choice


def build_prompt(state):
    """Construct the RAG-style prompt."""
    print("---AUGMENT (BUILDING GENERATIVE PROMPT)---")
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


def check_context_relevance(state):
    """Determine whether to retrieved context is relevant or not."""
    print("---CONTEXT RELEVANCE CHECKER---")
    query = state["query"]
    context = state["context"]

    relevance_prompt = f"""
            Check the below context if the context is relevent to the user query or.
            ####
            Context:
            {context}
            ####
            User Query: {query}

            Options:
            - Yes: if the context is relevant.
            - No: if the context is not relevant.

            Please answer with only 'Yes' or 'No'.

            """
    relevance_decision_value = get_llm_response(relevance_prompt).strip()
    print(f"---RELEVANCE DECISION: {relevance_decision_value}---")
    state["is_relevant"] = relevance_decision_value
    return state

# Define the check_context_relevance function for the conditional edge
def relevance_decision(state: GraphState) -> str:
    iteration_count = state.get("iteration_count", 0)
    iteration_count += 1
    state["iteration_count"] = iteration_count
    ## Limiting to max 3 iterations
    if iteration_count >= 3:
        print("---MAX ITERATIONS REACHED, FORCING 'Yes'---")
        state["is_relevant"] = "Yes"
    return state["is_relevant"]





# === Build the workflow ===
## Define the state structure

class GraphState(TypedDict):
    query: str
    context: str
    prompt: str
    response: str
    source: str  # Which retriever/tool was used
    route: str  # Router decision (Retrieve_QnA, Retrieve_Device, Web_Search)
    is_relevant: str
    iteration_count: int

    
workflow = StateGraph(GraphState)

# Add nodes
workflow.add_node("Router", router)
workflow.add_node("Retrieve_QnA", retrieve_context_q_n_a)
workflow.add_node("Retrieve_Device", retrieve_context_medical_device)
workflow.add_node("Web_Search", web_search)
workflow.add_node("Relevance_Checker", check_context_relevance)
workflow.add_node("Augment", build_prompt)
workflow.add_node("Generate", call_llm)

# Define edges
workflow.add_edge(START, "Router")
workflow.add_conditional_edges(
    "Router",
    route_decision,  # this function decides the path dynamically
    {
        "Retrieve_QnA": "Retrieve_QnA",
        "Retrieve_Device": "Retrieve_Device",
        "Web_Search": "Web_Search",
    }
)
workflow.add_edge("Retrieve_QnA", "Relevance_Checker")
workflow.add_edge("Retrieve_Device", "Relevance_Checker")
workflow.add_edge("Web_Search", "Relevance_Checker")
workflow.add_conditional_edges(
    "Relevance_Checker",
    relevance_decision,  # this function decides the path dynamically
    {
        "Yes": "Augment",
        "No": "Web_Search",
    }
)
workflow.add_edge("Augment", "Generate")
workflow.add_edge("Generate", END)


# Compile the dynamic RAG agent
agentic_rag = workflow.compile()


# ===================================
# ===  Visualize Workflow (Optional) ===
# ===================================


# === Run it ===
graph_path = os.path.join(os.getcwd(), "agentic_rag_graph.png")
graph_bytes = agentic_rag.get_graph().draw_mermaid_png()

with open(graph_path, "wb") as graph_file:
    graph_file.write(graph_bytes)

print(f"Workflow graph saved to {graph_path}")

try:
    from IPython.display import Image, display

    display(Image(graph_path))
except ImportError:
    pass


input_state = {"query": "What are the treatments for Kawasaki disease ?"}

from pprint import pprint
final_response = None
for step in agentic_rag.stream(input_state):
    for key, value in step.items():
        pprint(f"Finished running: {key}:")
        if "response" in value:
            final_response = value["response"]
            pprint(final_response)

if final_response:
    response_path = os.path.join(os.getcwd(), "agentic_rag_response.txt")
    with open(response_path, "w", encoding="utf-8") as response_file:
        response_file.write(final_response)
    print(f"Response saved to {response_path}")
else:
    print("No response generated to save.")




# input_state = {"query": "What are the usage of Dialysis Machine Device?"}

# from pprint import pprint
# for step in agentic_rag.stream(input_state):
#     for key, value in step.items():
#         pprint(f"Finished running: {key}:")
# pprint(value["response"])

# input_state = {"query": "What's the export duty on medical tablets on India by USA in 2025?"}

# from pprint import pprint
# for step in agentic_rag.stream(input_state):
#     for key, value in step.items():
#         pprint(f"Finished running: {key}:")
# pprint(value["response"])

# input_state = {"query": "What are medicines/treatment for COVID?"}

# from pprint import pprint
# for step in agentic_rag.stream(input_state):
#     for key, value in step.items():
#         pprint(f"Finished running: {key}:")
# pprint(value["response"])