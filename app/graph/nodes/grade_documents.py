from typing import Any, Dict

from chains.SuperMemory_retrieval_grader import retrieval_grader
from state import GraphState


def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """

    print("---CHECK MEMORY DATA RELEVANCE TO QUERY---")
    query = state["query"]
    memory_data = state["memory_data"]

    
    
    web_search = False


    score = retrieval_grader.invoke(
        {"query": query, "memory_data": memory_data}
    )
    grade = score.binary_score
    if grade.lower() == "yes":
        print("---GRADE: DOCUMENT RELEVANT---")
        memory_data = memory_data
    else:
        print("---GRADE: DOCUMENT NOT RELEVANT---")
        memory_data = ""
    web_search = True
            
    return {"memory_data": memory_data, "query": query, "web_search": web_search}