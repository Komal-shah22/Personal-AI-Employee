"""
Instagram Queue Processing Script

This script processes Instagram posts from a queue and tracks their status.
"""
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Add the MCP server path to Python path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".claude", "mcp-servers", "social-mcp"))

from server import SocialMCPServer


class InstagramQueueProcessor:
    """Process Instagram posts from a queue and track their status"""

    def __init__(self):
        self.server = SocialMCPServer()
        self.vault_path = Path("../AI_Employee_Vault")
        self.queue_file = self.vault_path / "instagram_queue.json"
        self.completed_posts_file = self.vault_path / "completed_instagram_posts.json"

    def load_queue(self) -> List[Dict[str, Any]]:
        """Load the Instagram post queue from file"""
        if self.queue_file.exists():
            with open(self.queue_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_queue(self, queue: List[Dict[str, Any]]):
        """Save the Instagram post queue to file"""
        self.vault_path.mkdir(parents=True, exist_ok=True)
        with open(self.queue_file, 'w', encoding='utf-8') as f:
            json.dump(queue, f, indent=2, ensure_ascii=False)

    def load_completed_posts(self) -> List[Dict[str, Any]]:
        """Load completed Instagram posts from file"""
        if self.completed_posts_file.exists():
            with open(self.completed_posts_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_completed_posts(self, posts: List[Dict[str, Any]]):
        """Save completed Instagram posts to file"""
        self.vault_path.mkdir(parents=True, exist_ok=True)
        with open(self.completed_posts_file, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)

    async def process_queue(self):
        """Process all pending Instagram posts in the queue"""
        queue = self.load_queue()

        if not queue:
            print("📭 No pending Instagram posts in the queue")
            return

        print(f"📦 Processing {len(queue)} Instagram posts from queue...")
        completed_posts = self.load_completed_posts()

        for i, post in enumerate(queue):
            print(f"\n📝 Processing post {i+1}/{len(queue)}: {post['caption'][:50]}...")

            # Post to Instagram
            result = await self.post_to_instagram(post)

            if result:
                print(f"✅ Post {i+1} completed successfully!")
                print(f"   Post ID: {result['post_id']}")
                print(f"   URL: {result['post_url']}")

                # Add to completed posts
                completed_posts.append({
                    **post,
                    "post_id": result['post_id'],
                    "post_url": result['post_url'],
                    "timestamp": datetime.now().isoformat(),
                    "status": "completed"
                })

                # Remove from queue
                queue = [p for p in queue if p != post]
            else:
                print(f"❌ Failed to post {i+1}")
                # Mark as failed but don't remove from queue
                post['status'] = 'failed'
                post['error_timestamp'] = datetime.now().isoformat()

        # Save updated queue and completed posts
        self.save_queue(queue)
        self.save_completed_posts(completed_posts)

        print(f"\n📈 Processed {len([p for p in completed_posts if p.get('status') == 'completed'])} posts successfully")
        print(f"📋 {len(queue)} posts remain in queue")

    async def post_to_instagram(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post content to Instagram

        Args:
            post_data: Dictionary containing 'caption' and optional 'image_url'

        Returns:
            Dictionary with response from the MCP server
        """
        # Prepare the request to the MCP server
        request = {
            "jsonrpc": "2.0",
            "id": hash(post_data['caption']) % 10000,  # Simple ID generation
            "method": "create_instagram_post",
            "params": {
                "caption": post_data['caption'],
                "image_path": "",  # Using image_url instead
                "image_url": post_data.get('image_url', '')
            }
        }

        # Send request to MCP server
        response = await self.server.handle_request(request)

        # Check for success
        if "result" in response and response["result"]["status"] == "success":
            return response["result"]
        else:
            print(f"   Error: {response.get('error', {}).get('message', 'Unknown error')}")
            return None

    def add_to_queue(self, caption: str, image_url: str = None):
        """Add a post to the Instagram queue"""
        queue = self.load_queue()

        post = {
            "caption": caption,
            "image_url": image_url,
            "timestamp": datetime.now().isoformat(),
            "status": "pending"
        }

        queue.append(post)
        self.save_queue(queue)

        print(f"✅ Added post to queue:")
        print(f"   Caption: {caption[:50]}...")
        if image_url:
            print(f"   Image: {image_url}")

    def check_post_status(self, post_id: str):
        """Check the status of a specific post"""
        completed_posts = self.load_completed_posts()

        for post in completed_posts:
            if post.get('post_id') == post_id:
                print(f"\n📊 Status for post ID: {post_id}")
                print(f"Caption: {post['caption'][:100]}...")
                print(f"Status: {post.get('status', 'unknown')}")
                print(f"Posted at: {post.get('timestamp', 'unknown')}")
                print(f"URL: {post.get('post_url', 'N/A')}")
                return

        print(f"❌ Post with ID {post_id} not found in completed posts")

    def show_queue_status(self):
        """Show current queue status"""
        queue = self.load_queue()
        completed = self.load_completed_posts()

        print(f"\n📋 Instagram Queue Status:")
        print(f"   Pending posts: {len(queue)}")
        print(f"   Completed posts: {len(completed)}")

        if queue:
            print(f"\n   Pending posts:")
            for i, post in enumerate(queue):
                print(f"     {i+1}. {post['caption'][:50]}... (added: {post['timestamp']})")


async def main():
    """Main function to run the Instagram Queue Processor"""
    print("📸 Instagram Queue Processing Tool for Personal AI Employee")
    print("=" * 60)

    processor = InstagramQueueProcessor()

    print("\nWhat would you like to do?")
    print("1. Process pending Instagram posts in queue")
    print("2. Add a new post to queue")
    print("3. Check queue status")
    print("4. Check specific post status")
    print("5. Show completed posts")

    choice = input("\nEnter your choice (1-5): ").strip()

    if choice == "1":
        await processor.process_queue()

    elif choice == "2":
        caption = input("\nEnter your Instagram caption: ").strip()
        image_url = input("Enter image URL (optional, press Enter to skip): ").strip()

        if not image_url:
            image_url = None

        processor.add_to_queue(caption, image_url)

    elif choice == "3":
        processor.show_queue_status()

    elif choice == "4":
        post_id = input("\nEnter the Instagram post ID to check: ").strip()
        processor.check_post_status(post_id)

    elif choice == "5":
        completed_posts = processor.load_completed_posts()
        print(f"\n✅ Completed Instagram Posts ({len(completed_posts)}):")

        for i, post in enumerate(completed_posts[-10:], 1):  # Show last 10
            print(f"\n{i}. {post['caption'][:50]}...")
            print(f"   ID: {post.get('post_id', 'N/A')}")
            print(f"   URL: {post.get('post_url', 'N/A')}")
            print(f"   Posted: {post.get('timestamp', 'N/A')}")

        if len(completed_posts) > 10:
            print(f"\n... and {len(completed_posts) - 10} more posts")

    else:
        print("Invalid choice. Please run the script again and select 1-5.")


if __name__ == "__main__":
    asyncio.run(main())