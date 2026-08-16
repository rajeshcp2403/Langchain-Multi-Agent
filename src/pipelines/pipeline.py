from src.Agents.agents import build_search_agent, ReaderAgent, writer_chain, critic_chain

def run_research_pipeline(topic: str) -> dict:

    state = {}

    # step 1 - search agent working
    print("\n"+" ="*50)
    print("step 1 - search agent is working ...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = search_result['messages'][-1].content

    print("\n search result ", state['search_results'])

    # step 2 - reader agent scraping
    print("\n"+" ="*50)
    print("step 2 - reader agent is scraping top resources ...")
    print("="*50)

    reader_agent = ReaderAgent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })
    state['scraped_content'] = reader_result['messages'][-1].content

    print("\n scraped content ", state['scraped_content'])

    # step 3 - writer chain generating the report
    print("\n"+" ="*50)
    print("step 3 - writer agent is drafting the report ...")
    print("="*50)

    combined_research = (
        f"Search Results (contains source URLs):\n{state['search_results']}\n\n"
        f"Scraped Detailed Content:\n{state['scraped_content']}"
    )

    report = writer_chain.invoke({
        "topic": topic,
        "research": combined_research
    })
    state['report'] = report

    print("\n draft report:\n", state['report'])



    print("\n"+" ="*50)
    print("step 4 - critic agent is reviewing the report ...")
    print("="*50)

    critique = critic_chain.invoke({
        "report": state['report']
    })
    state['critique'] = critique

    print("\n critique:\n", state['critique'])

    return state
