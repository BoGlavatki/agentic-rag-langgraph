from dotenv import load_dotenv
import os
from langchain_openai import AzureChatOpenAI

from langchain_core.tools import tool, Tool
from langchain.agents.output_parsers import ReActSingleInputOutputParser

from langchain.prompts import PromptTemplate
from langchain_core.tools.render import render_text_description
from langchain_core.runnables import RunnablePassthrough
from textwrap import dedent
from typing import Union, List
from langchain.schema import AgentAction, AgentFinish
from callbacks import AgentCallbackHandler

load_dotenv()


@tool
def get_text_length(text: str) -> int:
    """
    Get the length of the input text.
    """
    return len(text)




if __name__ == "__main__":
    # Your main code here
    text = "Hello, LangChain!"
    tools = [get_text_length]
    
    template = dedent( """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:{agent_scratchpad}
    """)

    prompt = PromptTemplate(
        
        input_variables=["input", "agent_scratchpad", "tool_names", "tools"],
        template=template
    )
    
    llm = AzureChatOpenAI(
        azure_deployment="o4-mini",  # aus deinem Azure-Deployment
        api_version="2024-12-01-preview",
        api_key=os.getenv("api_key"),
        azure_endpoint=os.getenv("azure_endpoint"),
        callbacks=[AgentCallbackHandler()]
    ).bind(stop=["\nObservation:"])

    agent = RunnablePassthrough() | prompt | llm | ReActSingleInputOutputParser()
    intermediate_steps = []

    agent_step: Union[AgentAction, AgentFinish] = agent.invoke({"input": text, "agent_scratchpad": intermediate_steps,
        "tool_names": ", ".join(tool.name for tool in tools),
        "tools": render_text_description(tools)})
    print("AgentStep:", agent_step)

    def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
        for tool in tools:
            if tool.name == tool_name:
                return tool
        raise ValueError(f"Tool '{tool_name}' not found")

    if isinstance(agent_step, AgentAction):
        tool_name = agent_step.tool
        tool_to_use = find_tool_by_name(tools, tool_name)
        tool_input = agent_step.tool_input
        
        observation = tool_to_use.func(str(tool_input))
        intermediate_steps.append((agent_step, str(observation)))
        print("Intermediate Steps:", intermediate_steps)
        print(f"Tool '{tool_name}' executed with input '{tool_input}'. Observation: {observation}")