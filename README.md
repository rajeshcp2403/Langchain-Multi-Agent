# Research Intelligence Suite

A multi-agent research assistant that uses LangChain, Tavily, Google Gemini, and Python to search the web, scrape useful content, synthesize findings, and review the final report.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/LangChain-Multi--Agent-000000?style=for-the-badge" alt="LangChain Multi-Agent" />
  <img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
</p>

## What This Project Does

Research Intelligence Suite is a multi-agent AI research tool. It accepts a topic, searches the web for relevant information, extracts useful content from a selected webpage, writes a structured research report, and reviews the report for quality.

The project is designed to show how separate AI agents can work together in one workflow instead of making a single model do everything.

## Overview

Research Intelligence Suite demonstrates a practical agent-based workflow for web research. Instead of asking one model to handle the whole task, the pipeline separates the work into focused steps:

- Search Agent finds recent and relevant web sources with Tavily.
- Reader Agent selects a useful source and extracts readable page content.
- Writer Agent drafts a structured research report from the gathered material.
- Critic Agent evaluates the report and gives specific feedback.

The result is a compact research workflow that mirrors a small research team: discover sources, inspect evidence, write clearly, and critique the output.

## Features

- Multi-agent orchestration with LangChain
- Web search through Tavily
- URL scraping with `requests`, `trafilatura`, `readability-lxml`, and BeautifulSoup
- Report generation with Google Gemini through `langchain-google-genai`
- Critique and scoring step for quality review
- Streamlit interface for running the full workflow from a browser
- CLI entry point for quickly testing the pipeline

## Skills Used

- Python programming
- LangChain agent creation
- Multi-agent workflow design
- Prompt engineering
- Google Gemini LLM integration
- Tavily API integration
- Web scraping and readable content extraction
- Streamlit web app development
- Environment variable management with `.env`
- Modular project structure
- Research report generation
- AI-based report review and evaluation

## Architecture

```text
User Topic
    |
    v
Search Agent
    |-- Tavily Search API
    v
Reader Agent
    |-- URL selection and scraping
    v
Writer Agent
    |-- Report synthesis
    v
Critic Agent
    |-- Review and feedback
    v
Final Research State
```

## Tech Stack

- Python
- LangChain
- Google Gemini
- Tavily API
- Streamlit
- BeautifulSoup
- readability-lxml
- trafilatura
- python-dotenv
- rich

## Project Structure

```text
Langchain-Multi-Agent/
|-- app.py
|-- main.py
|-- requirements.txt
|-- README.md
|-- LICENSE
|-- src/
|   |-- Agents/
|   |   |-- agents.py
|   |   `-- __init__.py
|   |-- pipelines/
|   |   |-- pipeline.py
|   |   `-- __init__.py
|   `-- tools/
|       |-- tools.py
|       `-- __init__.py
`-- venv/
```

## Installation Process

1. Clone the project and open the project directory.

2. Create and activate a virtual environment.

```powershell
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies.

```powershell
pip install -r requirements.txt
```

4. Create a `.env` file in the project root.

```env
TAVILY_API_KEY=your_tavily_api_key
GOOGLE_API_KEY=your_google_api_key
```

The project uses `ChatGoogleGenerativeAI`, so the Gemini key should be available as `GOOGLE_API_KEY`.

## Run

Run the Streamlit app:

```powershell
streamlit run app.py
```

Run the sample CLI pipeline:

```powershell
python main.py
```

`main.py` currently runs the pipeline with a built-in sample topic:

```python
"The impact of artificial intelligence on the job market"
```

## Example Usage

Use the pipeline directly from Python:

```python
from src.pipelines.pipeline import run_research_pipeline

state = run_research_pipeline("The impact of quantum computing on cryptography")

print(state["report"])
print(state["critique"])
```

The returned `state` dictionary contains:

- `search_results`
- `scraped_content`
- `report`
- `critique`

## How It Works

1. The user provides a research topic.
2. The Search Agent queries Tavily for relevant sources.
3. The Reader Agent chooses a source from the search results and scrapes readable content.
4. The Writer Agent combines search snippets and scraped content into a structured report.
5. The Critic Agent reviews the draft and returns a score, strengths, areas to improve, and a verdict.

## Notes

Some websites block automated scraping and may return `403 Forbidden`. The scraper handles these cases with controlled error messages so the pipeline can fail gracefully instead of crashing.

## Future Improvements

- Search and summarize multiple source URLs per report
- Add source ranking and deduplication
- Add structured citations and references
- Cache repeated search and scrape results
- Add PDF or Markdown export from the Streamlit UI
- Improve error handling and retry behavior
- Add tests for tools and pipeline orchestration

## License

This project is licensed under the terms in [LICENSE](LICENSE).

---

Built as a practical portfolio project for multi-agent research automation with LangChain and modern Python tooling.
