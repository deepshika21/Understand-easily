import streamlit as st
import requests

# ================= CONFIG =================
N8N_WEBHOOK_URL = "https://deepshika021.app.n8n.cloud/webhook/eli5"
# ==========================================

st.set_page_config(
    page_title="Explain It Like I'm 5",
    page_icon="🧠",
    layout="wide"
)

# ---------- HEADER ----------
st.markdown(
    """
    <style>
    /* ---------- Textarea & Input ---------- */
    textarea, input {
        background-color: #1f2933 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: 1px solid #6b7280 !important; /* soft gray */
    }

    textarea:focus, input:focus {
        outline: none !important;
        border: 1px solid #9ca3af !important; /* lighter gray on focus */
        box-shadow: 0 0 4px rgba(156, 163, 175, 0.4) !important;
    }

    /* ---------- Selectbox (LEVEL DROPDOWN) ---------- */
    div[data-baseweb="select"] > div {
        background-color: #1f2933 !important;
        border-radius: 8px !important;
        border: 1px solid #6b7280 !important; /* soft gray */
        color: #ffffff !important;
    }

    div[data-baseweb="select"] > div:focus-within {
        border: 1px solid #9ca3af !important; /* soft focus */
        box-shadow: 0 0 4px rgba(156, 163, 175, 0.4) !important;
    }

    /* Dropdown menu items */
    ul[role="listbox"] {
        background-color: #111827 !important;
        border: 1px solid #374151 !important;
    }

    li {
        color: #e5e7eb !important;
    }

    li:hover {
        background-color: #1f2933 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.divider()

# ---------- INPUT SECTION ----------
col1, col2 = st.columns([2, 1])

with col1:
    concept = st.text_area(
        "📌 Concept you want to understand",
        placeholder="e.g. Probability, Deadlock, Ohm's Law",
        height=120
    )

with col2:
    level = st.selectbox(
        "🎒 Your level",
        ["School Student", "College Student", "Exam Preparation"]
    )

st.markdown("")  # spacing

# ---------- ACTION ----------
if st.button("✨ Explain"):
    if concept.strip() == "":
        st.warning("Please enter a concept.")
    else:
        with st.spinner("Thinking like a good teacher..."):
            response = requests.post(
                N8N_WEBHOOK_URL,
                json={
                    "concept": concept,
                    "level": level
                },
                timeout=60
            )

        if response.status_code == 200:
            data = response.json()
            explanation = data.get("output", "No explanation received.")

            st.divider()
            st.subheader("📘 Explanation")

            # ---------- SMART DISPLAY ----------
            # Split sections based on headers
            sections = explanation.split("\n\n")

            for section in sections:
                if "EXPLAIN LIKE I’M 5" in section or "ELI5" in section:
                    with st.expander("🧒 Explain Like I'm 5"):
                        st.markdown(section)
                elif "STUDENT" in section:
                    with st.expander("🎓 Student Explanation"):
                        st.markdown(section)
                elif "EXAM" in section:
                    with st.expander("📝 Exam-Ready Explanation"):
                        st.markdown(section)
                elif "CHECK" in section or "QUESTION" in section:
                    with st.expander("❓ Check Your Understanding"):
                        st.markdown(section)
                else:
                    st.markdown(section)

        else:
            st.error(f"Error {response.status_code}: {response.text}")

# ---------- FOOTER ----------
st.divider()
st.markdown(
    "<p style='text-align:center; color:gray;'>Built to learn, not to memorise.</p>",
    unsafe_allow_html=True
)



