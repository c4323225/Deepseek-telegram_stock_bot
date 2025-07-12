import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import yfinance as yf
import os
import logging

logger = logging.getLogger(__name__)

def generate_candlestick_chart(symbol, period="1mo"):
    try:
        stock = yf.Ticker(symbol + ".NS")
        data = stock.history(period=period)
        
        if data.empty:
            return None
            
        # Create candlestick chart
        mpf.plot(data, type='candle', style='charles', 
                 title=f"{symbol} Price", ylabel="Price (₹)",
                 savefig=f"{symbol}_candle.png")
        
        return f"{symbol}_candle.png"
    except Exception as e:
        logger.error(f"Error generating candlestick chart: {e}")
        return None

def generate_technical_chart(symbol, period="3mo"):
    try:
        stock = yf.Ticker(symbol + ".NS")
        data = stock.history(period=period)
        
        if data.empty:
            return None
            
        plt.figure(figsize=(12, 8))
        
        # Price
        plt.subplot(2, 1, 1)
        plt.plot(data.index, data['Close'], label='Price', color='blue')
        plt.plot(data.index, data['Close'].rolling(window=50).mean(), label='50DMA', color='orange')
        plt.plot(data.index, data['Close'].rolling(window=200).mean(), label='200DMA', color='red')
        plt.title(f'{symbol} Technical Analysis')
        plt.ylabel('Price (₹)')
        plt.legend()
        plt.grid(True)
        
        # Volume
        plt.subplot(2, 1, 2)
        plt.bar(data.index, data['Volume'], color='green', alpha=0.3)
        plt.ylabel('Volume')
        plt.grid(True)
        
        chart_path = f"{symbol}_technical.png"
        plt.savefig(chart_path)
        plt.close()
        return chart_path
    except Exception as e:
        logger.error(f"Error generating technical chart: {e}")
        return None
