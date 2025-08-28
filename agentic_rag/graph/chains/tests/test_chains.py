from dotenv import load_dotenv, find_dotenv
import pprint

load_dotenv(find_dotenv())

from graph.chains.retrieval_grader import GradeDocuments, retrieval_grader

from graph.chains.hallucination_grader import GradeHallucination, hallucination_grader
from ingestion import retriever
from graph.chains.generation import chain

# def test_retrieval_grader_answer_yes():
#     question = "what is retrieval?"
    
#     docs = retriever.invoke(question, k=3)
#     doc_txt = docs[0].page_content
    
#     res: GradeDocuments = retrieval_grader.invoke({"documents": doc_txt, "user_question": question})
#     assert res.binary_grade == "yes"
    
# def test_retrieval_grader_answer_no():
#     question = "how to make pizza?"
    
#     docs = retriever.invoke(question, k=3)
#     doc_txt = docs[0].page_content
    
#     res: GradeDocuments = retrieval_grader.invoke({"documents": doc_txt, "user_question": question})
#     assert res.binary_grade == "no"
    
    
# def test_generation_chain() -> None:
#     question = "Agent memory"
#     docs = retriever.invoke(question, k=3)

#     generation = chain.invoke({ "context": docs,           # statt "documents"
#     "question": question})
    
#     pprint.pprint(generation)


def test_hallucination_grader_answer_yes() -> None:
    question = "Agent memory"
    docs = retriever.invoke(question, k=3)

    generation = chain.invoke({ "context": docs,           # statt "documents"
    "question": question})

    res: GradeHallucination = hallucination_grader.invoke({
        "documents": docs,
        "answer": generation
    })

    print("Vor Print: binary_score:", res.binary_score)
    print("Docs:", docs)
    print("Generation:", generation)
    print("Grader result:", res)
    print("Nach Print: binary_score:", res.binary_score)

    assert res.binary_score
    
def test_hallucination_grader_answer_no() -> None:
    question = "Agent memory"
    docs = retriever.invoke(question, k=3)

    # generation = chain.invoke({ "context": docs,           # statt "documents"
    # "question": question})

    res: GradeHallucination = hallucination_grader.invoke({
        "documents": docs,
        "answer": "Pizza .... "
    })
    


    assert not res.binary_score