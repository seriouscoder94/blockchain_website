import requests
from requests_oauthlib import OAuth1Session
import time
import random
import cryptocompare
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

def post_tweet(text):
    try:
        # Create OAuth1Session
        twitter = OAuth1Session(
            os.getenv('TWITTER_API_KEY'),
            client_secret=os.getenv('TWITTER_API_SECRET'),
            resource_owner_key=os.getenv('TWITTER_ACCESS_TOKEN'),
            resource_owner_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )
        
        url = "https://api.twitter.com/2/tweets"
        payload = {"text": text}
        response = twitter.post(url, json=payload)
        
        if response.status_code != 201:
            print(f"Request returned an error: {response.status_code} {response.text}")
            return False
            
        return True
        
    except Exception as e:
        print(f"Error posting tweet: {e}")
        return False

def get_crypto_news():
    try:
        url = f"https://min-api.cryptocompare.com/data/v2/news/?lang=EN&api_key={os.getenv('CRYPTO_COMPARE_API_KEY')}"
        response = requests.get(url)
        if response.status_code == 200:
            news = response.json()['Data']
            return random.choice(news)
        return None
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None

def get_crypto_prices():
    try:
        cryptos = ['BTC', 'ETH', 'BNB', 'XRP', 'SOL', 'ADA', 'DOGE']
        prices = {}
        for crypto in cryptos:
            price_data = cryptocompare.get_price(crypto, 'USD')
            if price_data and crypto in price_data:
                prices[crypto] = price_data[crypto]['USD']
        return prices
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return None

def create_news_tweet():
    news = get_crypto_news()
    if news:
        title = news['title']
        url = news['url']
        tweet = f" {title}\n\nRead more: {url}\n\n#Crypto #Blockchain #News"
        return tweet[:280]
    return None

def create_market_tweet():
    prices = get_crypto_prices()
    if prices:
        tweet = " Current Crypto Prices:\n\n"
        for crypto, price in prices.items():
            tweet += f"{crypto}: ${price:,.2f}\n"
        tweet += "\n#Crypto #Trading #Markets"
        return tweet[:280]
    return None

def send_tweet():
    try:
        current_hour = datetime.now().hour
        # Use more market updates during trading hours, more news during off-hours
        if 6 <= current_hour <= 20:  # During active trading
            tweet_functions = [create_market_tweet, create_market_tweet, create_news_tweet]  # 2:1 ratio for market updates
        else:
            tweet_functions = [create_market_tweet, create_news_tweet, create_news_tweet]  # 2:1 ratio for news
        
        tweet_content = random.choice(tweet_functions)()
        
        if tweet_content:
            success = post_tweet(tweet_content)
            if success:
                print(f"Tweet posted successfully at {datetime.now()}")
                return True
            else:
                print("Failed to post tweet")
                return False
        else:
            print("Failed to generate tweet content")
            return False
    except Exception as e:
        print(f"Error posting tweet: {e}")
        return False

def main():
    print(f"Bot starting daily posts at {datetime.now()}")
    
    # Post intervals (in seconds)
    intervals = [
        7200,   # 2 hours between posts
        7200,   # 2 hours
        7200,   # 2 hours
        7200,   # 2 hours
        7200,   # 2 hours
        7200,   # 2 hours
        7200,   # 2 hours
        7200,   # 2 hours
        7200    # 2 hours
    ]
    
    # Make first post immediately
    send_tweet()
    
    # Make remaining posts with delays
    for interval in intervals:
        time.sleep(interval)  # Wait for the specified interval
        send_tweet()
        
    print(f"Daily posting complete at {datetime.now()}")

if __name__ == "__main__":
    main()
