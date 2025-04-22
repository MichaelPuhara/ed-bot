import streamlit as st
import openai

# Claude-style Socratic Tutor Prompt
SYSTEM_PROMPT = """
You are a Socratic tutor designed to help students think critically and learn deeply. 
Instead of providing direct answers, you guide them through reflective questions, 
clarify misconceptions, and encourage structured problem-solving. 
Always assume the student is capable of arriving at the answer with your support.
"""

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Send message to OpenAI
def query_openai(chat_history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Or use "gpt-3.5-turbo" for lower cost
            messages=messages,
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Error: {e}"

# Streamlit UI
st.set_page_config(page_title="Claude for Education", page_icon="🧠")
st.title("🧠 Claude-style Socratic Tutor")
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
        st.session_state.chat.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            response = query_openai(st.session_state.chat)
            st.session_state.chat.append({"role": "assistant", "content": response})
        st.rerun()
