import os
import logging

logger = logging.getLogger(__name__)

def format_referral_link(bot_username, user_id):
    return f"https://t.me/{bot_username}?start=ref_{user_id}"

def format_currency(value):
    return f"₹{value:,.2f}"

def format_percentage(value):
    return f"{value:+.2f}%"

def cleanup_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.error(f"Error cleaning up file: {e}")

def validate_stock_symbol(symbol):
    # Simple validation - could be extended with NSE symbol list
    return symbol.isalpha() and len(symbol) >= 2 and len(symbol) <= 10
