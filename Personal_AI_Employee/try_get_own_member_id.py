#!/usr/bin/env python3
"""
Try to get the authenticated user's member ID using alternative endpoints
"""

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

def try_get_member_id():
    """Try various endpoints to get the member ID"""
    access_token = load_access_token()
    if not access_token:
        print("No access token found!")
        return

    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-RestLi-Protocol-Version': '2.0.0',
        'Content-Type': 'application/json'
    }

    # Test different endpoints that might return member information
    endpoints_to_try = [
        # Standard me endpoint (we know this fails with current scope)
        ("me", f"{LINKEDIN_API_URL}/me"),

        # Try with actions endpoint which might return user context
        ("ugcPosts with query", f"{LINKEDIN_API_URL}/ugcPosts"),

        # Try the network endpoint
        ("network", f"{LINKEDIN_API_URL}/networkElements"),

        # Try the connections endpoint
        ("connections", f"{LINKEDIN_API_URL}/connections"),

        # Try a search for the authenticated user
        ("search for self", f"{LINKEDIN_API_URL}/search?q=members&firstName=firstName&lastName=lastName"),
    ]

    for name, endpoint in endpoints_to_try:
        print(f"\nTrying: {name}")
        try:
            if name == "ugcPosts with query":
                # Try to query own posts
                response = requests.get(endpoint,
                    headers=headers,
                    params={'q': 'author', 'author': 'me'})
            elif name == "search for self":
                response = requests.get(endpoint, headers=headers)
            else:
                response = requests.get(endpoint, headers=headers)

            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("SUCCESS! Response contains data - might have user ID")
                try:
                    data = response.json()
                    print(f"Response: {json.dumps(data, indent=2)[:500]}...")
                    # Look for ID fields in the response
                    if 'elements' in data:
                        for element in data.get('elements', []):
                            if 'person' in element:
                                person = element['person']
                                if 'entityUrn' in person:
                                    print(f"Found entity URN: {person['entityUrn']}")
                                if 'id' in person:
                                    print(f"Found ID: {person['id']}")
                            elif 'id' in element:
                                print(f"Found element ID: {element['id']}")
                    # Check for any ID field
                    for key, value in data.items():
                        if 'id' in key.lower():
                            print(f"Found ID field {key}: {value}")
                except:
                    print(f"Non-JSON response: {response.text[:500]}...")
            elif response.status_code == 403:
                print("Access denied - insufficient permissions")
            elif response.status_code == 404:
                print("Endpoint not found")
            else:
                print(f"Response: {response.text[:500]}...")
        except Exception as e:
            print(f"Error: {e}")

def main():
    print("Attempting to get member ID from LinkedIn API")
    print("=" * 50)

    try_get_member_id()

    print("\n" + "="*50)
    print("CONCLUSION:")
    print("If the above attempts didn't return a numeric member ID,")
    print("then LinkedIn only provides member IDs with higher permission scopes.")
    print("")
    print("To get your numeric LinkedIn member ID, you may need to:")
    print("1. Update your LinkedIn app to request 'r_liteprofile' scope")
    print("2. Use a LinkedIn tool or service that can extract member IDs")
    print("3. Or continue using the queue-based posting approach")

if __name__ == '__main__':
    main()