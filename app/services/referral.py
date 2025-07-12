import os
import sqlite3
import logging

logger = logging.getLogger(__name__)

REFERRAL_REQUIREMENT = 10
DATABASE_NAME = os.getenv("DATABASE_NAME", "stockbot.db")

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        referral_count INTEGER DEFAULT 0,
        invited_by INTEGER DEFAULT 0
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS referrals (
        referrer_id INTEGER,
        referred_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

def add_user(user_id, username, invited_by=0):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username) 
        VALUES (?, ?)
        ''', (user_id, username))
        
        if invited_by:
            cursor.execute('''
            INSERT INTO referrals (referrer_id, referred_id)
            VALUES (?, ?)
            ''', (invited_by, user_id))
            
            cursor.execute('''
            UPDATE users SET referral_count = referral_count + 1 
            WHERE user_id = ?
            ''', (invited_by,))
            
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
    finally:
        conn.close()

def get_referral_count(user_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
        SELECT referral_count FROM users WHERE user_id = ?
        ''', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else 0
    finally:
        conn.close()

def can_access_premium(user_id):
    return get_referral_count(user_id) >= REFERRAL_REQUIREMENT

# Initialize database on import
init_db()
