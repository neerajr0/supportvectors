"""
Script to store glossary terms from each transcript in the SQLite database table glossary. 
We create a new table glossary with the following schema: 
- glossary
    - id (primary key that is generated)
    - doc_id (id of the root document this glossary term comes from in the document table)
    - chunk_id (chunk_id that this qa pair corresponds to)
    - term
    - definition
"""

import sqlite3
import uuid
from openai import OpenAI
import json

client = OpenAI()

# Database file
db_file = "data_ingest.db"

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create the glossary table
cursor.execute('''
CREATE TABLE IF NOT EXISTS glossary (
    id TEXT PRIMARY KEY,
    doc_id TEXT NOT NULL,
    chunk_id TEXT NOT NULL,
    term TEXT NOT NULL,
    definition TEXT NOT NULL,
    FOREIGN KEY (doc_id) REFERENCES document (id)
)
''')
conn.commit()

# Fetch all chunks from the abstractive_summary
cursor.execute('SELECT id, doc_id, chunk_summary FROM abstractive_summary')
chunks = cursor.fetchall()

# Prompt for glossary
# Read the prompt from the file
prompt_file = "prompts/glossary.txt"
with open(prompt_file, 'r') as file:
    user_prompt = file.read().strip()

# glossary fetching function using GPT-4
def get_glossary_term(raw_text):
    print("Fetching glossary term..")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"{user_prompt}\n{raw_text}"}
        ]
    )
    glossary_pairs = response.choices[0].message.content
    print("Fetched glossary pair")
    return glossary_pairs

for chunk_id, doc_id, chunk_summary in chunks:
    print(f"Processing document ID: {doc_id}")

    # Get the glossary from the chunk
    # Get glossary pairs using GPT-4
    glossary_pair = get_glossary_term(chunk_summary)
    try:
        glossary_pair = json.loads(glossary_pair.replace("```json", "").replace("```", ""))
    except json.JSONDecodeError:
        continue

    term = glossary_pair.get("term")
    definition = glossary_pair.get("definition")

    if term and definition:
        # Insert the glossary pair into the database
        cursor.execute('''
        INSERT INTO glossary (id, doc_id, chunk_id, term, definition)
        VALUES (?, ?, ?, ?)
        ''', (str(uuid.uuid4()), doc_id, chunk_id, term, definition))
    
    print(f"Finished processing document ID: {doc_id}")

# Commit changes and close the database connection
conn.commit()

# Print the contents of the glossary table
print("\nGlossary Table Contents:")
cursor.execute('SELECT id, doc_id, chunk_id, term, definition FROM glossary')
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Doc ID: {row[1]}, Chunk ID: {row[2]}, Term: {row[3]}, Definition: {row[4]}")  # Truncate text for readability

# Close the database connection
conn.close()

print(f"\nglossary completed and saved to {db_file}.")
