"""
Instagram Validation and Status Check Tool

This script validates Instagram posts before posting and checks their status.
"""
import asyncio
import os
import sys
from pathlib import Path

# Add the MCP server path to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".claude", "mcp-servers", "social-mcp"))

from instagram_integration import InstagramIntegration


async def validate_instagram_post(caption: str):
    """Validate an Instagram post before posting"""
    print("🔍 Validating Instagram post...")

    # Create Instagram integration instance
    instagram = InstagramIntegration()

    # Validate the post
    validation_result = instagram.validate_post_format(caption)

    print("\n📋 Validation Results:")
    print(f"Character count: {validation_result['character_count']}")
    print(f"Hashtag count: {validation_result['hashtag_count']}")
    print(f"Mention count: {validation_result['mention_count']}")
    print(f"Emoji count: {validation_result['emoji_count']}")
    print(f"Has question: {validation_result['includes_question']}")

    if validation_result['issues']:
        print(f"\n⚠️ Issues found ({len(validation_result['issues'])}):")
        for issue in validation_result['issues']:
            print(f"   - {issue}")

    if validation_result['suggestions']:
        print(f"\n💡 Suggestions ({len(validation_result['suggestions'])}):")
        for suggestion in validation_result['suggestions']:
            print(f"   - {suggestion}")

    print(f"\n✅ Post is {'valid' if validation_result['valid'] else 'not valid'}")

    return validation_result


def create_instagram_post_with_validation():
    """Main function to validate and check Instagram posts"""
    print("📸 Instagram Validation and Status Check Tool")
    print("=" * 50)

    print("\nThis tool will:")
    print("1. Validate your Instagram caption")
    print("2. Show you suggestions for improvement")

    caption = input("\nEnter your Instagram caption to validate: ")

    # Run async validation
    validation_result = asyncio.run(validate_instagram_post(caption))

    if validation_result['valid']:
        print("\n✅ Your post is ready to go! It follows Instagram best practices.")
    else:
        print("\n⚠️ Consider these improvements before posting:")
        if validation_result['suggestions']:
            for suggestion in validation_result['suggestions']:
                print(f"   - {suggestion}")

        fix_choice = input("\nWould you like to fix and validate again? (y/n): ")

        if fix_choice.lower() == 'y':
            new_caption = input("\nEnter your improved caption: ")
            print()
            asyncio.run(validate_instagram_post(new_caption))


if __name__ == "__main__":
    create_instagram_post_with_validation()