import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Reddit API credentials
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    USER_AGENT = os.getenv('USER_AGENT')

    # Directories
    DATA_DIR = 'data'
    LOG_DIR = 'logs'

    # Check if directories exist and create them if they don't
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    # File paths
    RAW_CSV_PATH = os.path.join(DATA_DIR, 'fastapi_subreddits_posts.csv')
    CLEANED_CSV_PATH = os.path.join(DATA_DIR, 'cleaned_file.csv')
    SHUFFLED_CSV_PATH = os.path.join(DATA_DIR, 'shuffled_cleaned_file.csv')
    LOG_FILE_PATH = os.path.join(LOG_DIR, 'reddit_scraper.log')

    # Reddit API parameters
    SEARCH_QUERY = ''  # Your search query
    SUBREDDIT_LIMIT = 5
    POST_LIMIT = 10
    POSTS_SORT = 'hot'
    POSTS_FIELDS = ['title', 'self_text', 'score', 'num_comments', 'created_utc', 'permalink', 'url', 'author']
