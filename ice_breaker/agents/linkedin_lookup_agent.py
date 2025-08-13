import os

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.tools import Tool, tool
from langchain import hub

from langchain.agents import AgentExecutor, create_tool_calling_agent

from tools.tools import get_profile_url_tavily
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def lookup(name: str) -> str:
    """Lookup a person on LinkedIn and return their profile summary."""
    llm = AzureChatOpenAI(
        azure_deployment="o4-mini",  # aus deinem Azure-Deployment
        api_version="2024-12-01-preview",
        api_key=os.getenv("api_key"),
        azure_endpoint=os.getenv("azure_endpoint"),
    )

    system_prompt = (
        "You are a helpful assistant. Use the available tools when needed. "
        "Return only the final answer."
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    template = (
        "Given the full name {name_of_person}, return only a direct URL "
        "to the person's LinkedIn profile page."
    )
    user_prompt = PromptTemplate(input_variables=["name_of_person"], template=template)
    # Create a tool for the agent

    # react_prompt = hub.pull("hwchase17/react")
    tools_for_agent = [get_profile_url_tavily]

    agent = create_tool_calling_agent(llm=llm, tools=tools_for_agent, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": user_prompt.format(name_of_person=name)}
    )
    linkedin_profile_url = result["output"]

    return linkedin_profile_url


if __name__ == "__main__":
    linkedin_url = lookup(name="Eden Marco udemy")
    print("LINKEDIN URL:", linkedin_url)
