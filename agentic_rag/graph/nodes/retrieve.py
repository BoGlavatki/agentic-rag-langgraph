from typing import Any, Dict

from agentic_rag.graph.state import State
from agentic_rag.ingestion import retriever

def retrieve_documents(state: State) -> Dict[str, Any]:
    query = state.get("question", "")
    results = retriever.invoke(query, k=3)
    
    print("QUESTION:RETRIEVER", state["question"])
    return {"documents": results, "question": query}