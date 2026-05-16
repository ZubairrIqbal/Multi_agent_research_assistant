import streamlit as st
import time
from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Outfit:wght@600;700;800;900&display=swap');

/* ═══════════════════════════════════════════
   DESIGN TOKENS
═══════════════════════════════════════════ */
:root {
  --bg-base:       #060d18;
  --bg-surface:    #0c1829;
  --bg-elevated:   #111f35;

  --border-subtle: rgba(255,255,255,0.07);
  --border-mid:    rgba(255,255,255,0.12);
  --border-cyan:   rgba(56,189,248,0.30);
  --border-green:  rgba(34,211,107,0.28);

  --cyan:   #38bdf8;
  --purple: #a78bfa;
  --green:  #22d36b;

  --text-hi:  #f1f7ff;
  --text-mid: #8fa4c0;
  --text-lo:  #4d6380;

  --r-sm: 10px;
  --r-md: 16px;
  --r-lg: 22px;
  --r-xl: 28px;
}

/* ── base ── */
html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
  color: var(--text-hi);
}
.stApp {
  background-color: var(--bg-base);
  background-image:
    radial-gradient(ellipse 80% 50% at 10% 0%,  rgba(56,189,248,0.09)  0%, transparent 55%),
    radial-gradient(ellipse 60% 50% at 90% 100%, rgba(167,139,250,0.08) 0%, transparent 55%);
  min-height: 100vh;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 3rem 5rem; max-width: 1280px; margin: 0 auto; }

/* ═══════════════════════════════════════════
   HERO
═══════════════════════════════════════════ */
.hero { text-align: center; padding: 4rem 0 3rem; }
.hero-badge {
  display: inline-flex; align-items: center; gap: 0.5rem;
  background: rgba(56,189,248,0.08);
  border: 1px solid rgba(56,189,248,0.22);
  border-radius: 100px;
  padding: 0.35rem 1.1rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.67rem; font-weight: 500;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--cyan); margin-bottom: 1.6rem;
}
.hero-badge::before {
  content: ''; width: 6px; height: 6px; border-radius: 50%;
  background: var(--cyan);
  animation: pdot 2s ease-in-out infinite;
}
@keyframes pdot { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.4;transform:scale(.7)} }

.hero h1 {
  font-family: 'Outfit', sans-serif;
  font-size: clamp(3rem, 6.5vw, 5.5rem);
  font-weight: 900; line-height: .95;
  letter-spacing: -.04em; color: var(--text-hi);
  margin: 0 0 1.2rem;
}
.hero h1 .grad {
  background: linear-gradient(135deg, #38bdf8 0%, #a78bfa 55%, #22d36b 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-sub { font-size:1.05rem; font-weight:400; color:var(--text-mid); max-width:500px; margin:0 auto; line-height:1.7; }

/* ── rule ── */
.rule { height:1px; background:linear-gradient(90deg,transparent,rgba(56,189,248,.22),rgba(167,139,250,.18),transparent); margin:2.5rem 0; }

/* ═══════════════════════════════════════════
   INPUT CARD
═══════════════════════════════════════════ */
.input-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-cyan);
  border-radius: var(--r-xl);
  padding: 2rem 2.2rem;
  margin-bottom: 1.4rem;
  box-shadow: 0 8px 32px rgba(0,0,0,.45), 0 0 40px rgba(56,189,248,.08);
  position: relative; overflow: hidden;
}
.input-card::before {
  content:''; position:absolute; top:0;left:0;right:0; height:1px;
  background:linear-gradient(90deg,transparent,var(--cyan),transparent); opacity:.5;
}

/* ═══════════════════════════════════════════
   TEXT INPUT  — THE KEY FIX
   We target every selector Streamlit uses so
   the background is always the dark token and
   text is always near-white.
═══════════════════════════════════════════ */
.stTextInput input,
.stTextInput > div > div > input,
div[data-testid="stTextInput"] input,
[data-baseweb="input"] input {
  background-color: #091422 !important;
  background:       #091422 !important;
  border: 1.5px solid rgba(56,189,248,.28) !important;
  border-radius: var(--r-sm) !important;
  color: #f1f7ff !important;
  -webkit-text-fill-color: #f1f7ff !important;  /* stops Streamlit autofill overriding color */
  caret-color: var(--cyan) !important;
  font-family: 'Inter', sans-serif !important;
  font-size: .975rem !important;
  font-weight: 400 !important;
  padding: .85rem 1.1rem !important;
  transition: border-color .2s, box-shadow .2s !important;
  outline: none !important;
}
.stTextInput input::placeholder,
.stTextInput > div > div > input::placeholder,
div[data-testid="stTextInput"] input::placeholder {
  color: #4d6380 !important;
  -webkit-text-fill-color: #4d6380 !important;
  opacity: 1 !important;
}
.stTextInput input:focus,
.stTextInput > div > div > input:focus,
div[data-testid="stTextInput"] input:focus {
  background-color: #0d1e35 !important;
  background:       #0d1e35 !important;
  border-color: var(--cyan) !important;
  box-shadow: 0 0 0 3px rgba(56,189,248,.15), 0 0 20px rgba(56,189,248,.07) !important;
  color: #f1f7ff !important;
  -webkit-text-fill-color: #f1f7ff !important;
}

/* Also override the BaseWeb/Streamlit wrapper background */
[data-baseweb="input"],
[data-baseweb="base-input"] {
  background: #091422 !important;
  background-color: #091422 !important;
}

.stTextInput > label,
div[data-testid="stTextInput"] label {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: .70rem !important; font-weight: 500 !important;
  letter-spacing: .18em !important; text-transform: uppercase !important;
  color: var(--cyan) !important; margin-bottom: .5rem !important;
}

/* ═══════════════════════════════════════════
   RUN BUTTON
═══════════════════════════════════════════ */
.stButton > button {
  background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #a78bfa 100%) !important;
  color: #fff !important;
  font-family: 'Outfit', sans-serif !important;
  font-weight: 700 !important; font-size: .95rem !important;
  letter-spacing: .03em !important;
  border: none !important; border-radius: var(--r-sm) !important;
  padding: .85rem 2rem !important; cursor: pointer !important;
  width: 100% !important;
  transition: all .2s ease !important;
  box-shadow: 0 4px 20px rgba(56,189,248,.25), 0 1px 3px rgba(0,0,0,.3) !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(56,189,248,.35) !important;
  filter: brightness(1.08) !important;
}
.stButton > button:active { transform: translateY(0) !important; filter: brightness(.96) !important; }

/* ═══════════════════════════════════════════
   CHIPS
═══════════════════════════════════════════ */
.chip-row { display:flex; flex-wrap:wrap; align-items:center; gap:.5rem; margin-bottom:1.5rem; }
.chip-label { font-family:'JetBrains Mono',monospace; font-size:.64rem; letter-spacing:.18em; color:var(--text-lo); text-transform:uppercase; }
.chip {
  background:rgba(255,255,255,.04); border:1px solid var(--border-mid);
  border-radius:8px; padding:.3rem .75rem;
  font-size:.77rem; font-weight:400; color:var(--text-mid);
  cursor:default; transition:all .15s;
}

/* ═══════════════════════════════════════════
   SECTION HEADING
═══════════════════════════════════════════ */
.section-heading {
  font-family:'Outfit',sans-serif; font-size:1.05rem; font-weight:700;
  color:var(--text-hi); letter-spacing:-.01em; margin:.5rem 0 1.2rem;
  display:flex; align-items:center; gap:.6rem;
}
.section-heading::after { content:''; flex:1; height:1px; background:var(--border-subtle); margin-left:.4rem; }

/* ═══════════════════════════════════════════
   PIPELINE STEP CARDS
═══════════════════════════════════════════ */
.step-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--r-md);
  padding: 1.1rem 1.4rem; margin-bottom:.8rem;
  position:relative; overflow:hidden;
  transition: border-color .25s, background .25s;
}
.step-card::before {
  content:''; position:absolute; left:0;top:0;bottom:0; width:3px;
  background:var(--border-subtle); border-radius:4px 0 0 4px; transition:background .3s;
}
.step-card.active { background:rgba(56,189,248,.06); border-color:rgba(56,189,248,.35); }
.step-card.active::before { background:var(--cyan); }
.step-card.done   { background:rgba(34,211,107,.05); border-color:rgba(34,211,107,.25); }
.step-card.done::before   { background:var(--green); }

.step-header { display:flex; align-items:center; gap:.7rem; }
.step-num {
  font-family:'JetBrains Mono',monospace; font-size:.62rem; font-weight:500;
  letter-spacing:.12em; color:var(--text-lo);
  background:rgba(255,255,255,.05); padding:.15rem .45rem; border-radius:4px;
}
.step-card.active .step-num { color:var(--cyan);  background:rgba(56,189,248,.10); }
.step-card.done   .step-num { color:var(--green); background:rgba(34,211,107,.10); }
.step-title { font-size:.9rem; font-weight:600; color:var(--text-hi); }
.step-desc  { font-size:.77rem; color:var(--text-lo); margin-top:.25rem; padding-left:calc(.7rem + 2.4rem); }
.step-status {
  margin-left:auto;
  font-family:'JetBrains Mono',monospace; font-size:.62rem; letter-spacing:.1em; font-weight:500;
  padding:.15rem .6rem; border-radius:100px;
}
.status-waiting { color:var(--text-lo);  background:rgba(255,255,255,.04); border:1px solid var(--border-subtle); }
.status-running { color:var(--cyan);     background:rgba(56,189,248,.10);  border:1px solid rgba(56,189,248,.25); animation:blink 1.4s ease-in-out infinite; }
.status-done    { color:var(--green);    background:rgba(34,211,107,.10);  border:1px solid rgba(34,211,107,.25); }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.45} }

/* ═══════════════════════════════════════════
   EXPANDER
═══════════════════════════════════════════ */
details { background:var(--bg-surface)!important; border:1px solid var(--border-subtle)!important; border-radius:var(--r-md)!important; padding:.2rem .8rem!important; margin-bottom:.8rem!important; }
details summary { font-family:'JetBrains Mono',monospace!important; font-size:.72rem!important; color:var(--text-mid)!important; letter-spacing:.08em!important; cursor:pointer!important; padding:.6rem 0!important; }

/* ═══════════════════════════════════════════
   RAW RESULT PANELS
═══════════════════════════════════════════ */
.result-panel {
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--r-md);
  padding: 1.5rem 1.8rem; margin:.5rem 0 1rem;
}
.result-panel-title {
  font-family:'JetBrains Mono',monospace; font-size:.64rem; font-weight:500;
  letter-spacing:.22em; text-transform:uppercase; color:var(--cyan);
  margin-bottom:1rem; padding-bottom:.6rem;
  border-bottom:1px solid rgba(56,189,248,.12);
}
.result-content {
  font-family:'Inter',sans-serif; font-size:.875rem; line-height:1.85;
  color: #ddeeff !important;        /* HIGH-CONTRAST: always readable on dark bg */
  white-space:pre-wrap; word-break:break-word; opacity:1 !important;
}

/* ═══════════════════════════════════════════
   REPORT PANEL
═══════════════════════════════════════════ */
.report-panel {
  background: var(--bg-surface);
  border: 1px solid var(--border-cyan);
  border-radius: var(--r-xl);
  padding: 2.2rem 2.5rem; margin-top:1.2rem;
  box-shadow: 0 8px 32px rgba(0,0,0,.45), 0 0 40px rgba(56,189,248,.08);
  position:relative; overflow:hidden;
}
.report-panel::before {
  content:''; position:absolute; top:0;left:0;right:0; height:1px;
  background:linear-gradient(90deg,transparent,var(--cyan),var(--purple),transparent); opacity:.55;
}

/* Make ALL Streamlit markdown inside report bright */
.report-panel *,
.report-panel .stMarkdown *,
.report-panel p, .report-panel li,
.report-panel h1,.report-panel h2,.report-panel h3,.report-panel h4,.report-panel h5,
.report-panel strong, .report-panel em, .report-panel span {
  color: #e8f4ff !important;
  opacity: 1 !important;
}
.report-panel h1,.report-panel h2 { color:#f5faff!important; font-weight:700!important; }
.report-panel h3,.report-panel h4 { color:#d8eeff!important; font-weight:600!important; }
.report-panel strong             { color:#ffffff!important; }
.report-panel code {
  background:rgba(56,189,248,.12)!important; border:1px solid rgba(56,189,248,.2)!important;
  border-radius:4px!important; padding:.1rem .4rem!important; color:#a5d8ff!important;
}

/* ═══════════════════════════════════════════
   FEEDBACK / CRITIC PANEL
═══════════════════════════════════════════ */
.feedback-panel {
  background: var(--bg-surface);
  border: 1px solid var(--border-green);
  border-radius: var(--r-xl);
  padding: 2.2rem 2.5rem; margin-top:1.2rem;
  box-shadow: 0 8px 32px rgba(0,0,0,.45), 0 0 40px rgba(34,211,107,.07);
  position:relative; overflow:hidden;
}
.feedback-panel::before {
  content:''; position:absolute; top:0;left:0;right:0; height:1px;
  background:linear-gradient(90deg,transparent,var(--green),transparent); opacity:.45;
}
.feedback-panel *,
.feedback-panel .stMarkdown *,
.feedback-panel p, .feedback-panel li,
.feedback-panel h1,.feedback-panel h2,.feedback-panel h3,.feedback-panel h4,.feedback-panel h5,
.feedback-panel strong {
  color: #e2f7ec !important;
  opacity: 1 !important;
}
.feedback-panel strong { color:#f0fff7!important; }

/* ── panel labels ── */
.panel-label {
  font-family:'JetBrains Mono',monospace; font-size:.64rem; font-weight:500;
  letter-spacing:.22em; text-transform:uppercase;
  margin-bottom:1.4rem; padding-bottom:.8rem;
  display:flex; align-items:center; gap:.6rem;
}
.panel-label.cyan  { color:var(--cyan);  border-bottom:1px solid rgba(56,189,248,.15); }
.panel-label.green { color:var(--green); border-bottom:1px solid rgba(34,211,107,.15); }
.panel-label .dot  { width:6px;height:6px;border-radius:50%;flex-shrink:0; }
.panel-label.cyan  .dot { background:var(--cyan);  box-shadow:0 0 8px var(--cyan); }
.panel-label.green .dot { background:var(--green); box-shadow:0 0 8px var(--green); }

/* ── download button ── */
.stDownloadButton > button {
  background:transparent!important; border:1.5px solid rgba(56,189,248,.35)!important;
  border-radius:var(--r-sm)!important; color:var(--cyan)!important;
  font-family:'Inter',sans-serif!important; font-size:.85rem!important; font-weight:500!important;
  padding:.6rem 1.4rem!important; transition:all .2s!important; margin-top:1rem!important;
}
.stDownloadButton > button:hover {
  background:rgba(56,189,248,.08)!important; border-color:var(--cyan)!important;
  box-shadow:0 0 20px rgba(56,189,248,.15)!important;
}

/* ── misc ── */
.stSpinner > div { color:var(--cyan)!important; }
.stAlert { background:rgba(251,191,36,.08)!important; border:1px solid rgba(251,191,36,.25)!important; border-radius:var(--r-sm)!important; color:#fde68a!important; }

/* ── footer ── */
.footer {
  font-family:'JetBrains Mono',monospace; font-size:.64rem;
  color:var(--text-lo); text-align:center; margin-top:4rem;
  letter-spacing:.1em; padding-top:1.5rem; border-top:1px solid var(--border-subtle);
}
</style>
""", unsafe_allow_html=True)


# ── Helper: step card ─────────────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("IDLE",   "status-waiting"),
        "running": ("● LIVE", "status-running"),
        "done":    ("✓ DONE", "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls   = {"running": "active", "done": "done"}.get(state, "")

    st.markdown(f"""
    <div class="step-card {card_cls}">
      <div class="step-header">
        <span class="step-num">{num}</span>
        <span class="step-title">{title}</span>
        <span class="step-status {cls}">{label}</span>
      </div>
      {"<div class='step-desc'>" + desc + "</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">Multi-Agent AI System</div>
  <h1>Researcher<span class="grad">Agent</span></h1>
  <p class="hero-sub">
    Four specialized AI agents collaborate — searching, scraping, writing,
    and critiquing — to deliver a polished research report on any topic.
  </p>
</div>
<div class="rule"></div>
""", unsafe_allow_html=True)


# ── LAYOUT ────────────────────────────────────────────────────────────────────
col_input, col_gap, col_pipeline = st.columns([5, 0.4, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Roadmap for AGI development in next 5 years",
        key="topic_input",
    )

    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    examples = [
        "Future of LLM in Tech Industry",
        "All Latest AI Agents in 2026",
        "Roadmap for AGI development in next 5 years",
    ]
    chips_html = '<div class="chip-row"><span class="chip-label">Try →</span>'
    for ex in examples:
        chips_html += f'<span class="chip">{ex}</span>'
    chips_html += '</div>'
    st.markdown(chips_html, unsafe_allow_html=True)


with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results

    def s(step):
        if not r:
            return "waiting"
        if step in r:
            return "done"
        if st.session_state.running:
            for k in ["search", "reader", "writer", "critic"]:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent", s("search"), "Gathers recent web information")
    step_card("02", "Reader Agent", s("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain", s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain", s("critic"), "Reviews & scores the report")


# ── RUN PIPELINE ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done    = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results   = {}
    topic_val = st.session_state.topic_input

    with st.spinner("🔍 Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("📄 Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}")]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("✍️ Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    with st.spinner("🧐 Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({"report": results["writer"]})
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done    = True
    st.rerun()


# ── RESULTS ───────────────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(f"""
            <div class="result-panel">
              <div class="result-panel-title">Search Agent Output</div>
              <div class="result-content">{r["search"]}</div>
            </div>""", unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(f"""
            <div class="result-panel">
              <div class="result-panel-title">Reader Agent Output</div>
              <div class="result-content">{r["reader"]}</div>
            </div>""", unsafe_allow_html=True)

    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
          <div class="panel-label cyan"><span class="dot"></span>Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
          <div class="panel-label green"><span class="dot"></span>Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  ResearchAgent &nbsp;·&nbsp; Powered by LangChain Multi-Agent Pipeline &nbsp;·&nbsp; Built with Streamlit
</div>
""", unsafe_allow_html=True)