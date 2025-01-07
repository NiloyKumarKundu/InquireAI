import streamlit as st
from ollama import chat
from ollama import ChatResponse


# Streamlit app
st.title("Multi-Model LLM Question Answering App")
st.markdown("""
This app allows you to interact with multiple LLMs simultaneously. 
Choose from the available models, ask a question, and compare the answers!
""")

# Sidebar for model selection
# st.sidebar.header("Model Selection")
available_models = ["llama3.2", "smollm"]  # Update with your models
selected_model = st.selectbox("Choose Models", available_models, placeholder="Choose an option", index=0)

# Input for question
question = st.text_input("Enter your question:", placeholder="Type your question here...")

# Submit button
if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    elif not selected_model:
        st.warning("Please select at least one model.")
    else:
        # Display the responses
        st.write("### Responses:")
        # for model in selected_models:
            
        st.write(f"**{selected_model}**:")
        
        # Display a placeholder for streaming output
        response_placeholder = st.empty()
        response_text = ""
        try:
            # Send the question to the selected model
            stream = chat(
                model='llama3.2',
                messages=[{'role': 'user', 'content': question}],
                stream=True,
            )
            

            for chunk in stream:
                response_text += chunk['message']['content']
                response_placeholder.write(response_text)
            # st.success(response['message']['content'])
        except Exception as e:
            st.error(f"Error with model {selected_model}: {str(e)}")
