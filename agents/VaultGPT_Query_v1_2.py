# VaultGPT_Query_v1_2.py
# GPT-4 Vault Query Tool v1.2 – Safe batching, markdown export, role-guided summarization

import os
import textwrap
import datetime
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

VAULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Vault"))
ANSWER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "VaultAnswers"))
os.makedirs(ANSWER_DIR, exist_ok=True)

MAX_TOKENS_PER_BATCH = 6000  # tokens, safe limit for GPT-4

def find_enhanced_files():
    return [
        os.path.join(root, f)
        for root, _, files in os.walk(VAULT_DIR)
        for f in files
        if f.endswith("_enhanced.md")
    ]

def estimate_tokens(text):
    return len(text.split()) * 1.3  # conservative estimate

def collect_safe_chunks(query, tag=None):
    chunks, total_tokens = [], 0
    for path in find_enhanced_files():
        fname = os.path.basename(path)
        if tag and tag.lower() not in fname.lower():
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        tokens = estimate_tokens(content)
        if total_tokens + tokens <= MAX_TOKENS_PER_BATCH:
            chunks.append((fname, content))
            total_tokens += tokens
    return chunks

def build_prompt(query, chunks, role=None):
    role_instruction = f"You are answering as {role}." if role else ""
    sources = "\n\n---\n\n".join([f"## {f}\n{c}" for f, c in chunks])
    return f"""{role_instruction}
Answer the following question based ONLY on the knowledge in the provided sources.
Include insight, bold ideas, strategy, and references to filenames if possible.

QUESTION: {query}

SOURCES:
{sources}
"""

def ask_gpt(query, chunks, role=None):
    prompt = build_prompt(query, chunks, role)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response.choices[0].message.content.strip()

def save_markdown(query, answer):
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fname = os.path.join(ANSWER_DIR, f"vault_answer_{ts}.md")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"# Vault Answer\n\n")
        f.write(f"**Question:** {query}\n\n")
        f.write(answer)
    print(f"📝 Saved to: {fname}")

def run_query_loop():
    print("🧠 VaultGPT v1.2 (GPT-4 Smart Mode)")
    while True:
        query = input("\n> ").strip()
        if query.lower() in ["exit", "quit"]:
            print("👋 Exiting VaultGPT.")
            break

        tag = input("📎 (Optional) Filter by tag in filename (or press Enter to skip): ").strip()
        role = input("🎭 (Optional) Answer as who? (e.g. Alex Hormozi, strategist, advisor): ").strip()

        print("🔍 Scanning vault...")
        chunks = collect_safe_chunks(query, tag)
        if not chunks:
            print("❌ No relevant files or too large for batching.")
            continue

        print(f"📂 Loaded {len(chunks)} files safely into GPT-4 context.")
        answer = ask_gpt(query, chunks, role)
        print("\n💬 GPT Response:")
        print(textwrap.fill(answer, width=100))
        save_markdown(query, answer)

        refine = input("\n🔁 Refine this answer? (Y/N): ").strip().upper()
        if refine == "Y":
            followup = input("Type your follow-up instruction: ").strip()
            combined = f"Previous Answer:\n{answer}\n\nNow, {followup}"
            refined = ask_gpt(combined, [], role)
            print("\n🔁 Refined Response:")
            print(textwrap.fill(refined, width=100))
            save_markdown(f"{query} + refinement: {followup}", refined)

if __name__ == "__main__":
    run_query_loop()
