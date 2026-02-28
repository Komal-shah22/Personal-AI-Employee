# Instagram Post Skill

This skill enables the Personal AI Employee to create and manage Instagram posts as part of the Gold Tier social media integration.

## Functions

### `post_to_instagram(caption, image_path=None, image_url=None, hashtags=None)`
Create a single image/video Instagram post.

**Parameters:**
- `caption` (str): The caption for the Instagram post (max 2200 characters)
- `image_path` (str, optional): Local path to the image file
- `image_url` (str, optional): URL of the image to use
- `hashtags` (list, optional): List of hashtags to include

**Returns:** Dict with success status and post details

### `post_instagram_carousel(caption, media_urls, hashtags=None)`
Create an Instagram carousel post with multiple images/videos.

**Parameters:**
- `caption` (str): The caption for the carousel post
- `media_urls` (list): List of URLs for the media items in the carousel (2-10 items)
- `hashtags` (list, optional): List of hashtags to include

**Returns:** Dict with success status and carousel post details

### `get_instagram_analytics(post_id)`
Get analytics for an Instagram post.

**Parameters:**
- `post_id` (str): The ID of the Instagram post

**Returns:** Dict with analytics data for the post

## Usage Examples

1. Create a simple Instagram post:
   ```python
   result = post_to_instagram(
       caption="Check out our new product launch! #newproduct #innovation",
       image_url="https://example.com/product.jpg",
       hashtags=["#newproduct", "#innovation", "#launch"]
   )
   ```

2. Create an Instagram carousel:
   ```python
   result = post_instagram_carousel(
       caption="Behind the scenes of our product development process",
       media_urls=[
           "https://example.com/image1.jpg",
           "https://example.com/image2.jpg",
           "https://example.com/image3.jpg"
       ],
       hashtags=["#behindthescenes", "#process", "#development"]
   )
   ```

3. Get analytics for a post:
   ```python
   analytics = get_instagram_analytics("instagram_123456789")
   ```

## Notes
- Captions are limited to 2200 characters
- Carousel posts must contain 2-10 media items
- At least one of image_path or image_url is required for single posts
- The skill logs all activities to the vault for audit trail
- Actual posting is handled by the social MCP server