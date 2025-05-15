# PDFVaultImporter.py
# Purpose: Extract text from PDF files, clean it, split into logical chunks, and save to the Vault.

import os
import datetime
import sqlite3
from PyPDF2 import PdfReader

PDF_DIR = "./TabernacleEmpire/Raw"
VAULT_DIR = "./TabernacleEmpire/Vault/PDFs"
DB_PATH = "./TabernacleEmpire/Index/vault_index.db"

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

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    all_text = ""
    for page in reader.pages:
        try:
            text = page.extract_text()
            if text:
                all_text += text + "\n\n"
        except Exception as e:
            print(f"Error reading page: {e}")
    return all_text

def tag_file_with_ai(content):
    # Placeholder for future GPT tagging
    return {
        "source": "PDF",
        "category": "General",
        "subtopic": "Untitled"
    }

def save_all_formats(content, tags, filename_base):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    subfolder = os.path.join(VAULT_DIR, filename_base)
    os.makedirs(subfolder, exist_ok=True)

    # Save .md
    md_path = os.path.join(subfolder, f"{filename_base}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {tags['subtopic']}{content}")

    # Save .json
    json_path = os.path.join(subfolder, f"{filename_base}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"tags": tags, "content": content}, f, indent=2)

    # Save .txt
    txt_path = os.path.join(subfolder, f"{filename_base}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(content)

    for format, path in zip(["md", "json", "txt"], [md_path, json_path, txt_path]):
        index_file(filename_base, tags, format, path)

def index_file(filename, tags, format, path):
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
        format,
        path,
        datetime.datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def process_pdfs():
    for fname in os.listdir(PDF_DIR):
        if fname.endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIR, fname)
            print(f"📖 Processing: {fname}")
            content = extract_text_from_pdf(pdf_path)
            cleaned = content.replace("\n", " ").strip()
            tags = tag_file_with_ai(cleaned)
            filename_base = os.path.splitext(fname)[0]
            save_all_formats(cleaned, tags, filename_base)

if __name__ == "__main__":
    initialize_database()
    process_pdfs()
    print("✅ PDF Import Complete.")

import subprocess
base_path = os.path.dirname(__file__)
subprocess.run(["python", "VaultProcessor_AI.py"], cwd=base_path)
subprocess.run(["python", "VaultEnhancer_AI.py"], cwd=base_path)
