import praw
import requests
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import schedule
import random
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO
import sys

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

# CryptoCompare API endpoint
CRYPTOCOMPARE_NEWS_URL = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"

def download_image(url):
    """Download and save image from URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Get file extension from URL
        parsed_url = urlparse(url)
        ext = os.path.splitext(parsed_url.path)[1].lower()
        if not ext:
            ext = '.jpg'  # Default to jpg if no extension found
            
        # Create images directory if it doesn't exist
        os.makedirs('images', exist_ok=True)
        
        # Generate unique filename
        filename = f"images/crypto_news_{int(time.time())}{ext}"
        
        # Save image
        img = Image.open(BytesIO(response.content))
        img.save(filename)
        return filename
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def get_crypto_news():
    """Fetch latest crypto news from CryptoCompare API"""
    try:
        response = requests.get(CRYPTOCOMPARE_NEWS_URL)
        response.raise_for_status()
        
        result = response.json()
        if 'Data' in result:
            articles = result['Data']
            if not articles:
                print("No articles found in the response")
                return None
                
            # Get today's news
            today = datetime.now().date()
            today_news = []
            
            for article in articles:
                try:
                    article_date = datetime.fromtimestamp(article['published_on']).date()
                    if article_date == today:
                        # Download and save the article image
                        image_path = None
                        if 'imageurl' in article:
                            image_path = download_image(article['imageurl'])
                        
                        today_news.append({
                            'title': article['title'],
                            'url': article['url'],
                            'source': {'title': article['source']},
                            'published_at': datetime.fromtimestamp(article['published_on']).isoformat(),
                            'body': article['body'],
                            'categories': article['categories'],
                            'tags': article.get('tags', []),
                            'image_path': image_path
                        })
                except KeyError as e:
                    print(f"Skipping article due to missing field: {e}")
                    continue
            
            # Return random 3 articles from today's news
            if today_news:
                print(f"Found {len(today_news)} articles from today")
                return random.sample(today_news, min(3, len(today_news)))
            else:
                print("No today's news found, returning random 3 articles")
                random_articles = random.sample(articles, min(3, len(articles)))
                latest_news = []
                for article in random_articles:
                    try:
                        # Download and save the article image
                        image_path = None
                        if 'imageurl' in article:
                            image_path = download_image(article['imageurl'])
                            
                        latest_news.append({
                            'title': article['title'],
                            'url': article['url'],
                            'source': {'title': article['source']},
                            'published_at': datetime.fromtimestamp(article['published_on']).isoformat(),
                            'body': article['body'],
                            'categories': article['categories'],
                            'tags': article.get('tags', []),
                            'image_path': image_path
                        })
                    except KeyError as e:
                        print(f"Skipping article due to missing field: {e}")
                        continue
                return latest_news if latest_news else None
        else:
            print("No 'Data' field found in the API response")
            return None
            
    except Exception as e:
        print(f"Error fetching crypto news: {e}")
        return None

def create_reddit_posts():
    """Create Reddit posts for news items"""
    print(f"Starting scheduled post at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    news_items = get_crypto_news()
    
    if not news_items:
        print("No news items to post")
        return

    subreddit = reddit.subreddit('BlockchainFriendly')
    
    for item in news_items:
        try:
            # Format the post content
            post_title = f" {item['title']}"
            
            post_body = f"""
{item['body']}

---
**Source**: {item['source']['title']}
**Published**: {item['published_at']}
**Categories**: {', '.join(item['categories'])}
**Tags**: {', '.join(item['tags']) if item['tags'] else 'None'}

[Read full article]({item['url']})

---
*This update is brought to you by BlockchainFriendlyNewsBot* 
            """
            
            # Create the post with image if available
            if item['image_path']:
                post = subreddit.submit_image(
                    title=post_title,
                    image_path=item['image_path']
                )
                # Add the article text as a comment
                post.reply(post_body)
            else:
                post = subreddit.submit(title=post_title, selftext=post_body)
                
            print(f"Successfully created post: {post.url}")
            
            # Clean up image file
            if item['image_path'] and os.path.exists(item['image_path']):
                os.remove(item['image_path'])
            
            # Wait between posts to avoid rate limits
            time.sleep(5)
            
        except Exception as e:
            print(f"Error creating post for {item['title']}: {e}")
            # Clean up image file in case of error
            if item['image_path'] and os.path.exists(item['image_path']):
                os.remove(item['image_path'])
            continue

def schedule_posts():
    """Schedule posts throughout the day"""
    # Post 5 times a day
    schedule.every().day.at("09:00").do(create_reddit_posts)  # Morning
    schedule.every().day.at("12:00").do(create_reddit_posts)  # Noon
    schedule.every().day.at("15:00").do(create_reddit_posts)  # Afternoon
    schedule.every().day.at("18:00").do(create_reddit_posts)  # Evening
    schedule.every().day.at("21:00").do(create_reddit_posts)  # Night
    
    while True:
        schedule.run_pending()
        time.sleep(60)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--schedule":
        print("Starting scheduled posting...")
        schedule_posts()
    else:
        print("Running single post test...")
        create_reddit_posts()

if __name__ == "__main__":
    import sys
    main()
