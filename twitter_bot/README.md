# Blockchain Website Twitter Bot

Automated Twitter bot for posting cryptocurrency news and market updates.

## Features
- Posts 9 times daily
- Alternates between market updates and news
- Covers major cryptocurrencies
- Includes relevant hashtags

## Setup
1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
CRYPTO_COMPARE_API_KEY=your_cryptocompare_api_key
```

3. Run the bot:
```bash
python twitter_bot.py
```
