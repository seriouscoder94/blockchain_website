# Reddit Crypto News Bot

This bot automatically posts daily cryptocurrency news updates to specified subreddits. It fetches news from CryptoPanic and creates well-formatted posts on Reddit.

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Reddit API Setup**
   - Go to https://www.reddit.com/prefs/apps
   - Click "Create App" or "Create Another App"
   - Select "script"
   - Fill in the name and description
   - Set the redirect uri to http://localhost:8080
   - Note down the client ID and client secret

3. **CryptoPanic API Setup**
   - Go to https://cryptopanic.com/
   - Create an account
   - Get your API key from the dashboard

4. **Configuration**
   - Copy `.env.example` to `.env`
   - Fill in your Reddit and CryptoPanic credentials
   - Modify the subreddit list in `reddit_bot.py` if needed

5. **Running the Bot**
   ```bash
   python reddit_bot.py
   ```

The bot will run continuously and post news daily at 9:00 AM.

## Features
- Fetches top crypto news from CryptoPanic
- Posts to multiple subreddits
- Includes source attribution and links
- Runs on a daily schedule
- Includes error handling and rate limiting

## Customization
- Edit the posting schedule in `reddit_bot.py`
- Modify the post format in the `create_reddit_post` function
- Add or remove target subreddits in the `daily_task` function

## Note
Make sure to follow Reddit's API terms of service and the rules of each subreddit you post to.
