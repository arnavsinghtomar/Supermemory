from langgraph.graph import StateGraph, END
import os
from chains.review_interrupt import review_or_interrupt
from dotenv import load_dotenv
load_dotenv()
from consts import *
from state import GraphState
from nodes.web_search import web_search
from nodes.generate import generate
from nodes.grade_document import grade_documents
from nodes.SuperMemory import memory_search
from nodes.SuperMemory import save_to_memory



def decide_to_generate(state):
    """
    Decide whether to generate a response or perform a web search.
    
    Args:
        state: The current workflow state
        
    Returns:
        str: The next node to transition to (WEB_SEARCH or GENERATE)
    """
    print("---ASSESS GRADED DOCUMENTS---")

    # Check if we need to do a web search
    if not state.get("memory_data"):
        print("---DECISION: NO MEMORY DATA FOUND, PERFORMING WEB SEARCH---")
        return WEB_SEARCH
    else:
        print("---DECISION: GENERATING RESPONSE FROM MEMORY---")
        return GENERATE




def route_decision(state):
    if state["memory_data"] != "":  # Check if memory_data is not empty
        print("✅ Found in SuperMemory → Generate")
        return GRADE_DOCUMENTS
    print("⚠️ Not in memory → Web Search")
    return WEB_SEARCH



workflow = StateGraph(GraphState)
workflow.add_node(MEMORY_SEARCH, memory_search)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(WEB_SEARCH, web_search)
workflow.add_node(GENERATE, generate)
workflow.add_node(SAVE, save_to_memory)
# entry point
workflow.set_entry_point(MEMORY_SEARCH)
workflow.add_conditional_edges(MEMORY_SEARCH, route_decision, {
    GRADE_DOCUMENTS: GRADE_DOCUMENTS,
    WEB_SEARCH: WEB_SEARCH
})
workflow.add_conditional_edges(GRADE_DOCUMENTS, decide_to_generate, {
    WEB_SEARCH: WEB_SEARCH,
    GENERATE: GENERATE,
})

workflow.add_edge(WEB_SEARCH,GENERATE)
workflow.add_edge(GENERATE,SAVE)
workflow.add_edge(SAVE,END)

app = workflow.compile()

if __name__ == "__main__":
    app.get_graph().draw_mermaid_png(output_file_path="graph.png")
    print("Graph visualization saved to graph.png")
    query = input("Enter your query: ")
    app.invoke({"query": query})