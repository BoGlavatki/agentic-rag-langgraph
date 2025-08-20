from langchain import hub
from dotenv import load_dotenv
import os
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain.tools import Tool
from langchain_experimental.agents import create_csv_agent


def main():
    print("Starting the agentic RAG LangGraph...")
    load_dotenv()
    
    instructions = """You are an agent designed to write and execute python code to answer questions.
    You have access to a python REPL, which you can use to execute python code.
    If you get an error, debug your code and try again.
    Only use the output of your code to answer the question. 
    You might know the answer without running any code, but you should still run the code to get the answer.
    If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
    """
    
    base_prompt = hub.pull("langchain-ai/react-agent-template")
    tools = [PythonREPLTool()]
    prompt = base_prompt.partial(
    instructions=instructions,
    tools="\n".join([tool.name for tool in tools]),
    tool_names=", ".join([tool.name for tool in tools])
)
    
  
    
    llm = AzureChatOpenAI(
        azure_deployment="o4-mini",  # aus deinem Azure-Deployment
        api_version="2024-12-01-preview",
        api_key=os.getenv("api_key"),
        azure_endpoint=os.getenv("azure_endpoint"),
    )
    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
        
    )

    # agent that generates code to create QR codes
    python_agent_executor = AgentExecutor(agent=agent, verbose=True, tools=tools)
    
    # python_agent_executor.invoke(
    #     input={
    #         "input": """generate and save in current working directory 15 QR codes in PNG format in newfolder named 'qrcodes'
    #                             that point to www.udemy.com/course/langchain, you have qrcode package installed already""",
    #                                 "agent_scratchpad": ""
    #     }
    # )

    s = "generate and save in current working directory 15 QR codes in PNG format in newfolder named 'qrcodes' that point to www.udemy.com/course/langchain, you have qrcode package installed already"

    csv_agent = create_csv_agent(llm=llm,
                                 path="episode_info.csv",
                                 verbose=True,
                                 allow_oversized=True,
                                 allow_dangerous_code=True)
    # csv_agent.run("how many columns are there in file episode_info.csv?")
    def python_agent_tool(input: str) -> str:
        return python_agent_executor.invoke({"input": input, "agent_scratchpad": ""})
    
    tools = [
        Tool(
            name= "Python_Agent",
            func=python_agent_tool,
            description="""useful when you need to transform natural language to python code and execute the code., 
            returnig the results of the code execution
            DOES NOT ACCEPT CODE AS INPUT"""
        ),
        Tool(
            name="CSV_Agent",
            func=csv_agent.invoke,
            description="""useful when you need to interact with CSV files,
            allowing you to query and manipulate CSV data in episode_info.csv
            take an input the entire question and returns the answer after running pandas calculations"""
        )
    ]
    
    
    prompt = base_prompt.partial(instructions="",
                                 tools="\n".join([tool.name for tool in tools]),
                                 tool_names=", ".join([tool.name for tool in tools])
    )

    router_agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )
    
    router_agent_executor = AgentExecutor(agent=router_agent, verbose=True, tools=tools)

    router_agent_executor.invoke(
        input={
            "input":  s,
            "agent_scratchpad": ""
        }
    )


if __name__ == "__main__":
    main()