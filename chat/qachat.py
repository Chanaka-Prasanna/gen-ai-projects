import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import uuid

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(question, chat_model):
    response = chat_model.send_message(question, stream=True)
    return response

# Set page config
st.set_page_config(page_title="Gemini Chat", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stTextInput > div > div > input {
        background-color: #2D2D2D;
        color: #FFFFFF;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for conversations
if 'conversations' not in st.session_state:
    st.session_state['conversations'] = []
if 'current_conversation' not in st.session_state:
    st.session_state['current_conversation'] = None

# Sidebar for conversations
with st.sidebar:
    st.title("Conversations")
    
    if st.button("New Chat", key="new_chat"):
        new_id = str(uuid.uuid4())
        st.session_state['conversations'].append({
            'id': new_id,
            'title': f"New Chat {len(st.session_state['conversations']) + 1}",
            'messages': []
        })
        st.session_state['current_conversation'] = new_id

    for convo in st.session_state['conversations'][-5:]:
        if st.button(convo['title'], key=f"convo_{convo['id']}"):
            st.session_state['current_conversation'] = convo['id']

# Main chat interface
col1, col2 = st.columns([3, 1])

with col1:
    colored_header(label="Gemini Chat", description="Chat with Gemini AI", color_name="green-70")
    add_vertical_space(2)

    if st.session_state['current_conversation']:
        current_convo = next((c for c in st.session_state['conversations'] if c['id'] == st.session_state['current_conversation']), None)
        
        if current_convo:
            for message in current_convo['messages']:
                with st.chat_message(message['role']):
                    st.write(message['content'])

            user_input = st.chat_input("Type your message here...")

            if user_input:
                current_convo['messages'].append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.write(user_input)

                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    chat_model = genai.GenerativeModel('gemini-pro').start_chat(history=[])
                    for chunk in get_gemini_response(user_input, chat_model):
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                current_convo['messages'].append({"role": "assistant", "content": full_response})

with col2:
    st.subheader("About")
    st.write("This is a modern chat interface for Gemini AI. Ask any question and get AI-powered responses.")
