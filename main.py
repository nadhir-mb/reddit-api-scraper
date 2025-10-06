import praw
import csv
import time
from datetime import datetime, timedelta

# Replace placeholders with your Reddit app credentials
reddit = praw.Reddit(
    client_id='CLIENT-ID',
    client_secret='CLIENT-SECRET',
    user_agent='app-name/v1.0 (by u/User-Name)'
)
# Optional: include username/password if needed for private subreddits or features
# reddit.username = 'YOUR_USERNAME'
# reddit.password = 'YOUR_PASSWORD'

subreddit_name = 'subreddit-name'
subreddit = reddit.subreddit(subreddit_name)

# === Helper: Convert UTC timestamp to readable date ===
def format_date(utc_timestamp):
    return datetime.utcfromtimestamp(utc_timestamp).strftime('%Y-%m-%d %H:%M:%S')

# === Fetch "hot" posts (All-time) in batches ===
all_posts = []
after = None
while True:
    try:
        # Fetch up to 100 posts per request (max allowed per call) for pagination
        batch = list(subreddit.hot(limit=100, params={'after': after}))
    except Exception as e:
        print(f"Error fetching posts: {e}. Retrying after delay.")
        time.sleep(60)  # wait and retry on error (API exception or rate limit)
        continue

    if not batch:
        break  # no more posts
    all_posts.extend(batch)
    print(f"Fetched {len(batch)} posts; total so far = {len(all_posts)}")
    
    # Prepare for next batch: use fullname of last post as 'after' cursor
    after = batch[-1].fullname
    # If fewer than 100 were returned, we're likely at the end of available posts
    if len(batch) < 100:
        break
    # Respect rate limit: sleep a bit between batches
    time.sleep(2)  # PRAW does ~2s delay internally for 100-item calls:contentReference[oaicite:7]{index=7}; extra sleep for safety

# === (Optional) Fetch posts from the past year ===
# Since "hot" cannot be time-filtered, use top(time_filter='year') as an alternative
one_year_ago = datetime.utcnow() - timedelta(days=365)
year_posts = []
try:
    for submission in subreddit.top(time_filter='year', limit=None):
        year_posts.append(submission)
except Exception as e:
    print(f"Error fetching past year posts: {e}")
print(f"Total posts from past year (top by score): {len(year_posts)}")
# You could merge year_posts with all_posts or handle separately if desired

# === (Optional) Fetch posts from all time ===
# Using top(time_filter='all') to get highest-scoring posts ever
all_time_posts = []
try:
    for submission in subreddit.top(time_filter='all', limit=None):
        all_time_posts.append(submission)
except Exception as e:
    print(f"Error fetching all-time posts: {e}")
print(f"Total all-time posts (top by score): {len(all_time_posts)}")

# Combine or choose which collection to save. For demonstration, we’ll use all_posts (hot) list.
posts_to_save = all_posts

# === Save to CSV ===
csv_filename = 'algeria_posts.csv'
fieldnames = ['title', 'author', 'score', 'num_comments', 'created_utc', 'url', 'selftext']
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for post in posts_to_save:
        writer.writerow({
            'title': post.title,
            'author': post.author.name if post.author else '[deleted]',
            'score': post.score,
            'num_comments': post.num_comments,
            'created_utc': format_date(post.created_utc),
            'url': post.url,
            'selftext': post.selftext.replace('\n', ' ')  # replace newlines in text
        })

print(f"Saved {len(posts_to_save)} posts to {csv_filename}")
