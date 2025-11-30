import streamlit as st
import requests
import uuid

# ================= CONFIG =================
N8N_WEBHOOK_URL = "https://deepshika021.app.n8n.cloud/webhook/eli5"

st.set_page_config(
    page_title="Understand Easily",
    page_icon="💡",
    layout="wide"
)

# ================= SESSION STATE =================
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "active_chat" not in st.session_state:
    cid = str(uuid.uuid4())
    st.session_state.active_chat = cid
    st.session_state.chats[cid] = {
        "title": "New Chat",
        "messages": []
    }

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if "level" not in st.session_state:
    st.session_state.level = "Beginner"

# ================= THEME COLORS =================
if st.session_state.theme == "dark":
    BG = "#0d0f16"
    CARD = "#1c1f29"
    INPUT = "#2b2f3a"
    BORDER = "#3a3f4d"
    TEXT = "#ffffff"
    SUB = "#9ca3af"
else:
    BG = "#f5f6f8"
    CARD = "#ffffff"
    INPUT = "#f1f3f6"
    BORDER = "#d1d5db"
    TEXT = "#000000"
    SUB = "#4b5563"

# ================= CSS =================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Helvetica+Neue:wght@300;400;500;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Helvetica Neue', sans-serif !important;
}}

.stApp {{
    background-color: {BG};
    color: {TEXT};
}}

header[data-testid="stHeader"] {{
    background: transparent;
}}

#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}

input, textarea {{
    background: {INPUT} !important;
    color: {TEXT} !important;
    border-radius: 8px !important;
    border: 1px solid {BORDER} !important;
    font-size: 16px !important;
}}

textarea:focus, input:focus {{
    outline: none !important;
    border: 1px solid #6b7280 !important;
}}

.chat-box {{
    max-width: 900px;
    margin: auto;
    padding-top: 20px;
}}

.msg {{
    padding: 14px 18px;
    border-radius: 10px;
    margin-bottom: 14px;
    line-height: 1.6;
    white-space: pre-wrap;
}}

.user {{ background: {INPUT}; }}
.bot {{ background: {CARD}; }}

button[kind="primary"] {{
    background-color: #bcdcff !important;
    color: #000 !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    padding: 10px 26px !important;
}}

.caption {{
    text-align:center;
    margin-top: 40px;
    color:{SUB};
    font-size:14px;
}}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("### 💬 Chats")

    search = st.text_input("Search")

    for cid, c in st.session_state.chats.items():
        if search.lower() in c["title"].lower():
            if st.button(c["title"], key=cid):
                st.session_state.active_chat = cid
                st.rerun()

    st.divider()

    if st.button("➕ New Chat"):
        cid = str(uuid.uuid4())
        st.session_state.chats[cid] = {
            "title": "New Chat",
            "messages": []
        }
        st.session_state.active_chat = cid
        st.rerun()

    if st.button("🧹 Clear Chat"):
        st.session_state.chats[st.session_state.active_chat]["messages"] = []
        st.rerun()

    st.divider()

    st.session_state.level = st.selectbox(
        "🎓 Explanation Level",
        ["Beginner", "School Student", "College Student", "Advanced"]
    )

    st.session_state.theme = st.toggle(
        "🌗 Light Mode", value=(st.session_state.theme == "light")
    ) and "light" or "dark"

# ================= HEADER =================
st.markdown(
    f"<h2 style='text-align:center;'>💡 Understand Easily</h2>"
    f"<p style='text-align:center; color:{SUB};'>Learning made simple, one explanation at a time.</p>",
    unsafe_allow_html=True
)

# ================= CHAT =================
chat = st.session_state.chats[st.session_state.active_chat]

st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
for m in chat["messages"]:
    cls = "user" if m["role"] == "user" else "bot"
    st.markdown(f"<div class='msg {cls}'>{m['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ================= INPUT =================
with st.form("input"):
    user_text = st.text_area(
        "",
        placeholder="Ask a concept or follow-up question…",
        height=90
    )
    submitted = st.form_submit_button("Explain")

if submitted and user_text.strip():
    chat["messages"].append({"role": "user", "content": user_text})

    if chat["title"] == "New Chat":
        chat["title"] = user_text[:28] + "..."

    with st.spinner("Explaining…"):
        try:
            r = requests.post(
                N8N_WEBHOOK_URL,
                json={"concept": user_text, "level": st.session_state.level},
                timeout=60
            )
            reply = r.json().get("output", "Something went wrong.")
        except:
            reply = "Server error. Please try again."

    chat["messages"].append({"role": "assistant", "content": reply})
    st.rerun()

# ================= FOOTER =================
st.markdown("<p class='caption'>Built to understand, not memorise.</p>", unsafe_allow_html=True)
