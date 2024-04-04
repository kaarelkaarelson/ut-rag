import logging
import sys
import os


from qdrant_client import QdrantClient

from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings
import vectors
from qdrant_client import QdrantClient
if __name__ == '__main__':

    client = QdrantClient("localhost", port=6333)


    Settings.embed_model = OpenAIEmbedding(model = 'text-embedding-ada-002', api_key = openai_api_key)
    Settings.llm = OpenAI(model= 'gpt-3.5-turbo', api_key=openai_api_key)

    #create_storage(client)
    #print("Complete!")
    #client.delete_collection(collection_name="docs_vectors")
    index = VectorStoreIndex.from_documents(SimpleDirectoryReader(input_dir="qdrant_storage/collections/docs_vectors").load_data())
    query = "Mis teleskoope kasutatakse Tartu Ülikoolis?"
    vectors.prompt(index, query)
