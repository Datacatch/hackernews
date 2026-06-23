import requests
import json
from datetime import datetime

BASE_URL = "https://hacker-news.firebaseio.com/v0"

def get_top_stories(limit=10):
    # Step 1: Get list of top story IDs
    response = requests.get(f"{BASE_URL}/topstories.json")
    story_ids = response.json()[:limit]  # take first N

    stories = []
    for story_id in story_ids:
        # Step 2: Fetch each story's details
        story = requests.get(f"{BASE_URL}/item/{story_id}.json").json()
        stories.append({
            "title": story.get("title"),
            "url": story.get("url"),
            "score": story.get("score"),
            "by": story.get("by"),
            "time": datetime.fromtimestamp(story.get("time")).strftime("%Y-%m-%d %H:%M")
        })

    return stories

if __name__ == "__main__":
    stories = get_top_stories(10)
    for i, s in enumerate(stories, 1):
        print(f"{i}. [{s['score']} pts] {s['title']}")
        print(f"   By: {s['by']} | {s['time']}")
        print(f"   URL: {s['url']}\n")