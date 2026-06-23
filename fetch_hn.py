import requests
import json
from datetime import datetime

BASE_URL = "https://hacker-news.firebaseio.com/v0"

def get_top_stories(limit=10):
    """Fetch top N stories from HackerNews"""
    print(f"\n🔍 Fetching top {limit} HackerNews stories...")
    print(f"⏰ Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Step 1: Get list of top story IDs
    response = requests.get(f"{BASE_URL}/topstories.json")
    response.raise_for_status()
    story_ids = response.json()[:limit]

    stories = []
    for story_id in story_ids:
        # Step 2: Fetch each story's details
        story_resp = requests.get(f"{BASE_URL}/item/{story_id}.json")
        story_resp.raise_for_status()
        story = story_resp.json()

        stories.append({
            "id": story.get("id"),
            "title": story.get("title"),
            "url": story.get("url", "No URL"),
            "score": story.get("score", 0),
            "by": story.get("by"),
            "comments": story.get("descendants", 0),
            "time": datetime.fromtimestamp(story.get("time")).strftime("%Y-%m-%d %H:%M")
        })

    return stories


def save_to_json(stories, filename="stories.json"):
    """Save stories to a JSON file"""
    with open(filename, "w") as f:
        json.dump({
            "fetched_at": datetime.now().isoformat(),
            "count": len(stories),
            "stories": stories
        }, f, indent=2)
    print(f"💾 Saved {len(stories)} stories to {filename}")


def print_stories(stories):
    """Print stories to console"""
    print("=" * 60)
    print("🔥 TOP HACKERNEWS STORIES")
    print("=" * 60)
    for i, s in enumerate(stories, 1):
        print(f"\n{i}. {s['title']}")
        print(f"   ⭐ Score : {s['score']} pts | 💬 Comments: {s['comments']}")
        print(f"   👤 By    : {s['by']} | 🕐 {s['time']}")
        print(f"   🔗 URL   : {s['url']}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    stories = get_top_stories(limit=10)
    print_stories(stories)
    save_to_json(stories)
    print("✅ Done!")