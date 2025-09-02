from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
from langchain.tools import StructuredTool
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel
from typing import Literal

output_parser = StrOutputParser()

from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())
llm = AzureChatOpenAI(
    api_version=os.getenv("api_version"),
    azure_endpoint=os.getenv("azure_endpoint"),
    streaming=True,
    api_key=os.getenv("api_key"),
    temperature=0.0,
)


class QuellenDto(BaseModel):
    name: str
    url: str
    chunk: str


class ResponseDto(BaseModel):
    event: Literal["chunk", "quellen"]
    data: str
    quelle: list[QuellenDto]

    def to_print(self):
        print(f"Event: {self.event}")
        print(f"Data: {self.data}")
        print("Quellen:")
        for quelle in self.quelle:
            print(f" - {quelle.name}: {quelle.url} ({quelle.chunk})")


class GreetingResponse(BaseModel):
    greeting: str


structured_output = llm.with_structured_output(GreetingResponse)


@tool
def greet(name: str) -> str:
    """Gibt einen Begrüßungstext für den angegebenen Namen zurück."""
    llm_response = structured_output.invoke(f"Generate a friendly greeting for {name}.")
    return {"response": llm_response.greeting}


@tool
def farewell(name: str) -> str:
    """Gibt einen Abschiedstext für den angegebenen Namen zurück."""
    return f"Auf Wiedersehen, {name}!"


@tool
def search_tool(query: str) -> list[QuellenDto]:
    """
    Searches for sources based on the given query and returns a list of QuellenDto objects.
    Dieses Tool soll nach einer Suchanfrage aufgerufen werden, um relevante Quellen bereitzustellen.
    Die Ergebnisse sind beispielhaft und enthalten Informationen wie Name, URL und Chunk der Quelle.
    Args:
        query (str): Die Suchanfrage, für die Quellen gefunden werden sollen.
    Returns:
        list[QuellenDto]: Eine Liste von QuellenDto-Objekten mit den gefundenen Quellen.
    """

    return [
        QuellenDto(name="example", url="https://www.example.com/ss/sx", chunk="Seite 3"),
        QuellenDto(
            name="Wikipedia", url="https://de.wikipedia.org/wiki/Sachsen", chunk="Intro"
        ),
    ]


system_prompt = """You are a helpful assistant.
Use the tool greet if the user says 'Hello'.
Use the tool farewell if the user says 'Goodbye'.
Use the tool search_tool if the user asks for search sources."""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(
    llm, tools=[greet, farewell, search_tool], prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=[greet, farewell, search_tool],
    verbose=True,
    output_parser=output_parser,
)


import asyncio


async def main():
    events = []
    async for event in agent_executor.astream_events(
        {"input": "Hello. I am Boleslav, please give me a search sources tool."},
        version="v1",
    ):
        events.append(event)
        # if "output" in event:
        #     parsed_output = output_parser.parse(event["output"])
        #     print("FINAL OUTPUT:", parsed_output)
        # else:
        #     print("CHUNK:", event, end="|")
    print("EVENTS (model_dump):")
    for event in events:
        if event["event"] == "on_tool_end":
            if event["name"] == "search_tool":
                tool_output = event["data"]["output"]
                print("\n\n")
                yield ResponseDto(
                    event="quellen",
                    data="Here are some sources I found:",
                    quelle=tool_output,
                ).to_print()
        # if event["event"] == "on_chat_model_start":
        #     print("\n\n")
        #     print("****")
        #     print(event)

    # async for chunk in llm.astream("Hello. tell me something nice about cats."):
    #     chunks.append(chunk)
    #     print(chunk.content, end="|")
    #     print("\n\n")

    # print("CHUNKS", chunks[0].content)


async def runner():
    async for response in main():
        print(response)


if __name__ == "__main__":
    asyncio.run(runner())
