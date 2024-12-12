import praw
import requests
import schedule
import time
import os
from datetime import datetime
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize colorama for Windows
init()

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

def log_info(message):
    """Print info message with timestamp"""
    print(f"{Fore.CYAN}[{datetime.now().strftime('%H:%M:%S')}] INFO: {message}{Style.RESET_ALL}")

def log_success(message):
    """Print success message with timestamp"""
    print(f"{Fore.GREEN}[{datetime.now().strftime('%H:%M:%S')}] SUCCESS: {message}{Style.RESET_ALL}")

def log_error(message):
    """Print error message with timestamp"""
    print(f"{Fore.RED}[{datetime.now().strftime('%H:%M:%S')}] ERROR: {message}{Style.RESET_ALL}")

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
        log_error(f"Error fetching news: {e}")
        return None

def create_reddit_post(subreddit_name, news_items):
    """Create a Reddit post with the news items"""
    if not news_items:
        log_error("No news items to post")
        return False
    
    try:
        subreddit = reddit.subreddit(subreddit_name)
        
        # Create SEO-friendly title
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%I:%M %p")
        
        # Extract key topics for better searchability
        topics = []
        for news in news_items:
            for keyword in ['Bitcoin', 'BTC', 'Ethereum', 'ETH', 'Crypto', 'Blockchain', 'NFT', 'DeFi']:
                if keyword.lower() in news['title'].lower():
                    topics.append(keyword)
        topics = list(dict.fromkeys(topics))  # Remove duplicates
        
        # Create search-optimized title
        topics_str = f"[{' | '.join(topics[:2])}] " if topics else "[Crypto News] "
        post_title = f"{topics_str}Daily Blockchain & Crypto Update - {current_date} {current_time} CT"
        
        # Create post content with plain text alternatives for emojis
        post_content = "## Latest Blockchain & Cryptocurrency News\n\n"
        
        for idx, news in enumerate(news_items, 1):
            post_content += f"### {idx}. {news['title']}\n"
            post_content += f"Source: {news['source']['title']}\n"
            post_content += f"[Read Full Article]({news['url']})\n\n"
            if news.get('metadata', {}).get('description'):
                post_content += f"> {news['metadata']['description']}\n\n"
        
        # Add engagement prompts
        post_content += "\n## Discussion\n"
        post_content += "* What are your thoughts on these developments?\n"
        post_content += "* How might these news items impact the blockchain industry?\n"
        post_content += "* Share your analysis below!\n\n"
        
        post_content += "\n---\n"
        post_content += "**Stay Updated**: Visit [BlockchainFriendly.com](https://blockchainfriendly.com) "
        post_content += "for more insights and educational content about blockchain technology and cryptocurrency.\n\n"
        post_content += "*This update is brought to you by the BlockchainFriendly News Bot*"
        
        # Create the post
        try:
            post = subreddit.submit(title=post_title, selftext=post_content)
            log_success(f"Posted to r/{subreddit_name}")
            log_info(f"Post URL: {post.url}")
            return True
        except praw.exceptions.RedditAPIException as api_exception:
            log_error(f"Reddit API Error: {api_exception}")
            return False
        except Exception as post_error:
            log_error(f"Error creating post: {post_error}")
            return False
            
    except Exception as e:
        log_error(f"Critical Error: {e}")
        return False

def daily_task():
    """Main task to run daily"""
    log_info("Starting daily news update task...")
    news_items = get_crypto_news()
    if news_items:
        success = create_reddit_post('BlockchainFriendly', news_items)
        if success:
            log_success("Daily task completed successfully!")
        else:
            log_error("Daily task completed with errors")
    else:
        log_error("Could not fetch news items for daily task")

def test_post():
    """Make an immediate test post"""
    log_info("Making a test post to r/BlockchainFriendly...")
    news_items = get_crypto_news()
    if news_items:
        success = create_reddit_post('BlockchainFriendly', news_items)
        if success:
            log_success("Test post successful!")
        else:
            log_error("Test post failed")
    else:
        log_error("Could not fetch news for test post")

def main():
    """Main function to schedule and run the bot"""
    log_info("Starting BlockchainFriendly Reddit Bot...")
    
    # Make an initial test post
    test_post()
    
    # Schedule posts throughout the day (Central Time)
    schedule.every().day.at("08:00").do(daily_task)  # Morning update
    schedule.every().day.at("12:00").do(daily_task)  # Midday update
    schedule.every().day.at("16:00").do(daily_task)  # Afternoon update
    schedule.every().day.at("20:00").do(daily_task)  # Evening update
    
    log_info("Bot scheduled to post at:")
    print(f"{Fore.YELLOW}   • 8:00 AM CT (Morning Update)")
    print(f"   • 12:00 PM CT (Midday Update)")
    print(f"   • 4:00 PM CT (Afternoon Update)")
    print(f"   • 8:00 PM CT (Evening Update){Style.RESET_ALL}")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except Exception as e:
            log_error(f"Scheduler Error: {e}")
            time.sleep(300)  # Wait 5 minutes before retrying

if __name__ == "__main__":
    main()
