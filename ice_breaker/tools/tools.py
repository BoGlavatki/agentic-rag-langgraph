from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import Tool, tool


@tool
def get_profile_url_tavily(name: str):
    """Use Tavily to search for a LinkedIn profile URL."""
    search = TavilySearchResults()
    results = search.run(f"LinkedIn profile of {name}")

    return results
