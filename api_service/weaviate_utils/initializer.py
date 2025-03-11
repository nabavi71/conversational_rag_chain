import os
from models.models import WeaviateConfig
from weaviate_utils.weaviateUtils import WeaviateConnect



weaviate_config = WeaviateConfig(
    weaviate_host = os.environ.get('WEAVIATE_HOST'),
    weaviate_port = os.environ.get('WEAVIATE_PORT'),
    weaviate_api_key = os.environ.get('WEAVIATE_API_KEY'))

weaviate_connect = WeaviateConnect(weaviate_config)
client = weaviate_connect.connect()
