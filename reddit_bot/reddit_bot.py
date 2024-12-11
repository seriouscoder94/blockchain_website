import praw
import requests
import schedule
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Reddit API credentials
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT'),
    username=os.getenv('REDDIT_USERNAME'),
    password=os.getenv('REDDIT_PASSWORD')
)

# Crypto news API credentials
CRYPTO_API_KEY = os.getenv('CRYPTO_API_KEY')
CRYPTO_NEWS_URL = "https://cryptopanic.com/api/v1/posts/"

def get_crypto_news():
    """Fetch latest crypto news from CryptoPanic API"""
    try:
        params = {
            'auth_token': CRYPTO_API_KEY,
            'kind': 'news',
            'filter': 'hot',
            'regions': 'en',  # English news only
            'public': True,
            'metadata': 'true'
        }
        response = requests.get(CRYPTO_NEWS_URL, params=params)
        response.raise_for_status()
        
        news = response.json()['results']
        # Get fresh news items and avoid duplicates
        fresh_news = [item for item in news 
                     if (datetime.now() - datetime.strptime(item['published_at'][:19], 
                         '%Y-%m-%dT%H:%M:%S')).total_seconds() < 14400]  # Last 4 hours
        
        return fresh_news[:3] if fresh_news else news[:3]  # Return top 3 news items
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None

def create_reddit_post(subreddit_name, news_items):
    """Create a Reddit post with the news items"""
    if not news_items:
        return
    
    try:
        subreddit = reddit.subreddit(subreddit_name)
        
        # Create SEO-friendly title (Reddit search optimization)
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%I:%M %p")
        
        # Extract key topics for better searchability
        topics = []
        for news in news_items:
            for keyword in ['Bitcoin', 'BTC', 'Ethereum', 'ETH', 'Crypto', 'Blockchain']:
                if keyword.lower() in news['title'].lower():
                    topics.append(keyword)
        topics = list(dict.fromkeys(topics))  # Remove duplicates
        
        # Create search-optimized title
        topics_str = f"[{' | '.join(topics[:2])}] " if topics else ""
        post_title = f"{topics_str}Crypto News Update - {current_date} {current_time} CT"
        
        # Create post content
        post_content = "## 🚀 Latest Cryptocurrency News & Updates\n\n"
        
        for idx, news in enumerate(news_items, 1):
            post_content += f"### {idx}. {news['title']}\n"
            post_content += f"📰 Source: {news['source']['title']}\n"
            post_content += f"🔗 [Read Full Article]({news['url']})\n\n"
            if news.get('metadata', {}).get('description'):
                post_content += f"> {news['metadata']['description']}\n\n"
        
        # Add engagement prompts (increases comment activity)
        post_content += "\n## 💬 Discussion\n"
        post_content += "* What's your take on these developments?\n"
        post_content += "* Which news do you think is most significant?\n"
        post_content += "* Share your insights below!\n\n"
        
        post_content += "\n---\n"
        post_content += "🌐 **Stay Updated**: Visit [BlockchainFriendly.com](https://seriouscoder94.github.io/blockchain_website/) "
        post_content += "for more insights and educational content about blockchain technology and cryptocurrency.\n\n"
        post_content += "*This update is brought to you by the BlockchainFriendly News Bot* 🤖"
        
        # Add post flair for better categorization
        post = subreddit.submit(title=post_title, selftext=post_content)
        print(f"Successfully posted to r/{subreddit_name}")
    
    except Exception as e:
        print(f"Error creating Reddit post: {e}")

def daily_task():
    """Main task to run daily"""
    news_items = get_crypto_news()
    if news_items:
        # Post only to our subreddit
        create_reddit_post('BlockchainFriendly', news_items)
        print(f"Successfully posted to r/BlockchainFriendly")

def test_post():
    """Make an immediate test post"""
    print("Making a test post to r/BlockchainFriendly...")
    news_items = get_crypto_news()
    if news_items:
        # Test post to our subreddit
        create_reddit_post('BlockchainFriendly', news_items)
        print("Test post completed! Check r/BlockchainFriendly for your post.")
    else:
        print("Error: Could not fetch news for test post.")

def main():
    """Main function to schedule and run the bot"""
    print("Starting Reddit Crypto News Bot...")
    
    # Make a test post first
    test_post()
    
    # Schedule 5 posts throughout the day at optimal times
    schedule.every().day.at("09:00").do(daily_task)  # Morning US/Evening Asia
    schedule.every().day.at("12:00").do(daily_task)  # Lunch time US
    schedule.every().day.at("15:00").do(daily_task)  # Afternoon US/Evening Europe
    schedule.every().day.at("18:00").do(daily_task)  # Evening US/Night Europe
    schedule.every().day.at("21:00").do(daily_task)  # Night US/Morning Asia
    
    print("Bot scheduled to post at: 9 AM, 12 PM, 3 PM, 6 PM, and 9 PM Central Time")
    
    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
