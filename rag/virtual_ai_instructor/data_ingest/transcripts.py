"""
Script to ingest every transcript into a SQLite database with the following schema:
- Document table:
    - id (primary_key, can extract from file name which contains unique id)
    - title (transcript file title)
    - youtube_id (optional)
    - raw_text (transcript text)
"""

import os
import sqlite3
import re

# Directory containing the transcript files
directory = "./only_transcript"

# SQLite database file name
db_file = "data_ingest.db"

# Create SQLite database and table
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS document (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    raw_text TEXT NOT NULL
)
''')
conn.commit()

# Helper function to extract the id from the file name
def extract_id(file_name):
    match = re.search(r"\[([^\]]+)\]_transcript\.txt$", file_name)
    return match.group(1) if match else None

# Process each .txt file in the directory
for file_name in os.listdir(directory):
    if file_name.endswith("_transcript.txt"):
        file_path = os.path.join(directory, file_name)
        
        # Extract the id from the file name
        doc_id = extract_id(file_name)
        if not doc_id:
            print(f"Skipping {file_name}: Unable to extract id.")
            continue

        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()

        # Insert data into the database
        cursor.execute('''
        INSERT OR IGNORE INTO document (id, title, raw_text)
        VALUES (?, ?, ?)
        ''', (doc_id, file_name, raw_text))
        print(f"Inserted {file_name} into the database.")

# Commit changes and close the connection
conn.commit()

# Print the contents of the database
print("\nDatabase contents:")
cursor.execute('SELECT id, title, raw_text FROM document')
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Title: {row[1]}, Raw Text: {row[2][:100]}...")  # Truncate raw_text for readability

# Close the connection
conn.close()

print(f"\nDatabase {db_file} created and populated successfully.")

