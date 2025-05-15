# RedditScraper_Agent.py
# Headless agent to scrape posts from a given subreddit and store them in the Raw folder for Vault processing

import os
import datetime
import json
import praw

# Configure Reddit API credentials (update these with your own)
REDDIT_CLIENT_ID = "q_W54yxLuLVrKU66DVCzlQ"
REDDIT_CLIENT_SECRET = "YO8BS_R0XrF_c68dPAhukyrlCQQuVA"
REDDIT_USER_AGENT = "TabernacleEmpireScraper/0.1 by Kadmiel"

SAVE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Raw"))

def initialize_reddit():
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

def scrape_subreddit(subreddit_name, limit=25):
    reddit = initialize_reddit()
    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    print(f"[INFO] Scraping r/{subreddit_name} (limit {limit})...")
    for submission in subreddit.hot(limit=limit):
        post_data = {
            "title": submission.title,
            "author": str(submission.author),
            "score": submission.score,
            "url": submission.url,
            "selftext": submission.selftext,
            "created_utc": datetime.datetime.utcfromtimestamp(submission.created_utc).isoformat()
        }
        posts.append(post_data)

    return posts

def save_posts(posts, subreddit_name):
    if not posts:
        print("[WARN] No posts found.")
        return None

    os.makedirs(SAVE_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_name = f"reddit_{subreddit_name}_{timestamp}"
    json_path = os.path.join(SAVE_DIR, f"{base_name}.json")
    txt_path = os.path.join(SAVE_DIR, f"{base_name}.txt")
    md_path = os.path.join(SAVE_DIR, f"{base_name}.md")

    # Save .json
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)

    # Save .txt and .md
    lines = []
    for post in posts:
        lines.append("Title: {}".format(post['title']))
        lines.append("Author: {}".format(post['author']))
        lines.append("Score: {}".format(post['score']))
        lines.append("URL: {}".format(post['url']))
        lines.append("Posted: {}".format(post['created_utc']))
        lines.append("")
        lines.append(post['selftext'])
        lines.append("\n---\n")

    text_output = "\n".join(lines)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text_output)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Reddit Knowledge Dump\n\n" + text_output)



    print("[SAVED] {}".format(json_path))
    print("[SAVED] {}".format(txt_path))
    print("[SAVED] {}".format(md_path))
    return [json_path, txt_path, md_path]

if __name__ == "__main__":
    # Example usage
    subreddit = "Entrepreneur"
    posts = scrape_subreddit(subreddit, limit=25)
    save_posts(posts, subreddit)
    print("✅ Reddit scrape complete.")

import subprocess
subprocess.run(["python", "VaultProcessor_AI.py"], cwd=os.path.dirname(__file__))
