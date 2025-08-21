from dotenv import load_dotenv, find_dotenv
import os

from langchain_openai import AzureChatOpenAI

from langchain_tavily import TavilySearch

from langchain_core.tools import StructuredTool

from langchain.agents import  AgentExecutor, StructuredChatAgent

from langgraph.prebuilt import ToolNode

from schemas import AnswerQuestionSchema, ReviseAnswerSchema
load_dotenv(find_dotenv())

tavily_tool = TavilySearch(max_results=5, api_key=os.getenv("TAVILY_API_KEY"))

def run_queries(search_queries: list[str], **kwargs):
    """Run the generated queries"""
    return tavily_tool.batch([{"query": query} for query in search_queries])

execute_tools = ToolNode([
    StructuredTool.from_function(run_queries, name=AnswerQuestionSchema.__name__,),
    StructuredTool.from_function(run_queries, name=ReviseAnswerSchema.__name__,)
])