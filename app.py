import re
from datetime import datetime

import streamlit as st
from src.pipelines.pipeline import run_research_pipeline

st.set_page_config(
    page_title="Research Intelligence Suite",
    page_icon="◆",
    layout="wide"
)

# ---------------------------------------------------------------------------
# THEME — "field briefing" dark mode
# Palette: ink background, warm parchment text (never gray-on-gray),
# amber accent for the signature agent rail, teal for secondary status.
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600;8..60,700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

    :root {
        --bg:        #0a0c12;
        --panel:     #12151f;
        --card:      #161a26;
        --card-hi:   #1b2030;
        --border:    #262c3d;
        --border-hi: #3a4058;
        --text:      #edeae1;
        --text-dim:  #9aa1b5;
        --text-faint:#5f6580;
        --amber:     #e0a63d;
        --amber-dim: #7a5f2c;
        --teal:      #5fd6c4;
    }

    html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

    .stApp { background: var(--bg); }
    .block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 900px; }

    header[data-testid="stHeader"] { background: transparent; }
    div[data-testid="stStatusWidget"] { display: none; }

    /* ---------- hero ---------- */
    .eyebrow {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--amber);
        margin-bottom: 0.5rem;
        display: flex; align-items: center; gap: 0.5rem;
    }
    .eyebrow::before {
        content: "";
        width: 7px; height: 7px;
        background: var(--amber);
        border-radius: 50%;
        box-shadow: 0 0 8px 2px rgba(224,166,61,0.6);
        display: inline-block;
    }
    .hero h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.3rem;
        font-weight: 700;
        color: var(--text);
        margin: 0 0 0.35rem 0;
        letter-spacing: -0.01em;
    }
    .hero-sub {
        color: var(--text-dim);
        font-size: 0.98rem;
        margin-bottom: 1.8rem;
        max-width: 560px;
        line-height: 1.5;
    }

    /* ---------- agent rail (signature element) ---------- */
    .rail-wrap {
        display: flex;
        justify-content: space-between;
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.3rem 1.6rem 1.1rem 1.6rem;
        margin-bottom: 1.4rem;
        position: relative;
    }
    .rail-node { flex: 1; text-align: center; position: relative; }
    .rail-node:not(:last-child)::after {
        content: "";
        position: absolute;
        top: 13px; right: -50%;
        width: 100%; height: 1px;
        background: repeating-linear-gradient(90deg, var(--border-hi) 0, var(--border-hi) 4px, transparent 4px, transparent 9px);
    }
    .rail-dot {
        width: 26px; height: 26px;
        margin: 0 auto 0.55rem auto;
        border-radius: 50%;
        background: var(--card-hi);
        border: 1.5px solid var(--amber);
        display: flex; align-items: center; justify-content: center;
        font-size: 0.85rem;
        color: var(--amber);
        box-shadow: 0 0 10px rgba(224,166,61,0.25);
        position: relative; z-index: 1;
        font-family: 'IBM Plex Mono', monospace;
    }
    .rail-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--text);
        font-weight: 600;
    }
    .rail-status {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.62rem;
        color: var(--teal);
        margin-top: 0.15rem;
        letter-spacing: 0.04em;
    }

    /* trace log inside expander */
    .trace-row {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.78rem;
        color: var(--text-dim);
        padding: 0.55rem 0;
        border-bottom: 1px dashed var(--border);
        display: flex; gap: 0.7rem;
    }
    .trace-row:last-child { border-bottom: none; }
    .trace-fn { color: var(--teal); }
    .trace-ok { color: var(--amber); margin-left: auto; }

    /* ---------- stat strip ---------- */
    .stat-strip {
        display: flex;
        gap: 0.9rem;
        margin-bottom: 1.6rem;
    }
    .stat-box {
        flex: 1;
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 0.85rem 1rem;
    }
    .stat-num {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: var(--amber);
        line-height: 1.1;
    }
    .stat-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.64rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--text-faint);
        margin-top: 0.3rem;
    }

    /* ---------- report document ---------- */
    .report-doc {
        background: var(--card);
        border: 1px solid var(--border);
        border-top: 3px solid var(--amber);
        border-radius: 4px 4px 14px 14px;
        padding: 2.3rem 2.5rem 2.6rem 2.5rem;
        box-shadow: 0 20px 50px rgba(0,0,0,0.35);
    }
    .doc-kicker {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--amber-dim);
        margin-bottom: 0.6rem;
    }
    .doc-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.7rem;
        font-weight: 700;
        color: var(--text);
        line-height: 1.3;
        margin-bottom: 0.4rem;
    }
    .doc-meta {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        color: var(--text-faint);
        margin-bottom: 1.6rem;
        padding-bottom: 1.4rem;
        border-bottom: 1px solid var(--border);
    }
    .doc-summary {
        font-family: 'Source Serif 4', serif;
        font-size: 1.08rem;
        line-height: 1.75;
        color: var(--text);
        background: var(--card-hi);
        border-left: 3px solid var(--teal);
        padding: 1.15rem 1.4rem;
        border-radius: 0 10px 10px 0;
        margin-bottom: 1.8rem;
        position: relative;
    }
    .doc-summary .tag {
        display: block;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--teal);
        margin-bottom: 0.5rem;
    }
    .doc-section-head {
        display: flex;
        align-items: baseline;
        gap: 0.6rem;
        margin-top: 1.9rem;
        margin-bottom: 0.7rem;
    }
    .doc-section-num {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.78rem;
        color: var(--amber);
        opacity: 0.8;
    }
    .doc-section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.08rem;
        font-weight: 700;
        color: var(--text);
    }
    .doc-body {
        font-family: 'Source Serif 4', serif;
        font-size: 1.02rem;
        line-height: 1.8;
        color: #cfcdc4;
    }

    /* ---------- sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: var(--panel);
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] * { color: var(--text) !important; }
    section[data-testid="stSidebar"] .eyebrow { color: var(--amber) !important; }
    section[data-testid="stSidebar"] textarea {
        background: var(--card) !important;
        border: 1px solid var(--border-hi) !important;
        border-radius: 10px !important;
        color: var(--text) !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.85rem !important;
    }
    section[data-testid="stSidebar"] textarea:focus {
        border-color: var(--amber) !important;
        box-shadow: 0 0 0 1px var(--amber) !important;
    }
    div[data-testid="stButton"] button {
        border-radius: 9px;
        font-weight: 700;
        font-family: 'IBM Plex Mono', monospace;
        letter-spacing: 0.04em;
        background: var(--amber);
        color: #1a1305 !important;
        border: none;
        padding: 0.6rem 1rem;
        box-shadow: 0 6px 18px rgba(224,166,61,0.25);
    }
    div[data-testid="stButton"] button:hover {
        background: #f0b955;
    }
    div[data-testid="stDownloadButton"] button {
        border-radius: 9px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.82rem;
        background: var(--card-hi);
        color: var(--teal) !important;
        border: 1px solid var(--border-hi);
    }
    div[data-testid="stExpander"] {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 12px;
    }
    div[data-testid="stExpander"] summary {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.8rem;
        color: var(--text-dim);
    }
    div[data-testid="stAlert"] {
        background: var(--card);
        border: 1px solid var(--border-hi);
        color: var(--text) !important;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------------
# TEXT HELPERS
# ---------------------------------------------------------------------------
def clean_text(text):
    if not text:
        return ""
    text = str(text).replace("\r\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def extract_sections(report_text):
    if not report_text:
        return []
    lines = [line.strip() for line in str(report_text).splitlines() if line.strip()]
    sections = []
    current_heading = "Overview"
    current_body = []

    def flush():
        if current_body:
            content = " ".join(current_body).strip()
            if content:
                sections.append({"heading": current_heading, "content": content})

    for line in lines:
        is_heading = (
            len(line) <= 80
            and not line.endswith((".", "!", "?"))
            and (" " not in line or len(line) < 50)
        ) or line.lower().startswith((
            "executive summary", "key findings", "analysis", "recommendations",
            "conclusion", "impact", "overview", "sources"
        ))

        if is_heading and len(line) < 100:
            flush()
            current_heading = line.strip(":")
            current_body = []
        else:
            current_body.append(line)

    flush()

    if not sections:
        sections.append({"heading": "Report", "content": report_text.strip()})

    return sections


def get_report_title(topic, state):
    report = state.get("report") if isinstance(state, dict) else ""
    if isinstance(report, str) and report.strip():
        first_line = report.strip().splitlines()[0].strip()
        if len(first_line) < 120:
            return first_line.strip("# ").strip()
    return f"Research Report: {topic}"


AGENT_META = {
    "Search Agent":  {"glyph": "S"},
    "Reader Agent":  {"glyph": "R"},
    "Writer Agent":  {"glyph": "W"},
    "Critic Agent":  {"glyph": "C"},
    "Research Workflow": {"glyph": "•"},
}


def build_steps(state):
    steps = []
    if isinstance(state, dict):
        if state.get("search_results"):
            steps.append({
                "label": "Search Agent",
                "function": "build_search_agent()",
                "tool": "web_search",
                "status": "Completed",
                "detail": "Collected relevant search results for the topic."
            })
        if state.get("scraped_content"):
            steps.append({
                "label": "Reader Agent",
                "function": "ReaderAgent.invoke()",
                "tool": "scrape_url",
                "status": "Completed",
                "detail": "Scraped and cleaned the most relevant source."
            })
        if state.get("report"):
            steps.append({
                "label": "Writer Agent",
                "function": "writer_chain.invoke()",
                "tool": "writer_chain",
                "status": "Completed",
                "detail": "Generated the final research report."
            })
        if state.get("critique"):
            steps.append({
                "label": "Critic Agent",
                "function": "critic_chain.invoke()",
                "tool": "critic_chain",
                "status": "Completed",
                "detail": "Reviewed the report for clarity and quality."
            })

    if not steps:
        steps = [{
            "label": "Research Workflow", "function": "run_research_pipeline()",
            "tool": "pipeline", "status": "Completed", "detail": "Pipeline executed successfully."
        }]
    return steps


# ---------------------------------------------------------------------------
# RENDER PIECES
# ---------------------------------------------------------------------------
def render_hero():
    st.markdown(
        """
        <div class="eyebrow">Multi-agent research pipeline</div>
        <div class="hero">
            <h1>Research Intelligence Suite</h1>
        </div>
        <div class="hero-sub">
            Enter a topic and a chain of specialist agents searches, reads,
            writes, and reviews a briefing for you — trace every step below.
        </div>
        """,
        unsafe_allow_html=True
    )


def render_rail(steps):
    html = '<div class="rail-wrap">'
    for step in steps:
        glyph = AGENT_META.get(step["label"], {}).get("glyph", "•")
        html += f"""
        <div class="rail-node">
            <div class="rail-dot">{glyph}</div>
            <div class="rail-label">{step['label'].replace(' Agent', '')}</div>
            <div class="rail-status">{step['status']}</div>
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_trace(steps):
    html = ""
    for step in steps:
        html += f"""
        <div class="trace-row">
            <span class="trace-fn">{step['function']}</span>
            <span>tool: {step['tool']}</span>
            <span class="trace-ok">✓ {step['status'].upper()}</span>
        </div>
        """
    st.markdown(html, unsafe_allow_html=True)


def render_stats(report_text, sections, steps, state):
    word_count = len(report_text.split()) if report_text else 0
    read_time = max(1, round(word_count / 200))
    section_count = max(len(sections) - 1, 0) or len(sections)
    sources = state.get("search_results") if isinstance(state, dict) else None
    source_count = len(sources) if isinstance(sources, (list, tuple)) else "—"

    stats = [
        (str(len(steps)), "Agents run"),
        (str(source_count), "Sources scanned"),
        (str(section_count), "Sections"),
        (f"{read_time} min", "Read time"),
    ]
    html = '<div class="stat-strip">'
    for num, label in stats:
        html += f"""<div class="stat-box">
                        <div class="stat-num">{num}</div>
                        <div class="stat-label">{label}</div>
                    </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_report(state, topic):
    report = state.get("report", "")
    title = get_report_title(topic, state)
    report_text = clean_text(report) if isinstance(report, str) else clean_text(str(report))
    steps = build_steps(state)

    render_hero()
    render_rail(steps)

    with st.expander("View full agent trace log"):
        render_trace(steps)

    if not report_text:
        st.info("The pipeline finished but returned no report content.")
        return

    sections = extract_sections(report_text)
    render_stats(report_text, sections, steps, state)

    timestamp = datetime.now().strftime("%d %b %Y · %H:%M")

    doc_html = f"""
    <div class="report-doc">
        <div class="doc-kicker">Briefing · {topic[:60]}</div>
        <div class="doc-title">{title}</div>
        <div class="doc-meta">GENERATED {timestamp.upper()} &nbsp;·&nbsp; {len(steps)} AGENTS &nbsp;·&nbsp; {len(report_text.split())} WORDS</div>
    """

    if sections:
        summary = sections[0]["content"]
        summary_display = summary[:1500] if len(summary) > 1500 else summary
        doc_html += f"""
        <div class="doc-summary">
            <span class="tag">Executive summary</span>
            {summary_display}
        </div>
        """
        for i, section in enumerate(sections[1:], start=1):
            doc_html += f"""
            <div class="doc-section-head">
                <span class="doc-section-num">{i:02d}</span>
                <span class="doc-section-title">{section['heading']}</span>
            </div>
            <div class="doc-body">{section['content']}</div>
            """
    else:
        doc_html += f'<div class="doc-body">{report_text}</div>'

    doc_html += "</div>"
    st.markdown(doc_html, unsafe_allow_html=True)

    st.download_button(
        "↓ Export briefing (Markdown)",
        data=report_text,
        file_name="research_briefing.md",
        mime="text/markdown"
    )


# ---------------------------------------------------------------------------
# LAYOUT
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="eyebrow">Console</div>', unsafe_allow_html=True)
    topic = st.text_area(
        "Research topic",
        value="The impact of artificial intelligence on the job market",
        height=120,
        label_visibility="collapsed"
    )
    generate = st.button("Run briefing ▸", type="primary", use_container_width=True)
    st.caption("The agent chain runs search → read → write → review on your topic.")

if generate:
    if not topic.strip():
        st.warning("Enter a research topic before running the briefing.")
    else:
        with st.spinner("Running search → read → write → review…"):
            try:
                state = run_research_pipeline(topic)
                render_report(state, topic)
                st.session_state["last_steps"] = build_steps(state)
            except Exception as e:
                st.error(f"Research failed: {e}")
else:
    render_hero()
    st.info("Enter a topic in the sidebar and select **Run briefing** to begin.")