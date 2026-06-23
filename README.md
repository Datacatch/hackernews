# 🔥 HackerNews Top Stories Fetcher

Automatically fetches the top 10 HackerNews stories daily using GitHub Actions — no server needed!

## 📁 Project Structure

```
hackernews/
├── fetch_hn.py              # Main script
├── stories.json             # Auto-updated daily (by GitHub Actions)
├── requirements.txt         # Python dependencies
├── .gitignore
└── .github/
    └── workflows/
        └── fetch-hn.yml     # GitHub Actions cron job
```

## ⚙️ How It Works

1. GitHub Actions runs every day at **8:00 AM UTC (1:30 PM IST)**
2. It fetches the top 10 stories from the [HackerNews API](https://github.com/HackerNews/API)
3. Saves results to `stories.json`
4. Commits and pushes the file back to this repo automatically

## 🚀 Run Manually

Trigger it anytime from **GitHub → Actions → Fetch HackerNews Top Stories → Run workflow**

## 🔗 API Used

- Base URL: `https://hacker-news.firebaseio.com/v0/`
- No API key required, no rate limits