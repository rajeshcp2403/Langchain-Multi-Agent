from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """
    Perform a web search using the Tavily API.

    Args:
        query (str): The search query.

    Returns:
        str: The search results.
    """
    response = tavily.search(query=query, max_results=5)
    results = response.get("results", [])  # pull the actual list out

    out = []
    for result in results:
        out.append(
            f"Title: {result['title']}\nURL: {result['url']}\nSnippet: {result['content'][:300]}\n"
        )
    return "\n".join(out)



@tool
def scrape_url(url: str) -> str:
    """
    Scrape and extract the main readable content from a webpage URL.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        str: The cleaned main text content of the page.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 403:
            return f"Error scraping {url}: 403 Client Error: Forbidden. The site is blocking automated requests."
        response.raise_for_status()
        html = response.text

        extracted = trafilatura.extract(
            html,
            include_tables=False,
            include_comments=False,
            include_links=False
        )
        if extracted and len(extracted.strip()) > 200:
            text = extracted
            text = re.sub(r'\[\d+\]', '', text)
            text = re.sub(r'\n\s*\n', '\n\n', text)
            text = re.sub(r'[ \t]+', ' ', text)
            return text.strip()[:3000]

        doc = Document(html)
        summary_html = doc.summary()
        soup = BeautifulSoup(summary_html, "lxml")

        for table in soup.find_all("table"):
            table.decompose()

        text = soup.get_text(separator="\n")
        if text and len(text.strip()) > 200:
            text = re.sub(r'\[\d+\]', '', text)
            text = re.sub(r'\n\s*\n', '\n\n', text)
            text = re.sub(r'[ \t]+', ' ', text)
            return text.strip()[:3000]

        soup = BeautifulSoup(html, "lxml")
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        text = "\n".join(paragraphs)
        if text:
            text = re.sub(r'\[\d+\]', '', text)
            text = re.sub(r'\n\s*\n', '\n\n', text)
            text = re.sub(r'[ \t]+', ' ', text)
            return text.strip()[:3000]

        return "No content could be extracted."

    except Exception as e:
        return f"Error scraping {url}: {str(e)}"