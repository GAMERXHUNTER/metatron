# Starter Python Script: YouTube Topic Scraper (OpenAI API v1.0 Compatible)

# Required Libraries
# pip install requests
# pip install openai

import requests
import json
import openai

# YouTube Trending Scraper using RapidAPI
def scrape_youtube_trending():
    url = "https://youtube138.p.rapidapi.com/trending/?hl=en&gl=US"

    headers = {
        "X-RapidAPI-Key": "c540cfcd13msh56c825ca7355b90p15b3cdjsn13f78b9d5a30",
        "X-RapidAPI-Host": "youtube138.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    trending_data = response.json()

    trending_titles = []
    for video in trending_data.get('contents', []):
        title = video['video']['title']['runs'][0]['text']
        trending_titles.append(title)

    return trending_titles

# GPT Filtering Function (updated for OpenAI 1.0+)
def filter_trending_topics(trending_titles, niche_focus):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""Filter the following trending YouTube video titles to ONLY show titles related to {niche_focus}.
Titles:
{trending_titles}

Return 5–10 titles that are a good match."""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    filtered_topics = response.choices[0].message.content
    return filtered_topics

# Main Runner
if __name__ == "__main__":
    niche = "supplements and health"
    trending_titles = scrape_youtube_trending()
    print(trending_titles)
    relevant_topics = filter_trending_topics(trending_titles, niche)

    print("Recommended Topics:")
    print(relevant_topics)
