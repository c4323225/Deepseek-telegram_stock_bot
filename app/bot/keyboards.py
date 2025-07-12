from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔍 Analyze Stock", switch_inline_query_current_chat="")],
        [InlineKeyboardButton("📰 Market News", callback_data='market_news')],
        [InlineKeyboardButton("🏆 Top Gainers", callback_data='top_gainers')],
        [InlineKeyboardButton("📊 My Portfolio", callback_data='portfolio')],
        [InlineKeyboardButton("❓ Help", callback_data='help')]
    ]
    return InlineKeyboardMarkup(keyboard)

def referral_progress_keyboard(bot_username, user_id):
    referral_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    keyboard = [
        [InlineKeyboardButton("⬅️ Back to Main", callback_data='main_menu')],
        [InlineKeyboardButton("📤 Share Link", switch_inline_query=f"Join for stock insights! {referral_link}")]
    ]
    return InlineKeyboardMarkup(keyboard)
