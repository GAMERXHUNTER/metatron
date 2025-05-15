# Mastermold_Orchestrator.py v1.1

import os
import json
import time
import subprocess
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

JOBS_FILE = os.path.abspath("jobs.json")
LOG_DIR = os.path.abspath("Logs")
os.makedirs(LOG_DIR, exist_ok=True)

SCRAPER_MAP = {
    "youtube": "YouTubeScraper_Agent.py",
    "reddit": "RedditScraper_Agent.py",
    "article": "ArticleScraper_Agent.py",
    "pdf": "PDFVaultImporter.py"
}

def load_jobs():
    if not os.path.exists(JOBS_FILE):
        return []
    with open(JOBS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_jobs(jobs):
    with open(JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)

def log_job(result):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(LOG_DIR, f"job_{timestamp}.json")
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

# PATCH: update run_script to show live status

def run_script(script_name):
    print(f"[RUNNING] {script_name}")
    try:
        process = subprocess.Popen(
            ["python", script_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                print(f"[{script_name}] {output.strip()}")

        stderr_output = process.stderr.read()
        return {
            "script": script_name,
            "returncode": process.returncode,
            "stdout": f"[Streaming output shown above]",
            "stderr": stderr_output,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "script": script_name,
            "returncode": 1,
            "stdout": "",
            "stderr": str(e),
            "timestamp": datetime.now().isoformat()
        }

def run_next_job(jobs):
    if not jobs:
        print("[QUEUE] No jobs in queue.")
        return jobs

    job = jobs.pop(0)
    job_type = job.get("type")
    print(f"[INFO] Starting job: {job}")

    if job_type in SCRAPER_MAP:
        result = run_script(SCRAPER_MAP[job_type])
    elif job_type == "vault_clean":
        result = run_script("VaultCleaner_AI.py")
    elif job_type == "enhance_all":
        result = run_script("VaultEnhancer_AI.py")
    else:
        print(f"[SKIP] Unknown job type: {job_type}")
        return jobs

    log_job(result)
    return jobs

def add_topic_based_jobs():
    topic = input("🔍 Enter topic to scrape (e.g. AI business automation): ").strip()
    print("Choose sources: [Y] YouTube  [R] Reddit  [A] Article (e.g. YRA)")
    sources = input("Sources: ").strip().upper()
    limit = input("Enter scrape limit (e.g. 5, 10, 25): ").strip()
    jobs = []

    for char in sources:
        if char == "Y":
            jobs.append({"type": "youtube", "topic": topic, "limit": int(limit)})
        elif char == "R":
            jobs.append({"type": "reddit", "topic": topic, "limit": int(limit)})
        elif char == "A":
            jobs.append({"type": "article", "topic": topic, "limit": int(limit)})

    queue = load_jobs()
    queue.extend(jobs)
    save_jobs(queue)
    print(f"✅ {len(jobs)} jobs added for topic: {topic}")

def add_youtube_url_job():
    url = input("📺 Enter YouTube video, playlist, or channel URL: ").strip()
    job = {"type": "youtube", "url": url, "mode": "full"}
    queue = load_jobs()
    queue.append(job)
    save_jobs(queue)
    print("✅ YouTube full scrape job added.")

def show_dashboard(jobs):
    print("\n🧠 MASTERMOLD CONSOLE v1.1")
    print("==============================")
    print(f"📋 Jobs in queue: {len(jobs)}")
    if jobs:
        print(f"🔜 Next job: {jobs[0].get('type')}")
    print("📁 Logs stored in: ./Logs/")
    print("------------------------------")
    print("[1] Add Topic + Source Jobs")
    print("[2] Add YouTube URL Job")
    print("[3] Run Next Job")
    print("[4] Run All Jobs")
    print("[5] Ask GPT for Vault Insight")
    print("[6] View Job Queue")
    print("[7] Exit")
    print("==============================")

def ask_gpt_and_suggest_jobs():
    question = input("🧠 Ask Mastermold: ")
    messages = [{"role": "user", "content": question}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.4
    )
    answer = response.choices[0].message.content.strip()
    print("\n💬 GPT Insight:")
    print(answer)
    if "1." in answer:
        print("\nAdd suggested topics as jobs? (Y/N)")
        if input("> ").strip().upper() == "Y":
            print("Choose sources for suggestions: (e.g. YRA)")
            sources = input("Sources: ").strip().upper()
            limit = input("Limit per source (e.g. 5, 10): ").strip()
            suggested = [line.strip("0123456789. ").strip() for line in answer.splitlines() if line.startswith(tuple("1234567890"))]
            jobs = []
            for topic in suggested:
                for src in sources:
                    jtype = {"Y": "youtube", "R": "reddit", "A": "article"}.get(src)
                    if jtype:
                        jobs.append({"type": jtype, "topic": topic, "limit": int(limit)})
            queue = load_jobs()
            queue.extend(jobs)
            save_jobs(queue)
            print(f"✅ Added {len(jobs)} jobs based on GPT insight.")

def main():
    jobs = load_jobs()
    while True:
        show_dashboard(jobs)
        choice = input("Select an option: ")

        if choice == "1":
            add_topic_based_jobs()
            jobs = load_jobs()
        elif choice == "2":
            add_youtube_url_job()
            jobs = load_jobs()
        elif choice == "3":
            jobs = run_next_job(jobs)
            save_jobs(jobs)
        elif choice == "4":
            while jobs:
                jobs = run_next_job(jobs)
                save_jobs(jobs)
        elif choice == "5":
            ask_gpt_and_suggest_jobs()
            jobs = load_jobs()
        elif choice == "6":
            print(json.dumps(jobs, indent=2))
        elif choice == "7":
            print("👋 Exiting Mastermold.")
            break
        else:
            print("❌ Invalid option.")

if __name__ == "__main__":
    main()
