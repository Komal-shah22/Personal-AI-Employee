"""
Instagram Post and Check Status Script for Personal AI Employee

This script allows direct posting to Instagram and checking of post status
using the Social MCP server.
"""
import asyncio
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

# Add the MCP server path to Python path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".claude", "mcp-servers", "social-mcp"))

from server import SocialMCPServer


class InstagramPostChecker:
    """Class to handle Instagram posting and status checking"""

    def __init__(self):
        self.server = SocialMCPServer()

    async def post_to_instagram(self, caption: str, image_url: str = None) -> Dict[str, Any]:
        """
        Post content to Instagram

        Args:
            caption: The caption for the Instagram post
            image_url: Optional URL of the image to post

        Returns:
            Dictionary with response from the MCP server
        """
        # Prepare the request to the MCP server
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "create_instagram_post",
            "params": {
                "caption": caption,
                "image_path": "",  # Using image_url instead
                "image_url": image_url
            }
        }

        print(f"Attempting to post to Instagram: {caption[:50]}...")

        # Send request to MCP server
        response = await self.server.handle_request(request)

        # Check for success
        if "result" in response and response["result"]["status"] == "success":
            print("✅ Instagram post created successfully!")
            print(f"   Post URL: {response['result']['post_url']}")
            print(f"   Post ID: {response['result']['post_id']}")
            return response["result"]
        else:
            print("❌ Failed to post to Instagram")
            print(f"   Error: {response.get('error', {}).get('message', 'Unknown error')}")
            return None

    async def check_post_status(self, post_id: str) -> Dict[str, Any]:
        """
        Check the status analytics of an Instagram post

        Args:
            post_id: The ID of the Instagram post to check

        Returns:
            Dictionary with post analytics from the MCP server
        """
        # Prepare the request to get analytics
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "get_instagram_analytics",
            "params": {
                "post_id": post_id
            }
        }

        print(f"Checking Instagram post analytics for ID: {post_id}")

        # Send request to MCP server
        response = await self.server.handle_request(request)

        if "result" in response:
            return response["result"]
        else:
            print("❌ Failed to get post analytics")
            print(f"   Error: {response.get('error', {}).get('message', 'Unknown error')}")
            return None


async def main():
    """Main function to run the Instagram post and check functionality"""
    print(": Instagram Post and Check Status Tool for Personal AI Employee")
    print("=" * 60)

    if not os.getenv("INSTAGRAM_ACCESS_TOKEN"):
        print("⚠️  Warning: INSTAGRAM_ACCESS_TOKEN not set in environment")
        print("   You need to set this environment variable to post to Instagram")
        print("   Example: export INSTAGRAM_ACCESS_TOKEN=your_token_here")

    if not os.getenv("INSTAGRAM_ACCOUNT_ID"):
        print("⚠️  Warning: INSTAGRAM_ACCOUNT_ID not set in environment")
        print("   You need to set this environment variable to post to Instagram")
        print("   Example: export INSTAGRAM_ACCOUNT_ID=your_account_id_here")

    checker = InstagramPostChecker()

    # Ask user for action
    print("\nWhat would you like to do?")
    print("1. Post to Instagram")
    print("2. Check Instagram post status")
    print("3. Both (Post then check)")

    choice = input("\nEnter your choice (1-3): ").strip()

    if choice == "1":
        caption = input("\nEnter your Instagram caption: ").strip()
        image_url = input("Enter image URL (optional, press Enter to skip): ").strip()

        if not image_url:
            image_url = None

        result = await checker.post_to_instagram(caption, image_url)

        if result:
            print("\n✅ Post completed successfully!")
            print(f"Post ID: {result.get('post_id', 'N/A')}")
            print(f"URL: {result.get('post_url', 'N/A')}")
        else:
            print("\n❌ Failed to post to Instagram")

    elif choice == "2":
        post_id = input("\nEnter the Instagram post ID to check: ").strip()

        result = await checker.check_post_status(post_id)

        if result and result.get("success"):
            print("\n📊 Instagram Post Analytics:")
            print(f"Post ID: {result.get('post_id', 'N/A')}")
            print(f"Impressions: {result.get('impressions', 'N/A')}")
            print(f"Reach: {result.get('reach', 'N/A')}")
            print(f"Likes: {result.get('likes', 'N/A')}")
            print(f"Comments: {result.get('comments', 'N/A')}")
            print(f"Shares: {result.get('shares', 'N/A')}")
            print(f"Saves: {result.get('saves', 'N/A')}")
            print(f"Engagement Rate: {result.get('engagement_rate', 'N/A')}%")
        else:
            print("\n❌ Failed to retrieve post analytics")

    elif choice == "3":
        caption = input("\nEnter your Instagram caption: ").strip()
        image_url = input("Enter image URL (optional, press Enter to skip): ").strip()

        if not image_url:
            image_url = None

        # First post
        result = await checker.post_to_instagram(caption, image_url)

        if result:
            post_id = result.get("post_id", "")
            print(f"\n✅ Post completed successfully!")
            print(f"Post ID: {post_id}")
            print(f"URL: {result.get('post_url', 'N/A')}")

            # Then check status
            print("\n" + "="*50)
            print("Checking status of the post we just created...")

            status_result = await checker.check_post_status(post_id)

            if status_result and status_result.get("success"):
                print("\n📊 Instagram Post Analytics:")
                print(f"Post ID: {status_result.get('post_id', 'N/A')}")
                print(f"Impressions: {status_result.get('impressions', 'N/A')}")
                print(f"Reach: {status_result.get('reach', 'N/A')}")
                print(f"Likes: {status_result.get('likes', 'N/A')}")
                print(f"Comments: {status_result.get('comments', 'N/A')}")
                print(f"Shares: {status_result.get('shares', 'N/A')}")
                print(f"Saves: {status_result.get('saves', 'N/A')}")
                print(f"Engagement Rate: {status_result.get('engagement_rate', 'N/A')}%")
            else:
                print("\n❌ Failed to retrieve post analytics")
        else:
            print("\n❌ Failed to post to Instagram")

    else:
        print("Invalid choice. Please run the script again and select 1, 2, or 3.")


if __name__ == "__main__":
    asyncio.run(main())