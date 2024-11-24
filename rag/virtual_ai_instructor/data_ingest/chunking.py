"""
Script to chunk every transcript in the SQLite database table document. 
We create a new table semantic_chunking with the following schema: 
- semantic_chunks
    - id (primary key that is generated)
    - doc_id (id of the root document this chunk comes from in the document table)
    - parent_chunk_id (id of the parent chunk of this chunk)
    - sequence_id (id path from root to self)
    - chunk_text (the text of the chunk)
"""

import sqlite3
import uuid
from semchunk import chunk
import tiktoken

# Database file
db_file = "data_ingest.db"

# Chunking parameters
PARENT_CHUNK_SIZE = 1000
CHILD_CHUNK_SIZE = 100

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create the semantic_chunking table
cursor.execute('''
CREATE TABLE IF NOT EXISTS semantic_chunking (
    id TEXT PRIMARY KEY,
    doc_id TEXT NOT NULL,
    parent_chunk_id TEXT,
    sequence_id TEXT NOT NULL,
    chunk_text TEXT NOT NULL,
    FOREIGN KEY (doc_id) REFERENCES document (id)
)
''')
conn.commit()

# Fetch all transcripts from the document table
cursor.execute('SELECT id, raw_text FROM document')
documents = cursor.fetchall()

# Create a function to pass to chunk that counts the number
# of tokens in a text
tiktoken_tokenizer = tiktoken.encoding_for_model('gpt-4')
def tiktoken_token_counter(text: str) -> int:
    """Count the number of tokens in a text."""
    
    return len(tiktoken_tokenizer.encode(text))

for doc_id, raw_text in documents[:1]:
    print(f"Processing document ID: {doc_id}")
    
    # Generate parent chunks
    parent_chunks = chunk(raw_text, chunk_size=PARENT_CHUNK_SIZE, token_counter=tiktoken_token_counter)
    
    for i, parent_chunk in enumerate(parent_chunks):
        parent_chunk_id = str(uuid.uuid4())
        sequence_id = parent_chunk_id  # Root level has only its own ID
        
        # Insert the parent chunk into the database
        cursor.execute('''
        INSERT INTO semantic_chunking (id, doc_id, parent_chunk_id, sequence_id, chunk_text)
        VALUES (?, ?, ?, ?, ?)
        ''', (parent_chunk_id, doc_id, None, sequence_id, parent_chunk))
        
        # Generate child chunks for the parent chunk
        child_chunks = chunk(parent_chunk, chunk_size=CHILD_CHUNK_SIZE, token_counter=tiktoken_token_counter)
        
        for j, child_chunk in enumerate(child_chunks):
            child_chunk_id = str(uuid.uuid4())
            child_sequence_id = sequence_id + "#" + child_chunk_id  # Append to parent sequence ID
            
            # Insert the child chunk into the database
            cursor.execute('''
            INSERT INTO semantic_chunking (id, doc_id, parent_chunk_id, sequence_id, chunk_text)
            VALUES (?, ?, ?, ?, ?)
            ''', (child_chunk_id, doc_id, parent_chunk_id, child_sequence_id, child_chunk))
    
    print(f"Finished processing document ID: {doc_id}")

# Commit changes and close the database connection
conn.commit()

# Print the contents of the semantic_chunking table
print("\nSemantic Chunking Table Contents:")
cursor.execute('SELECT id, doc_id, parent_chunk_id, sequence_id, chunk_text FROM semantic_chunking')
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Doc ID: {row[1]}, Parent Chunk ID: {row[2]}, Sequence ID: {row[3]}, Chunk Text: {row[4][:50]}...")  # Truncate text for readability

# Close the database connection
conn.close()

print(f"\nSemantic chunking completed and saved to {db_file}.")
