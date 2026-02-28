#!/usr/bin/env python3
"""
Test script to debug the exact token capabilities
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

def test_endpoints():
    access_token = load_access_token()
    if not access_token:
        print("No access token found")
        return

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Test /me endpoint
    print("Testing /me endpoint...")
    response = requests.get('https://api.linkedin.com/v2/me', headers=headers)
    print(f"/me - Status: {response.status_code}")
    print(f"/me - Response: {response.text[:200]}...")  # First 200 chars

    # Test /me with projection
    print("\nTesting /me?projection=(id) endpoint...")
    response = requests.get('https://api.linkedin.com/v2/me?projection=(id)', headers=headers)
    print(f"/me?projection=(id) - Status: {response.status_code}")
    print(f"/me?projection=(id) - Response: {response.text[:200]}...")  # First 200 chars

    # Test /userinfo endpoint
    print("\nTesting /userinfo endpoint...")
    response = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers)
    print(f"/userinfo - Status: {response.status_code}")
    print(f"/userinfo - Response: {response.text[:200]}...")  # First 200 chars

    # Test token introspection by trying to post with a generic method
    print("\nTesting if we can get the user ID from token introspection...")
    # Sometimes the user ID can be obtained from the token itself
    # Let's try to make a post with a different approach
    print("Based on LinkedIn API documentation for w_member_social scope:")
    print("We might need to use the member ID from the original auth process")
    print("This is a common limitation with unverified LinkedIn apps.")

if __name__ == '__main__':
    test_endpoints()