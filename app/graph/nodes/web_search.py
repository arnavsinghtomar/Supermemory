from utils.tavily_client import tavily_client
import os


def web_search(state):
    """
    Perform a web search and update the state with results.
    
    Args:
        state: The current workflow state
        
    Returns:
        dict: Updated state with web search results and flag
    """
    print("---RUNNING TAVILY SEARCH---")
    results = tavily_client.search(query=state["query"], max_results=3)
    docs = [r["content"] for r in results["results"]]
    state["web_data"] = "\n".join(docs)
    state["web_search_performed"] = True  # Set the flag
    print(state["web_data"])
    return state
