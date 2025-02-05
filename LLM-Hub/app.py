import streamlit as st
from ollama import Client
import logging
from datetime import datetime
import os
import ssl
import time
# from langchain_ollama.llms import OllamaLLM
from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import trim_messages
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ['LANGCHAIN_TRACING_V2'] = "true"

# ssl._create_default_https_context = ssl._create_unverified_context

store = {}
config = {
    'configurable': {
        'session_id': 'first_chat'
    }
}
# messages = []


# Set up logging
def set_log():
    log_dir = "/app/logs"
    os.makedirs(log_dir, exist_ok=True)  # Ensure the logs directory exists
    log_file = os.path.join(log_dir, f"app_log_{datetime.now().strftime('%Y%m%d')}.log")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

def get_prompt():
    prompt_template = ChatPromptTemplate([
        ("system", "You are a chatbot name MLHub.space. Answer all questions to the best of your ability."),
        ('human', 'What is up?'),
        ('assistant','I am a chatbot. I am here to help you. How can I help you today?'),
        MessagesPlaceholder(variable_name='messages'),
    ])
    return prompt_template



def get_model():
    # Load the model
    try:
        llm = ChatOllama(
            model="llama3.2",
            convert_system_message_to_human=True
        )
        return llm
    except Exception as e:
        logging.error(f"Failed to load model: {e}")
        print("error")

def get_trimmer():
    trimmer = trim_messages(
        max_tokens=10000,
        strategy="last",
        token_counter=get_model(),
        include_system=True,
        allow_partial=False,
        start_on='human'
    )
    
    return trimmer


def get_chain():
    llm = get_model()
    output_parser = StrOutputParser()
    prompt = get_prompt()
    trimmer = get_trimmer()
    
    chain = (
        RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer) | 
        prompt | 
        llm | 
        output_parser
        )
    return chain

        

def pipeline():
    while True:    
        user_input = input("Write here...\n")
        if user_input == "exit":
            break
        
        chain = get_chain()
        
        # response = chain.invoke({'messages':user_input}, config=config)
        
        model_with_history = RunnableWithMessageHistory(chain, get_session_history, input_messages_key='messages')
        
        response = model_with_history.invoke({'messages': user_input}, config)
        print(model_with_history.astream(input=response, config=config))
    print(store)
    return response        

def run():
    pipeline()
            

        
if __name__ == "__main__":
    # set_log()
    run()

# Streamlit app
# st.set_page_config(page_title="MlHub", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
# st.title("Multi-Model LLM Question Answering App")

# st.markdown("""
# This app allows you to interact with multiple LLMs simultaneously. 
# Choose from the available models, ask a question, and compare the answers!
# """)

# # Sidebar for model selection
# available_models = ["llama3.2", "smollm2", "mistral", "deepseek-v3", "deepseek-r1"]  # Update with your models
# selected_model = st.sidebar.selectbox("Choose Model", available_models, placeholder="Choose an option", index=4)

# if selected_model == "deepseek-v3":
#     selected_model = "nezahatkorkmaz/deepseek-v3"
    
# logging.info(f"User selected model: {selected_model}")

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # React to user input
# if prompt := st.chat_input("What is up?"):
#     logging.info(f"User input received: {prompt}")

#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})
    
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
    
#     try:
#         # Show status updates while processing
#         # with st.status("Sending request...", expanded=True, state="running") as status:
#         #     status.write("Searching for model...")
#         #     time.sleep(1)  # Simulate waiting for the model
#         with st.chat_message("assistant"):
#             status = st.empty()
#             status.status("Sending request...", state="running")
#             time.sleep(1)  # Simulate waiting for the model
            
#             # Handle Conversation History
#             conversation_history = ""
#             for message in st.session_state.messages:
#                 conversation_history += f"{message['role']}: {message['content']} \n"
            
#             # Start the stream for assistant's response
#             stream = client.chat(
#                 model=selected_model,
#                 messages=[{'role': 'user', 'content': conversation_history}],
#                 stream=True,
#             )
#             logging.info(f"Chat request sent to model: {selected_model}")
            
#             # Display status update while receiving the response
#             status.status("Receiving response...")
            
#             # Update status to "Complete" after the response is received
#             status.status(label="Response complete!", state="complete")
#             time.sleep(1)  # Simulate waiting for the response
        
#             # Display assistant response in chat message container
#             response_text = ""
#             response_placeholder = status.empty()  # Placeholder for the streaming response
            
#             for chunk in stream:
#                 response_text += chunk['message']['content']
#                 response_placeholder.markdown(response_text)  # Update the placeholder with new content
        
#         # Add assistant response to chat & conversation history
#         conversation_history += f"'assistant': {response_text} \n"
#         st.session_state.messages.append({"role": "assistant", "content": response_text})
#         logging.info(f"Model response received: {response_text}")
#         logging.info(f"Conversation history: {conversation_history}")

#     except Exception as e:
#         logging.error(f"Error during model interaction: {e}")
#         st.error("An error occurred while processing your request. Please try again.")

# # Log app exit
# logging.info("Streamlit app execution ended.")
