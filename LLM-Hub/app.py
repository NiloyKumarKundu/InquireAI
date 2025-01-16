import streamlit as st
from ollama import Client
import logging
from datetime import datetime
import os
import ssl
import time

ssl._create_default_https_context = ssl._create_unverified_context

# Set up logging
log_dir = "/app/logs"
os.makedirs(log_dir, exist_ok=True)  # Ensure the logs directory exists
log_file = os.path.join(log_dir, f"app_log_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Log app start
logging.info("Streamlit app started.")

# Ollama Client
try:
    client = Client(host='http://ollama:11434')
    logging.info("Ollama client initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize Ollama client: {e}")
    st.error("Failed to initialize LLM client. Please check the logs for details.")
    st.stop()

# Streamlit app
st.set_page_config(page_title="MlHub", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Multi-Model LLM Question Answering App")

st.markdown("""
This app allows you to interact with multiple LLMs simultaneously. 
Choose from the available models, ask a question, and compare the answers!
""")

# Sidebar for model selection
available_models = ["llama3.2", "smollm2", "mistral", "deepseek-v3"]  # Update with your models
selected_model = st.sidebar.selectbox("Choose Model", available_models, placeholder="Choose an option", index=0)

if selected_model == "deepseek-v3":
    selected_model = "nezahatkorkmaz/deepseek-v3"
    
logging.info(f"User selected model: {selected_model}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    logging.info(f"User input received: {prompt}")

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Show status updates while processing
        # with st.status("Sending request...", expanded=True, state="running") as status:
        #     status.write("Searching for model...")
        #     time.sleep(1)  # Simulate waiting for the model
        with st.chat_message("assistant"):
            status = st.empty()
            status.status("Sending request...", state="running")
            time.sleep(1)  # Simulate waiting for the model
            
            # Start the stream for assistant's response
            stream = client.chat(
                model=selected_model,
                messages=[{'role': 'user', 'content': prompt}],
                stream=True,
            )
            logging.info(f"Chat request sent to model: {selected_model}")
            
            # Display status update while receiving the response
            status.write("Receiving response...")
            
            # Update status to "Complete" after the response is received
            status.update(label="Response complete!", state="complete")
            time.sleep(1)  # Simulate waiting for the response
        
        # Display assistant response in chat message container
        
            response_text = ""
            response_placeholder = status.empty()  # Placeholder for the streaming response
            
            for chunk in stream:
                response_text += chunk['message']['content']
                response_placeholder.markdown(response_text)  # Update the placeholder with new content
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        logging.info(f"Model response received: {response_text}")

    except Exception as e:
        logging.error(f"Error during model interaction: {e}")
        st.error("An error occurred while processing your request. Please try again.")

# Log app exit
logging.info("Streamlit app execution ended.")
