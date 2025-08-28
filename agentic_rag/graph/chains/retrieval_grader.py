from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import AzureChatOpenAI

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os

llm = AzureChatOpenAI(
    
    api_version=os.getenv("api_version"),
    azure_endpoint=os.getenv("azure_endpoint"),
    api_key=os.getenv("api_key"),
    temperature=0.0
)


class GradeDocuments(BaseModel):
    binary_grade: str = Field(..., description="Documents are relevant to the question, 'yes' or 'no'")    
    
structured_llm_grader = llm.with_structured_output(GradeDocuments)


system = """You are a grader assessing relevance of a retrieved document to a user question. 
 
    It does not need to be a stringent test. The goal is to filter out erroneous retrievals. 

    If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. 

    Give a binary score  'yes' or 'no' score to indicate whether the document is relevant to the question."""

grade_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", "Retrieving document: \n\n{documents}\n\n User question: {user_question}"),
])

retrieval_grader = grade_prompt | structured_llm_grader