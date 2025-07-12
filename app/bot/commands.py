from telegram import Update
from telegram.ext import ContextTypes
from app.services.referral import add_user, get_referral_count
from app.services.stock_service import get_stock_data, generate_stock_chart
from app.services.news_service import get_stock_news
from app.bot.keyboards import main_menu_keyboard, referral_progress_keyboard
from app.utils.helpers import format_referral_link
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    
    invited_by = None
    if args and args[0].startswith('ref_'):
        try:
            invited_by = int(args[0].split('_')[1])
        except (IndexError, ValueError):
            pass
    
    add_user(user.id, user.username, invited_by)
    referral_count = get_referral_count(user.id)
    REFERRAL_REQUIREMENT = 10  # Could be from env
    
    if referral_count >= REFERRAL_REQUIREMENT:
        await show_main_menu(update, "🌟 Premium Access Activated! Choose an option:")
        return
    
    bot_username = (await context.bot.get_me()).username
    referral_link = format_referral_link(bot_username, user.id)
    message = (
        f"👋 Welcome {user.first_name}!\n\n"
        "📊 To access premium stock analysis features, "
        f"you need to invite {REFERRAL_REQUIREMENT} friends.\n\n"
        f"✅ You've invited: {referral_count}/{REFERRAL_REQUIREMENT} friends\n\n"
        f"🔗 Your referral link:\n`{referral_link}`\n\n"
        "Share this link with friends to unlock features!"
    )
    
    await update.message.reply_text(
        message, 
        reply_markup=referral_progress_keyboard(bot_username, user.id),
        parse_mode='Markdown'
    )

async def show_main_menu(update, context, text="📈 Stock Analysis Bot:"):
    await update.message.reply_text(
        text,
        reply_markup=main_menu_keyboard()
    )
