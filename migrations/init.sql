CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    referral_count INTEGER DEFAULT 0,
    invited_by INTEGER DEFAULT 0
);

CREATE TABLE referrals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    referrer_id INTEGER,
    referred_id INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
