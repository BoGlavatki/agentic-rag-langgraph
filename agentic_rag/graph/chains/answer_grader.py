from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field
from langchain_openai import AzureChatOpenAI

class GradeAnswer(BaseModel):
    binary_score: bool = Field(..., description="Whether the answer is correct 'yes' or not 'no'")


llm = AzureChatOpenAI(
    api_version=os.getenv("api_version"),
    azure_endpoint=os.getenv("azure_endpoint"),
    api_key=os.getenv("api_key"),
    temperature=0.0
)
structured_llm_grader = llm.with_structured_output(GradeAnswer)

system ="""You are a grader assessing whether an answer addresses / resolves a question \n Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question."""

answer_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", "User question: \n\n {question} \n\n LLM answer: \n\n {answer}")
])

answer_grader: RunnablePassthrough = answer_prompt | structured_llm_grader
