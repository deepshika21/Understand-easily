import streamlit as st
import requests

# ================= CONFIG =================
N8N_WEBHOOK_URL = "https://deepshika021.app.n8n.cloud/webhook/eli5"
# ==========================================

st.set_page_config(
    page_title="Understand Easily",
    page_icon="📘",
    layout="wide"
)

# ---------- SESSION STATE ----------
if "last_explanation" not in st.session_state:
    st.session_state.last_explanation = None

# ---------- CUSTOM CSS ----------
st.markdown(
    """
    <style>
    body { background-color: #0d0f16; color: #ffffff; }
    .stApp { background-color: #0d0f16; }

    .container {
        max-width: 1100px;
        margin: auto;
        padding-top: 60px;
    }

    h1 {
        font-size: 48px;
        font-weight: 700;
        text-align: center;
    }

    .subtitle {
        font-size: 18px;
        color: #b8b9c4;
        text-align: center;
        margin-bottom: 40px;
    }

    .hint {
        text-align: right;
        font-size: 13px;
        color: #9ca3af;
        margin-top: -8px;
        margin-bottom: 10px;
    }

    textarea {
        background: #2b2f3a !important;
        border: 1px solid #3a3f4d !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        height: 90px !important;
        font-size: 16px !important;
    }

    textarea:focus {
        border: 1px solid #6b7280 !important;
        outline: none !important;
    }

    div[data-baseweb="select"] > div {
        background: #2b2f3a !important;
        border: 1px solid #3a3f4d !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-size: 16px !important;
    }

    button[kind="primary"] {
        background: #ffffff !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        padding: 12px 30px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- CONTENT ----------
st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown("<h1>Understand Easily</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Clear explanations — from child-level intuition to exam-ready understanding</p>",
    unsafe_allow_html=True
)

# ---------- FORM ----------
with st.form("explain_form", clear_on_submit=False):
    col1, col2 = st.columns([3, 1])

    with col1:
        concept = st.text_area(
            "Concept",
            placeholder="Type a concept or a follow-up question…",
            key="concept_input"
        )
        st.markdown("<div class='hint'>Press Ctrl + Enter to explain</div>", unsafe_allow_html=True)

    with col2:
        level = st.selectbox(
            "Your Level",
            ["School Student", "College Student", "Beginner", "Advanced"]
        )

    submit = st.form_submit_button("Explain")

# ---------- ACTION ----------
if submit:
    if concept.strip() == "":
        st.warning("Please enter a concept.")
    else:
        with st.spinner("Explaining clearly…"):
            payload = {
                "concept": concept,
                "level": level,
                "previous_context": st.session_state.last_explanation
            }

            response = requests.post(
                N8N_WEBHOOK_URL,
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                data = response.json()
                explanation = data.get("output", "")
                st.session_state.last_explanation = explanation

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(explanation)
            else:
                st.error(f"Error: {response.status_code}")

# ---------- FOOTER ----------
st.markdown("<footer>Built to understand, not memorise.</footer>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
