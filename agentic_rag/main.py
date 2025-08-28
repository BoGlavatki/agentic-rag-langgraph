from dotenv import load_dotenv, find_dotenv
import os
from langchain_openai import AzureChatOpenAI
from agentic_rag.graph.graph import app


if __name__ == "__main__":
   print("HELLO RAG!")
   print(app.invoke(input={"question": "What is the agent memory?"}))