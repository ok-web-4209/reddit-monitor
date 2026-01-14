import feedparser
import requests
import os
import time
from datetime import datetime, timezone

# --- CONFIGURATION ---
RSS_URL = "https://www.reddit.com/r/slavelabour/new/.rss"
WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

# Time Window: How far back to check (in seconds).
# Since GitHub runs roughly every 5 mins, we check the last 10 mins (600s) 
# to ensure we never miss a post, even if GitHub is late.
# (You might see a duplicate occasionally, but it's safer than missing a job).
CHECK_WINDOW = 600 

def check_feed():
    print("--- CHECKING SLAVELABOUR (ALL POSTS) ---")
    
    # 1. Parse the Feed
    feed = feedparser.parse(RSS_URL, agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    
    if not feed.entries:
        print("❌ Error: Feed is empty or blocked.")
        return

    current_time = datetime.now(timezone.utc).timestamp()
    
    # 2. Loop through posts
    # We reverse the list to send oldest -> newest so they appear in order in Discord
    for entry in reversed(feed.entries):
        
        # Convert RSS time to compatible format
        post_time_struct = entry.published_parsed
        post_timestamp = time.mktime(post_time_struct)
        
        # 3. Check if it's new
        if (current_time - post_timestamp) < CHECK_WINDOW:
            print(f"MATCH: {entry.title}")
            
            # 4. Create the "Open App" Embed
            # We add a clean title and a clear "Open in App" link.
            msg = {
                "embeds": [{
                    "title": entry.title,
                    "url": entry.link,  # Clicking title opens browser
                    "description": "Click the link below to open in Reddit App:",
                    "color": 16729344,  # Reddit Orange
                    "fields": [
                        {
                            "name": "📱 Mobile Link",
                            "value": f"[**Tap to Open in App**]({entry.link})",
                            "inline": True
                        }
                    ],
                    "footer": {
                        "text": "r/slavelabour • New Post"
                    },
                    "timestamp": datetime.fromtimestamp(post_timestamp).isoformat()
                }]
            }
            
            try:
                requests.post(WEBHOOK_URL, json=msg)
                time.sleep(2) # Slight pause to ensure order
            except Exception as e:
                print(f"Error sending to Discord: {e}")

if __name__ == "__main__":
    check_feed()
