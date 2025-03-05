import os
from models.models import LlmConfig
from rag_utils.historical_chatBot import ChatbotRAG

llm_config = LlmConfig(
    ollama_host = os.environ.get("OLLAMA_HOST"),
    ollama_port = os.environ.get("OLLAMA_PORT"),
    model_name = os.environ.get("MODEL_NAME"))

chatbot = ChatbotRAG(llm_config)
