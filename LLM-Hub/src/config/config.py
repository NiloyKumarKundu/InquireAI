import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration for API keys and environment settings
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGCHAIN_TRACING_V2 = "true"

# Session-related settings
SESSION_ID = 'first_chat'
