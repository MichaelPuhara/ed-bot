import streamlit as st
import requests

# Claude-style Socratic Tutor Prompt
SYSTEM_PROMPT = """
You are a Socratic tutor designed to help students think critically and learn deeply. 
Instead of providing direct answers, you guide them through reflective questions, 
clarify misconceptions, and encourage structured problem-solving. 
Always assume the student is capable of arriving at the answer with your support.
"""

# Send message to Ollama server
def query_ollama(chat_history):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "mistral",
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history,
        "stream": False
    }

    try:
        res = requests.post(url, json=payload)
        res.raise_for_status()
        return res.json().get("message", {}).get("content", "⚠️ No response from model.")
    except requests.RequestException as e:
        return f"⚠️ Error: {e}"

# Streamlit UI
st.set_page_config(page_title="Claude for Education", page_icon="🧠")
st.title("🧠 Personalised Tutor")
st.markdown("_Ask a question and let your AI tutor guide your thinking._")

# Session state for chat
if "chat" not in st.session_state:
    st.session_state.chat = []

# Display chat history
for msg in st.session_state.chat:
    if msg["role"] == "user":
        st.markdown(f"**🧑‍🎓 You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**🧠 Tutor:** {msg['content']}")

# Text input
user_input = st.text_area("Enter your question or idea", height=100)

if st.button("Ask Tutor"):
    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        # Add user message to chat
        st.session_state.chat.append({"role": "user", "content": user_input})

        # Get tutor response
        with st.spinner("Thinking..."):
            response = query_ollama(st.session_state.chat)
            st.session_state.chat.append({"role": "assistant", "content": response})

        # Only rerun after the interaction is complete
        st.rerun()
