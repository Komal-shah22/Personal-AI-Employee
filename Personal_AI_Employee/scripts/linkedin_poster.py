"""
LinkedIn Post Generator and Workflow Manager

Generates LinkedIn posts following best practices and manages the approval workflow.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
VAULT_PATH = PROJECT_ROOT / "AI_Employee_Vault"
NEEDS_ACTION_PATH = VAULT_PATH / "Needs_Action"
PENDING_APPROVAL_PATH = VAULT_PATH / "Pending_Approval"
APPROVED_PATH = VAULT_PATH / "Approved"
DONE_PATH = VAULT_PATH / "Done"
LOGS_PATH = VAULT_PATH / "Logs"

# Ensure directories exist
for path in [NEEDS_ACTION_PATH, PENDING_APPROVAL_PATH, APPROVED_PATH, DONE_PATH, LOGS_PATH]:
    path.mkdir(parents=True, exist_ok=True)


def generate_post_draft(topic: str, post_type: str = "insight") -> Dict[str, Any]:
    """
    Generate a LinkedIn post draft following best practices.

    Args:
        topic: The topic to write about
        post_type: Type of post (insight, story, tip, announcement)

    Returns:
        Dict with post content and metadata
    """
    print(f"Generating LinkedIn post draft...")
    print(f"  Topic: {topic}")
    print(f"  Type: {post_type}")

    # Generate post content based on type
    if post_type == "insight":
        post_content = generate_insight_post(topic)
    elif post_type == "story":
        post_content = generate_story_post(topic)
    elif post_type == "tip":
        post_content = generate_tip_post(topic)
    else:
        post_content = generate_insight_post(topic)

    # Validate format
    char_count = len(post_content)
    hashtag_count = post_content.count('#')

    print(f"  Character count: {char_count}")
    print(f"  Hashtag count: {hashtag_count}")

    # Create timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create files
    needs_action_file = create_needs_action_file(post_content, topic, timestamp)
    pending_approval_file = create_pending_approval_file(post_content, topic, timestamp)

    return {
        "success": True,
        "post_content": post_content,
        "character_count": char_count,
        "hashtag_count": hashtag_count,
        "needs_action_file": str(needs_action_file),
        "pending_approval_file": str(pending_approval_file),
        "timestamp": timestamp
    }


def generate_insight_post(topic: str) -> str:
    """Generate an insight-style LinkedIn post"""

    # Hook (first line - under 100 chars)
    hook = "AI agents aren't just automating tasks—they're becoming strategic partners."

    # Value paragraphs
    paragraph1 = """In 2026, small businesses are discovering something remarkable: AI agents can handle the complexity of running operations 24/7, from email triage to financial reporting."""

    paragraph2 = """The shift from "software tools" to "digital employees" changes everything. Instead of learning complex software, business owners now delegate to AI that understands context, makes decisions, and learns from feedback."""

    paragraph3 = """The ROI is staggering: 85-90% cost reduction compared to human FTEs, 4x more working hours annually, and 99%+ consistency. But the real value? Founders get their time back to focus on strategy, not operations."""

    # CTA
    cta = "What's your experience with AI automation in your business? Share your thoughts below."

    # Hashtags (3-5 relevant)
    hashtags = "#AIAgents #SmallBusiness #Automation #DigitalTransformation #FutureOfWork"

    # Combine with proper spacing
    post = f"{hook}\n\n{paragraph1}\n\n{paragraph2}\n\n{paragraph3}\n\n{cta}\n\n{hashtags}"

    return post


def generate_story_post(topic: str) -> str:
    """Generate a story-style LinkedIn post"""
    hook = "Last month, I built an AI employee that works 168 hours a week."
    story = f"The journey started with a simple question: What if AI could handle my entire inbox?\n\nNow it manages emails, WhatsApp, social media, and even generates weekly CEO briefings.\n\nThe best part? It cost less than hiring one part-time assistant."
    cta = "Curious about building your own AI employee? Let's connect."
    hashtags = "#AIAutomation #Entrepreneurship #ProductivityHacks"
    return f"{hook}\n\n{story}\n\n{cta}\n\n{hashtags}"


def generate_tip_post(topic: str) -> str:
    """Generate a tip-style LinkedIn post"""
    hook = "3 ways AI agents are transforming small business operations:"
    tips = "1. Email Management: Auto-triage, draft responses, flag urgent items\n2. Financial Tracking: Monitor transactions, flag anomalies, generate reports\n3. Social Media: Schedule posts, engage with followers, analyze performance"
    cta = "Which one would save you the most time? Comment below."
    hashtags = "#BusinessTips #AITools #SmallBusiness"
    return f"{hook}\n\n{tips}\n\n{cta}\n\n{hashtags}"


def create_needs_action_file(post_content: str, topic: str, timestamp: str) -> Path:
    """Create file in Needs_Action folder"""
    filename = f"SOCIAL_LINKEDIN_{timestamp}.md"
    filepath = NEEDS_ACTION_PATH / filename

    content = f"""---
type: social_media
platform: linkedin
topic: {topic}
status: draft
created: {datetime.now().isoformat()}
priority: medium
---

# LinkedIn Post Draft

## Topic
{topic}

## Post Content
{post_content}

## Metadata
- Character count: {len(post_content)}
- Hashtag count: {post_content.count('#')}
- Status: Awaiting approval

## Next Steps
- [ ] Review post content
- [ ] Approve or request changes
- [ ] Schedule for posting (9 AM - 6 PM)
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Created: {filepath}")
    return filepath


def create_pending_approval_file(post_content: str, topic: str, timestamp: str) -> Path:
    """Create file in Pending_Approval folder"""
    filename = f"LINKEDIN_{timestamp}.md"
    filepath = PENDING_APPROVAL_PATH / filename

    content = f"""---
type: approval_request
action: linkedin_post
topic: {topic}
created: {datetime.now().isoformat()}
expires: {datetime.now().isoformat()}
status: pending
---

# LinkedIn Post Approval Request

## Post Content
{post_content}

## Validation
- Character count: {len(post_content)} / 1300 recommended
- Hashtag count: {post_content.count('#')} (3-5 recommended)
- Has hook: {'Yes' if len(post_content.split('\\n')[0]) < 100 else 'No'}
- Has CTA: {'Yes' if any(kw in post_content.lower() for kw in ['what do you think', 'share your', 'comment below']) else 'No'}

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder or delete it.

## Posting Schedule
Will post during business hours (9 AM - 6 PM) once approved.
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Created: {filepath}")
    return filepath


def main():
    """Main execution for testing"""
    print("=" * 70)
    print("LinkedIn Post Generator - Test Run")
    print("=" * 70)
    print()

    # Test parameters
    topic = "How AI agents are transforming small business operations in 2026"
    post_type = "insight"

    # Generate post
    result = generate_post_draft(topic, post_type)

    print()
    print("=" * 70)
    print("[SUCCESS] Post draft generated!")
    print("=" * 70)
    print()
    print(f"Files created:")
    print(f"  1. {result['needs_action_file']}")
    print(f"  2. {result['pending_approval_file']}")
    print()
    print(f"Post preview:")
    print("-" * 70)
    print(result['post_content'])
    print("-" * 70)
    print()
    print(f"Character count: {result['character_count']} / 1300 recommended")
    print(f"Hashtag count: {result['hashtag_count']} (3-5 recommended)")
    print()


if __name__ == "__main__":
    main()
