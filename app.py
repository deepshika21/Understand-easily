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
        margin-bottom: 10px;
    }

    .subtitle {
        font-size: 18px;
        color: #b8b9c4;
        text-align: center;
        margin-bottom: 40px;
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
        outline: none !important;
        border: 1px solid #6b7280 !important;
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
        margin-top: 10px !important;
    }

    footer {
        margin-top: 80px;
        color: #a5a6b1;
        font-size: 14px;
        text-align: center;
        margin-bottom: 40px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- PAGE CONTENT ----------
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
            placeholder="Type a concept or follow-up question…",
            key="concept_input"
        )

    with col2:
        level = st.selectbox(
            "Your Level",
            ["School Student", "College Student", "Beginner", "Advanced"]
        )

    submit = st.form_submit_button("Explain")

# ---------- SUBMIT LOGIC ----------
if submit:
    if concept.strip() == "":
        st.warning("Please enter a concept.")
    else:
        with st.spinner("Explaining clearly…"):
            response = requests.post(
                N8N_WEBHOOK_URL,
                json={
                    "concept": concept,
                    "level": level,
                    "previous_context": st.session_state.last_explanation
                },
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

# ---------- ENTER / SHIFT+ENTER HANDLER ----------
st.markdown(
    """
    <script>
    const textarea = parent.document.querySelector("textarea");

    if (textarea) {
        textarea.addEventListener("keydown", function(e) {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();

                const buttons = parent.document.querySelectorAll("button");
                buttons.forEach(btn => {
                    if (btn.innerText === "Explain") {
                        btn.click();
                    }
                });
            }
        });
    }
    </script>
    """,
    unsafe_allow_html=True
)

# ---------- FOOTER ----------
st.markdown("<footer>Built to understand, not memorise.</footer>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
