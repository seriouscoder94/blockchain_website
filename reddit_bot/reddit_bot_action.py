import praw
import requests
import os
from datetime import datetime

# Reddit API credentials from GitHub secrets
reddit = praw.Reddit(
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_CLIENT_SECRET'],
    user_agent=os.environ['REDDIT_USER_AGENT'],
    username=os.environ['REDDIT_USERNAME'],
    password=os.environ['REDDIT_PASSWORD']
)

# Crypto news API credentials
CRYPTO_API_KEY = os.environ['CRYPTO_API_KEY']
CRYPTO_NEWS_URL = "https://cryptopanic.com/api/v1/posts/"

def get_crypto_news():
    """Fetch latest crypto news from CryptoPanic API"""
    try:
        params = {
            'auth_token': CRYPTO_API_KEY,
            'kind': 'news',
            'filter': 'hot',
            'regions': 'en',
            'public': True,
            'metadata': 'true'
        }
        response = requests.get(CRYPTO_NEWS_URL, params=params)
        response.raise_for_status()
        
        news = response.json()['results']
        # Get fresh news items
        fresh_news = [item for item in news 
                     if (datetime.now() - datetime.strptime(item['published_at'][:19], 
                         '%Y-%m-%dT%H:%M:%S')).total_seconds() < 14400]
        
        return fresh_news[:3] if fresh_news else news[:3]
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None

def create_reddit_post(subreddit_name, news_items):
    """Create a Reddit post with the news items"""
    if not news_items:
        return
    
    try:
        subreddit = reddit.subreddit(subreddit_name)
        
        # Create SEO-friendly title
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%I:%M %p")
        
        # Extract key topics
        topics = []
        for news in news_items:
            for keyword in ['Bitcoin', 'BTC', 'Ethereum', 'ETH', 'Crypto', 'Blockchain']:
                if keyword.lower() in news['title'].lower():
                    topics.append(keyword)
        topics = list(dict.fromkeys(topics))
        
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
        
        # Add engagement prompts
        post_content += "\n## 💬 Discussion\n"
        post_content += "* What's your take on these developments?\n"
        post_content += "* Which news do you think is most significant?\n"
        post_content += "* Share your insights below!\n\n"
        
        post_content += "\n---\n"
        post_content += "🌐 **Stay Updated**: Visit [BlockchainFriendly.com](https://seriouscoder94.github.io/blockchain_website/) "
        post_content += "for more insights and educational content about blockchain technology and cryptocurrency.\n\n"
        post_content += "*This update is brought to you by the BlockchainFriendly News Bot* 🤖"
        
        # Create the post
        post = subreddit.submit(title=post_title, selftext=post_content)
        print(f"Successfully posted to r/{subreddit_name}")
    
    except Exception as e:
        print(f"Error creating Reddit post: {e}")

def main():
    """Main function to run the bot"""
    print("Starting Reddit Crypto News Bot...")
    news_items = get_crypto_news()
    if news_items:
        create_reddit_post('BlockchainFriendly', news_items)
    else:
        print("No news items found to post")

if __name__ == "__main__":
    main()
