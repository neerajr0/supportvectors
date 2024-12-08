"""
Main methods to retrieve query results
from our Qdrant collection and generate a
plausible response
"""

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Qdrant setup
QDRANT_HOST = "localhost"  # Replace with your Qdrant instance address
QDRANT_PORT = 6333         # Default port for Qdrant

# Initialize Qdrant client
qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Embedding model setup (using SentenceTransformers as an example)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Replace with your desired model

def retrieve_results(query: str, collection_option: str):

     # Generate vector for the user query
    query_vector = embedding_model.encode(query).tolist()
    
    # Perform a similarity search in Qdrant
    search_results = qdrant_client.search(
        collection_name=collection_option,
        query_vector=query_vector,
        limit=5,  # Return top 5 results
    )

    return search_results

def generate_response(query, query_result):
    """
    Given the query and the query result fetched from Qdrant,
    generate a response that answers the query using the 
    info in the query result.

    Fields in the query_result object that might be useful:
    chunk_text
    chunk_summary
    question
    answer
    term
    definition

    Implement using an LLM like Ollama or GPT-4.
    """
    pass
        