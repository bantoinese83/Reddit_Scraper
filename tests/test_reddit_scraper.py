from datetime import datetime
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest

from app.reddit_scraper import RedditScraper, CLIENT_ID, CLIENT_SECRET, USER_AGENT, RAW_CSV_PATH, CLEANED_CSV_PATH, \
    SHUFFLED_CSV_PATH, LOG_FILE_PATH


@pytest.fixture
def mock_reddit_instance():
    with patch('app.reddit_scraper.praw.Reddit') as MockReddit:
        mock_instance = MockReddit.return_value
        yield mock_instance


@pytest.fixture
def mock_scraper(mock_reddit_instance):
    scraper = RedditScraper(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
    return scraper


def test_setup_logging():
    with patch('app.reddit_scraper.logger.add') as mock_logger_add:
        RedditScraper.setup_logging()
        mock_logger_add.assert_called_once_with(LOG_FILE_PATH, rotation='10 MB', level='INFO', backtrace=True,
                                                diagnose=True)


def test_initialize_reddit_failure(mock_scraper):
    with patch('app.reddit_scraper.praw.Reddit', side_effect=Exception("API error")):
        with pytest.raises(Exception, match="API error"):
            mock_scraper.initialize_reddit()


def test_save_posts_to_csv_success():
    posts = [{'subreddit': 'testsub', 'title': 'Test Post', 'score': 10, 'id': 'test_id', 'url': 'http://example.com',
              'num_comments': 5, 'created_at': datetime(2021, 3, 24), 'content': 'This is a test post'}]
    with patch('app.reddit_scraper.pd.DataFrame.to_csv') as mock_to_csv:
        RedditScraper.save_posts_to_csv(posts, RAW_CSV_PATH)
        mock_to_csv.assert_called_once_with(RAW_CSV_PATH, index=False)


def test_save_posts_to_csv_failure():
    posts = [{'subreddit': 'testsub', 'title': 'Test Post', 'score': 10, 'id': 'test_id', 'url': 'http://example.com',
              'num_comments': 5, 'created_at': datetime(2021, 3, 24), 'content': 'This is a test post'}]
    with patch('app.reddit_scraper.pd.DataFrame.to_csv', side_effect=Exception("File error")):
        with pytest.raises(Exception, match="File error"):
            RedditScraper.save_posts_to_csv(posts, RAW_CSV_PATH)


def test_clean_dataframe_success():
    df = pd.DataFrame({'col1': ['Hello, World! 🌍'], 'col2': ['Test String!!!']})
    with patch('app.reddit_scraper.pd.read_csv', return_value=df), \
            patch('app.reddit_scraper.pd.DataFrame.to_csv') as mock_to_csv:
        scraper = RedditScraper(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
        scraper.clean_dataframe(RAW_CSV_PATH, CLEANED_CSV_PATH)
        mock_to_csv.assert_called_once_with(CLEANED_CSV_PATH, index=False)


def test_clean_dataframe_failure():
    with patch('app.reddit_scraper.pd.read_csv', side_effect=Exception("Read error")):
        scraper = RedditScraper(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
        with pytest.raises(Exception, match="Read error"):
            scraper.clean_dataframe(RAW_CSV_PATH, CLEANED_CSV_PATH)


def test_shuffle_and_save_dataframe_success():
    df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
    with patch('app.reddit_scraper.pd.read_csv', return_value=df), \
            patch('app.reddit_scraper.pd.DataFrame.to_csv') as mock_to_csv:
        RedditScraper.shuffle_and_save_dataframe(CLEANED_CSV_PATH, SHUFFLED_CSV_PATH)
        mock_to_csv.assert_called_once_with(SHUFFLED_CSV_PATH, index=False)


def test_shuffle_and_save_dataframe_failure():
    with patch('app.reddit_scraper.pd.read_csv', side_effect=Exception("Read error")):
        with pytest.raises(Exception, match="Read error"):
            RedditScraper.shuffle_and_save_dataframe(CLEANED_CSV_PATH, SHUFFLED_CSV_PATH)


def test_run_failure(mock_scraper):
    mock_scraper.initialize_reddit = MagicMock(side_effect=Exception("Initialization error"))
    mock_scraper.spinner.fail = MagicMock()

    mock_scraper.run()
    mock_scraper.spinner.fail.assert_called_once_with("An error occurred: Initialization error")


@patch('app.reddit_scraper.praw.Reddit')
def test_initialize_reddit_success(mock_reddit, mock_reddit_instance):
    mock_scraper = RedditScraper(
        client_id="test_client_id",
        client_secret="test_client_secret",
        user_agent="test_user_agent"
    )
    mock_reddit_instance = mock_reddit.return_value
    mock_scraper.initialize_reddit()
    mock_reddit.assert_called_once()
    assert mock_scraper.reddit == mock_reddit_instance


@patch('app.reddit_scraper.praw.Reddit')
def test_fetch_reddit_posts_success(mock_reddit, mock_reddit_instance):
    mock_scraper = RedditScraper(
        client_id="test_client_id",
        client_secret="test_client_secret",
        user_agent="test_user_agent"
    )
    mock_reddit_instance = mock_reddit.return_value
    mock_scraper.reddit = mock_reddit_instance
    mock_reddit_instance.subreddits.search.return_value = [MagicMock(display_name="testsub")]
    mock_submission = MagicMock()
    mock_submission.title = "Test Post"
    mock_submission.score = 10
    mock_submission.id = "test_id"
    mock_submission.url = "http://example.com"
    mock_submission.num_comments = 5
    mock_submission.created_utc = 1616582223
    mock_submission.selftext = "This is a test post"
    mock_reddit_instance.subreddit.return_value.hot.return_value = [mock_submission]

    posts = mock_scraper.fetch_reddit_posts("fastapi", 1, 1)
    assert len(posts) == 1


@patch('app.reddit_scraper.praw.Reddit')
def test_fetch_reddit_posts_failure(mock_reddit, mock_reddit_instance):
    mock_scraper = RedditScraper(
        client_id="test_client_id",
        client_secret="test_client_secret",
        user_agent="test_user_agent"
    )
    mock_reddit_instance = mock_reddit.return_value
    mock_scraper.reddit = mock_reddit_instance
    mock_reddit_instance.subreddits.search.side_effect = Exception("API error")
    with pytest.raises(Exception, match="API error"):
        mock_scraper.fetch_reddit_posts("fastapi", 1, 1)


def test_clean_text():
    text = "Hello, World! 🌍"
    cleaned_text = RedditScraper.clean_text(text).strip()
    assert cleaned_text == "hello world"


@patch('app.reddit_scraper.praw.Reddit')
def test_run_success(mock_reddit, mock_reddit_instance):
    mock_scraper = RedditScraper(
        client_id="test_client_id",
        client_secret="test_client_secret",
        user_agent="test_user_agent"
    )
    mock_reddit_instance = mock_reddit.return_value
    mock_scraper.reddit = mock_reddit_instance
    mock_scraper.fetch_reddit_posts = MagicMock(return_value=[])
    mock_scraper.save_posts_to_csv = MagicMock()
    mock_scraper.clean_dataframe = MagicMock()
    mock_scraper.shuffle_and_save_dataframe = MagicMock()
    mock_scraper.spinner = MagicMock()

    mock_scraper.run()

    mock_scraper.spinner.start.assert_any_call('Initializing Reddit instance...')
    mock_scraper.spinner.start.assert_any_call('Fetching Reddit posts...')
