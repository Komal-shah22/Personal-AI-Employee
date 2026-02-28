#!/usr/bin/env python3
"""
Debug script to test LinkedIn token and get user information
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

def test_user_endpoints(access_token):
    """Test various LinkedIn API endpoints to get user information"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-RestLi-Protocol-Version': '2.0.0'
    }

    # Test different endpoints
    endpoints = [
        f"{LINKEDIN_API_URL}/me?projection=(id,firstName,lastName,vanityName)",
        f"{LINKEDIN_API_URL}/me",
        f"{LINKEDIN_API_URL}/me?fields=id,firstName,lastName,vanityName",
    ]

    print("Testing different LinkedIn API endpoints...")

    for i, endpoint in enumerate(endpoints, 1):
        print(f"\nTesting endpoint {i}: {endpoint}")
        try:
            response = requests.get(endpoint, headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")

            if response.status_code == 200:
                data = response.json()
                print(f"Parsed JSON: {json.dumps(data, indent=2)}")

                user_id = data.get('id')
                if user_id:
                    user_urn = f"urn:li:person:{user_id}"
                    print(f"Found user URN: {user_urn}")
                    return user_urn
                else:
                    print("No 'id' field found in response")

        except Exception as e:
            print(f"Error with endpoint {i}: {e}")

    return None

def main():
    print("LinkedIn Token Debug Tool")
    print("=" * 30)

    access_token = load_access_token()

    if not access_token:
        print("No LinkedIn access token found!")
        return

    print(f"Access token loaded (first 20 chars): {access_token[:20]}...")

    # Get token scope
    try:
        with open(TOKEN_FILE, 'r') as f:
            token_data = json.load(f)
            scope = token_data.get('scope', 'unknown')
            print(f"Token scope: {scope}")
    except:
        print("Could not determine token scope")

    user_urn = test_user_endpoints(access_token)

    if user_urn:
        print(f"\nSUCCESS: Found user URN - {user_urn}")
    else:
        print(f"\nFAILED: Could not retrieve user URN")
        print("Your token may have insufficient permissions for direct posting.")
        print("The w_member_social scope may not include the right permissions to get user ID.")
        print("You might need additional scopes or a different app configuration.")

if __name__ == '__main__':
    main()