"""
Script to store glossary terms from each transcript in the SQLite database table glossary. 
We create a new table glossary with the following schema: 
- glossary
    - id (primary key that is generated)
    - doc_id (id of the root document this glossary term comes from in the document table)
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
    term TEXT NOT NULL,
    definition TEXT NOT NULL,
    FOREIGN KEY (doc_id) REFERENCES document (id)
)
''')
conn.commit()

# Fetch all transcripts from the document table
cursor.execute('SELECT id, raw_text FROM document')
documents = cursor.fetchall()

# Prompt for glossary
# Read the prompt from the file
prompt_file = "prompts/glossary.txt"
with open(prompt_file, 'r') as file:
    user_prompt = file.read().strip()

# glossary fetching function using GPT-4
def get_glossary_terms(raw_text):
    print("Fetching glossary terms..")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"{user_prompt}\n{raw_text}"}
        ]
    )
    glossary_pairs = response.choices[0].message.content
    print("Fetched glossary pairs")
    return glossary_pairs

for doc_id, raw_text in documents[:5]:
    print(f"Processing document ID: {doc_id}")

    # Get the glossary from the document
    # Get glossary pairs using GPT-4
    glossary_pairs = get_glossary_terms(raw_text)
    try:
        glossary_pairs = json.loads(glossary_pairs.replace("```json", "").replace("```", ""))
    except json.JSONDecodeError:
        continue

    for glossary_pair in glossary_pairs:
        term = glossary_pair.get("term")
        definition = glossary_pair.get("definition")

        if term and definition:
            # Insert the glossary pair into the database
            cursor.execute('''
            INSERT INTO glossary (id, doc_id, term, definition)
            VALUES (?, ?, ?, ?)
            ''', (str(uuid.uuid4()), doc_id, term, definition))
    
    print(f"Finished processing document ID: {doc_id}")

# Commit changes and close the database connection
conn.commit()

# Print the contents of the glossary table
print("\nGlossary Table Contents:")
cursor.execute('SELECT id, doc_id, term, definition FROM glossary')
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Doc ID: {row[1]}, Term: {row[2]}, Definition: {row[3]}")  # Truncate text for readability

# Close the database connection
conn.close()

print(f"\nglossary completed and saved to {db_file}.")
