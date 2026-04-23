import streamlit as st
from speech_to_text import start_recording, stop_recording, speech_to_text
from llm_response import ask_llm
import os

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎤",
    layout="wide"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080c14 !important;
    font-family: 'DM Sans', sans-serif;
    color: #e8eaf0;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(56,189,248,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(99,102,241,0.10) 0%, transparent 60%),
        #080c14 !important;
}

/* hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(15, 20, 35, 0.95) !important;
    border-right: 1px solid rgba(56,189,248,0.12);
}

/* ── Main container ── */
.block-container {
    max-width: 1100px !important;
    padding: 2.5rem 2rem 4rem !important;
}

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}

.hero-badge {
    display: inline-block;
    background: rgba(56,189,248,0.1);
    border: 1px solid rgba(56,189,248,0.3);
    color: #38bdf8;
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    padding: 0.4rem 1.1rem;
    border-radius: 100px;
    margin-bottom: 1.4rem;
}

.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 5vw, 3.6rem);
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #e8eaf0 30%, #38bdf8 70%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.9rem;
    letter-spacing: -0.02em;
}

.hero p {
    color: rgba(232,234,240,0.55);
    font-size: 1.05rem;
    font-weight: 300;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Divider ── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.2), rgba(129,140,248,0.2), transparent);
    margin: 2rem 0;
}

/* ── Status pill ── */
.status-idle, .status-recording {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Syne', sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.45rem 1rem;
    border-radius: 100px;
    margin-bottom: 2rem;
}

.status-idle {
    background: rgba(232,234,240,0.06);
    border: 1px solid rgba(232,234,240,0.12);
    color: rgba(232,234,240,0.45);
}

.status-recording {
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.35);
    color: #f87171;
    animation: pulse-border 2s infinite;
}

@keyframes pulse-border {
    0%, 100% { box-shadow: 0 0 0 0 rgba(239,68,68,0.3); }
    50%       { box-shadow: 0 0 0 6px rgba(239,68,68,0); }
}

.dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: currentColor;
}
.dot-recording { animation: blink 1s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }

/* ── Control Buttons ── */
.stButton > button {
    width: 100% !important;
    padding: 0.85rem 1.5rem !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    transition: all 0.2s ease !important;
    border: none !important;
    cursor: pointer !important;
}

/* Start button */
div[data-testid="column"]:first-child .stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
    color: #fff !important;
    box-shadow: 0 0 24px rgba(14,165,233,0.3) !important;
}

div[data-testid="column"]:first-child .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 36px rgba(14,165,233,0.5) !important;
}

/* Stop button */
div[data-testid="column"]:last-child .stButton > button {
    background: rgba(239,68,68,0.12) !important;
    color: #f87171 !important;
    border: 1px solid rgba(239,68,68,0.3) !important;
    box-shadow: none !important;
}

div[data-testid="column"]:last-child .stButton > button:hover {
    background: rgba(239,68,68,0.22) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 0 20px rgba(239,68,68,0.25) !important;
}

/* ── Cards ── */
.card {
    background: rgba(15, 22, 38, 0.7);
    border: 1px solid rgba(56,189,248,0.1);
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin: 1.2rem 0;
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.5), transparent);
}

.card-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.card-label-answer {
    color: #818cf8;
}

.card-content {
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.75;
    color: rgba(232,234,240,0.85);
}

/* ── Alert / success override ── */
[data-testid="stAlert"] {
    background: rgba(16,185,129,0.08) !important;
    border: 1px solid rgba(16,185,129,0.25) !important;
    border-radius: 10px !important;
    color: #6ee7b7 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] > div {
    color: #38bdf8 !important;
}

/* ── Features grid ── */
.features-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
    margin-top: 0.5rem;
}

.feature-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    font-size: 0.88rem;
    color: rgba(232,234,240,0.65);
    font-weight: 300;
}

.feature-icon {
    font-size: 1rem;
    flex-shrink: 0;
}

.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(232,234,240,0.3);
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ────────────────────────────────────────────────────────────
if "recording" not in st.session_state:
    st.session_state.recording = False
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "answer" not in st.session_state:
    st.session_state.answer = None

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">AI-Powered Practice</div>
    <h1>Interview Coach</h1>
    <p>Speak your question aloud. Get sharp, structured answers in real time.</p>
</div>
""", unsafe_allow_html=True)

# ── Status Indicator ──────────────────────────────────────────────────────────
if st.session_state.recording:
    st.markdown("""
    <div style="text-align:center">
        <span class="status-recording">
            <span class="dot dot-recording"></span> Recording in progress
        </span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align:center">
        <span class="status-idle">
            <span class="dot"></span> Ready
        </span>
    </div>
    """, unsafe_allow_html=True)

# ── Controls ──────────────────────────────────────────────────────────────────
col1, col_gap, col2 = st.columns([1, 0.08, 1])

with col1:
    if st.button("🎙  Start Recording", use_container_width=True):
        if not st.session_state.recording:
            start_recording()
            st.session_state.recording = True
            st.rerun()

with col2:
    if st.button("⏹  Stop & Analyze", use_container_width=True):
        if st.session_state.recording:
            audio_file = stop_recording()
            st.session_state.recording = False

            with st.spinner("Transcribing your question…"):
                transcript = speech_to_text(audio_file)
                st.session_state.transcript = transcript

            with st.spinner("Generating answer…"):
                answer = ask_llm(transcript)
                st.session_state.answer = answer

            os.remove(audio_file)
            st.rerun()

# ── Results ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

if st.session_state.transcript:
    st.markdown(f"""
    <div class="card">
        <div class="card-label">🎙 &nbsp; Question Detected</div>
        <div class="card-content">{st.session_state.transcript}</div>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.answer:
    st.markdown(f"""
    <div class="card">
        <div class="card-label card-label-answer">✦ &nbsp; AI Answer</div>
        <div class="card-content">{st.session_state.answer}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Features Footer ───────────────────────────────────────────────────────────
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-heading">What\'s included</div>', unsafe_allow_html=True)

st.markdown("""
<div class="features-grid">
    <div class="feature-item"><span class="feature-icon">🎙</span> Live voice recording</div>
    <div class="feature-item"><span class="feature-icon">📝</span> Whisper transcription</div>
    <div class="feature-item"><span class="feature-icon">🤖</span> Gemma AI answers</div>
    <div class="feature-item"><span class="feature-icon">🏆</span> Interview practice mode</div>
</div>
""", unsafe_allow_html=True)