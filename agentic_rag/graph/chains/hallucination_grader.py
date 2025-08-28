from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import AzureChatOpenAI
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())


llm = AzureChatOpenAI(
    api_version=os.getenv("api_version"),
    azure_endpoint=os.getenv("azure_endpoint"),
    api_key=os.getenv("api_key"),
    temperature=0.0
)

class GradeHallucination(BaseModel):
    binary_score: bool = Field(..., description="Answer is grounded in the facts, 'yes' or 'no'")
    # explanation: str = Field(..., description="Explanation of the grading decision")
    
structured_llm_grader = llm.with_structured_output(GradeHallucination)

system ="""You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts.

Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts.
Explain your choice."""

hallucination_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", "Set of facts: \n\n{documents}\n\n LLM answer: {answer}"),
])

hallucination_grader: RunnableSequence = hallucination_prompt | structured_llm_grader