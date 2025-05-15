# YouTubeScraper_Agent.py (with Title-Based Filename Saving)

import os
import re
from pytube import YouTube

SAVE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Raw"))
os.makedirs(SAVE_DIR, exist_ok=True)

def sanitize_filename(title):
    return re.sub(r'[\\/:*?"<>|]', '_', title)[:100]

def download_transcript(video_url):
    try:
        yt = YouTube(video_url)
        title = sanitize_filename(yt.title)
        video_id = yt.video_id
        transcript = yt.captions.get_by_language_code("en")
        if not transcript:
            print(f"[SKIP] No English transcript for: {yt.title}")
            return
        text = transcript.generate_srt_captions()
        fname = f"{title}_{video_id}.txt"
        path = os.path.join(SAVE_DIR, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[SAVED] {path}")
    except Exception as e:
        print(f"[ERROR] Failed to process {video_url}: {e}")

def main():
    urls = []
    with open("youtube_urls.txt", "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        download_transcript(url)

if __name__ == "__main__":
    main()
