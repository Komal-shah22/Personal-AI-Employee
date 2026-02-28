"""
Instagram Post and Status Checker for Personal AI Employee

This script combines posting and checking functionality for Instagram.
"""
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Add the MCP server path to Python path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".claude", "mcp-servers", "social-mcp"))

from server import SocialMCPServer


class InstagramManager:
    """Manage Instagram posting and status checking"""

    def __init__(self):
        self.server = SocialMCPServer()
        self.vault_path = Path("../AI_Employee_Vault/Instagram")
        self.vault_path.mkdir(parents=True, exist_ok=True)
        self.log_file = self.vault_path / "instagram_log.json"

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

            # Log the post
            self.log_post(response['result'])
            return response["result"]
        else:
            print("❌ Failed to post to Instagram")
            print(f"   Error: {response.get('error', {}).get('message', 'Unknown error')}")
            return None

    def log_post(self, post_result: Dict[str, Any]):
        """Log the post to the vault"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "instagram_post",
            "post_id": post_result.get('post_id'),
            "url": post_result.get('post_url'),
            "validation": post_result.get('validation'),
            "message": post_result.get('message')
        }

        # Load existing log
        log_data = []
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)

        # Add new entry
        log_data.append(log_entry)

        # Save log
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)

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
            print(f"\n📊 Analytics for post {post_id}:")
            print(f"   Impressions: {response['result'].get('impressions', 'N/A')}")
            print(f"   Reach: {response['result'].get('reach', 'N/A')}")
            print(f"   Likes: {response['result'].get('likes', 'N/A')}")
            print(f"   Comments: {response['result'].get('comments', 'N/A')}")
            print(f"   Shares: {response['result'].get('shares', 'N/A')}")
            print(f"   Saves: {response['result'].get('saves', 'N/A')}")
            print(f"   Engagement Rate: {response['result'].get('engagement_rate', 'N/A')}%")

            return response["result"]
        else:
            print("❌ Failed to get post analytics")
            print(f"   Error: {response.get('error', {}).get('message', 'Unknown error')}")
            return None

    def show_recent_posts(self):
        """Show recent Instagram posts from the log"""
        if not self.log_file.exists():
            print("📭 No Instagram posts logged yet")
            return

        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_data = json.load(f)

        if not log_data:
            print("📭 No Instagram posts logged yet")
            return

        print(f"\n📝 Recent Instagram Posts ({len(log_data)}):")
        for i, entry in enumerate(log_data[-5:], 1):  # Show last 5
            print(f"\n{i}. {entry['timestamp']}")
            print(f"   ID: {entry['post_id']}")
            print(f"   URL: {entry['url']}")
            print(f"   Message: {entry['message']}")

    async def post_and_check(self, caption: str, image_url: str = None):
        """Post to Instagram and then check the status"""
        # First, post
        result = await self.post_to_instagram(caption, image_url)

        if result:
            post_id = result.get('post_id', '')
            print(f"\n✅ Post completed successfully!")
            print(f"Post ID: {post_id}")
            print(f"URL: {result.get('post_url', 'N/A')}")

            # Check if user wants to check status immediately
            check_now = input("\nWould you like to check the post status now? (y/n): ").strip().lower()

            if check_now == 'y':
                await self.check_post_status(post_id)
        else:
            print("\n❌ Failed to post to Instagram")


async def main():
    """Main function to run the Instagram Manager"""
    print("📸 Instagram Post & Status Checker for Personal AI Employee")
    print("=" * 60)

    # Check for required environment variables
    if not os.getenv("INSTAGRAM_ACCESS_TOKEN"):
        print("⚠️  Warning: INSTAGRAM_ACCESS_TOKEN not set in environment")
        print("   You need to set this environment variable to post to Instagram")

    if not os.getenv("INSTAGRAM_ACCOUNT_ID"):
        print("⚠️  Warning: INSTAGRAM_ACCOUNT_ID not set in environment")
        print("   You need to set this environment variable to post to Instagram")

    manager = InstagramManager()

    print("\nWhat would you like to do?")
    print("1. Post to Instagram and check status")
    print("2. Post to Instagram only")
    print("3. Check status of existing post")
    print("4. View recent posts")

    choice = input("\nEnter your choice (1-4): ").strip()

    if choice == "1":
        caption = input("\nEnter your Instagram caption: ").strip()
        image_url = input("Enter image URL (optional, press Enter to skip): ").strip()

        if not image_url:
            image_url = None

        await manager.post_and_check(caption, image_url)

    elif choice == "2":
        caption = input("\nEnter your Instagram caption: ").strip()
        image_url = input("Enter image URL (optional, press Enter to skip): ").strip()

        if not image_url:
            image_url = None

        result = await manager.post_to_instagram(caption, image_url)

        if result:
            print(f"\n✅ Post completed successfully!")
            print(f"Post ID: {result.get('post_id', 'N/A')}")
            print(f"URL: {result.get('post_url', 'N/A')}")
        else:
            print("\n❌ Failed to post to Instagram")

    elif choice == "3":
        post_id = input("\nEnter the Instagram post ID to check: ").strip()

        await manager.check_post_status(post_id)

    elif choice == "4":
        manager.show_recent_posts()

    else:
        print("Invalid choice. Please run the script again and select 1-4.")


if __name__ == "__main__":
    asyncio.run(main())