import os
import time
import random
import prawcore
from dotenv import load_dotenv
from search_agent import run_search_agent
from reddit_client import RedditClient
from content_scraper import ContentScraper
from image_processor import ImageProcessor
from comment_generator import CommentGenerator
from post_manager import PostManager

NEON_GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET_COLOR = '\033[0m'

def main():
    reddit_client = RedditClient()
    content_scraper = ContentScraper()
    image_processor = ImageProcessor()
    comment_generator = CommentGenerator()
    post_manager = PostManager()

    last_comment_time = 0
    replied_posts = post_manager.load_replied_posts()

    while True:
        for subreddit_name in reddit_client.subreddits:
            print(f"Searching in subreddit: {subreddit_name}")
            subreddit = reddit_client.get_subreddit(subreddit_name)
            try:
                for post in subreddit.new(limit=50):
                    if post.id in replied_posts:
                        continue
                    post_title = post.title.lower()

                    for keyword in reddit_client.keywords:
                        if keyword.lower() in post_title:
                            current_time = time.time()
                            elapsed_time = current_time - last_comment_time
                            if elapsed_time >= random.randint(1800, 3600):
                                post_content = post.selftext.lower()
                                url_content = content_scraper.scrape_url_content(post.url)
                                image_description = image_processor.process_post_image(post)

                                comment_text = comment_generator.generate_comment(post.title, post_content, url_content, image_description)
                                post.reply(comment_text)
                                print(f"Commented on post: {post.title}")
                                print(NEON_GREEN + comment_text + RESET_COLOR)
                                print("---")
                                last_comment_time = current_time
                                replied_posts.add(post.id)
                                post_manager.save_replied_posts(replied_posts)
                            else:
                                remaining_time = random.randint(1800, 3600) - elapsed_time
                                print(f"Waiting for {remaining_time // 60} minutes before commenting again")
                            break
            except prawcore.exceptions.BadRequest as e:
                print(f"Error: {str(e)}")
                continue
        time.sleep(300)

if __name__ == "__main__":
    main()