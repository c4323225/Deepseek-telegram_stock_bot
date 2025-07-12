import sqlite3
import os
import logging

logger = logging.getLogger(__name__)

def init_db():
    try:
        DATABASE_NAME = os.getenv("DATABASE_NAME", "stockbot.db")
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            referral_count INTEGER DEFAULT 0,
            invited_by INTEGER DEFAULT 0
        )''')
        
        # Create referrals table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS referrals (
            referrer_id INTEGER,
            referred_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Create portfolio table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolio (
            user_id INTEGER,
            symbol TEXT,
            quantity REAL,
            buy_price REAL,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

def get_db_connection():
    DATABASE_NAME = os.getenv("DATABASE_NAME", "stockbot.db")
    return sqlite3.connect(DATABASE_NAME)

# Initialize database on import
init_db()
