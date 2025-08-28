from typing import Any, Dict
from agentic_rag.graph.state import State
from agentic_rag.graph.chains.retrieval_grader import GradeDocuments, retrieval_grader

def grade_documents(state: State) -> Dict[str, Any]:
    question = state["question"]
    docs = state["documents"]

    filtered_docs = []
    
    for doc in docs:
       score = retrieval_grader.invoke({"documents": doc.page_content, "user_question": question})
       if score.binary_grade == "yes":
           filtered_docs.append(doc)
       else:
           web_search = True  # Set flag to perform web search if any document is irrelevant
           continue

    return {"documents": filtered_docs, "question": question, "web_search": web_search}