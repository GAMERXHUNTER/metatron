
import os
import time
import subprocess
from datetime import datetime

# Configuration
SCRIPT = "agents/Mastermold_Orchestrator.py"
INTERVAL_MINUTES = 60  # Change this as needed

def run_mastermold():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🕓 [{timestamp}] Running Mastermold...")
    if os.path.exists(SCRIPT):
        subprocess.run(["python", SCRIPT])
    else:
        print(f"❌ Could not find: {SCRIPT}")

def main():
    print("🧠 Mastermold Scheduler Started")
    print(f"⏱ Will run every {INTERVAL_MINUTES} minute(s)")

    while True:
        run_mastermold()
        time.sleep(INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    main()
