import feedparser
import requests
import os
import time

# --- CONFIGURATION ---
RSS_URL = "https://www.reddit.com/r/Slavelabour/new/.rss"
WEBHOOK_URL = os.environ["HUSTLEGPT_WEBHOOK_URL"]

def check_rss_feed():
    print("--- CHECKING RSS FEED ---")
    
    # 1. Parse the RSS Feed
    # We still use a 'fake' user agent so Reddit thinks we are a browser
    feed = feedparser.parse(RSS_URL, agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    
    # 2. Check if we got data
    if len(feed.entries) == 0:
        print("❌ Error: Feed is empty or Reddit blocked us.")
        return
    
    print(f"✅ Success! Found {len(feed.entries)} posts.")

    # 3. Send the TOP 3 posts (Just to prove it works right now)
    # In the future, you can limit this to the top 1
    for entry in feed.entries[:3]:
        print(f"   -> Found: {entry.title}")
        
        msg = {
            "content": f"📰 **Hustle RSS:** {entry.title}\n🔗 {entry.link}"
        }
        
        try:
            requests.post(WEBHOOK_URL, json=msg)
            time.sleep(2) # Wait 2 seconds between messages
        except Exception as e:
            print(f"   ❌ Discord Error: {e}")

if __name__ == "__main__":
    check_rss_feed()
