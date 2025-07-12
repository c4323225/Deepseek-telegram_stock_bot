import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
    InlineQueryHandler
)
from app.services import stock_service, referral_service
from app.utils import helpers, database
from app.bot import keyboards

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    invited_by = int(args[0].split('_')[1]) if args and args[0].startswith('ref_') else 0
    
    referral_service.add_user(user.id, user.username, invited_by)
    referral_count = referral_service.get_referral_count(user.id)
    
    if referral_service.can_access_premium(user.id):
        await keyboards.show_main_menu(update, "🌟 Premium Access Activated! Choose an option:")
        return
    
    bot_username = (await context.bot.get_me()).username
    referral_link = helpers.format_referral_link(bot_username, user.id)
    message = (
        f"👋 Welcome {user.first_name}!\n\n"
        "📊 To access premium stock analysis features, "
        f"you need to invite {referral_service.REFERRAL_REQUIREMENT} friends.\n\n"
        f"✅ You've invited: {referral_count}/{referral_service.REFERRAL_REQUIREMENT} friends\n\n"
        f"🔗 Your referral link:\n`{referral_link}`\n\n"
        "Share this link with friends to unlock features!"
    )
    
    await update.message.reply_text(
        message, 
        reply_markup=keyboards.referral_progress_keyboard(bot_username, user.id),
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if query.data == 'check_ref':
        referral_count = referral_service.get_referral_count(user_id)
        bot_username = (await context.bot.get_me()).username
        referral_link = helpers.format_referral_link(bot_username, user_id)
        
        if referral_service.can_access_premium(user_id):
            await keyboards.show_main_menu(query, "🎉 You now have premium access!")
        else:
            message = (
                f"📊 Referral Progress: {referral_count}/{referral_service.REFERRAL_REQUIREMENT}\n\n"
                f"🔗 Your referral link:\n`{referral_link}`"
            )
            await query.edit_message_text(
                text=message,
                reply_markup=keyboards.referral_progress_keyboard(bot_username, user_id),
                parse_mode='Markdown'
            )
    
    elif query.data == 'main_menu':
        await keyboards.show_main_menu(query)
    
    elif query.data.startswith('stock_'):
        symbol = query.data.split('_')[1]
        await analyze_stock(update, context, symbol)
    
    elif query.data == 'market_news':
        await get_market_news(update, context)

async def analyze_stock(update: Update, context: ContextTypes.DEFAULT_TYPE, symbol):
    query = update.callback_query
    user_id = query.from_user.id
    
    if not referral_service.can_access_premium(user_id):
        await query.answer("❌ Premium feature! Invite friends to access", show_alert=True)
        return
    
    await query.answer(f"🔍 Analyzing {symbol}...")
    
    # Get all data
    stock_data = await stock_service.get_stock_data(symbol)
    chart_path = await stock_service.generate_stock_chart(symbol)
    news = await stock_service.get_stock_news(symbol)
    
    # Prepare report
    report = (
        f"📈 *{symbol} Stock Report*\n\n"
        f"💰 Current Price: *₹{stock_data['current']:.2f}*\n"
        f"📉 Daily Change: `{stock_data['change']:+.2f}` "
        f"({stock_data['change_pct']:+.2f}%)\n\n"
        "📰 *Top News Headlines:*\n"
    )
    
    for i, article in enumerate(news[:3], 1):
        report += f"{i}. [{article['title']}]({article['url']})\n"
    
    # Send report with chart
    with open(chart_path, 'rb') as chart_file:
        media = InputMediaPhoto(
            media=chart_file,
            caption=report,
            parse_mode='Markdown'
        )
        await context.bot.send_media_group(
            chat_id=query.message.chat_id,
            media=[media]
        )
    
    # Clean up chart file
    helpers.cleanup_file(chart_path)

async def handle_inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.upper()
    if not query:
        return
    
    try:
        stock_data = await stock_service.get_stock_data(query)
        if not stock_data:
            return
            
        message = (
            f"📈 {query}:\n"
            f"💰 Price: ₹{stock_data['current']:.2f}\n"
            f"📊 Change: {stock_data['change']:+.2f} ({stock_data['change_pct']:+.2f}%)"
        )
        
        results = [{
            "type": "article",
            "id": query,
            "title": f"{query} Stock",
            "description": f"₹{stock_data['current']:.2f} | {stock_data['change_pct']:+.2f}%",
            "input_message_content": {
                "message_text": "Select option for full analysis:",
                "parse_mode": "Markdown"
            },
            "reply_markup": {
                "inline_keyboard": [[
                    {
                        "text": "📊 Full Analysis",
                        "callback_data": f"stock_{query}"
                    }
                ]]
            }
        }]
        
        await update.inline_query.answer(results, cache_time=60)
    except Exception as e:
        logger.error(f"Inline query error: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🌟 *Stock Analysis Bot Help* 🌟\n\n"
        "🔍 *How to use:*\n"
        "1. Invite friends to unlock premium features\n"
        "2. Search stocks with /stock command\n"
        "3. Get detailed analysis with charts\n\n"
        "📋 *Commands:*\n"
        "/start - Check referral status\n"
        "/stock [SYMBOL] - Analyze stock\n"
        "/news - Latest market news\n"
        "/help - Show this message\n\n"
        "💎 *Premium Features:*\n"
        "- Detailed technical analysis\n"
        "- Advanced chart patterns\n"
        "- Sentiment analysis\n"
        "- News aggregation"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def get_market_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    news = await stock_service.get_market_news()
    response = "📰 *Latest Market News:*\n\n"
    
    for i, item in enumerate(news[:5], 1):
        response += f"{i}. [{item['title']}]({item['url']}) - {item['source']}\n"
    
    await query.edit_message_text(
        text=response,
        parse_mode='Markdown',
        reply_markup=keyboards.back_to_main_keyboard()
    )

def setup_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, keyboards.show_main_menu))
    application.add_handler(InlineQueryHandler(handle_inline_query))
