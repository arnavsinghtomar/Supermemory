
# from typing import TypedDict
# class GraphState(TypedDict):
    
#     query: str = ""
#     memory_data: str = ""
#     web_data: str = ""
#     generation: str = ""
#     web_search_performed: bool = False


from typing import TypedDict, List, Dict, Any
from datetime import datetime, timezone

class GraphState(TypedDict):
    # Current query/input
    query: str
    
    # Memory components
    memory_data: str
    web_data: str
    generation: str
    
    # State flags
    web_search_performed: bool
    
    # Short-term memory (last 5 messages)
    conversation_history: List[Dict[str, Any]]
    
class GraphStateWrapper:
    """Wrapper class to handle GraphState with methods."""
    
    def __init__(self, state: dict):
        self.state = state
        if 'conversation_history' not in self.state:
            self.state['conversation_history'] = []
    
    def __getitem__(self, key):
        return self.state[key]
    
    def __setitem__(self, key, value):
        self.state[key] = value
    
    def get(self, key, default=None):
        return self.state.get(key, default)
    
    def add_message(self, role: str, content: str) -> None:
        if 'conversation_history' not in self.state:
            self.state['conversation_history'] = []
        
        self.state['conversation_history'].append({
            'role': role,
            'content': content,
            'timestamp': datetime.now(timezone.utc).isoformat()  # Updated to use timezone-aware datetime
        })
        # Keep only the last 5 messages
        self.state['conversation_history'] = self.state['conversation_history'][-5:]

    def to_dict(self) -> dict:
        """Convert the wrapper to a dictionary."""
        return dict(self.state)
