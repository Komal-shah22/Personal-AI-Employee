#!/usr/bin/env python3
"""
LinkedIn OAuth Setup - Authenticate with LinkedIn API
"""

import os
import json
import webbrowser
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, will use system env vars

# LinkedIn OAuth Configuration
LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID', '')
LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET', '')
REDIRECT_URI = 'http://localhost:8888/callback'
SCOPES = 'w_member_social r_liteprofile r_emailaddress'

# Storage
CREDENTIALS_DIR = Path('credentials')
TOKEN_FILE = CREDENTIALS_DIR / 'linkedin_token.json'

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback"""

    def do_GET(self):
        """Handle GET request from OAuth callback"""
        query = urlparse(self.path).query
        params = parse_qs(query)

        if 'code' in params:
            auth_code = params['code'][0]

            # Exchange code for access token
            token_data = exchange_code_for_token(auth_code)

            if token_data:
                # Save token
                CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
                with open(TOKEN_FILE, 'w') as f:
                    json.dump(token_data, f, indent=2)

                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                html_content = """
                    <html>
                    <body style="font-family: Arial; text-align: center; padding: 50px;">
                        <h1 style="color: #0077B5;">✅ LinkedIn Authentication Successful!</h1>
                        <p>You can close this window and return to the terminal.</p>
                        <p>Your LinkedIn account is now connected to the AI Employee Dashboard.</p>
                    </body>
                    </html>
                """
                self.wfile.write(html_content.encode('utf-8'))

                print("\n[SUCCESS] LinkedIn authenticated successfully!")
                print(f"Token saved to: {TOKEN_FILE}")
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                html_content = """
                    <html>
                    <body style="font-family: Arial; text-align: center; padding: 50px;">
                        <h1 style="color: red;">❌ Authentication Failed</h1>
                        <p>Could not exchange authorization code for access token.</p>
                        <p>Please check your LinkedIn API credentials and try again.</p>
                    </body>
                    </html>
                """
                self.wfile.write(html_content.encode('utf-8'))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('<html><body><h1>Error: No authorization code received</h1></body></html>'.encode('utf-8'))

    def log_message(self, format, *args):
        """Suppress log messages"""
        pass

def exchange_code_for_token(auth_code):
    """Exchange authorization code for access token"""
    token_url = 'https://www.linkedin.com/oauth/v2/accessToken'

    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': LINKEDIN_CLIENT_ID,
        'client_secret': LINKEDIN_CLIENT_SECRET
    }

    try:
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def main():
    print("=" * 60)
    print("LinkedIn OAuth Setup for AI Employee Dashboard")
    print("=" * 60)

    # Check if credentials are set
    if not LINKEDIN_CLIENT_ID or not LINKEDIN_CLIENT_SECRET:
        print("\n[ERROR] LinkedIn API credentials not found!")
        print("\nPlease set the following environment variables:")
        print("  - LINKEDIN_CLIENT_ID")
        print("  - LINKEDIN_CLIENT_SECRET")
        print("\nOr create a .env file with these values.")
        print("\nTo get LinkedIn API credentials:")
        print("1. Go to https://www.linkedin.com/developers/apps")
        print("2. Create a new app or select existing app")
        print("3. Get Client ID and Client Secret from 'Auth' tab")
        print("4. Add redirect URL: http://localhost:8888/callback")
        return

    # Build authorization URL
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={LINKEDIN_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPES}"
    )

    print("\n[SETUP] Instructions:")
    print("1. A browser window will open")
    print("2. Log in to LinkedIn if not already logged in")
    print("3. Authorize the application")
    print("4. You'll be redirected back automatically")
    print("\nStarting OAuth flow...\n")

    # Start local server
    server = HTTPServer(('localhost', 8888), OAuthCallbackHandler)

    # Open browser
    print(f"Opening browser for authentication...")
    webbrowser.open(auth_url)

    print("Waiting for authorization...")
    print("(Server running on http://localhost:8888)")

    # Handle one request (the callback)
    server.handle_request()

    print("\nSetup complete!")

if __name__ == '__main__':
    main()
