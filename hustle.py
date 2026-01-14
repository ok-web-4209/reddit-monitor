import requests
import os
import json

# --- CONFIGURATION ---
SUBREDDIT = "HustleGPT"
# Get the secret. If this fails, the workflow logs will tell us.
WEBHOOK_URL = os.environ.get("HUSTLEGPT_WEBHOOK_URL")

def debug_bot():
    print("--- STARTING DEBUG RUN ---")

    # 1. VERIFY DISCORD CONNECTION
    if not WEBHOOK_URL:
        print("❌ CRITICAL ERROR: The Secret 'HUSTLEGPT_WEBHOOK_URL' is missing or empty!")
        return

    print("1. Sending Test Message to Discord...")
    test_payload = {"content": "✅ **TEST:** The Bot is connected and running! (If you see this, the Webhook is correct)."}
    try:
        test_resp = requests.post(WEBHOOK_URL, json=test_payload)
        if test_resp.status_code in [200, 204]:
            print("   ✅ Discord Test Sent Successfully.")
        else:
            print(f"   ❌ Discord Rejected the message. Code: {test_resp.status_code}")
            print(f"   Response: {test_resp.text}")
    except Exception as e:
        print(f"   ❌ Failed to connect to Discord: {e}")

    # 2. VERIFY REDDIT CONNECTION
    print(f"\n2. Checking r/{SUBREDDIT} (No filters)...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    url = f"https://www.reddit.com/r/{SUBREDDIT}/new.json?limit=5"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"   ❌ Reddit Blocked the request. Status Code: {response.status_code}")
            return
        
        data = response.json()
        posts = data['data']['children']
        print(f"   ✅ Successfully fetched {len(posts)} posts from Reddit.")

        # Send the newest post to Discord just to prove it can scrape
        if posts:
            top_post = posts[0]['data']
            print(f"   Attempting to send post: {top_post['title']}")
            msg = {
                "content": f"🕵️ **Debug Found Post:** {top_post['title']}\n🔗 https://reddit.com{top_post['permalink']}"
            }
            requests.post(WEBHOOK_URL, json=msg)
            print("   ✅ Sent top post to Discord.")
        else:
            print("   ⚠️ Reddit returned 0 posts (Subreddit might be empty?)")

    except Exception as e:
        print(f"   ❌ Script crashed: {e}")

if __name__ == "__main__":
    debug_bot()
