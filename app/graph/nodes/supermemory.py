from utils.Supermemory_client import supermemory_client
import os
# 
def memory_search(state):
    print("---CHECKING SUPERMEMORY---")
    results = supermemory_client.search.memories(q=state["query"], limit=5)
    
    if results.results:
        print("\n".join([result.memory for result in results.results]))
    state["memory_data"] = "\n".join([result.memory for result in results.results]) 
    state["web_search_performed"] = False
    print(state["memory_data"])
    return state

def save_to_memory(state):
    print("---SAVING TO SUPERMEMORY---")
    saved_memory = supermemory_client.memories.add(
            content=state["generation"]
        )
    print(saved_memory)
    return state