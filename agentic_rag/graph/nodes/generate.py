from typing import Any, Dict
from agentic_rag.graph.chains.generation import chain

from agentic_rag.graph.state import State

def generate(state: State) -> Dict[str, Any]:
    print("---Generate---")
    question = state["question"]
    documents = state["documents"]

    generation = chain.invoke({"context": documents, "question": question})
    return {"documents":documents, "question": question, "generation": generation}