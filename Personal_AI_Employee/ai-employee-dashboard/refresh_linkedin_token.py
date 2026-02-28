#!/usr/bin/env python3
"""
Script to refresh the LinkedIn access token using the refresh token from the parent directory
"""

import json
import requests
from urllib.parse import urlencode
from pathlib import Path
import os

def refresh_access_token(refresh_token, client_id, client_secret):
    """Refresh the access token using refresh token"""
    token_url = 'https://www.linkedin.com/oauth/v2/accessToken'

    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }

    print("Attempting to refresh access token...")
    response = requests.post(token_url, data=payload)

    if response.status_code == 200:
        token_data = response.json()
        print("Successfully refreshed access token!")
        return token_data
    else:
        print(f"Error refreshing access token: {response.status_code} - {response.text}")
        return None

def main():
    # Load token data from parent directory where the refresh token exists
    token_file = Path('../credentials/linkedin_token.json')

    if not token_file.exists():
        print(f"Token file does not exist at {token_file}")
        return

    try:
        with open(token_file, 'r') as f:
            token_data = json.load(f)
    except Exception as e:
        print(f"Error loading token: {e}")
        return

    # Load credentials from environment
    from dotenv import load_dotenv
    load_dotenv('.env.local')

    client_id = os.getenv('LINKEDIN_CLIENT_ID')
    client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')

    if not all([client_id, client_secret]):
        print("LinkedIn credentials not found in environment variables")
        return

    # Get the refresh token
    refresh_token = token_data.get('refresh_token')

    if not refresh_token:
        print("No refresh token found in token data")
        print(f"Available keys in token data: {list(token_data.keys())}")
        return

    print(f"Current access token expires in: {token_data.get('expires_in', 'unknown')} seconds")
    print(f"Refresh token expires in: {token_data.get('refresh_token_expires_in', 'unknown')} seconds")

    # Attempt to refresh the token
    new_token_data = refresh_access_token(refresh_token, client_id, client_secret)

    if new_token_data:
        # Save the new token data to both locations to keep them in sync
        # Save to parent directory
        parent_token_file = Path('../credentials/linkedin_token.json')
        parent_token_file.parent.mkdir(parents=True, exist_ok=True)
        with open(parent_token_file, 'w') as f:
            json.dump(new_token_data, f, indent=2)

        # Save to current directory
        current_token_file = Path('credentials/linkedin_token.json')
        current_token_file.parent.mkdir(parents=True, exist_ok=True)
        with open(current_token_file, 'w') as f:
            json.dump(new_token_data, f, indent=2)

        print("New token saved to both locations")
        print(f"New token saved to {parent_token_file}")
        print(f"New token saved to {current_token_file}")

        # Display the new token info (without showing the actual token for security)
        print("Token refresh completed successfully!")
        print(f"New token expires in: {new_token_data.get('expires_in', 'unknown')} seconds")
        print(f"New refresh token expires in: {new_token_data.get('refresh_token_expires_in', 'unknown')} seconds")

        # Update the current working directory's token file as well
        if 'refresh_token' in new_token_data:
            print(f"New refresh token available: {bool(new_token_data.get('refresh_token'))}")
    else:
        print("Failed to refresh token. You may need to re-authenticate.")

if __name__ == '__main__':
    main()