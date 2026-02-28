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
CONFIG_FILE = Path('linkedin_config.json')

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
    """Get LinkedIn user profile information - tries multiple methods due to API restrictions"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Try standard /me endpoint first
    response = requests.get(
        f"{LINKEDIN_API_URL}/me",
        headers=headers
    )

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403:
        # For tokens with w_member_social scope, we might need to use a different approach
        # Check if the token is valid by trying to access a user-specific endpoint
        # that doesn't require full profile access
        print("Token has limited permissions but may still be valid for posting", file=sys.stderr)
        # Return a marker that indicates token is valid but can't get full user info
        return {"error": "permission_denied", "token_valid": True}

    return None

def load_hardcoded_urn():
    """Load hardcoded LinkedIn Person URN from config file"""
    if not CONFIG_FILE.exists():
        return None

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('linkedin_person_urn')
    except Exception as e:
        print(f"Error loading LinkedIn config: {e}", file=sys.stderr)
        return None

def get_user_urn(access_token):
    """Get user URN for posting with multiple fallback methods"""
    # First, try to use hardcoded URN from config file
    hardcoded_urn = load_hardcoded_urn()
    if hardcoded_urn:
        print(f"Using hardcoded URN from config: {hardcoded_urn}", file=sys.stderr)
        return hardcoded_urn

    # Fallback to API-based approach
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-RestLi-Protocol-Version': '2.0.0'
    }

    # First try to get user ID using projection with multiple scopes
    response = requests.get(
        f"{LINKEDIN_API_URL}/me?projection=(id,firstName,lastName,vanityName)",
        headers=headers
    )

    if response.status_code == 200:
        user_data = response.json()
        user_id = user_data.get('id')
        if user_id:
            # Try both possible URN formats that LinkedIn accepts
            # Format 1: urn:li:person:{id} - This is the original format
            # Format 2: urn:li:member:{id} - This is what the error message suggests
            user_urn = f"urn:li:member:{user_id}"
            return user_urn

    # If that fails, try without the projection parameter (as a fallback)
    response = requests.get(
        f"{LINKEDIN_API_URL}/me",
        headers=headers
    )

    if response.status_code == 200:
        user_data = response.json()
        user_id = user_data.get('id')
        if user_id:
            user_urn = f"urn:li:member:{user_id}"
            return user_urn

    print("Info: Unable to retrieve user URN directly. Token may have limited permissions.", file=sys.stderr)
    print("Info: Check if you have configured your LinkedIn Person URN in linkedin_config.json", file=sys.stderr)
    return None

def post_to_linkedin(access_token, content, image_url=None):
    """Post content to LinkedIn"""

    # First, try to get the user URN from the config file (hardcoded)
    user_urn = get_user_urn(access_token)

    # If we couldn't get it from config, fall back to API-based approach
    if not user_urn:
        # Get user info via API as fallback
        user_info = get_user_info(access_token)
        if not user_info:
            return {
                'success': False,
                'error': 'Failed to get user information. Token may be expired.'
            }

        user_id = user_info.get('id')
        if user_id:
            # LinkedIn API expects either urn:li:person:ID or urn:li:member:ID
            # Based on the error message, it seems like it should be urn:li:member:ID
            user_urn = f"urn:li:member:{user_id}"
        else:
            return {
                'success': False,
                'error': 'Could not retrieve user URN for posting.'
            }

    if not user_urn:
        return {
            'success': False,
            'error': 'Could not determine user URN for posting. Please configure your URN in linkedin_config.json or ensure you have proper API permissions.'
        }

    print(f"Attempting to post as {user_urn}", file=sys.stderr)

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
    elif response.status_code == 422 and "does not match urn:li:company:" in response.text and "urn:li:member:" in response.text:
        # This is the specific error we get when using non-numeric IDs
        print("Note: The URN contains non-numeric ID. LinkedIn requires numeric member IDs.", file=sys.stderr)
        print("You need to find your numeric LinkedIn member ID or use queue-based posting.", file=sys.stderr)
        return {
            'success': False,
            'error': 'LinkedIn API requires numeric member ID. Please use queue-based posting or find your numeric member ID.',
            'action_required': 'queue_fallback'
        }
    elif response.status_code == 403 and "Field Value validation failed" in response.text:
        # This is the error we get when using non-numeric IDs with the member format
        print("Note: The URN format is valid but the ID might not be numeric as required.", file=sys.stderr)
        return {
            'success': False,
            'error': 'LinkedIn API requires numeric member ID. Please use queue-based posting or find your numeric member ID.',
            'action_required': 'queue_fallback'
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
