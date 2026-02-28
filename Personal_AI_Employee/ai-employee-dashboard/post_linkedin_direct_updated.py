#!/usr/bin/env python3
"""
Direct LinkedIn Poster - Post to LinkedIn immediately
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

def get_user_info(access_token):
    """Get LinkedIn user profile information - tries multiple endpoints"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # First, try the standard /me endpoint
    response = requests.get(
        f"{LINKEDIN_API_URL}/me",
        headers=headers
    )

    if response.status_code == 200:
        return response.json()

    # If /me fails (403) but the token is valid, try alternatives for posting
    elif response.status_code == 403:
        print("Note: Token has limited permissions but may still be valid for posting", file=sys.stderr)
        # Return a special marker that indicates token is valid but we can't get user details
        return {"error": "permission_denied", "token_valid": True}

    # If we get other errors, return None
    return None

def get_user_urn_from_token(access_token):
    """Alternative method to get user URN when /me endpoint is not available"""
    # For tokens with w_member_social scope, often we can use a special header
    # to get the effective user without explicitly fetching profile data
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Make a test call to check if token is valid for posting
    response = requests.get(
        f"{LINKEDIN_API_URL}/ugcPosts",
        headers=headers,
        params={
            'q': 'author',
            'author': 'urn:li:person:me'  # Try using special 'me' URN
        }
    )

    # If this doesn't error with invalid token, then the token is valid
    # and we can try posting using 'urn:li:person:me' directly
    if response.status_code in [200, 403]:  # 403 might just mean no permission to list posts, not that token is invalid
        return 'urn:li:person:me'

    # If the above doesn't work, try to get user ID using userinfo endpoint (might work with limited scopes)
    response = requests.get(f"{LINKEDIN_API_URL}/userinfo", headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        user_id = user_data.get('sub')  # For userinfo endpoint, user ID is often in 'sub' field
        if user_id:
            return f"urn:li:person:{user_id}"

    return None

def post_to_linkedin(access_token, content, image_url=None):
    """Post content to LinkedIn"""

    # Try to get user info first
    user_info = get_user_info(access_token)

    if not user_info:
        # If user_info is None, the token is truly invalid
        return {
            'success': False,
            'error': 'Failed to get user information. Token may be expired.'
        }
    elif user_info.get('error') == 'permission_denied':
        # The token is valid but we can't get user info, try alternative approach
        print("Token valid but limited permissions detected. Attempting to post with default URN.", file=sys.stderr)
        user_urn = get_user_urn_from_token(access_token)

        if not user_urn:
            return {
                'success': False,
                'error': 'Unable to determine user URN for posting. Please verify token permissions.'
            }
    else:
        # Normal case where we can get user info
        user_id = user_info.get('id')
        if not user_id:
            return {
                'success': False,
                'error': 'Unable to retrieve user ID from token.'
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
            'error': 'Usage: python post_linkedin_direct.py <content> [image_url]'
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