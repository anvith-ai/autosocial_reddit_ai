import praw
import os
from dotenv import load_dotenv

class RedditClient:
    def __init__(self):
        load_dotenv(override=True)
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.user_agent = os.getenv("REDDIT_USER_AGENT")
        self.reddit_username = os.getenv("REDDIT_USERNAME")
        self.reddit_password = os.getenv("REDDIT_PASSWORD")
        self.subreddits = ["openai", "programming", "LocalLLaMA", "learnprogramming"]
        self.keywords = ["o1", "o1 model", "o1 mini", "o1 preview"]
        self.reddit = self.create_reddit_client()

    def create_reddit_client(self):
        return praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
            username=self.reddit_username,
            password=self.reddit_password
        )

    def get_subreddit(self, name):
        return self.reddit.subreddit(name)