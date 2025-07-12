import yfinance as yf
import matplotlib.pyplot as plt
import requests
import os
import logging
from datetime import datetime, timedelta
import pandas as pd

logger = logging.getLogger(__name__)

async def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol + ".NS")
        data = stock.history(period="1d")
        
        # Get historical data for moving averages
        hist_data = stock.history(period="200d")
        
        if data.empty:
            return None
            
        # Calculate moving averages
        ma50 = hist_data['Close'].rolling(window=50).mean().iloc[-1]
        ma200 = hist_data['Close'].rolling(window=200).mean().iloc[-1]
        
        return {
            'symbol': symbol,
            'current': data['Close'].iloc[-1],
            'change': data['Close'].iloc[-1] - data['Open'].iloc[-1],
            'change_pct': ((data['Close'].iloc[-1] - data['Open'].iloc[-1]) / data['Open'].iloc[-1]) * 100,
            'ma50': ma50,
            'ma200': ma200,
            'currency': '₹'
        }
    except Exception as e:
        logger.error(f"Error fetching stock data: {e}")
        return None

async def generate_stock_chart(symbol):
    try:
        stock = yf.Ticker(symbol + ".NS")
        data = stock.history(period="3mo")
        
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data['Close'], label='Price', color='blue')
        
        # Add moving averages
        plt.plot(data.index, data['Close'].rolling(window=50).mean(), label='50DMA', color='orange')
        plt.plot(data.index, data['Close'].rolling(window=200).mean(), label='200DMA', color='red')
        
        plt.title(f'{symbol} Price Trend')
        plt.xlabel('Date')
        plt.ylabel('Price (₹)')
        plt.grid(True)
        plt.legend()
        
        chart_path = f"{symbol}_chart.png"
        plt.savefig(chart_path)
        plt.close()
        return chart_path
    except Exception as e:
        logger.error(f"Error generating chart: {e}")
        return None

async def get_stock_news(symbol):
    try:
        NEWS_API_KEY = os.getenv('NEWS_API_KEY')
        if not NEWS_API_KEY:
            logger.error("NEWS_API_KEY not set")
            return []
            
        url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}&pageSize=5"
        response = requests.get(url)
        
        if response.status_code != 200:
            return []
        
        articles = response.json().get('articles', [])
        return [{
            'title': a['title'],
            'url': a['url'],
            'source': a['source']['name'],
            'date': a['publishedAt'][:10]
        } for a in articles]
    except Exception as e:
        logger.error(f"Error fetching stock news: {e}")
        return []

async def get_market_news():
    try:
        NEWS_API_KEY = os.getenv('NEWS_API_KEY')
        if not NEWS_API_KEY:
            logger.error("NEWS_API_KEY not set")
            return []
            
        url = f"https://newsapi.org/v2/top-headlines?category=business&country=in&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        
        if response.status_code != 200:
            return []
        
        articles = response.json().get('articles', [])
        return [{
            'title': a['title'],
            'url': a['url'],
            'source': a['source']['name'],
            'date': a['publishedAt'][:10]
        } for a in articles]
    except Exception as e:
        logger.error(f"Error fetching market news: {e}")
        return []

def cleanup_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.error(f"Error cleaning up file: {e}")
