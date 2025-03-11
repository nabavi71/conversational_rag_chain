from pydantic import BaseModel
from typing import Union


class WeaviateConfig(BaseModel):
    weaviate_host: str = "your_weaviate_host"
    weaviate_port: Union[str, int] = "your_weaviate_port"
    weaviate_api_key: str = "your_weaviate_api_key"

class LlmConfig(BaseModel):
    ollama_host: str
    ollama_port: Union[str, int]
    model_name: str

class QaConfig(BaseModel):
    query: str