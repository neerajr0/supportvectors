"""
Script to store question/answer pairs from each chunk in the SQLite database table qa.
We create a new table qa with the following schema: 
- qa
    - id (primary key that is generated)
    - doc_id (id of the root document this qa comes from in the document table)
    - chunk_id (chunk_id that this qa pair corresponds to)
    - question
    - answer
"""

import sqlite3
import uuid
from openai import OpenAI
import json

# OpenAI client
client = OpenAI()

# Database file
db_file = "data_ingest.db"

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create the qa table
cursor.execute('''
CREATE TABLE IF NOT EXISTS qa (
    id TEXT PRIMARY KEY,
    doc_id TEXT NOT NULL,
    chunk_id TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    FOREIGN KEY (doc_id) REFERENCES document (id)
)
''')
conn.commit()

# Fetch all chunks from the abstractive_summary
cursor.execute('SELECT id, doc_id, chunk_summary FROM abstractive_summary')
chunks = cursor.fetchall()

# Prompt for qa
# Read the prompt from the file
prompt_file = "prompts/qa.txt"
with open(prompt_file, 'r') as file:
    user_prompt = file.read().strip()

# QA fetching function using GPT-4
def get_qa_pair(raw_text):
    print("Fetching QA pair..")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"{user_prompt}\n{raw_text}"}
        ]
    )
    qa_pair = response.choices[0].message.content
    print("Fetched QA pair")
    return qa_pair

for chunk_id, doc_id, chunk_summary in chunks:
    print(f"Processing document ID: {doc_id}")

    # Get the qa pairs from the chunk
    # Get QA pairs using GPT-4
    qa_pair = get_qa_pair(chunk_summary)
    try:
        qa_pair = json.loads(qa_pair.replace("```json", "").replace("```", ""))
    except json.JSONDecodeError:
        continue

    question = qa_pair.get("question")
    answer = qa_pair.get("answer")

    if question and answer:
        # Insert the qa pair into the database
        cursor.execute('''
        INSERT INTO qa (id, doc_id, chunk_id, question, answer)
        VALUES (?, ?, ?, ?)
        ''', (str(uuid.uuid4()), doc_id, chunk_id, question, answer))
    
    print(f"Finished processing document ID: {doc_id}")

# Commit changes and close the database connection
conn.commit()

# Print the contents of the qa table
print("\nQA Table Contents:")
cursor.execute('SELECT id, doc_id, chunk_id, question, answer FROM qa')
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Doc ID: {row[1]}, Chunk ID: {row[2]}, Question: {row[3]}, Answer: {row[4]}")  # Truncate text for readability

# Close the database connection
conn.close()

print(f"\nQA completed and saved to {db_file}.")
