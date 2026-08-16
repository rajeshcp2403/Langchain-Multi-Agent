from src.tools.tools import web_search,scrape_url
from rich import print


# response = web_search.invoke("What is the capital of India?")

result = scrape_url.invoke(
    "https://www.britannica.com/place/New-Delhi"
)


print(result)
