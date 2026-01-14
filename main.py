import requests
import os
import time
from datetime import datetime, timezone

# --- SETTINGS ---
SUBREDDIT = "slavelabour" 
# Leave KEYWORDS empty [] if you want to be notified for EVERY new post
KEYWORDS = ["hiring", "task", "paypal", "urgent", "easy", "usd"] 

def check_reddit():
    print(f"Checking r/{SUBREDDIT}...")
    
    # We use a fake browser ID so Reddit thinks we are a human
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    url = f"https://www.reddit.com/r/{SUBREDDIT}/new.json?limit=10"
    
    try:
        # 1. Get the data from Reddit
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error: Reddit blocked us or is down. Code: {response.status_code}")
            return

        data = response.json()
        posts = data['data']['children']
        
        # 2. Figure out the time 10 minutes ago
        # We check the last 10 minutes to make sure we don't miss anything
        current_time = datetime.now(timezone.utc).timestamp()
        ten_mins_ago = current_time - (10 * 60) 

        # 3. Look through the posts
        webhook_url = os.environ["DISCORD_WEBHOOK_URL"]
        
        for post_obj in posts:
            post = post_obj['data']
            post_time = post['created_utc']
            
            # If the post is newer than 10 minutes ago...
            if post_time > ten_mins_ago:
                
                title = post['title'].lower()
                body = post.get('selftext', '').lower()
                
                # Check if it matches keywords (OR if keywords list is empty)
                if not KEYWORDS or any(word in title for word in KEYWORDS) or any(word in body for word in KEYWORDS):
                    
                    print(f"Found match: {post['title']}")
                    
                    # Send to Discord
                    message = {
                        "content": f"🚨 **New Job:** {post['title']}\n🔗 https://reddit.com{post['permalink']}"
                    }
                    requests.post(webhook_url, json=message)
                    time.sleep(2) # Wait 2 seconds so Discord doesn't get mad

    except Exception as e:
        print(f"Something went wrong: {e}")

if __name__ == "__main__":
    check_reddit()
