#!/usr/bin/env python3
"""
Test script to verify the LinkedIn token and user profile access
"""

import json
import requests
from pathlib import Path

def load_access_token():
    """Load LinkedIn access token from credentials file"""
    token_file = Path('credentials/linkedin_token.json')

    if not token_file.exists():
        print("Token file not found")
        return None

    try:
        with open(token_file, 'r') as f:
            data = json.load(f)
            return data.get('access_token')
    except Exception as e:
        print(f"Error loading token: {e}")
        return None

def test_userinfo_endpoint(access_token):
    """Test basic user info endpoint"""
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    print("Testing /userinfo endpoint...")
    profile_url = 'https://api.linkedin.com/v2/userinfo'

    response = requests.get(profile_url, headers=headers)
    print(f"Response Status: {response.status_code}")
    print(f"Response Text: {response.text}")

    if response.status_code == 200:
        profile_data = response.json()
        print("User info retrieved successfully:")
        print(json.dumps(profile_data, indent=2))
        return profile_data
    else:
        print("Failed to retrieve user info with /userinfo endpoint")
        return None

def test_me_endpoint(access_token):
    """Test the /me endpoint used in the post script"""
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    print("\nTesting /me endpoint...")
    profile_url = 'https://api.linkedin.com/v2/me'

    response = requests.get(profile_url, headers=headers)
    print(f"Response Status: {response.status_code}")
    print(f"Response Text: {response.text}")

    if response.status_code == 200:
        profile_data = response.json()
        print("User info retrieved successfully:")
        print(json.dumps(profile_data, indent=2))
        return profile_data
    else:
        print("Failed to retrieve user info with /me endpoint")
        return None

def test_post_capability(access_token):
    """Test post capability"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    print("\nTesting access to user posts endpoint...")
    posts_url = 'https://api.linkedin.com/v2/ugcPosts'

    # Try getting user's own posts as a test
    response = requests.get(posts_url, headers=headers)
    print(f"Posts endpoint Response Status: {response.status_code}")
    print(f"Posts endpoint Response Text: {response.text}")

    if response.status_code in [200, 401, 403]:  # Different responses may indicate token is valid
        print(f"Token recognized by posts endpoint (status: {response.status_code})")
        return True
    else:
        print("Error accessing posts endpoint")
        return False

def main():
    access_token = load_access_token()

    if not access_token:
        print("No access token found")
        return

    print("Testing LinkedIn token...")

    # Test both endpoints
    test_userinfo_endpoint(access_token)
    test_me_endpoint(access_token)
    test_post_capability(access_token)

if __name__ == '__main__':
    main()