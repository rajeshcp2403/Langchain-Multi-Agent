# Research Intelligence Suite

A multi-agent research assistant built with LangChain, Tavily, and Python to search, scrape, synthesize, and refine research into a polished report.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/LangChain-MultiAgent-000000?style=for-the-badge" alt="LangChain Multi-Agent" />
  <img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
</p>

## Overview

This project demonstrates a practical multi-agent AI workflow for research tasks. Instead of relying on a single model to do everything, the system splits responsibilities across specialized agents:

- Search Agent: finds recent and relevant sources
- Reader Agent: selects and scrapes a target page
- Writer Agent: drafts a structured research report
- Critic Agent: reviews the output for quality and clarity

The workflow is designed to mirror how a human research team operates: gather evidence, read deeper, write a report, and refine it.

## Why This Project

This project showcases:
- Agent-based orchestration with LangChain
- Tool calling and pipeline design
- Web search and content extraction
- AI-assisted report generation
- Clean presentation through a Streamlit interface
- Real-world patterns for building research automation systems

## Architecture

```text
User Query
   |
   v
Search Agent
   | --> Tavily Search API
   v
Reader Agent
   | --> URL selection + scraping
   v
Writer Agent
   | --> Research synthesis
   v
Critic Agent
   | --> Review + refinement
   v
Final Research Report
```

## Core Features

- Multi-agent research workflow
- Web-based source discovery using Tavily
- URL-level scraping and content extraction
- Clean text filtering and readability extraction
- Draft generation using LLM reasoning
- Critique and refinement cycle
- Professional Streamlit UI for report presentation

## Tech Stack

- Python
- LangChain
- Tavily API
- BeautifulSoup
- readability-lxml
- trafilatura
- Streamlit
- dotenv

## Project Structure

```text
langchain-multi-agent/
├── app.py
├── main.py
├── .env
├── requirements.txt
├── README.md
├── src/
│   ├── Agents/
│   │   └── agents.py
│   ├── pipelines/
│   │   └── pipeline.py
│   ├── tools/
│   │   └── tools.py
│   └── utils/
│       └── ...
└── venv/
```

## Setup

1. Clone the project
2. Create and activate a virtual environment

On Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies

```powershell
pip install -r requirements.txt
```

4. Create a `.env` file in the project root

```env
TAVILY_API_KEY=your_tavily_api_key
OPENAI_API_KEY=your_openai_api_key
```

## Run the Project

Run the pipeline directly:

```powershell
python main.py
```

Run the Streamlit app:

```powershell
streamlit run app.py
```

## Example Usage

```python
from src.pipelines.pipeline import run_research_pipeline

result = run_research_pipeline("The impact of artificial intelligence on the job market")
print(result)
```

## How It Works

The system starts with a user topic and performs a structured multi-step research workflow:

1. Search Agent queries the web for relevant sources.
2. Reader Agent selects the most relevant URL and extracts readable content.
3. Writer Agent uses the found research to draft a coherent report.
4. Critic Agent reviews the report and improves quality.

This creates an AI workflow that looks closer to an actual research team than a single prompt-driven pipeline.

## Current Challenges

Some websites enforce anti-bot protection and may reject automated requests with `403 Forbidden`. This is a common issue in research automation and is handled gracefully in the scraper layer with controlled error responses.

## Future Improvements

- Add caching for repeated search queries
- Support multiple source URLs per report
- Improve source-ranking logic
- Add PDF export
- Add structured citations and references
- Enhance UI with charts, summaries, and source cards

## License

This project is for educational and portfolio demonstration purposes.

## Contact

If you'd like to collaborate or discuss this project, feel free to connect.

---

Built to demonstrate a practical, production-style AI research workflow using LangChain and modern Python tooling.
