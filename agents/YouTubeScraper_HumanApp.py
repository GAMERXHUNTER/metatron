# YouTubeScraper_HumanApp.py
# GUI-based YouTube transcript downloader with path fix and debug

import tkinter as tk
from tkinter import messagebox
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from urllib.parse import urlparse, parse_qs
import os

SAVE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Raw"))

def extract_video_id(url):
    try:
        parsed_url = urlparse(url)
        if "youtu.be" in parsed_url.netloc:
            return parsed_url.path[1:]
        elif "youtube.com" in parsed_url.netloc:
            query = parse_qs(parsed_url.query)
            return query.get("v", [None])[0]
        return None
    except:
        return None

def download_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return "\n".join([entry["text"] for entry in transcript])
    except NoTranscriptFound:
        return "No transcript found."
    except TranscriptsDisabled:
        return "Transcripts disabled for this video."
    except Exception as e:
        return f"Error: {str(e)}"

def save_transcript(video_id, text):
    try:
        os.makedirs(SAVE_DIR, exist_ok=True)
        filename = f"{video_id}.txt"
        path = os.path.abspath(os.path.join(SAVE_DIR, filename))
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[DEBUG] Transcript saved to: {path}")
        print(f"[DEBUG] Transcript content start:\n{text[:300]}")
        return path
    except Exception as e:
        print(f"[ERROR] Failed to save transcript: {e}")
        return None

def download_and_save():
    url = entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube video URL.")
        return

    video_id = extract_video_id(url)
    if not video_id:
        messagebox.showerror("Error", "Invalid YouTube URL.")
        return

    status_text.set("Downloading...")
    text = download_transcript(video_id)
    path = save_transcript(video_id, text)

    if path:
        status_text.set(f"✅ Saved: {path}")
    else:
        status_text.set("❌ Save failed. Check debug log.")

# GUI setup
root = tk.Tk()
root.title("YouTube Transcript Downloader")

tk.Label(root, text="YouTube Video URL:").pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(padx=10)

tk.Button(root, text="Download Transcript", command=download_and_save).pack(pady=10)
status_text = tk.StringVar()
tk.Label(root, textvariable=status_text).pack(pady=5)

root.mainloop()
