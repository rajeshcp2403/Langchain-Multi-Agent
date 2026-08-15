from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os
from tavily import TavilyClient

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(query: str) -> str:
    """
    Perform a web search using the Tavily API.

    Args:
        query (str): The search query.

    Returns:
        str: The search results.
    """
    results = tavily.search(query=query,max_results=5)
    out = []
    for result in results:
        out.append(f"Title: {result['title']}\nURL: {result['url']}\nSnippet: {result['content'][:300]}\n")
        return "\n".join(out)