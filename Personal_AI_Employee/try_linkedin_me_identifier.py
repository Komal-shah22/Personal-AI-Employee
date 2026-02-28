#!/usr/bin/env python3
"""
Try different approaches to post to LinkedIn using the 'me' identifier
"""

import os
import json
import requests
from pathlib import Path

# LinkedIn API Configuration
LINKEDIN_API_URL = "https://api.linkedin.com/v2"
TOKEN_FILE = Path('credentials/linkedin_token.json')

def load_access_token():
    """Load LinkedIn access token from credentials file"""
    if not TOKEN_FILE.exists():
        return None

    try:
        with open(TOKEN_FILE, 'r') as f:
            data = json.load(f)
            return data.get('access_token')
    except Exception as e:
        print(f"Error loading token: {e}")
        return None

def try_post_with_me_identifier():
    """Try posting using the 'me' identifier in different formats"""
    access_token = load_access_token()
    if not access_token:
        print("No access token found!")
        return

    content = "Testing different LinkedIn posting approaches! 🚀"

    # Test different author formats that LinkedIn might accept
    author_formats = [
        "urn:li:person:me",
        "urn:li:member:me",
        "urn:li:in:me",
        "me"  # Just 'me' as a string
    ]

    for i, author in enumerate(author_formats, 1):
        print(f"\nTrying author format {i}: {author}")

        post_data = {
            "author": author,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": f"{content} (Format {i}: {author})"
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }

        response = requests.post(
            f"{LINKEDIN_API_URL}/ugcPosts",
            headers=headers,
            json=post_data
        )

        print(f"Status: {response.status_code}")
        if response.status_code != 201:
            print(f"Error: {response.text}")
        else:
            print("SUCCESS! Post created with this format.")

def main():
    print("Testing Different LinkedIn Author Formats")
    print("=" * 40)
    print("Testing various approaches to identify the poster on LinkedIn...")
    print()

    try_post_with_me_identifier()

if __name__ == '__main__':
    main()