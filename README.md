# Reddit Subreddit Scraper

A Python script to fetch posts from a subreddit using **PRAW** and save them to a CSV file.

## Features
- Fetch "hot" posts (all-time)
- Save post data: title, author, score, comments, date, URL, content

## Requirements
- Python 3.8+
- PRAW (`pip install praw`)

## Setup
1. Create a Reddit app: https://www.reddit.com/prefs/apps
2. Replace placeholders in the script with your credentials (`client_id`, `client_secret`, `user_agent`)
3. Set the target subreddit (`subreddit_name`)

## Usage
```bash
python reddit_scraper.py
