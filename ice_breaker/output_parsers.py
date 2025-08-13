from typing import Any, Dict, List
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Summary(BaseModel):
    summary: str = Field(
        description="A short summary of the person's LinkedIn profile."
    )
    facts: List[str] = Field(description="Two interesting facts about the person.")

    def to_dict(self) -> Dict[str, Any]:
        return {"Summary": self.summary, "Facts": self.facts}


summary_parser = PydanticOutputParser(pydantic_object=Summary)
