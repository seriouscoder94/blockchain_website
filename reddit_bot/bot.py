import praw
import os
from dotenv import load_dotenv
import requests
import time
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT'),
    username=os.getenv('REDDIT_USERNAME'),
    password=os.getenv('REDDIT_PASSWORD')
)

def get_crypto_news():
    """Fetch latest crypto news from CryptoPanic API"""
    api_key = os.getenv('CRYPTO_API_KEY')
    url = f'https://cryptopanic.com/api/v1/posts/?auth_token={api_key}&kind=news'
    
    try:
        response = requests.get(url)
        data = response.json()
        return data['results']
    except Exception as e:
        print(f"Error fetching crypto news: {e}")
        return None

def format_news_post(news):
    """Format news data into a Reddit post"""
    title = f"🚀 Latest Blockchain & Crypto News Update"
    
    content = []
    content.append("Hey crypto enthusiasts! 👋 Here are the latest updates from the blockchain world:\n")
    
    for idx, item in enumerate(news[:5], 1):
        content.append(f"{idx}. **{item['title']}**")
        content.append(f"   • Source: {item['source']['title']}")
        content.append(f"   • Link: {item['url']}\n")
    
    content.append("\n---")
    content.append("*This update is brought to you by BlockchainFriendlyNewsBot* 🤖")
    content.append("*Data provided by CryptoPanic*")
    
    return title, "\n".join(content)

def post_to_reddit(subreddit_name):
    """Post news to specified subreddit"""
    try:
        news = get_crypto_news()
        if not news:
            print("No news to post")
            return
        
        title, body = format_news_post(news)
        subreddit = reddit.subreddit(subreddit_name)
        subreddit.submit(title, selftext=body)
        print(f"Successfully posted to r/{subreddit_name}")
        
    except Exception as e:
        print(f"Error posting to Reddit: {e}")

def main():
    # List of crypto-related subreddits
    subreddits = ['CryptoNews', 'CryptoCurrency']  # Add more as needed
    
    for subreddit in subreddits:
        print(f"Posting to r/{subreddit}...")
        post_to_reddit(subreddit)
        time.sleep(10)  # Wait between posts to avoid rate limits

if __name__ == "__main__":
    main()
