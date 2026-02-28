#!/usr/bin/env python3
"""
LinkedIn Poster - Retrieve user ID properly and post
Uses LinkedIn API v2 for direct posting
"""

import os
import sys
import json
import requests
from datetime import datetime
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
        print(f"Error loading token: {e}", file=sys.stderr)
        return None

def get_user_id(access_token):
    """Get the LinkedIn user ID for posting using proper headers"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-RestLi-Protocol-Version': '2.0.0'
    }

    # Request specific fields that are allowed with w_member_social scope
    response = requests.get(
        f"{LINKEDIN_API_URL}/me?projection=(id)",
        headers=headers
    )

    if response.status_code == 200:
        user_data = response.json()
        user_id = user_data.get('id')
        if user_id:
            return user_id
        else:
            print(f"User ID not found in response: {user_data}", file=sys.stderr)
            return None
    elif response.status_code == 403:
        print(f"Permission denied getting user info: {response.text}", file=sys.stderr)
        # Try alternative endpoint for user info
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(
            f"{LINKEDIN_API_URL}/userinfo",
            headers=headers
        )
        if response.status_code == 200:
            user_data = response.json()
            user_id = user_data.get('sub')
            if user_id:
                return user_id
    else:
        print(f"Error getting user info: {response.status_code} - {response.text}", file=sys.stderr)

    return None

def post_to_linkedin(access_token, content, image_url=None):
    """Post content to LinkedIn"""

    # Get user ID - this is required for the author field
    user_id = get_user_id(access_token)
    if not user_id:
        return {
            'success': False,
            'error': 'Failed to retrieve user ID. Please verify token permissions for w_member_social scope.'
        }

    user_urn = f"urn:li:person:{user_id}"

    # Prepare post data
    post_data = {
        "author": user_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    # Add image if provided
    if image_url:
        post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "IMAGE"
        post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
            {
                "status": "READY",
                "originalUrl": image_url
            }
        ]

    # Make API request
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

    if response.status_code == 201:
        post_id = response.headers.get('X-RestLi-Id', 'unknown')
        return {
            'success': True,
            'post_id': post_id,
            'posted_at': datetime.now().isoformat(),
            'content': content,
            'method': 'linkedin_api_direct'
        }
    else:
        return {
            'success': False,
            'error': f'LinkedIn API error: {response.status_code} - {response.text}',
            'status_code': response.status_code
        }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            'success': False,
            'error': 'Usage: python post_linkedin_revised.py <content> [image_url]'
        }))
        sys.exit(1)

    content = sys.argv[1]
    image_url = sys.argv[2] if len(sys.argv) > 2 else None

    # Load access token
    access_token = load_access_token()

    if not access_token:
        print(json.dumps({
            'success': False,
            'error': 'LinkedIn not authenticated. Please run setup_linkedin_auth.py first.',
            'action_required': 'authentication'
        }))
        sys.exit(1)

    # Post to LinkedIn
    result = post_to_linkedin(access_token, content, image_url)
    print(json.dumps(result))

if __name__ == '__main__':
    main()