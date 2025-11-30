import streamlit as st
import requests

# ================= CONFIG =================
N8N_WEBHOOK_URL = "https://deepshika021.app.n8n.cloud/webhook/eli5"
# ==========================================

st.set_page_config(
    page_title="Understand Easily",
    page_icon="💡",
    layout="wide"
)

# ---------- SESSION STATE ----------
if "chats" not in st.session_state:
    # each chat: {"title": str, "messages": [{"role": "user"/"assistant", "content": str}]}
    st.session_state.chats = [{"title": "Chat 1", "messages": []}]
    st.session_state.current_chat_index = 0

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 💬 Chats")

    search = st.text_input("Search chats")

    if st.button("➕ New Chat"):
        st.session_state.chats.append(
            {"title": f"Chat {len(st.session_state.chats)+1}", "messages": []}
        )
        st.session_state.current_chat_index = len(st.session_state.chats) - 1

    if st.button("Empty Chat"):
        st.session_state.chats[st.session_state.current_chat_index]["messages"] = []

    st.markdown("---")

    # chat list
    for i, chat in enumerate(st.session_state.chats):
        title = chat["messages"][0]["content"][:25] + "..." if chat["messages"] else chat["title"]
        if search.lower() in title.lower():
            if st.button(title, key=f"chat-{i}"):
                st.session_state.current_chat_index = i

current_chat = st.session_state.chats[st.session_state.current_chat_index]

# ---------- CUSTOM CSS ----------
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: "Helvetica Neue", system-ui, -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp { background-color: #0d0f16; }

    .chat-box {
        max-width: 900px;
        margin: auto;
        padding-top: 20px;
    }

    .bubble {
        padding: 14px 18px;
        border-radius: 10px;
        margin-bottom: 16px;
        line-height: 1.6;
        white-space: pre-wrap;
        font-size: 16px;
    }

    .user { background-color: #2b2f3a; }
    .assistant { background-color: #1c1f29; }

    textarea {
        background: #2b2f3a !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: 1px solid #3a3f4d !important;
        font-size: 16px !important;
        box-shadow: none !important;     /* remove red glow */
    }
    textarea:focus {
        border: 1px solid #6b7280 !important;  /* soft grey, no red */
        box-shadow: none !important;
    }

    button[kind="primary"] {
        background-color: #bcdcff !important;  /* soft light blue */
        color: #000 !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        padding: 10px 24px !important;
    }

    .caption {
        text-align:center;
        margin-top: 30px;
        color:#9ca3af;
        font-size:14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- HEADER ----------
st.markdown(
    "<h2 style='text-align:center;'>💡 Understand Easily</h2>"
    "<p style='text-align:center; color:#b8b9c4;'>Learning made simple, one explanation at a time.</p>",
    unsafe_allow_html=True
)

# ---------- CHAT DISPLAY ----------
st.markdown("<div class='chat-box'>", unsafe_allow_html=True)

for msg in current_chat["messages"]:
    role_class = "user" if msg["role"] == "user" else "assistant"
    st.markdown(f"<div class='bubble {role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("---")

# ---------- INPUT (NO FORM) ----------
user_input = st.text_area(
    "",
    placeholder="Ask a concept or follow-up question...",
    height=80,
    key="chat_input"
)

level = st.selectbox(
    "Level",
    ["Beginner", "School Student", "College Student", "Advanced"],
    key="level_select"
)

explain_clicked = st.button("Explain")

# ---------- BACKEND CALL ----------
if explain_clicked and user_input.strip():
    # add user message
    current_chat["messages"].append({"role": "user", "content": user_input})

    with st.spinner("Explaining..."):
        try:
            response = requests.post(
                N8N_WEBHOOK_URL,
                json={"concept": user_input, "level": level},
                timeout=60
            )
            if response.status_code == 200:
                output = response.json().get("output", "")
            else:
                output = f"Something went wrong. (status {response.status_code})"
        except Exception as e:
            output = f"Request failed: {e}"

    current_chat["messages"].append({"role": "assistant", "content": output})
    st.rerun()  # this exists on your version; if it errors, change to st.rerun()

# ---------- JS: ENTER = EXPLAIN, SHIFT+ENTER = NEW LINE ----------
st.markdown(
    """
    <script>
    const textareas = parent.document.querySelectorAll('textarea');
    if (textareas.length > 0) {
        const ta = textareas[textareas.length - 1];  // last textarea = chat input
        ta.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const buttons = parent.document.querySelectorAll('button');
                buttons.forEach(btn => {
                    if (btn.innerText.trim() === 'Explain') {
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
st.markdown("<p class='caption'>Learning made simple, one explanation at a time.</p>", unsafe_allow_html=True)

