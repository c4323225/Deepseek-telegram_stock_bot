import requests
import os
import logging

logger = logging.getLogger(__name__)
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

async def get_stock_news(symbol):
    """Fetch news from NewsAPI"""
    if not NEWS_API_KEY:
        logger.error("NEWS_API_KEY not set")
        return []
        
    url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}&pageSize=5"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"News API error: {response.status_code}")
            return []
        
        articles = response.json().get('articles', [])
        return [{
            'title': a['title'],
            'url': a['url'],
            'source': a['source']['name'],
            'date': a['publishedAt'][:10]
        } for a in articles]
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return []
