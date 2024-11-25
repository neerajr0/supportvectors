import sqlite3
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer  # Example embedding model

# Qdrant setup
QDRANT_HOST = "localhost"  # Replace with your Qdrant instance address
QDRANT_PORT = 6333         # Default port for Qdrant
COLLECTION_NAME = "abstractive_summary"

# Initialize Qdrant client
qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Embedding model setup (using SentenceTransformers as an example)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Replace with your desired model

# Ensure the Qdrant collection exists
VECTOR_SIZE = 384  # Adjust based on the embedding model used
qdrant_client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.DOT)
)

# SQLite database setup
db_file = "data_ingest.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Fetch all chunks from the abstractive_summary table
cursor.execute('SELECT id, doc_id, parent_chunk_id, sequence_id, chunk_text FROM abstractive_summary')
chunks = cursor.fetchall()

# Vectorize and upload to Qdrant
for chunk_id, doc_id, parent_chunk_id, sequence_id, chunk_text in chunks:
    print(f"Processing chunk ID: {chunk_id}")
    
    # Generate the vector representation of the chunk
    chunk_vector = embedding_model.encode(chunk_text).tolist()
    
    # Create a Qdrant point
    point = PointStruct(
        id=chunk_id,  # Use the chunk ID as the point ID
        vector=chunk_vector,
        payload={
            "chunk_id": chunk_id,
            "document_id": doc_id,
            "parent_chunk_id": parent_chunk_id,
            "sequence_id": sequence_id,
            "chunk_text": chunk_text  # Optionally store the text in Qdrant
        }
    )
    
    # Upload the point to Qdrant
    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=[point])

# Fetch all QA pairs from the qa table
cursor.execute('SELECT id, doc_id, question, answer FROM qa')
qa = cursor.fetchall()
# Vectorize and upload to Qdrant
for qa_id, doc_id, question, answer in qa:
    print(f"Processing QA ID: {qa_id}")
    
    # Generate the vector representation of the chunk
    qa_vector = embedding_model.encode(question + " " + answer).tolist()
    
    # Create a Qdrant point
    point = PointStruct(
        id=qa_id,  # Use the chunk ID as the point ID
        vector=qa_vector,
        payload={
            "chunk_id": qa_id,
            "document_id": doc_id,
            "question": question,
            "answer": answer,
        }
    )
    
    # Upload the point to Qdrant
    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=[point])

# Fetch all glossary pairs from the glossary table
# cursor.execute('SELECT id, doc_id, term, definition FROM glossary')
# glossary = cursor.fetchall()
# # Vectorize and upload to Qdrant
# for glossary_id, doc_id, term, definition in glossary:
#     print(f"Processing glossary ID: {glossary_id}")
    
#     # Generate the vector representation of the chunk
#     glossary_vector = embedding_model.encode(term + " " + definition).tolist()
    
#     # Create a Qdrant point
#     point = PointStruct(
#         id=glossary_id,  # Use the chunk ID as the point ID
#         vector=glossary_vector,
#         payload={
#             "chunk_id": glossary_id,
#             "document_id": doc_id,
#             "term": term,
#             "definition": definition,
#         }
#     )
    
#     # Upload the point to Qdrant
#     qdrant_client.upsert(collection_name=COLLECTION_NAME, points=[point])

print(f"All chunks have been vectorized and uploaded to the Qdrant collection '{COLLECTION_NAME}'.")

# Close the database connection
conn.close()
