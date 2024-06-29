# Reddit Scraper

This project is a Reddit scraper built with Python. It uses the Reddit API to fetch posts from subreddits based on a search query.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.10
- pip

### Installation

1. Clone the repository:
    ```
    git clone https://github.com/bantoinese83/Reddit_Scraper.git
    ```
2. Navigate to the project directory:
    ```
    cd Reddit_Scraper
    ```
3. Install the required packages:
    ```
    pip install -r requirements.txt
    ```
4. Create a Reddit app:
    - Go to [Reddit](https://www.reddit.com/prefs/apps)
    - Click on "Create App"
    - Fill in the details and click on "Create App"
    - Copy the client ID and client secret
5. Create a virtual environment:
    ```
    python -m venv Reddit_Scraper
    ```
6. Activate the virtual environment:
    - Windows:
        ```
        Reddit_Scraper\Scripts\activate
        ```
    - MacOS/Linux:
        ```
        source Reddit_Scraper/bin/activate
        ```
7. Create a `.env` file in the project directory and add the following:
8. ```
    CLIENT_ID=<client_id>
    CLIENT_SECRET=<client_secret
    USER_AGENT=<user_agent>
    ```
9. Replace `<client_id>`, `<client_secret>`, and `<user_agent>` with the values from the Reddit app you created.
10. Deactivate the virtual environment:
    ```
    deactivate
    ```
## Usage

To run the Reddit scraper, execute the following command:
```
python main.py
```

## Testing

To run the tests, execute the following command:
```
path/to/your/env/Reddit_Scraper/bin/python -m pytest tests
```

## Built With

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [PRAW](https://praw.readthedocs.io/en/latest/)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration
- etc