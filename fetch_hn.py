import requests
import json
import smtplib
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

BASE_URL = "https://hacker-news.firebaseio.com/v0"
TO_EMAIL = "24pradeep@gmail.com"


def get_top_stories(limit=10):
    """Fetch top N stories from HackerNews"""
    print(f"\n🔍 Fetching top {limit} HackerNews stories...")
    print(f"⏰ Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    response = requests.get(f"{BASE_URL}/topstories.json")
    response.raise_for_status()
    story_ids = response.json()[:limit]

    stories = []
    for story_id in story_ids:
        story_resp = requests.get(f"{BASE_URL}/item/{story_id}.json")
        story_resp.raise_for_status()
        story = story_resp.json()

        stories.append({
            "id": story.get("id"),
            "title": story.get("title"),
            "url": story.get("url", "#"),
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


def build_html_email(stories):
    """Build a nice HTML email body"""
    today = datetime.now().strftime("%A, %d %B %Y")

    rows = ""
    for i, s in enumerate(stories, 1):
        hn_link = f"https://news.ycombinator.com/item?id={s['id']}"
        rows += f"""
        <tr style="border-bottom: 1px solid #e5e7eb;">
            <td style="padding: 16px 8px; font-size: 15px; color: #374151; vertical-align: top; width: 24px;">
                <span style="font-weight: bold; color: #ff6600;">{i}</span>
            </td>
            <td style="padding: 16px 8px;">
                <a href="{s['url']}" style="font-size: 15px; font-weight: 600; color: #1d4ed8; text-decoration: none;">
                    {s['title']}
                </a>
                <div style="margin-top: 6px; font-size: 13px; color: #6b7280;">
                    ⭐ {s['score']} pts &nbsp;|&nbsp;
                    💬 {s['comments']} comments &nbsp;|&nbsp;
                    👤 {s['by']} &nbsp;|&nbsp;
                    🕐 {s['time']}
                    &nbsp;&nbsp;
                    <a href="{hn_link}" style="color: #ff6600; text-decoration: none; font-weight: 500;">
                        [Discuss on HN]
                    </a>
                </div>
            </td>
        </tr>
        """

    html = f"""
    <html>
    <body style="margin: 0; padding: 0; background-color: #f9fafb; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
        <div style="max-width: 680px; margin: 32px auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">

            <!-- Header -->
            <div style="background: #ff6600; padding: 28px 32px;">
                <h1 style="margin: 0; color: #ffffff; font-size: 22px; font-weight: 700;">
                    🔥 HackerNews Top Stories
                </h1>
                <p style="margin: 6px 0 0; color: #fff3e0; font-size: 14px;">{today}</p>
            </div>

            <!-- Stories -->
            <div style="padding: 8px 24px 24px;">
                <table style="width: 100%; border-collapse: collapse;">
                    {rows}
                </table>
            </div>

            <!-- Footer -->
            <div style="background: #f3f4f6; padding: 16px 32px; text-align: center;">
                <p style="margin: 0; font-size: 12px; color: #9ca3af;">
                    Delivered daily by GitHub Actions &nbsp;|&nbsp;
                    <a href="https://news.ycombinator.com" style="color: #ff6600;">Visit HackerNews</a>
                </p>
            </div>

        </div>
    </body>
    </html>
    """
    return html


def send_email(stories):
    """Send stories via Gmail SMTP"""
    sender_email = os.environ.get("GMAIL_ADDRESS")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")

    if not sender_email or not app_password:
        print("❌ Email credentials not found in environment variables!")
        raise ValueError("Missing GMAIL_ADDRESS or GMAIL_APP_PASSWORD")

    today = datetime.now().strftime("%d %B %Y")
    subject = f"🔥 HackerNews Top 10 Stories — {today}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = TO_EMAIL

    html_body = build_html_email(stories)
    msg.attach(MIMEText(html_body, "html"))

    print(f"📧 Sending email to {TO_EMAIL}...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, TO_EMAIL, msg.as_string())

    print(f"✅ Email sent successfully to {TO_EMAIL}!")


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
    send_email(stories)
    print("✅ All done!")