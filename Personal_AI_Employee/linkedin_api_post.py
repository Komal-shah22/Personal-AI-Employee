"""
Post to LinkedIn using Shares API (works with w_member_social scope).
"""

import requests
import json
import uuid

# Load token
with open("credentials/linkedin_token.json", "r") as f:
    token_data = json.load(f)

ACCESS_TOKEN = token_data["access_token"]
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0"
}

POST_TEXT = "Testing AI Employee Dashboard! 🚀 #AI #Automation"

print("=" * 60)
print("LINKEDIN SHARES API POSTER")
print("=" * 60)

# Use the Shares API which works with w_member_social scope
print("\nCreating Share via POST https://api.linkedin.com/v2/shares")

# Build the share payload using Shares API format
share_data = {
    "text": {
        "text": POST_TEXT
    },
    "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
    },
    "lifecycleState": "PUBLISHED",
    "visibility": "PUBLIC",
    "shareMediaCategory": "NONE"
}

print(f"Payload: {json.dumps(share_data, indent=2)}")

try:
    response = requests.post(
        "https://api.linkedin.com/v2/shares",
        headers=HEADERS,
        json=share_data
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    
    if response.status_code in [200, 201]:
        try:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            
            post_id = result.get("id") or result.get("activity") or result.get("shareId")
            if post_id:
                print("\n" + "=" * 60)
                print("SUCCESS! Post created on LinkedIn")
                print(f"Post ID: {post_id}")
                print(f"View at: https://www.linkedin.com/feed/update/{post_id}")
                print("=" * 60)
            else:
                print("\n⚠ Post created but no ID returned")
        except json.JSONDecodeError:
            print(f"Raw response: {response.text}")
            print("\n⚠ Could not parse JSON response")
    else:
        print(f"\nERROR: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Try to parse error
        try:
            error_data = response.json()
            print(f"Parsed error: {json.dumps(error_data, indent=2)}")
        except:
            pass
            
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
