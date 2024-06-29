import streamlit as st
from reddit_scraper import CLIENT_ID, CLIENT_SECRET, USER_AGENT, RedditScraper


class StreamlitRedditScraper:
    def __init__(self):
        self.scraper = RedditScraper(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
        self.scraper.initialize_reddit()

    def fetch_posts(self, query):
        return self.scraper.fetch_reddit_posts(query, subreddit_limit=5, post_limit=5)

    def run(self):
        st.set_page_config(page_title="Reddit Scraper", page_icon=":mag:")

        st.title(':mag: Reddit Scraper')

        st.markdown("""
            Enter a search query to fetch the latest posts from Reddit.
            """)
        query = st.text_input('Enter a search query:', 'fastapi')

        if st.button('Fetch posts'):
            with st.spinner('Fetching posts... :hourglass_flowing_sand:'):
                posts = self.fetch_posts(query)
                if posts:
                    st.success(f'Found {len(posts)} posts for the query "{query}"! :tada:')
                    for post in posts:
                        st.markdown(f"""
                            **Subreddit:** {post['subreddit']}
                            **Title:** {post['title']}
                            **Score:** {post['score']} :star:
                            **Comments:** {post['num_comments']} :speech_balloon:
                            **URL:** [Link]({post['url']})
                            **Created At:** {post['created_at']}
                            **Content:** {post['content']}
                            ---
                            """)
                else:
                    st.error('No posts found for the provided query. :x:')
        else:
            st.info('Enter a query and click the "Fetch posts" button to get results. :information_source:')

        st.markdown("""
            ---
            :bulb: **Tip:** You can search for various topics like `python`, `fastapi`, `data science`, etc.
            """)


if __name__ == "__main__":
    scraper = StreamlitRedditScraper()
    scraper.run()
