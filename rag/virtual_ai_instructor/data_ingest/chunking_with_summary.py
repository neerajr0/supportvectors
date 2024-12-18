"""
Script to chunk every transcript SUMMARY in the SQLite database table chunking_with_summary. 
We create a new table abstractive_summary with the following schema: 
- abstractive_summary
    - id (primary key that is generated)
    - doc_id (id of the root document this chunk comes from in the document table)
    - parent_chunk_id (id of the parent chunk of this chunk)
    - sequence_id (id path from root to self)
    - chunk_text (the text of the chunk)
    - chunk_summary (the summarized text of the chunk using GPT-4)
"""

import sqlite3
import uuid
from semchunk import chunk
import tiktoken
from openai import OpenAI

# OpenAI client
client = OpenAI()

# Database file
db_file = "data_ingest.db"

# Chunking parameters
PARENT_CHUNK_SIZE = 1000
CHILD_CHUNK_SIZE = 200

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create the abstractive_summary table
cursor.execute('''
CREATE TABLE IF NOT EXISTS abstractive_summary (
    id TEXT PRIMARY KEY,
    doc_id TEXT NOT NULL,
    parent_chunk_id TEXT,
    sequence_id TEXT NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_summary TEXT NOT NULL,
    FOREIGN KEY (doc_id) REFERENCES document (id)
)
''')
conn.commit()

# Fetch all transcripts from the document table
cursor.execute('SELECT id, raw_text FROM document')
documents = cursor.fetchall()

# Create a function to pass to chunk that counts the number
# of tokens in a text
tiktoken_tokenizer = tiktoken.encoding_for_model('gpt-4o')
def tiktoken_token_counter(text: str) -> int:
    """Count the number of tokens in a text."""
    
    return len(tiktoken_tokenizer.encode(text))

# Prompt for summarization
# Read the prompt from the file
prompt_file = "prompts/abstractive_summary.txt"
with open(prompt_file, 'r') as file:
    user_prompt = file.read().strip()

# Summarization function using GPT-4
def summarize_text(raw_text):
    print("Summarizing text...")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"{user_prompt}\n{raw_text}"}
        ]
    )
    summary = response.choices[0].message.content
    print("Summary completed.")
    return summary

for doc_id, raw_text in documents:
    print(f"Processing document ID: {doc_id}")
    
    # Generate parent chunks
    parent_chunks = chunk(raw_text, chunk_size=PARENT_CHUNK_SIZE, token_counter=tiktoken_token_counter)
    
    for i, parent_chunk in enumerate(parent_chunks):
        # parent chunk is doc_id plus index of chunk so we can derive chunk order
        parent_chunk_id = doc_id + "#" + str(i)
        sequence_id = parent_chunk_id  # Root level has only its own ID

        # Summarize the chunk using GPT-4
        parent_chunk_summary = summarize_text(parent_chunk)
        
        # Insert the parent chunk into the database
        cursor.execute('''
        INSERT INTO abstractive_summary (id, doc_id, parent_chunk_id, sequence_id, chunk_text, chunk_summary)
        VALUES (?, ?, ?, ?, ?)
        ''', (parent_chunk_id, doc_id, None, sequence_id, parent_chunk, parent_chunk_summary))
        
        # Generate child chunks for the parent chunk
        child_chunks = chunk(parent_chunk, chunk_size=CHILD_CHUNK_SIZE, token_counter=tiktoken_token_counter)
        
        for j, child_chunk in enumerate(child_chunks):
            # child chunk is doc_id plus index of parent chunk plus index of child chunk
            child_chunk_id = parent_chunk_id + "#" + str(j)
            child_sequence_id = child_chunk_id

            child_chunk_summary = summarize_text(child_chunk)
            
            # Insert the child chunk into the database
            cursor.execute('''
            INSERT INTO abstractive_summary (id, doc_id, parent_chunk_id, sequence_id, chunk_text, chunk_summary)
            VALUES (?, ?, ?, ?, ?)
            ''', (child_chunk_id, doc_id, parent_chunk_id, child_sequence_id, child_chunk, child_chunk_summary))
    
    print(f"Finished processing document ID: {doc_id}")

# Commit changes and close the database connection
conn.commit()

# Print the contents of the abstractive_summary table
print("\nAbstractive Summary Table Contents:")
cursor.execute('SELECT id, doc_id, parent_chunk_id, sequence_id, chunk_text, chunk_summary FROM abstractive_summary')
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Doc ID: {row[1]}, Parent Chunk ID: {row[2]}, Sequence ID: {row[3]}, Chunk Text: {row[4][:50]}..., Chunk Text Summary: {row[5][:50]}")  # Truncate text for readability

# Close the database connection
conn.close()

print(f"\nAbstractive summary completed and saved to {db_file}.")
