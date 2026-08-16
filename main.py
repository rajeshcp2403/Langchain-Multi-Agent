from src.tools.tools import web_search,scrape_url
from rich import print

from src.pipelines.pipeline import run_research_pipeline

topic = run_research_pipeline("The impact of artificial intelligence on the job market")


