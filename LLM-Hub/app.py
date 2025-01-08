import streamlit as st
from ollama import chat
import random
import time

# Streamlit app
st.title("Multi-Model LLM Question Answering App")
st.markdown("""
This app allows you to interact with multiple LLMs simultaneously. 
Choose from the available models, ask a question, and compare the answers!
""")

# Sidebar for model selection
available_models = ["llama3.2", "smollm2", "mistral"]  # Update with your models
selected_model = st.sidebar.selectbox("Choose Model", available_models, placeholder="Choose an option", index=0)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Start the stream for assistant's response
    stream = chat(
        model=selected_model,
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response_text = ""
        response_placeholder = st.empty()  # Placeholder for the streaming response
        
        for chunk in stream:
            response_text += chunk['message']['content']
            response_placeholder.markdown(response_text)  # Update the placeholder with new content

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
