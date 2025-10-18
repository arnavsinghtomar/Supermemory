import streamlit as st
import os
import sys
from pathlib import Path
import io
from contextlib import redirect_stdout

# Add the project root and graph directory to the Python path
project_root = str(Path(__file__).parent.parent)
graph_dir = str(Path(__file__).parent / "graph")

for path in [project_root, graph_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Import after setting up the path
try:
    from graph.main_graph import app as workflow_app
    from graph.state import GraphState
except ImportError as e:
    st.error(f"Failed to import required modules: {e}")
    st.stop()

# Set page config
st.set_page_config(
    page_title="Personalize Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        max-width: 1000px;
        padding: 2rem;
    }
    .stTextArea textarea {
        min-height: 150px;
    }
    .stButton>button {
        width: 100%;
        padding: 0.5rem;
        font-weight: bold;
    }
    .stCodeBlock {
        max-height: 400px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🤖 Personalize Agent")
    st.caption("A smart assistant with memory and web search capabilities")
    
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Show a loading spinner while processing
            with st.spinner("Thinking..."):
                try:
                    # Capture logs
                    log_stream = io.StringIO()
                    with redirect_stdout(log_stream):
                        # Initialize state as a dictionary
                        state = {
                            "query": prompt,
                            "memory_data": "",
                            "web_data": "",
                            "generation": "",
                            "graded": False,
                            "web_search_performed": False,
                            "messages": st.session_state.messages
                        }
                        
                        # Run the workflow
                        result = workflow_app.invoke(state)
                        
                        # Get the generated response
                        response = result.get("generation", "I couldn't generate a response.")
                        
                        # Stream the response
                        for chunk in response.split():
                            full_response += chunk + " "
                            message_placeholder.markdown(full_response + "▌")
                            
                        message_placeholder.markdown(full_response)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                        
                        # Show logs in expander
                        with st.expander("View execution details"):
                            st.subheader("🔍 Execution Logs")
                            st.code(log_stream.getvalue(), language="bash")
                            
                            # Show full state
                            st.subheader("📊 Workflow State")
                            st.json({
                                k: v for k, v in result.items() 
                                if k not in ["memory_data", "web_data"]  # Skip large data
                            })
                            
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()
