"""
Streamlit UI for the research pipeline.

Run with:
    streamlit run app.py

Assumes `src/Agents/agents.py` exposes:
    build_search_agent()  -> agent with .invoke({"messages": [...]}) -> {"messages": [...]}
    ReaderAgent()          -> agent with .invoke({"messages": [...]}) -> {"messages": [...]}
    writer_chain.invoke({"topic": ..., "research": ...}) -> str
    critic_chain.invoke({"report": ...}) -> str
"""

import streamlit as st
from src.Agents.agents import build_search_agent, ReaderAgent, writer_chain, critic_chain

st.set_page_config(page_title="Research Pipeline", page_icon="🔎", layout="wide")

# ---------- Session state ----------
if "state" not in st.session_state:
    st.session_state.state = {}
if "running" not in st.session_state:
    st.session_state.running = False


def run_pipeline(topic: str):
    """Runs the 4-step pipeline, updating the UI live as each step finishes."""
    state = {}

    # ---- Step 1: Search ----
    with st.status("Step 1 · Search agent is working...", expanded=True) as status:
        search_agent = build_search_agent()
        search_result = search_agent.invoke(
            {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]}
        )
        state["search_results"] = search_result["messages"][-1].content
        st.markdown(state["search_results"])
        status.update(label="Step 1 · Search complete", state="complete", expanded=False)

    # ---- Step 2: Reader / scraping ----
    with st.status("Step 2 · Reader agent is scraping the top resource...", expanded=True) as status:
        reader_agent = ReaderAgent()
        reader_result = reader_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Based on the following search results about '{topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{state['search_results'][:800]}",
                    )
                ]
            }
        )
        state["scraped_content"] = reader_result["messages"][-1].content
        st.markdown(state["scraped_content"])
        status.update(label="Step 2 · Scraping complete", state="complete", expanded=False)

    # ---- Step 3: Writer ----
    with st.status("Step 3 · Writer agent is drafting the report...", expanded=True) as status:
        combined_research = (
            f"Search Results (contains source URLs):\n{state['search_results']}\n\n"
            f"Scraped Detailed Content:\n{state['scraped_content']}"
        )
        report = writer_chain.invoke({"topic": topic, "research": combined_research})
        state["report"] = report
        st.markdown(report if isinstance(report, str) else str(report))
        status.update(label="Step 3 · Draft complete", state="complete", expanded=False)

    # ---- Step 4: Critic ----
    with st.status("Step 4 · Critic agent is reviewing the report...", expanded=True) as status:
        critique = critic_chain.invoke({"report": state["report"]})
        state["critique"] = critique
        st.markdown(critique if isinstance(critique, str) else str(critique))
        status.update(label="Step 4 · Review complete", state="complete", expanded=False)

    return state


# ---------- UI ----------
st.title("🔎 Research Pipeline")
st.caption("Search → Read → Draft → Critique, powered by your agent pipeline.")

with st.form("topic_form"):
    topic = st.text_input("Research topic", placeholder="e.g. Impact of quantum computing on cryptography")
    submitted = st.form_submit_button("Run pipeline", disabled=st.session_state.running)

if submitted:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        st.session_state.running = True
        try:
            st.session_state.state = run_pipeline(topic)
        except Exception as e:
            st.error(f"Pipeline failed: {e}")
        finally:
            st.session_state.running = False

# ---------- Results (persist after run, shown in tabs) ----------
state = st.session_state.state
if state:
    st.divider()
    st.subheader("Results")
    tab_search, tab_scrape, tab_report, tab_critique = st.tabs(
        ["🔍 Search Results", "📄 Scraped Content", "📝 Draft Report", "🧐 Critique"]
    )

    with tab_search:
        st.markdown(state.get("search_results", "—"))

    with tab_scrape:
        st.markdown(state.get("scraped_content", "—"))

    with tab_report:
        report = state.get("report", "—")
        st.markdown(report if isinstance(report, str) else str(report))
        if isinstance(report, str):
            st.download_button("Download report (.md)", report, file_name="report.md")

    with tab_critique:
        critique = state.get("critique", "—")
        st.markdown(critique if isinstance(critique, str) else str(critique))