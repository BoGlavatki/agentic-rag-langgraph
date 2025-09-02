from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
from langchain.tools import StructuredTool
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain.agents import tool_calling_agent, AgentExecutor

from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
llm = AzureChatOpenAI(
    api_version=os.getenv("api_version"),
    azure_endpoint=os.getenv("azure_endpoint"),
    api_key=os.getenv("api_key"),
    temperature=0.0,
)


@tool
def greet(name: str) -> str:
    """Gibt einen Begrüßungstext für den angegebenen Namen zurück."""
    return f"Hallo, {name}!"


@tool
def farewell(name: str) -> str:
    """Gibt einen Abschiedstext für den angegebenen Namen zurück."""
    return f"Auf Wiedersehen, {name}!"


agent = tool_calling_agent(llm, tools=[greet, farewell])

agent_executor = AgentExecutor(
    agent, tools=[greet, farewell], verbose=True
)

system_prompt = "You are a helpful assistant. Take tool greet if you get Hello and put The Name inside and take tool farewell if you get Goodbye and put The Name inside."
