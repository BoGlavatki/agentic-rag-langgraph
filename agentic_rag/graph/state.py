from typing import List, TypedDict

class State(TypedDict):

    question: str
    generation: str
    web_search: bool
    documents: List[str]