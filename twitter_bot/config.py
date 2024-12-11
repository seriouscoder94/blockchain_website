import os
from dotenv import load_dotenv

load_dotenv()

# Twitter API Credentials
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# News API Key
CRYPTO_COMPARE_API_KEY = os.getenv('CRYPTO_COMPARE_API_KEY')

# Posting Schedule (in 24-hour format)
POST_TIMES = ['09:00', '12:00', '15:00', '18:00', '21:00']

# Top cryptocurrencies to track
TOP_CRYPTOS = ['BTC', 'ETH', 'BNB', 'XRP', 'SOL', 'ADA', 'DOGE']
