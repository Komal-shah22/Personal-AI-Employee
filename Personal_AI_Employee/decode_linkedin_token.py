#!/usr/bin/env python3
"""
Decode the LinkedIn access token to see if we can extract the user's member ID
"""

import json
import base64
from pathlib import Path

def decode_jwt_payload(token):
    """Decode JWT token payload to extract information"""
    try:
        # Split the token into its parts
        parts = token.split('.')
        if len(parts) != 3:
            print("Invalid JWT token format")
            return None

        # The payload is the second part, base64 encoded
        payload_b64 = parts[1]

        # Add padding if necessary
        missing_padding = len(payload_b64) % 4
        if missing_padding:
            payload_b64 += '=' * (4 - missing_padding)

        # Decode the payload
        payload_bytes = base64.b64decode(payload_b64)
        payload_str = payload_bytes.decode('utf-8')

        import json
        payload = json.loads(payload_str)
        return payload
    except Exception as e:
        print(f"Error decoding token: {e}")
        return None

def main():
    print("LinkedIn Token Decoder")
    print("=" * 25)

    TOKEN_FILE = Path('credentials/linkedin_token.json')

    if not TOKEN_FILE.exists():
        print("No LinkedIn token file found!")
        print("Run 'python setup_linkedin_auth.py' to authenticate first.")
        return

    # Load the token
    with open(TOKEN_FILE, 'r') as f:
        token_data = json.load(f)
        access_token = token_data.get('access_token')

    if not access_token:
        print("No access token found in credentials file")
        return

    print("Decoding access token...")
    payload = decode_jwt_payload(access_token)

    if payload:
        print("\nToken Payload Information:")
        print("-" * 30)
        for key, value in payload.items():
            print(f"{key}: {value}")

        print(f"\nLooking for user ID in token...")
        user_id = None
        possible_keys = ['sub', 'member_id', 'id', 'userId', 'user_id']

        for key in possible_keys:
            if key in payload:
                user_id = payload[key]
                print(f"Found potential user ID in '{key}': {user_id}")
                break

        if user_id:
            print(f"\nYou can update your config with this ID:")
            print(f'  "linkedin_person_urn": "urn:li:member:{user_id}"')
        else:
            print("\nCould not find user ID in token payload.")
            print("The user ID might not be included in the token.")
    else:
        print("Could not decode token.")

if __name__ == '__main__':
    main()