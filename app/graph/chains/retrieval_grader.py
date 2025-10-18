from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

# Use relative import for GraphState
from state import GraphState

load_dotenv()

llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")


class Grade_SuperMemory_Retrieval(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )




structured_llm_grader = llm.with_structured_output(Grade_SuperMemory_Retrieval)

system = """You are a grader assessing relevance of a retrieved memory_data to a user question. \n 
    If the memory_data contains keyword(s) or semantic meaning related to the query, grade it as relevant. \n
    Give a binary score 'yes' or 'no' score to indicate whether the memory_data is relevant to the question."""
grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Memory data: \n\n {memory_data}\n\n User query: {query}"),
    ]
)

retrieval_grader = grade_prompt | structured_llm_grader