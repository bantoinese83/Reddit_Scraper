from fastapi import FastAPI, HTTPException, Path

from app.reddit_scraper import RedditScraper, CLIENT_ID, CLIENT_SECRET, USER_AGENT, SUBREDDIT_LIMIT, POST_LIMIT

app = FastAPI()


class FastApiRedditScraper:
    def __init__(self, client_id, client_secret, user_agent):
        self.scraper = RedditScraper(client_id, client_secret, user_agent)
        self.scraper.initialize_reddit()

    def fetch_posts(self, query, subreddit_limit, post_limit):
        return self.scraper.fetch_reddit_posts(query, subreddit_limit, post_limit)


@app.get("/scrape/{query}")
async def scrape(query: str = Path(..., description="The search query to scrape Reddit posts for")):
    if not query:
        raise HTTPException(status_code=400, detail="Query must be provided")

    try:
        scraper = FastApiRedditScraper(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
        fetched_posts = scraper.fetch_posts(query, SUBREDDIT_LIMIT, POST_LIMIT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while scraping: {str(e)}")

    if not fetched_posts:
        raise HTTPException(status_code=404, detail="No posts found for the provided query")

    return {"posts": fetched_posts}
