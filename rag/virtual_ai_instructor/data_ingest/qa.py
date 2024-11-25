"""
Script to store question/answer pairs from each transcript in the SQLite database table qa. 
We create a new table qa with the following schema: 
- qa
    - id (primary key that is generated)
    - doc_id (id of the root document this qa comes from in the document table)
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
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    FOREIGN KEY (doc_id) REFERENCES document (id)
)
''')
conn.commit()

# Fetch all transcripts from the document table
cursor.execute('SELECT id, raw_text FROM document')
documents = cursor.fetchall()

# Prompt for qa
# Read the prompt from the file
prompt_file = "prompts/qa.txt"
with open(prompt_file, 'r') as file:
    user_prompt = file.read().strip()

# QA fetching function using GPT-4
def get_qa_pairs(raw_text):
    print("Fetching QA pairs..")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"{user_prompt}\n{raw_text}"}
        ]
    )
    qa_pairs = response.choices[0].message.content
    print("Fetched QA pairs")
    return qa_pairs

for doc_id, raw_text in documents[:5]:
    print(f"Processing document ID: {doc_id}")

    # Get the qa pairs from the document
    # Get QA pairs using GPT-4
    qa_pairs = get_qa_pairs(raw_text)
    try:
        qa_pairs = json.loads(qa_pairs.replace("```json", "").replace("```", ""))
    except json.JSONDecodeError:
        continue

    for pair in qa_pairs:
        print(f"QA pair: {pair}")
        question = pair.get("question")
        answer = pair.get("answer")

        if question and answer:
            # Insert the qa pair into the database
            cursor.execute('''
            INSERT INTO qa (id, doc_id, question, answer)
            VALUES (?, ?, ?, ?)
            ''', (str(uuid.uuid4()), doc_id, question, answer))
    
    print(f"Finished processing document ID: {doc_id}")

# Commit changes and close the database connection
conn.commit()

# Print the contents of the qa table
print("\nQA Table Contents:")
cursor.execute('SELECT id, doc_id, question, answer FROM qa')
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Doc ID: {row[1]}, Question: {row[2]}, Answer: {row[3]}")  # Truncate text for readability

# Close the database connection
conn.close()

print(f"\nQA completed and saved to {db_file}.")
