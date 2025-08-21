import datetime

from dotenv import load_dotenv, find_dotenv
import os

from langchain_core.output_parsers.openai_tools import (JsonOutputToolsParser, PydanticToolsParser)

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from schemas import AnswerQuestionSchema, ReviseAnswerSchema

from langchain_openai import AzureChatOpenAI
load_dotenv(find_dotenv())
llm = AzureChatOpenAI(
    azure_deployment="o4-mini",  # aus deinem Azure-Deployment
    api_version="2024-12-01-preview",
    api_key=os.getenv("api_key"),
    azure_endpoint=os.getenv("azure_endpoint")
)
parser = JsonOutputToolsParser(return_id=True)
parser_pydantic = PydanticToolsParser(tools=[AnswerQuestionSchema])

actor_prompt_template = ChatPromptTemplate.from_messages(
    [( "system",
            """You are expert researcher.
Current time: {time}

1. {first_instruction}
2. Reflect and critique your answer. Be severe to maximize improvement.
3. Recommend search queries to research information and improve your answer.""",),
     
     MessagesPlaceholder(variable_name="messages"),
     ("system","Answer the user's question above using required format."), ]
).partial(time=datetime.datetime.now().isoformat())


first_responder_template = actor_prompt_template.partial(first_instruction="Provide a detailed 250 word answer")

first_responder = first_responder_template | llm.bind_tools(tools = [AnswerQuestionSchema], tool_choice="AnswerQuestionSchema")

reviser_instructions ="""Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words.
"""


revisor = actor_prompt_template.partial(first_instruction = reviser_instructions)| llm.bind_tools(tools = [ReviseAnswerSchema], tool_choice="ReviseAnswerSchema")   





if __name__ == "__main__":
  
    
    # Example usage
    question = "Write about AI-Powered SOC / autonomous SOC problem domain, list startups that do that and raised capital"
    messages = [HumanMessage(content=question)]

    chain = (first_responder_template | llm.bind_tools(tools=[AnswerQuestionSchema], tool_choice="AnswerQuestionSchema") | parser_pydantic)
    # Parse the response using the Pydantic parser
    parsed_response = chain.invoke({"messages": messages})

    print("Parsed Response:", parsed_response)