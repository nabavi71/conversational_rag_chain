from pydantic import BaseModel
from typing import Union


class WeaviateConfig(BaseModel):
    weaviate_host: str = "192.168.13.198"
    weaviate_port: Union[str, int] = "9191"
    weaviate_api_key: str = "hfz-ai-TheBert2022"

class LlmConfig(BaseModel):
    ollama_host: str
    ollama_port: Union[str, int]
    model_name: str

class QaConfig(BaseModel):
    query: str