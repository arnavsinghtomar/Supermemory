from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import Dict, Any
import os


def generate(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a response based on the given context.
    
    Args:
        state: The current workflow state containing query and context
        
    Returns:
        Dict[str, Any]: Updated state with generated response
    """
    print("---GENERATING ANSWER---")
    
    # Get the context from memory or web data
    context = state.get("memory_data") or state.get("web_data", "")
    query = state.get("query", "")
    
    if not context:
        state["generation"] = "I couldn't find enough information to answer your question."
        return state
    
    try:
        # Create the prompt template
        prompt = ChatPromptTemplate.from_template("""
        You are a helpful AI assistant. Use the following context to answer the user's question.
        
        Context:
        {context}
        
        Question: {query}
        
        Answer:""")
        
        # Initialize the language model
        llm = ChatOpenAI(
            model="gpt-4o",  # Using GPT-4 by default
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7
        )
        
        # Create the chain
        chain = prompt | llm
        
        # Generate the response
        response = chain.invoke({
            "context": context,
            "query": query
        })
        
        # Update the state with the generated response
        state["generation"] = response.content
        print(f"Generated response: {response.content}")  # Print first 100 chars
        
    except Exception as e:
        error_msg = f"Error generating response: {str(e)}"
        print(error_msg)
        state["generation"] = "I encountered an error while generating a response. Please try again later."
    
    return state