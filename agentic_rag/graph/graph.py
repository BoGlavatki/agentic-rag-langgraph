from dotenv import find_dotenv, load_dotenv

from langgraph.graph import StateGraph, END
from agentic_rag.graph.chains.hallucination_grader import GradeHallucination, hallucination_grader
from agentic_rag.graph.chains.answer_grader import GradeAnswer, answer_grader
from agentic_rag.graph.consts import RETRIEVE, GRADE_DOCUMENTS, GENERATE, WEBSEARCH
from agentic_rag.graph.nodes import generate, grade_documents, web_search, retrieve_documents
from agentic_rag.graph.state import State

load_dotenv(find_dotenv())

def decide_to_generate(state: State):
    print("---ASSESS GRADED DOCUMENTS---")
    if state["web_search"]:
        print("---DECISION: WEBSEARCH---")
        return WEBSEARCH
    else:
        print("---DECISION: GENERATE---")
        return GENERATE


def grade_generation_grounded_in_documents_adn_question(state:State) -> str:
    print("---GRADE GENERATION---")
    documents = state["documents"]
    generation = state["generation"]
    question = state["question"]

    score = hallucination_grader.invoke({
        "documents": documents,
        "answer": generation,
    })
    if score.binary_score:
        print("--DECISION: GENERATION IS GROUNDED IN DOCUMENTS--")
        print("---GRADE GENERATION vs QUESTION---")
        score_answer = answer_grader.invoke({"question": question, "answer": generation,})
        if score_answer.binary_score:
            print("--DECISION: GENERATION ANSWERS THE QUESTION--")
            return "useful"
        else:
            print("--DECISION: GENERATION DOES NOT ANSWER THE QUESTION--")
            return "not useful"
    else:
        print("--DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS--")
        return "not supported"


workflow = StateGraph(State)

workflow.add_node(RETRIEVE, retrieve_documents)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)


workflow.set_entry_point(RETRIEVE)
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(GRADE_DOCUMENTS, decide_to_generate, {
    WEBSEARCH: WEBSEARCH,
    GENERATE: GENERATE
    }
)


workflow.add_conditional_edges(GENERATE, grade_generation_grounded_in_documents_adn_question, {
    "useful": END,
    "not useful": WEBSEARCH,
    "not supported": GENERATE
})


workflow.add_edge(WEBSEARCH, GENERATE)
workflow.add_edge(GENERATE, END)
app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="agentic_rag_graph.png")