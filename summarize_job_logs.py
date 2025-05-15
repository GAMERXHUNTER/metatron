
import os
import json
from datetime import datetime

LOG_DIR = "Logs"
SUMMARY_FILE = "docs/job_log_summary.md"

def summarize_job(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        summary = {
            "filename": os.path.basename(filepath),
            "timestamp": data.get("timestamp") or "Unknown",
            "job_type": data.get("type") or "Unknown",
            "source": data.get("source") or "N/A",
            "status": data.get("status") or "No status",
            "outputs": data.get("outputs", [])
        }
        return summary
    except Exception as e:
        return {
            "filename": os.path.basename(filepath),
            "error": str(e)
        }

def main():
    os.makedirs("docs", exist_ok=True)
    with open(SUMMARY_FILE, 'w', encoding='utf-8') as out:
        out.write("# 📊 Metatron Job Log Summary\n\n")
        for file in os.listdir(LOG_DIR):
            if file.startswith("job_") and file.endswith(".json"):
                path = os.path.join(LOG_DIR, file)
                summary = summarize_job(path)
                out.write(f"## `{summary.get('filename')}`\n")
                if 'error' in summary:
                    out.write(f"- ❌ Error reading file: {summary['error']}\n\n")
                else:
                    out.write(f"- 🕓 Timestamp: {summary['timestamp']}\n")
                    out.write(f"- 🧠 Job Type: {summary['job_type']}\n")
                    out.write(f"- 📁 Source: {summary['source']}\n")
                    out.write(f"- ✅ Status: {summary['status']}\n")
                    if summary['outputs']:
                        out.write(f"- 📦 Outputs: {', '.join(summary['outputs'])}\n")
                out.write("\n---\n\n")

    print(f"✅ Summary saved to {SUMMARY_FILE}")

if __name__ == "__main__":
    main()
