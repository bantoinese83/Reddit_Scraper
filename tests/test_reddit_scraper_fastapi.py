import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.fast_api_scraper import app, FastApiRedditScraper
client = TestClient(app)


@pytest.fixture
def mock_reddit_instance():
    with patch('app.reddit_scraper.praw.Reddit') as MockReddit:
        mock_instance = MockReddit.return_value
        yield mock_instance


@pytest.fixture
def mock_scraper(mock_reddit_instance):
    scraper = FastApiRedditScraper("fake_client_id", "fake_client_secret", "fake_user_agent")
    return scraper


def test_fetch_posts_success(mock_scraper, mock_reddit_instance):
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

    posts = mock_scraper.fetch_posts("fastapi", 1, 1)

    assert len(posts) == 1
    assert posts[0]['title'] == "Test Post"


def test_scrape_endpoint_success(mock_reddit_instance):
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

    response = client.get("/scrape/fastapi")

    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response['posts']) == 1
    assert json_response['posts'][0]['title'] == "Test Post"


def test_scrape_endpoint_no_query():
    response = client.get("/scrape/")
    assert response.status_code == 404  # FastAPI will raise a 404 for missing path parameter


def test_scrape_endpoint_no_posts_found(mock_reddit_instance):
    mock_reddit_instance.subreddits.search.return_value = []

    response = client.get("/scrape/fastapi")

    assert response.status_code == 404
    assert response.json() == {"detail": "No posts found for the provided query"}


def test_scrape_endpoint_error(mock_reddit_instance):
    mock_reddit_instance.subreddits.search.side_effect = Exception("API error")

    response = client.get("/scrape/fastapi")

    assert response.status_code == 500
    assert response.json() == {"detail": "An error occurred while scraping: API error"}
