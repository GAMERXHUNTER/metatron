# VaultEnhancer_AI.py (Structured 11-Section Extractor - gpt-3.5-turbo)

import os
import re
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

VAULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Vault"))
CHUNK_SIZE = 6000
SECTIONS = [
    "Key Ideas", "Philosophy", "Psychology", "Strategy", "Methodology",
    "Process", "How-To Guide", "Impactful Quotes", "Mental Models", "Pitfalls / Don'ts", "Target Audience"
]

def find_target_files(extension=".md"):
    return [
        os.path.join(root, f)
        for root, _, files in os.walk(VAULT_DIR)
        for f in files
        if f.endswith(extension) and not any(x in f for x in ["_enhanced"])
    ]

def chunk_content(content, chunk_size=CHUNK_SIZE):
    return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

def build_prompt(chunk):
    return f"""
You are an AI that extracts structured knowledge from business, marketing, or productivity transcripts and essays.

Extract the following 11 sections in clean Markdown format:

1. Key Ideas  
2. Philosophy  
3. Psychology  
4. Strategy  
5. Methodology  
6. Process  
7. How-To Guide  
8. Impactful Quotes  
9. Mental Models  
10. Pitfalls / Don'ts  
11. Target Audience

Focus on actionable insights and intellectual depth. Be specific. Group information under each header clearly.

--- START OF CONTENT ---

{chunk}

--- END OF CONTENT ---
"""

def run_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response.choices[0].message.content.strip()

def enhance_file(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    chunks = chunk_content(content)
    outputs = []

    for i, chunk in enumerate(chunks):
        try:
            print(f"🧠 Enhancing chunk {i+1}/{len(chunks)} for file: {os.path.basename(fpath)}")
            prompt = build_prompt(chunk)
            result = run_gpt(prompt)
            outputs.append(result)
        except Exception as e:
            print(f"[ERROR] Chunk {i+1} failed: {e}")

    combined_output = "\n\n---\n\n".join(outputs)
    output_path = os.path.splitext(fpath)[0] + "_enhanced.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Enhanced Knowledge Summary\n\n")
        f.write(combined_output)

    print(f"[SAVED] {output_path}")

def enhance_all_files():
    files = find_target_files(".md")
    print(f"[INFO] Found {len(files)} files to enhance.")
    for fpath in files:
        try:
            enhance_file(fpath)
        except FileNotFoundError:
            print(f"[SKIPPED] File not found: {fpath}")
    print("\n✅ Vault enhancement (11-section) complete.")

if __name__ == "__main__":
    enhance_all_files()
