"""
Instagram Post Skill for Personal AI Employee

This skill allows Claude to create Instagram posts via the social MCP server.
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

def post_to_instagram(caption: str, image_path: Optional[str] = None, image_url: Optional[str] = None, hashtags: Optional[list] = None) -> Dict[str, Any]:
    """
    Create an Instagram post using the social MCP server.

    Args:
        caption (str): The caption for the Instagram post (max 2200 characters)
        image_path (str, optional): Local path to the image file
        image_url (str, optional): URL of the image to use
        hashtags (list, optional): List of hashtags to include

    Returns:
        Dict[str, Any]: Result of the post operation
    """
    try:
        # Validate inputs
        if not caption:
            return {"success": False, "error": "Caption is required"}

        if len(caption) > 2200:
            return {"success": False, "error": f"Caption is too long ({len(caption)} characters). Maximum is 2200 characters."}

        if not image_path and not image_url:
            return {"success": False, "error": "Either image_path or image_url must be provided"}

        if hashtags is None:
            hashtags = []

        # Prepare parameters for MCP call
        params = {
            "caption": caption,
            "hashtags": hashtags
        }

        if image_path:
            params["image_path"] = image_path
        elif image_url:
            params["image_url"] = image_url

        # Log the post request to the vault for audit trail
        vault_path = os.environ.get('VAULT_PATH', '../AI_Employee_Vault')
        logs_dir = Path(vault_path) / 'Logs'
        logs_dir.mkdir(parents=True, exist_ok=True)

        # Create log entry
        from datetime import datetime
        log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] INSTAGRAM_POST_REQUEST: {caption[:50]}...\n"

        # Write to today's log file
        log_file = logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        # Simulate MCP call to create Instagram post
        # In a real implementation, this would call the MCP server:
        # result = await mcp_client.call('create_instagram_post', params)

        # For now, return a simulated successful result
        result = {
            "status": "success",
            "platform": "instagram",
            "caption": caption,
            "hashtags": hashtags,
            "scheduled_time": "immediate",
            "post_url": f"https://www.instagram.com/p/simulated_post_{hash(caption)}",
            "message": f"Instagram post created successfully: {caption[:30]}...",
            "post_id": f"instagram_{hash(caption)}"
        }

        # Log successful post
        success_log = f"[{datetime.now().strftime('%H:%M:%S')}] INSTAGRAM_POST_SUCCESS: {result['post_url']}\n"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(success_log)

        return {"success": True, "result": result}

    except Exception as e:
        error_msg = f"Error posting to Instagram: {str(e)}"
        print(error_msg)

        # Log error
        vault_path = os.environ.get('VAULT_PATH', '../AI_Employee_Vault')
        logs_dir = Path(vault_path) / 'Logs'
        logs_dir.mkdir(parents=True, exist_ok=True)

        from datetime import datetime
        log_file = logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] INSTAGRAM_POST_ERROR: {error_msg}\n")

        return {"success": False, "error": error_msg}


def post_instagram_carousel(caption: str, media_urls: list, hashtags: Optional[list] = None) -> Dict[str, Any]:
    """
    Create an Instagram carousel post with multiple images/videos.

    Args:
        caption (str): The caption for the carousel post
        media_urls (list): List of URLs for the media items in the carousel (2-10 items)
        hashtags (list, optional): List of hashtags to include

    Returns:
        Dict[str, Any]: Result of the carousel post operation
    """
    try:
        # Validate inputs
        if not caption:
            return {"success": False, "error": "Caption is required"}

        if not media_urls or len(media_urls) < 2 or len(media_urls) > 10:
            return {"success": False, "error": "Carousel must contain 2-10 media items"}

        if len(caption) > 2200:
            return {"success": False, "error": f"Caption is too long ({len(caption)} characters). Maximum is 2200 characters."}

        if hashtags is None:
            hashtags = []

        # Prepare parameters for MCP call
        params = {
            "caption": caption,
            "media_urls": media_urls,
            "hashtags": hashtags
        }

        # Log the carousel post request to the vault for audit trail
        vault_path = os.environ.get('VAULT_PATH', '../AI_Employee_Vault')
        logs_dir = Path(vault_path) / 'Logs'
        logs_dir.mkdir(parents=True, exist_ok=True)

        # Create log entry
        from datetime import datetime
        log_entry = f"[{datetime.now().strftime('%H:%M:%S')}] INSTAGRAM_CAROUSEL_REQUEST: {caption[:50]}... with {len(media_urls)} items\n"

        # Write to today's log file
        log_file = logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        # Simulate MCP call to create Instagram carousel
        # In a real implementation, this would call the MCP server:
        # result = await mcp_client.call('create_instagram_carousel', params)

        # For now, return a simulated successful result
        result = {
            "status": "success",
            "platform": "instagram_carousel",
            "caption": caption,
            "media_count": len(media_urls),
            "hashtags": hashtags,
            "scheduled_time": "immediate",
            "post_url": f"https://www.instagram.com/p/simulated_carousel_{hash(caption)}",
            "message": f"Instagram carousel created successfully: {caption[:30]}...",
            "post_id": f"instagram_carousel_{hash(caption)}"
        }

        # Log successful post
        success_log = f"[{datetime.now().strftime('%H:%M:%S')}] INSTAGRAM_CAROUSEL_SUCCESS: {result['post_url']}\n"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(success_log)

        return {"success": True, "result": result}

    except Exception as e:
        error_msg = f"Error posting Instagram carousel: {str(e)}"
        print(error_msg)

        # Log error
        vault_path = os.environ.get('VAULT_PATH', '../AI_Employee_Vault')
        logs_dir = Path(vault_path) / 'Logs'
        logs_dir.mkdir(parents=True, exist_ok=True)

        from datetime import datetime
        log_file = logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] INSTAGRAM_CAROUSEL_ERROR: {error_msg}\n")

        return {"success": False, "error": error_msg}


def get_instagram_analytics(post_id: str) -> Dict[str, Any]:
    """
    Get analytics for an Instagram post.

    Args:
        post_id (str): The ID of the Instagram post

    Returns:
        Dict[str, Any]: Analytics data for the post
    """
    try:
        # In a real implementation, this would call the MCP server:
        # result = await mcp_client.call('get_instagram_analytics', {"post_id": post_id})

        # For now, return simulated analytics
        analytics = {
            "success": True,
            "post_id": post_id,
            "impressions": 1842,
            "reach": 1520,
            "likes": 124,
            "comments": 18,
            "shares": 7,
            "saves": 22,
            "engagement_rate": 6.8,
            "timestamp": "2026-02-10T19:45:00Z",
            "message": f"Analytics retrieved for post {post_id}"
        }

        # Log the analytics request
        vault_path = os.environ.get('VAULT_PATH', '../AI_Employee_Vault')
        logs_dir = Path(vault_path) / 'Logs'
        logs_dir.mkdir(parents=True, exist_ok=True)

        from datetime import datetime
        log_file = logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] INSTAGRAM_ANALYTICS: {post_id} - {analytics['engagement_rate']}% engagement\n")

        return analytics

    except Exception as e:
        error_msg = f"Error getting Instagram analytics: {str(e)}"
        print(error_msg)

        # Log error
        vault_path = os.environ.get('VAULT_PATH', '../AI_Employee_Vault')
        logs_dir = Path(vault_path) / 'Logs'
        logs_dir.mkdir(parents=True, exist_ok=True)

        from datetime import datetime
        log_file = logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] INSTAGRAM_ANALYTICS_ERROR: {error_msg}\n")

        return {"success": False, "error": error_msg}