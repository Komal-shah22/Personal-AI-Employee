#!/usr/bin/env python3
"""
Check if we can get the user ID using the X-Robots-Tag header approach
or alternative methods that might work with w_member_social scope
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

def check_alternative_approaches():
    """Try alternative approaches to get user information"""
    access_token = load_access_token()

    if not access_token:
        print("No access token found")
        return

    # Headers with the proper protocol version
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-RestLi-Protocol-Version': '2.0.0',
        'Content-Type': 'application/json'
    }

    print("Testing alternative approaches for user identification...")

    # Try approach: Make a request to get the authenticated user's connections or similar
    # This might return metadata that includes the user's own ID
    print("\n=== Trying to use /networkSizes endpoint ===")
    try:
        response = requests.get(
            f"{LINKEDIN_API_URL}/networkSizes",
            headers=headers,
            params={'edgeType': 'S'}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"JSON Response: {json.dumps(data, indent=2)}")
            except:
                print(f"Non-JSON Response: {response.text}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

    # Try getting the user's own profile using the correct endpoint
    print("\n=== Trying /me endpoint with different parameters ===")
    try:
        # With the new LinkedIn API, the endpoint might require different setup
        response = requests.get(
            f"{LINKEDIN_API_URL}/me",
            headers=headers,
            params={'projection': '(id,firstName,lastName,vanityName,email)'}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"JSON Response: {json.dumps(data, indent=2)}")
                if 'id' in data:
                    user_id = data['id']
                    print(f"SUCCESS: Found user ID: {user_id}")
                    print(f"User URN would be: urn:li:member:{user_id}")
                    return f"urn:li:member:{user_id}"
            except:
                print(f"Non-JSON Response: {response.text}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

    # Try an alternative: Get the user's own shares to see if author info is included
    print("\n=== Trying to fetch user's own posts ===")
    try:
        response = requests.get(
            f"{LINKEDIN_API_URL}/ugcPosts",
            headers=headers,
            params={'q': 'author', 'author': 'me'}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

    # The most likely solution: Try using the /identityLookup endpoint if it exists
    print("\n=== Trying identity lookup approach ===")
    try:
        # This is a hypothetical approach - we'll see if there's an endpoint that can give us
        # the authenticated user's ID without requiring profile access
        response = requests.get(
            f"{LINKEDIN_API_URL}/me",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"JSON Response: {json.dumps(data, indent=2)}")
                if 'id' in data:
                    user_id = data['id']
                    print(f"SUCCESS: Found user ID: {user_id}")
                    print(f"User URN would be: urn:li:member:{user_id}")
                    return f"urn:li:member:{user_id}"
            except:
                print(f"Non-JSON Response: {response.text}")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

    return None

def main():
    print("LinkedIn User Identity Check")
    print("=" * 30)

    result = check_alternative_approaches()

    if result:
        print(f"\nFound user URN: {result}")
        print("You can now use this URN for posting by updating your script.")
    else:
        print("\nCould not retrieve user identity with current token permissions.")
        print("The 'w_member_social' scope appears to be limited for direct posting.")
        print("The current fallback to queue-based posting is the correct approach.")

if __name__ == '__main__':
    main()