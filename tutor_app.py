import streamlit as st
import openai

# Set up the client
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Claude-style Socratic Tutor Prompt
SYSTEM_PROMPT = """
You are a Socratic tutor designed to help students think critically and learn deeply. 
Instead of providing direct answers, you guide them through reflective questions, 
clarify misconceptions, and encourage structured problem-solving. 
Always assume the student is capable of arriving at the answer with your support.
"""

# Function to query OpenAI
def query_openai(chat_history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Or "gpt-3.5-turbo"
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {e}"

# Streamlit UI
st.set_page_config(page_title="Personalised Tutor", page_icon="🧠")
st.title("🧠 Personalised Tutor")
st.markdown("_Ask a question and let your Personalised tutor guide your thinking._")

if "chat" not in st.session_state:
    st.session_state.chat = []

for msg in st.session_state.chat:
    if msg["role"] == "user":
        st.markdown(f"**🧑‍🎓 You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**🧠 Tutor:** {msg['content']}")

user_input = st.text_area("Enter your question or idea", height=100)

if st.button("Ask Tutor"):
    if user_input.strip():
        st.session_state.chat.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            response = query_openai(st.session_state.chat)
            st.session_state.chat.append({"role": "assistant", "content": response})
        st.rerun()
    else:
        st.warning("Please enter a question.")
