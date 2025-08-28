from langchain import hub
from langchain_core.output_parsers import StrOutputParser
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

prompt = hub.pull("rlm/rag-prompt")


chain = prompt | llm | StrOutputParser()

