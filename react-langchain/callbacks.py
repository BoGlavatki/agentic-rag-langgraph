from typing import Any
from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult

class AgentCallbackHandler(BaseCallbackHandler):
    """A callback handler for the agent that prints the agent steps."""

    def on_llm_start(self,
serialized: dict[str, Any],
prompts: list[str],
*,
run_id: UUID,
parent_run_id: UUID | None = None,
tags: list[str] | None = None,
metadata: dict[str, Any] | None = None,
**kwargs: Any,
) -> Any:
        print(f"**** Prompt to LLM was:****\n{prompts[0]}")
        print("*********")

    def on_llm_end(self, response: LLMResult,*, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: Any,
) -> Any:
        print(f"**** LLM response was:****\n{response.generations[0][0].text}")
        print("*********")