import os
import requests
import json
from urllib.parse import urlencode
import webbrowser
import http.server
import socketserver
from threading import Thread
import time

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv('.env.local')
except ImportError:
    print("python-dotenv not found, environment variables will be loaded from system")
    pass

class LinkedInOAuth:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.authorization_base_url = 'https://www.linkedin.com/oauth/v2/authorization'
        self.token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
        # Using only w_member_social which allows posting to LinkedIn
        self.scopes = ['w_member_social']

    def get_authorization_url(self):
        """Generate the authorization URL for LinkedIn OAuth"""
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(self.scopes)
        }
        return f"{self.authorization_base_url}?{urlencode(params)}"

    def get_access_token(self, authorization_code):
        """Exchange authorization code for access token"""
        payload = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        response = requests.post(self.token_url, data=payload)
        if response.status_code == 200:
            token_data = response.json()
            return token_data
        else:
            raise Exception(f"Error getting access token: {response.text}")

    def refresh_access_token(self, refresh_token):
        """Refresh the access token using refresh token"""
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        response = requests.post(self.token_url, data=payload)
        if response.status_code == 200:
            token_data = response.json()
            return token_data
        else:
            raise Exception(f"Error refreshing access token: {response.text}")

    def verify_token(self, access_token):
        """Verify the access token by fetching user profile"""
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        # Only using the most basic profile endpoint that might work without special scopes
        profile_url = 'https://api.linkedin.com/v2/userinfo'

        profile_response = requests.get(profile_url, headers=headers)

        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            return {
                'profile': profile_data
            }
        elif profile_response.status_code == 403:
            # If 403, try alternative endpoint for validation
            test_url = 'https://api.linkedin.com/v2/ugcPosts'
            test_response = requests.get(test_url, headers=headers, params={'author': 'me'})
            if test_response.status_code == 200:
                return {'profile': {'success': 'Token validated through posts access'}}
            else:
                raise Exception(f"Error verifying token: {test_response.text}")
        else:
            raise Exception(f"Error verifying token: Profile {profile_response.text}")

class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/callback'):
            # Extract authorization code from URL
            query = self.path.split('?', 1)[1] if '?' in self.path else ''
            params = {}
            for param in query.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    params[key] = value

            authorization_code = params.get('code')
            if authorization_code:
                # Send success response to browser
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"""
                <html>
                    <body>
                        <h1>Authentication Successful!</h1>
                        <p>You can now close this window and return to the terminal.</p>
                    </body>
                </html>
                """)

                # Store the authorization code in the class
                self.server.authorization_code = authorization_code
            else:
                # Check if there's an error in the URL
                error = params.get('error')
                error_description = params.get('error_description')
                if error:
                    print(f"\nLinkedIn OAuth Error: {error}")
                    print(f"Error description: {error_description}")

                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<h1>Authorization failed</h1><p>Please check console for error details.</p>')
        else:
            self.send_response(404)
            self.end_headers()

def start_server(port=8888):
    """Start a simple HTTP server to handle OAuth callback"""
    server = socketserver.TCPServer(("", port), OAuthCallbackHandler)
    server.authorization_code = None
    return server

def setup_linkedin_auth():
    print("LinkedIn OAuth Setup")
    print("====================")
    print("\nNote: LinkedIn requires application verification for most API scopes.")
    print("For full profile access (r_basicprofile, r_emailaddress), you must:")
    print("1. Go to https://www.linkedin.com/developers/")
    print("2. Select your application")
    print("3. Submit for verification under 'Products' -> 'Sign In with LinkedIn'")
    print("4. Wait for approval before using those scopes\n")

    # Get credentials from .env.local or environment variables
    client_id = os.getenv('LINKEDIN_CLIENT_ID')
    client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
    redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI')

    if not all([client_id, client_secret, redirect_uri]):
        print("Error: LinkedIn credentials not found in environment variables.")
        print("Please make sure LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, and LINKEDIN_REDIRECT_URI are set in your .env.local file.")
        return

    oauth = LinkedInOAuth(client_id, client_secret, redirect_uri)

    # Start the callback server in a separate thread
    server = start_server()
    server_thread = Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print(f"Callback server started on {redirect_uri}")
    print("Getting authorization URL...")

    auth_url = oauth.get_authorization_url()
    print(f"Authorization URL: {auth_url}")

    # Open the authorization URL in the browser
    print("\nOpening LinkedIn authorization page in your browser...")
    webbrowser.open(auth_url)

    print("\nWaiting for authorization... (Please complete the authorization in your browser)")
    print("If the browser doesn't open automatically, please visit the URL above manually.")
    print("\nIMPORTANT: After logging into LinkedIn, you may see an error page.")
    print("This is normal if your LinkedIn app has not been verified for full profiles.")
    print("The authorization will still work if you've granted the 'w_member_social' permission.\n")

    # Wait for the authorization code
    timeout = 120  # 120 seconds timeout to accommodate the process
    start_time = time.time()

    while not server.authorization_code and time.time() - start_time < timeout:
        time.sleep(1)

    if server.authorization_code:
        print("\nAuthorization code received!")

        try:
            # Exchange authorization code for access token
            print("Exchanging authorization code for access token...")
            token_data = oauth.get_access_token(server.authorization_code)

            # Create credentials directory if it doesn't exist
            os.makedirs('credentials', exist_ok=True)

            # Save the token data to a file
            with open('credentials/linkedin_token.json', 'w') as f:
                json.dump(token_data, f, indent=2)

            print("\nAccess token saved to credentials/linkedin_token.json")
            print("Token data has been saved successfully.")

            # Try to verify the token
            print("\nVerifying the token...")
            try:
                user_info = oauth.verify_token(token_data['access_token'])
                print("Token verified successfully!")
                print("User profile info:", json.dumps(user_info['profile'], indent=2))
            except Exception as verify_error:
                print(f"Warning: Could not verify token details due to: {verify_error}")
                print("This is normal if LinkedIn app is not verified for profile scopes.")
                print("The token itself is still valid for the authorized scopes.")

        except Exception as e:
            print(f"Error getting access token: {e}")
    else:
        print("\nTimeout: Authorization code not received within 120 seconds.")
        print("Please try again, ensuring you:")
        print("1. Log into LinkedIn with the correct account")
        print("2. Approve the application permissions")
        print("3. Check for any pop-up blockers in your browser")

    # Shutdown the server
    server.shutdown()

if __name__ == "__main__":
    setup_linkedin_auth()