import os
import json
from datetime import datetime, timedelta

from dotenv import load_dotenv
# Load environment variables
load_dotenv('.env.local')

def save_token_to_file(token_data, file_path='credentials/linkedin_token.json'):
    """Save LinkedIn token data to a file with timestamp"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Add timestamp for tracking when the token was issued
    token_with_metadata = {
        **token_data,
        'timestamp': datetime.now().isoformat(),
        'expires_at': (datetime.now() + timedelta(seconds=token_data.get('expires_in', 0))).isoformat()
    }

    with open(file_path, 'w') as f:
        json.dump(token_with_metadata, f, indent=2)

    print(f"Token saved to {file_path}")

def load_token_from_file(file_path='credentials/linkedin_token.json'):
    """Load LinkedIn token data from file"""
    try:
        with open(file_path, 'r') as f:
            token_data = json.load(f)

        return token_data
    except FileNotFoundError:
        print(f"Token file {file_path} not found")
        return None

def is_token_expired(token_data):
    """Check if the token is expired"""
    if not token_data or 'expires_at' not in token_data:
        return True

    expires_at = datetime.fromisoformat(token_data['expires_at'])
    return datetime.now() > expires_at

def get_linkedin_access_token():
    """Get the LinkedIn access token from credentials file"""
    token_data = load_token_from_file()
    if token_data:
        return token_data.get('access_token')
    return None

def create_manual_token_file():
    """Create a manual token file if you have an existing token"""
    print("LinkedIn Token Setup - Manual Entry")
    print("==================================")
    print("If you have an existing LinkedIn access token, you can manually enter it here.")
    print("Otherwise, you'll need to go through the OAuth flow using the LinkedIn developers portal.")
    print()

    # Check for existing credentials
    client_id = os.getenv('LINKEDIN_CLIENT_ID')
    client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
    redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI')

    print(f"Client ID: {client_id or 'Not found in environment'}")
    print(f"Client Secret: {'*' * 10 if client_secret else 'Not found in environment'}")
    print(f"Redirect URI: {redirect_uri or 'Not found in environment'}")
    print()

    print("Note: To get a LinkedIn access token:")
    print("1. Go to https://www.linkedin.com/developers/")
    print("2. Create an app or select your existing app")
    print("3. Go to 'Products' and enable 'Share on LinkedIn'")
    print("4. Go to 'Auth' tab and use the OAuth 2.0 flow to get an access token")
    print()

    # For now, we'll just create a template
    template_token = {
        "access_token": "your_actual_access_token_here",
        "expires_in": 5184000,  # 60 days in seconds (typical for LinkedIn)
        "scope": "w_member_social",
        "token_type": "Bearer"
    }

    save_token_to_file(template_token)
    print()
    print("Template token file created with placeholder.")
    print("Replace 'your_actual_access_token_here' with your real access token in credentials/linkedin_token.json")

if __name__ == "__main__":
    create_manual_token_file()