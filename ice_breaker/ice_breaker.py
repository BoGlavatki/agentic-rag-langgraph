from langchain_openai import AzureChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
from linkedin import scrap_linkedin_profile

from agents.linkedin_lookup_agent import lookup
from output_parsers import summary_parser, Summary
from typing import Tuple


import os

load_dotenv()

chat = AzureChatOpenAI(
    azure_deployment="o4-mini",  # aus deinem Azure-Deployment
    api_version="2024-12-01-preview",
    api_key=os.getenv("api_key"),
    azure_endpoint=os.getenv("azure_endpoint"),
)


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_url = lookup(name=name)

    linkedin_data = scrap_linkedin_profile(linkedin_profile_url=linkedin_url, mock=True)

    summary_template = """
    given the LinkedIn information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    \n{format_instructions}
    """

    print("LinkedIn Data:", linkedin_data)

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    chain = summary_prompt_template | chat | summary_parser
    res: Summary = chain.invoke(input={"information": linkedin_data})
    print(res.summary)

    return res, linkedin_data["person"]


if __name__ == "__main__":
    ice_break_with("Harrison Chase")
