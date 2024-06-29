from halo import Halo
from loguru import logger
import subprocess

from app.fast_api_scraper import FastApiRedditScraper
from app.reddit_scraper import CLIENT_ID, CLIENT_SECRET, USER_AGENT, SUBREDDIT_LIMIT, POST_LIMIT, RedditScraper

logger.add("logs/app.log", rotation="10 MB", level="INFO", backtrace=True, diagnose=True)
spinner = Halo(text='Processing', spinner='dots')


def main():
    while True:
        print("\nMenu:")
        print("1. Run FastApiRedditScraper")
        print("2. Run RedditScraper")
        print("3. Run Streamlit app")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            # Initialize the scraper
            scraper = FastApiRedditScraper(CLIENT_ID, CLIENT_SECRET, USER_AGENT)

            # Get the query from the user
            query = input("Enter a search query: ")

            try:
                spinner.start('Fetching posts...')
                # Fetch the posts
                posts = scraper.fetch_posts(query, SUBREDDIT_LIMIT, POST_LIMIT)
                spinner.stop()

                # Check if any posts were found
                if not posts:
                    print("No posts found for the provided query.")
                    continue

                # Print the posts
                for post in posts:
                    print(f"Subreddit: {post['subreddit']}")
                    print(f"Title: {post['title']}")
                    print(f"Score: {post['score']}")
                    print(f"URL: {post['url']}")
                    print(f"Number of comments: {post['num_comments']}")
                    print(f"Created at: {post['created_at']}")
                    print(f"Content: {post['content']}")
                    print("\n" + "-" * 50 + "\n")
            except Exception as e:
                spinner.stop()
                logger.error(f"An error occurred while fetching posts: {str(e)}")
        elif choice == '2':
            scraper = RedditScraper(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
            scraper.run()
        elif choice == '3':
            try:
                subprocess.run(["streamlit", "run", "app/streamlit_app.py"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Streamlit app failed to start: {str(e)}")
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")


if __name__ == "__main__":
    main()
