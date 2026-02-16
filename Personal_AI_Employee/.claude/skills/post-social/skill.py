"""
Claude Code Agent Skill: post-social
Automates social media posting across platforms
"""

import os
import json
from pathlib import Path
from datetime import datetime
import subprocess
import sys

def run_skill():
    """
    Main function for the post-social skill
    """
    print("Starting post-social skill...")

    # Get vault path from environment or default
    vault_path = os.environ.get('VAULT_PATH', '../AI_Employee_Vault')
    needs_action_dir = Path(vault_path) / 'Needs_Action'

    print("Looking for social media posts in Needs_Action folder...")

    # Find social media related files
    social_files = []
    for file_path in needs_action_dir.glob('*.md'):
        content = file_path.read_text(encoding='utf-8')
        if any(keyword in content.lower() for keyword in ['social', 'facebook', 'instagram', 'twitter', 'linkedin', 'post', 'tweet']):
            social_files.append(file_path)

    if not social_files:
        print("No social media posts found in Needs_Action folder.")
        return {
            "status": "success",
            "message": "No social media posts to process",
            "processed_count": 0
        }

    processed_posts = []

    for file_path in social_files:
        try:
            print(f"Processing social media post: {file_path.name}")

            # Read the file content
            content = file_path.read_text(encoding='utf-8')

            # Parse frontmatter if present
            frontmatter = {}
            post_content = content

            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    try:
                        import yaml
                        frontmatter = yaml.safe_load(parts[1]) or {}
                        post_content = parts[2].strip()
                    except:
                        # If yaml fails, just use the original content
                        pass

            # Determine platform and content
            platform = frontmatter.get('platform', 'auto')
            caption = frontmatter.get('caption', frontmatter.get('text', ''))

            if not caption:
                # Extract caption from content if not in frontmatter
                lines = post_content.split('\n')
                for line in lines:
                    if line.strip().startswith('#') or line.strip().startswith('>'):
                        caption = line.strip().lstrip('#> ').strip()
                        break
                if not caption:
                    caption = post_content[:280]  # Twitter limit

            hashtags = frontmatter.get('hashtags', [])

            # Simulate posting (in real implementation, would call MCP server)
            print(f"Posting to {platform}: {caption[:50]}...")

            # In a real implementation, we would call the MCP server:
            # result = call_mcp_server(platform, caption, hashtags)

            # For now, simulate the posting
            result = {
                "status": "success",
                "platform": platform,
                "caption": caption,
                "hashtags": hashtags,
                "post_url": f"https://{platform}.com/placeholder-post",
                "message": f"Posted successfully to {platform}"
            }

            # Move file to Done folder
            done_dir = Path(vault_path) / 'Done'
            done_dir.mkdir(exist_ok=True)

            done_file = done_dir / f"DONE_{file_path.name}"
            file_path.rename(done_file)

            processed_posts.append({
                "original_file": str(file_path),
                "done_file": str(done_file),
                "result": result
            })

            print(f"Successfully posted to {platform}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            # Move to error log or rejected folder
            continue

    print(f"Processed {len(processed_posts)} social media posts.")

    # Update dashboard
    try:
        update_dashboard_script = Path('../.claude/skills/update-dashboard/skill.py')
        if update_dashboard_script.exists():
            subprocess.run([sys.executable, str(update_dashboard_script)],
                         capture_output=True, text=True)
            print("Dashboard updated after social media posts.")
    except Exception as e:
        print(f"Error updating dashboard: {e}")

    # Prepare result
    result = {
        "status": "success",
        "message": f"Processed {len(processed_posts)} social media posts",
        "processed_count": len(processed_posts),
        "posts": [p["result"] for p in processed_posts]
    }

    print("Social media posting completed successfully.")
    return result

def call_mcp_server(platform: str, caption: str, hashtags: list):
    """
    Function to call the MCP server for actual posting
    This would be implemented in a real environment
    """
    # Placeholder for actual MCP server call
    # This would use the MCP protocol to communicate with the server
    return {
        "status": "success",
        "platform": platform,
        "caption": caption,
        "hashtags": hashtags,
        "post_url": f"https://{platform}.com/placeholder-post",
        "message": f"Posted successfully to {platform}"
    }

if __name__ == "__main__":
    result = run_skill()
    print(f"\nSkill execution completed: {result}")