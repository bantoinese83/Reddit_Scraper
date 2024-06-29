import re
import string
from datetime import datetime

import pandas as pd
import praw
from halo import Halo
from loguru import logger

from app.config import Config

# Reddit API credentials
CLIENT_ID = Config.CLIENT_ID
CLIENT_SECRET = Config.CLIENT_SECRET
USER_AGENT = Config.USER_AGENT

# File paths
RAW_CSV_PATH = Config.RAW_CSV_PATH
CLEANED_CSV_PATH = Config.CLEANED_CSV_PATH
SHUFFLED_CSV_PATH = Config.SHUFFLED_CSV_PATH
LOG_FILE_PATH = Config.LOG_FILE_PATH

# Reddit API parameters
SEARCH_QUERY = Config.SEARCH_QUERY
SUBREDDIT_LIMIT = Config.SUBREDDIT_LIMIT
POST_LIMIT = Config.POST_LIMIT
POSTS_SORT = Config.POSTS_SORT
POSTS_FIELDS = Config.POSTS_FIELDS


class RedditScraper:
    def __init__(self, client_id, client_secret, user_agent):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.reddit = None
        self.spinner = Halo(text='Processing', spinner='dots')
        self.setup_logging()

    @staticmethod
    def setup_logging():
        logger.add(LOG_FILE_PATH, rotation='10 MB', level='INFO', backtrace=True, diagnose=True)

    def initialize_reddit(self):
        """Initialize and return a Reddit instance."""
        try:
            self.reddit = praw.Reddit(client_id=self.client_id,
                                      client_secret=self.client_secret,
                                      user_agent=self.user_agent)
            logger.info("Reddit instance initialized successfully.")
        except Exception as init_error:
            logger.error(f"Failed to initialize Reddit instance: {init_error}")
            raise

    def fetch_reddit_posts(self, search_query=SEARCH_QUERY, subreddit_limit=SUBREDDIT_LIMIT, post_limit=POST_LIMIT,
                           posts_sort=POSTS_SORT, posts_fields=POSTS_FIELDS):
        """Fetch posts from subreddits matching the search query."""
        if posts_fields is None:
            posts_fields = ['title', 'self_text', 'score', 'num_comments', 'created_utc', 'permalink', 'url', 'author']
        posts = []
        try:
            subreddits = self.reddit.subreddits.search(search_query, limit=subreddit_limit)
            for subreddit in subreddits:
                subreddit_name = subreddit.display_name
                if posts_sort == 'hot':
                    subreddit_posts = self.reddit.subreddit(subreddit_name).hot(limit=post_limit)
                elif posts_sort == 'top':
                    subreddit_posts = self.reddit.subreddit(subreddit_name).top(limit=post_limit)
                elif posts_sort == 'new':
                    subreddit_posts = self.reddit.subreddit(subreddit_name).new(limit=post_limit)
                else:
                    raise ValueError(f"Invalid sort option: {posts_sort}")

                for submission in subreddit_posts:
                    post = {}
                    for field in posts_fields:
                        if hasattr(submission, field):
                            if field == 'created_utc':
                                post['created_at'] = datetime.fromtimestamp(getattr(submission, field))
                            else:
                                post[field] = getattr(submission, field)
                    posts.append(post)
            logger.info(f"Fetched {len(posts)} posts from subreddits matching '{search_query}'.")
        except Exception as e:
            logger.error(f"Failed to fetch posts: {e}")
            raise
        return posts

    @staticmethod
    def save_posts_to_csv(posts, filename):
        """Save posts to a CSV file."""
        try:
            df = pd.DataFrame(posts)
            df.to_csv(filename, index=False)
            logger.info(f"Scraped {len(df)} posts and saved to {filename}.")
        except Exception as e:
            logger.error(f"Failed to save posts to CSV: {e}")
            raise

    @staticmethod
    def clean_text(text):
        """Convert text to lowercase, remove punctuation and emojis."""
        if isinstance(text, str):
            text = text.lower()
            text = text.translate(str.maketrans('', '', string.punctuation))
            text = re.sub(r'[^\w\s]', '', text)
        return text

    def clean_dataframe(self, file_path, cleaned_file_path):
        """Clean the data in the DataFrame and save it to a new CSV file."""
        try:
            df = pd.read_csv(file_path)
            df.columns = [col.lower() for col in df.columns]
            for col in df.columns:
                df[col] = df[col].map(self.clean_text)
            df.to_csv(cleaned_file_path, index=False)
            logger.info(f"Data cleaned and saved to {cleaned_file_path}.")
        except Exception as e:
            logger.error(f"Failed to clean DataFrame: {e}")
            raise

    @staticmethod
    def shuffle_and_save_dataframe(file_path, shuffled_file_path):
        """Shuffle the DataFrame and save it to a new CSV file."""
        try:
            df = pd.read_csv(file_path)
            shuffled_df = df.sample(frac=1).reset_index(drop=True)
            shuffled_df.to_csv(shuffled_file_path, index=False)
            logger.info(f"Shuffled file saved to {shuffled_file_path}.")
        except Exception as shuffle_error:
            logger.error(f"Failed to shuffle and save DataFrame: {shuffle_error}")
            raise

    def run(self):
        try:
            self.spinner.start('Initializing Reddit instance...')
            self.initialize_reddit()
            self.spinner.succeed('Reddit instance initialized.')

            self.spinner.start('Fetching Reddit posts...')
            fetched_posts = self.fetch_reddit_posts(SEARCH_QUERY, SUBREDDIT_LIMIT, POST_LIMIT)
            self.spinner.succeed('Reddit posts fetched.')

            self.spinner.start('Saving posts to CSV...')
            self.save_posts_to_csv(fetched_posts, RAW_CSV_PATH)
            self.spinner.succeed('Posts saved to CSV.')

            self.spinner.start('Cleaning DataFrame...')
            self.clean_dataframe(RAW_CSV_PATH, CLEANED_CSV_PATH)
            self.spinner.succeed('DataFrame cleaned.')

            self.spinner.start('Shuffling DataFrame...')
            self.shuffle_and_save_dataframe(CLEANED_CSV_PATH, SHUFFLED_CSV_PATH)
            self.spinner.succeed('DataFrame shuffled.')

        except Exception as error:
            self.spinner.fail(f"An error occurred: {error}")
            logger.exception("Exception occurred")
        finally:
            self.spinner.stop()
            logger.info("Process completed.")


if __name__ == "__main__":
    scraper = RedditScraper(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
    scraper.run()
