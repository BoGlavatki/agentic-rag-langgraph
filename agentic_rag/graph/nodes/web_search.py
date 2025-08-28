from typing import Any, Dict
from langchain.schema import Document

from langchain_tavily import TavilySearch

from agentic_rag.graph.state import State

from dotenv import load_dotenv, find_dotenv 
load_dotenv(find_dotenv())

web_search_tool = TavilySearch(max_results=3)

def web_search(state: State) -> Dict[str, Any]:
    print("---Web Search---")
    query = state["question"]
    documents = state["documents"]
    results = web_search_tool.invoke({"query": query})

    print("---Results---:", results)

    results_answer = results["results"]
    for result in results_answer:
        print("Result:", result, "\n\n\n")


    joined_tavily_result = "\n".join(str(result_) for result_ in results_answer)

    print("Joined Result:\n", joined_tavily_result)

    web_documents = Document(page_content=joined_tavily_result)
    
    if documents is not None:
        documents.append(web_documents)
    else:
        documents = [web_documents]
    
    return {"query": query, "documents": documents}


    
    
    # return {"query": query, "results": results, "documents": documents}

if __name__ == "__main__":
    web_search(state={"question":"agent memory", "documents": None})