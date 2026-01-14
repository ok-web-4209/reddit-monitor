import requests
import os
import time
from datetime import datetime, timezone

# --- CONFIGURATION ---
SUBREDDIT = "HustleGPT"
KEYWORDS = [] # Leave empty to get EVERY post, or add keywords like ["ai", "money"]

def check_reddit():
    print(f"Checking r/{SUBREDDIT}...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    url = f"https://www.reddit.com/r/{SUBREDDIT}/new.json?limit=10"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return

        posts = response.json()['data']['children']
        current_time = datetime.now(timezone.utc).timestamp()
        ten_mins_ago = current_time - (10 * 60) 
        
        # USE THE NEW SECRET HERE
        webhook_url = os.environ["HUSTLEGPT_WEBHOOK_URL"]

        for post_obj in posts:
            post = post_obj['data']
            if post['created_utc'] > ten_mins_ago:
                
                title = post['title'].lower()
                body = post.get('selftext', '').lower()
                
                if not KEYWORDS or any(k in title for k in KEYWORDS) or any(k in body for k in KEYWORDS):
                    print(f"Found: {post['title']}")
                    msg = {"content": f"🚀 **HustleGPT:** {post['title']}\n🔗 https://reddit.com{post['permalink']}"}
                    requests.post(webhook_url, json=msg)
                    time.sleep(2)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_reddit()
