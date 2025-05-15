# VaultProcessor_AI.py
# Auto-triggering vault processor to clean and structure raw content from all sources

import os
import json
import sqlite3
import datetime

RAW_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Vault", "Raw"))
VAULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Vault"))
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Vault", "Index", "vault_index.db"))

def initialize_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vault_index (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        source TEXT,
        category TEXT,
        subtopic TEXT,
        format TEXT,
        path TEXT,
        created_at TEXT
    )
    ''')
    conn.commit()
    conn.close()

def tag_file_with_ai(content):
    # Simulated tagger - replace with GPT when ready
    return {
        "source": "Reddit" if "reddit" in content.lower() else "YouTube",
        "category": "Business",
        "subtopic": "General Insights"
    }

def clean_text(text):
    return text.replace("\n", " ").strip()

def save_all_formats(content, tags, filename_base):
    subfolder = os.path.join(VAULT_DIR, tags["source"], tags["category"], tags["subtopic"])
    os.makedirs(subfolder, exist_ok=True)

    md_path = os.path.join(subfolder, f"{filename_base}.md")
    json_path = os.path.join(subfolder, f"{filename_base}.json")
    txt_path = os.path.join(subfolder, f"{filename_base}.txt")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# {}\n\n{}".format(tags['subtopic'], content))


    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"tags": tags, "content": content}, f, indent=2)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(content)

    for fmt, path in zip(["md", "json", "txt"], [md_path, json_path, txt_path]):
        index_file(filename_base, tags, fmt, path)

def index_file(filename, tags, fmt, path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO vault_index (filename, source, category, subtopic, format, path, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        filename,
        tags["source"],
        tags["category"],
        tags["subtopic"],
        fmt,
        path,
        datetime.datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def process_raw_files():
    for fname in os.listdir(RAW_DIR):
        if fname.endswith(".txt") or fname.endswith(".md"):
            with open(os.path.join(RAW_DIR, fname), "r", encoding="utf-8") as f:
                content = f.read()

            cleaned = clean_text(content)
            tags = tag_file_with_ai(cleaned)
            filename_base = os.path.splitext(fname)[0]
            save_all_formats(cleaned, tags, filename_base)

if __name__ == "__main__":
    initialize_database()
    process_raw_files()
    print("✅ Vault ingestion complete.")

import subprocess
subprocess.run(["python", "VaultEnhancer_AI.py"], cwd=os.path.dirname(__file__))
