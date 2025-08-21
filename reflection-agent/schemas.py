from typing import Any, Dict, List, Union

from pydantic import BaseModel, Field

class ReflectionAgentSchema(BaseModel):
    missing: str = Field(description="Critique of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous.")


class AnswerQuestionSchema(BaseModel):
    question: str = Field(description="Around 250 word detailed answer to the question.")
    context: ReflectionAgentSchema = Field(description="Your reflection on the initial answer.")
    search_queries: List[str] = Field(description="1-3  search queries for researching improvements to address the critique of your current answer.")


class ReviseAnswerSchema(AnswerQuestionSchema):

    references: List[str] = Field(description="References used to support the revised answer.")