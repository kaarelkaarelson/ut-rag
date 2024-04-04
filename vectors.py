import logging
import sys
import os

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import Settings

def create_storage(client):
    
    documents = SimpleDirectoryReader("./docs").load_data()

    vector_store = QdrantVectorStore(client=client, collection_name="docs_vectors")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        distance=Distance.COSINE
    )
    return index

def prompt(index, query):
    query_engine = index.as_query_engine(k=5)
    response = query_engine.query(query)
    print(response)


if __name__ == '__main__':
    client = QdrantClient("localhost", port=6333)


    Settings.embed_model = OpenAIEmbedding(model = 'text-embedding-ada-002', api_key = openai_api_key)
    Settings.llm = OpenAI(model= 'gpt-3.5-turbo', api_key=openai_api_key)

    #create_storage(client)
    #print("Complete!")
    #client.delete_collection(collection_name="docs_vectors")
    index = VectorStoreIndex.from_documents(SimpleDirectoryReader(input_dir="qdrant_storage/collections/docs_vectors").load_data())
    query = "Mis on Tartu Ülikooli õppimisvõimalused?"
    prompt(index, query)
    
    #new_prompt = "Mis teleskoope kasutatakse"
    #query_vector = encode_prompt(new_prompt)
    #results = query_collection(query_vector, top_k=5)    
    #query_collection()
    
    #a = client.get_collection(collection_name="doc_vecs")#client.delete_collection(collection_name="doc_vec")#
    #print(a)
