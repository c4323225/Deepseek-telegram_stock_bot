import yfinance as yf
import matplotlib.pyplot as plt
import os
import logging

logger = logging.getLogger(__name__)

async def get_stock_data(symbol):
    """Fetch stock data from Yahoo Finance"""
    try:
        stock = yf.Ticker(symbol + ".NS")
        data = stock.history(period="1d")
        
        if data.empty:
            return None
            
        # Get previous close from yesterday
        prev_close = stock.info.get('previousClose')
        current = data['Close'].iloc[-1]
        change = current - prev_close
        change_pct = (change / prev_close) * 100
        
        return {
            'current': current,
            'change': change,
            'change_pct': change_pct,
            'currency': '₹'
        }
    except Exception as e:
        logger.error(f"Error fetching stock data: {e}")
        return None

async def generate_stock_chart(symbol):
    """Generate stock price chart for 3 months"""
    try:
        stock = yf.Ticker(symbol + ".NS")
        data = stock.history(period="3mo")
        
        if data.empty:
            return None
            
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data['Close'], label='Price', color='blue')
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
