# VaultGPT_Plus_Agent.py
# Persistent memory GPT agent with vault access and action engine (GPT-3.5 fallback)

import os
import json
import datetime
import textwrap
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

VAULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Vault"))
MEMORY_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Vault/VaultAgentLogs", "agent_memory.json"))
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Vault/VaultAgentLogs"))
os.makedirs(LOG_DIR, exist_ok=True)

MAX_CONTEXT_CHARS = 6000

def load_vault_files():
    chunks = []
    for root, _, files in os.walk(VAULT_DIR):
        for f in files:
            if f.endswith("_enhanced.md"):
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8") as fp:
                    content = fp.read()
                    chunks.append((f, content[:2000]))  # only partial content for context
    return chunks

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"interactions": []}

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def build_context(memory, vault_chunks):
    recent_qna = memory["interactions"][-3:]
    context = "\n\n".join([f"Q: {m['question']}\nA: {m['answer']}" for m in recent_qna])
    vault_snippets = "\n\n---\n\n".join([f"## {name}\n{content}" for name, content in vault_chunks[:3]])
    return context, vault_snippets

def query_gpt(prompt):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # fallback model
        messages=messages,
        temperature=0.4
    )
    return response.choices[0].message.content.strip()

def log_interaction(question, answer):
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(LOG_DIR, f"plus_agent_{ts}.md")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"# VaultGPT+ Interaction\n\n**Q:** {question}\n\n**A:**\n\n{answer}")
    print(f"📝 Saved to {log_path}")

def run_agent():
    print("🧠 VaultGPT+ Agent (Persistent Memory Mode - GPT-3.5 Fallback)")
    memory = load_memory()
    vault_chunks = load_vault_files()

    while True:
        query = input("\n> ").strip()
        if query.lower() in ["exit", "quit"]:
            print("👋 Exiting VaultGPT+ Agent.")
            break

        context, vault_context = build_context(memory, vault_chunks)
        system_prompt = f"""
You are VaultGPT+, a strategic assistant to Kadmiel.

- Your goal is to help Kadmiel achieve £1M in assets/income using AI automation, scalable systems, and strategic thinking.
- You have persistent memory of his past queries and actions.
- You have access to structured vault knowledge extracted from trusted sources.
- When answering, combine his vision, recent chat memory, and insights from the vault.
- Be actionable. If something needs building or triggering, describe what you'd build and suggest next steps.

---

RECENT MEMORY:
{context}

---

VAULT CONTEXT:
{vault_context}

---

QUESTION:
{query}
"""

        answer = query_gpt(system_prompt)
        print("\n💬 GPT+ Response:")
        print(textwrap.fill(answer, width=100))
        memory["interactions"].append({"question": query, "answer": answer})
        save_memory(memory)
        log_interaction(query, answer)

if __name__ == "__main__":
    run_agent()
