import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

# Page Configuration
st.set_page_config(page_title="AI Assistant", page_icon="✨", layout="centered")

# Custom CSS for Professional Look and Watermark
st.markdown("""
<style>
/* Clean typography and layout */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* "Made by Yagya" watermark on the top right */
.watermark {
    position: fixed;
    top: 20px;
    right: 20px;
    font-size: 14px;
    font-weight: 500;
    color: #a0a0a0;
    z-index: 10000;
    padding: 8px 16px;
    border-radius: 50px;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.watermark:hover {
    background: rgba(255, 255, 255, 0.1);
    color: #fff;
    cursor: default;
}

/* Soft styling for chat inputs */
.stChatInputContainer {
    padding-bottom: 20px;
}
</style>
<div class="watermark">✨ Chatbot made by Yagya</div>
""", unsafe_allow_html=True)

# Main Chat Header
st.title("🤖 Intelligent Assistant")
st.caption("created by Yagya")

# st.session_state -> dict -> 
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input('Type your message here...')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    # stream the response
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})