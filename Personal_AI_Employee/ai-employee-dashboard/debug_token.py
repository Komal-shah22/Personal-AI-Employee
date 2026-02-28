#!/usr/bin/env python3
"""
Debug script to check token file loading
"""

import json
from pathlib import Path

def debug_load_token():
    """Debug loading LinkedIn token data from credentials file"""
    print("Current working directory:", Path.cwd())

    # Check in current directory first, then in parent directory
    token_file = Path('credentials/linkedin_token.json')
    print("Checking for token file:", token_file.absolute())
    print("Does current directory token file exist?", token_file.exists())

    if not token_file.exists():
        token_file = Path('../credentials/linkedin_token.json')
        print("Checking for parent directory token file:", token_file.absolute())
        print("Does parent directory token file exist?", token_file.exists())

    if not token_file.exists():
        print("Token file not found in current or parent directory")
        return None

    try:
        with open(token_file, 'r') as f:
            data = json.load(f)
            print("Token file loaded successfully!")
            print("Token keys:", list(data.keys()))
            return data
    except Exception as e:
        print(f"Error loading token: {e}")
        return None

# Run the debug function
token_data = debug_load_token()
if token_data:
    print("Refresh token exists:", 'refresh_token' in token_data)
    if 'refresh_token' in token_data:
        print("Refresh token value present:", bool(token_data.get('refresh_token')))