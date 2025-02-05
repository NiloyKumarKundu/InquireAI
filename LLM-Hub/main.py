import time
import asyncio
import streamlit as st
from src.Services.chatbot import chatbot
from src import logger


def render_chat_history() -> None:
    """
    Renders the session chat history in the Streamlit app.
    """
    history = chatbot.get_session_history()
    for message in history.messages:
        if message.type == "human":
            with st.chat_message("human"):
                st.markdown(message.content)
        elif message.type == "ai":
            with st.chat_message("ai"):
                st.markdown(message.content)


async def stream_response(user_prompt: str, placeholder: st.delta_generator.DeltaGenerator) -> None:
    """
    Asynchronously streams response chunks from the chatbot and updates the UI placeholder.

    Args:
        user_prompt: The input prompt provided by the user.
        placeholder: The Streamlit placeholder to update with the streamed response.
    """
    response_text = ""
    # Iterate over the asynchronous stream of response chunks from the chatbot.
    async for chunk in chatbot.process_input_streaming(user_prompt):
        response_text += chunk
        placeholder.markdown(response_text)
        # Optional: introduce a small delay to simulate a realistic streaming effect.
        await asyncio.sleep(0.02)


def run_async_function(coro) -> None:
    """
    Runs an asynchronous coroutine in a new event loop.

    Args:
        coro: A callable that returns an awaitable coroutine.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(coro())
    finally:
        loop.close()


def reset_session() -> None:
    """
    Resets the chatbot session and refreshes the Streamlit app.
    
    It is assumed that the chatbot has a method `reset_session()` to clear the session.
    After resetting, the app is rerun to reflect the changes.
    """
    logger.info("Resetting chat session...")
    chatbot.reset_session()  # Ensure this method exists in your chatbot module.
    st.experimental_rerun()



def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)




def main() -> None:
    """
    Main function for the Multi-Model LLM Question Answering App.
    
    Sets up the Streamlit page configuration, displays the chat interface,
    handles user input, and streams responses from the chatbot.
    """
    # Configure the Streamlit page
    st.set_page_config(
        page_title="MlHub",
        page_icon=None,
        layout="centered",
        initial_sidebar_state="auto",
    )
    st.title("Multi-Model LLM Question Answering App")
    st.markdown(
        """
        This app allows you to interact with multiple LLMs simultaneously. 
        Choose from the available models, ask a question, and compare the answers!
        """
    )

    # Sidebar: model selection
    available_models = ["llama3.2", "smollm2", "mistral", "deepseek-v3", "deepseek-r1"]
    selected_model = st.sidebar.selectbox(
        "Choose Model",
        available_models,
        placeholder="Choose an option",
        index=4
    )
    # Map model name if necessary
    if selected_model == "deepseek-v3":
        selected_model = "nezahatkorkmaz/deepseek-v3"
    logger.info(f"User selected model: {selected_model}")
    
    local_css("src/css/style.css")
    
    with st.sidebar:
        st.button("button sidebar 1")
    

    # Display existing chat history
    render_chat_history()

    # Get user input from the chat interface
    user_prompt = st.chat_input("What is up?")
    if user_prompt:
        logger.info(f"User input received: {user_prompt}")
        # Render the user's message
        with st.chat_message("human"):
            st.markdown(user_prompt)

        # Stream the AI's response in real time
        with st.chat_message("ai"):
            message_placeholder = st.empty()
            run_async_function(lambda: stream_response(user_prompt, message_placeholder))



if __name__ == "__main__":
    main()
