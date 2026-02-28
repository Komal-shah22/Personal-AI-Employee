#!/usr/bin/env python3
"""
LinkedIn Token Upgrade Helper
This script explains how to get a proper token with required scopes
for direct posting functionality.
"""

import json
from pathlib import Path

TOKEN_FILE = Path('credentials/linkedin_token.json')

def main():
    print("LinkedIn Token Upgrade Helper")
    print("=" * 35)
    print()

    if TOKEN_FILE.exists():
        print("[OK] Current token exists:")
        with open(TOKEN_FILE, 'r') as f:
            token_data = json.load(f)
            scope = token_data.get('scope', 'unknown')
            print(f"   Scope: {scope}")

        print()

        if 'r_liteprofile' not in scope:
            print("[ERROR] Issue detected: Token lacks 'r_liteprofile' scope")
            print("   This scope is required for direct posting to work.")
            print()
            print("To fix this, you need to:")
            print("   1. Update your LinkedIn App configuration to include 'r_liteprofile' scope")
            print("   2. Re-authenticate to get a new token with the required scopes")
            print()
            print("   Steps:")
            print("   1. Go to https://www.linkedin.com/developers")
            print("   2. Find your app in the 'My Apps' section")
            print("   3. Go to the 'Products' tab")
            print("   4. Ensure 'Share on LinkedIn' and 'Sign In with LinkedIn' are enabled")
            print("   5. Go to the 'Auth' tab and check the default scopes include 'r_liteprofile'")
            print("   6. Run 'python setup_linkedin_auth.py' again to get a new token")
            print()
            print("Note: The updated setup script now requests:")
            print("   - w_member_social (for posting)")
            print("   - r_liteprofile (for profile info)")
            print("   - r_emailaddress (for email info)")
        else:
            print("[OK] Token has the required 'r_liteprofile' scope for direct posting!")
    else:
        print("[ERROR] No token file found")
        print("   Run 'python setup_linkedin_auth.py' to create a new token")

    print()
    print("Current scopes needed for direct posting:")
    print("   - w_member_social: Required for posting on behalf of user")
    print("   - r_liteprofile: Required for retrieving user ID for URN")
    print("   - r_emailaddress: Recommended for additional profile info")
    print()
    print("Fallback option:")
    print("   If direct posting doesn't work, posts will be queued for")
    print("   processing by the orchestrator (this still works fine)")

if __name__ == '__main__':
    main()