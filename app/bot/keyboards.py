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

def back_to_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("⬅️ Back to Main", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def stock_analysis_keyboard(symbol):
    keyboard = [
        [
            InlineKeyboardButton("📈 Technicals", callback_data=f'tech_{symbol}'),
            InlineKeyboardButton("📰 News", callback_data=f'news_{symbol}')
        ],
        [InlineKeyboardButton("📊 Fundamentals", callback_data=f'fund_{symbol}')],
        [InlineKeyboardButton("⬅️ Main Menu", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def show_main_menu(update, text="📈 Stock Analysis Bot:"):
    if hasattr(update, 'message'):
        await update.message.reply_text(text, reply_markup=main_menu_keyboard())
    else:  # CallbackQuery
        await update.edit_message_text(text, reply_markup=main_menu_keyboard())
