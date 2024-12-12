import requests
from requests_oauthlib import OAuth1Session
import time
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import sys
import schedule
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

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

def post_tweet_with_image(text, image_path=None):
    """Post a tweet with optional image"""
    try:
        # Create OAuth1Session
        twitter = OAuth1Session(
            os.getenv('TWITTER_API_KEY'),
            client_secret=os.getenv('TWITTER_API_SECRET'),
            resource_owner_key=os.getenv('TWITTER_ACCESS_TOKEN'),
            resource_owner_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )
        
        if image_path:
            # First, upload the image
            url_media = "https://upload.twitter.com/1.1/media/upload.json"
            files = {"media": open(image_path, 'rb')}
            response = twitter.post(url_media, files=files)
            
            if response.status_code != 200:
                print(f"Error uploading media: {response.status_code} {response.text}")
                return False
                
            # Get media_id from response
            media_id = response.json()['media_id']
            
            # Post tweet with media
            url = "https://api.twitter.com/2/tweets"
            payload = {
                "text": text,
                "media": {"media_ids": [str(media_id)]}
            }
        else:
            # Post tweet without media
            url = "https://api.twitter.com/2/tweets"
            payload = {"text": text}
            
        response = twitter.post(url, json=payload)
        
        if response.status_code != 201:
            print(f"Error posting tweet: {response.status_code} {response.text}")
            return False
            
        print(f"Successfully posted tweet: {response.json()['data']['id']}")
        return True
        
    except Exception as e:
        print(f"Error posting tweet: {e}")
        return False

def get_crypto_news():
    """Fetch latest crypto news from CryptoCompare API"""
    try:
        url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
        response = requests.get(url)
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
                        
                        # Get a brief excerpt from the body (first 100 characters)
                        body_text = article.get('body', '').strip()
                        excerpt = body_text[:100] + '...' if len(body_text) > 100 else body_text
                        
                        today_news.append({
                            'title': article['title'],
                            'url': article['url'],
                            'source': article['source'],
                            'image_path': image_path,
                            'excerpt': excerpt
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
                            
                        # Get a brief excerpt from the body (first 100 characters)
                        body_text = article.get('body', '').strip()
                        excerpt = body_text[:100] + '...' if len(body_text) > 100 else body_text
                        
                        latest_news.append({
                            'title': article['title'],
                            'url': article['url'],
                            'source': article['source'],
                            'image_path': image_path,
                            'excerpt': excerpt
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

def create_tweets():
    """Create tweets from crypto news"""
    print(f"Starting scheduled tweets at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    news_items = get_crypto_news()
    
    if not news_items:
        print("No news items to tweet")
        return

    # Select only 3 random news items
    selected_items = random.sample(news_items[:10], min(3, len(news_items)))

    for item in selected_items:
        try:
            # Format the tweet text with title and timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tweet_text = f"📊 Crypto News Update | {current_time}\n\n"
            tweet_text += f"{item['title']}\n\n"
            
            # Add source attribution and CTA
            tweet_text += f"via {item['source']} {item['url']}\n"
            tweet_text += "#crypto #blockchain #news"
            
            # Trim if tweet is too long (Twitter limit is 280 characters)
            if len(tweet_text) > 280:
                # Keep the timestamp and title, trim URL if needed
                header = f"📊 Crypto News Update | {current_time}\n\n"
                title = f"{item['title']}\n\n"
                footer = f"\nvia {item['source']} #crypto #blockchain #news"
                
                # Calculate available space for URL
                available_chars = 280 - len(header) - len(title) - len(footer)
                if available_chars > 30:  # Minimum reasonable URL length
                    tweet_text = header + title + f"via {item['source']} {item['url']}" + footer
                else:
                    tweet_text = header + title + footer
            
            # Post tweet with image if available
            success = post_tweet_with_image(tweet_text, item['image_path'])
            
            if success:
                print(f"Successfully tweeted about: {item['title']}")
            
            # Clean up image file
            if item['image_path'] and os.path.exists(item['image_path']):
                os.remove(item['image_path'])
            
            # Wait between tweets to avoid rate limits
            time.sleep(5)
            
        except Exception as e:
            print(f"Error creating tweet for {item['title']}: {e}")
            # Clean up image file in case of error
            if item['image_path'] and os.path.exists(item['image_path']):
                os.remove(item['image_path'])
            continue

def schedule_tweets():
    """Schedule tweets throughout the day"""
    # Tweet 5 times a day at optimal times for engagement
    schedule.every().day.at("08:00").do(create_tweets)  # Early morning
    schedule.every().day.at("11:30").do(create_tweets)  # Late morning
    schedule.every().day.at("14:30").do(create_tweets)  # Early afternoon
    schedule.every().day.at("17:30").do(create_tweets)  # Evening rush
    schedule.every().day.at("20:00").do(create_tweets)  # Prime time
    
    while True:
        schedule.run_pending()
        time.sleep(60)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--schedule":
        print("Starting scheduled tweets...")
        schedule_tweets()
    else:
        print("Running single tweet test...")
        create_tweets()

if __name__ == "__main__":
    main()
