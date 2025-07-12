from telegram import Update
from telegram.ext import ContextTypes
from app.services import referral_service, stock_service
from app.bot import keyboards
import logging

logger = logging.getLogger(__name__)

async def analyze_stock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper() if context.args else None
        if not symbol:
            await update.message.reply_text("Please specify a stock symbol. Example: /stock RELIANCE")
            return
        
        user_id = update.effective_user.id
        if not referral_service.can_access_premium(user_id):
            await update.message.reply_text(
                "❌ Premium feature! You need to invite more friends to access stock analysis. "
                "Use /start to check your referral status."
            )
            return
        
        # Get stock data
        stock_data = await stock_service.get_stock_data(symbol)
        chart_path = await stock_service.generate_stock_chart(symbol)
        
        # Send response
        message = (
            f"📈 *{symbol} Stock Analysis*\n\n"
            f"💰 Current Price: *₹{stock_data['current']:.2f}*\n"
            f"📉 Daily Change: `{stock_data['change']:+.2f}` "
            f"({stock_data['change_pct']:+.2f}%)\n"
            f"📊 50-Day MA: ₹{stock_data['ma50']:.2f}\n"
            f"📈 200-Day MA: ₹{stock_data['ma200']:.2f}"
        )
        
        with open(chart_path, 'rb') as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=message,
                parse_mode='Markdown',
                reply_markup=keyboards.stock_analysis_keyboard(symbol)
            )
        
        # Cleanup
        stock_service.cleanup_file(chart_path)
        
    except Exception as e:
        logger.error(f"Stock command error: {e}")
        await update.message.reply_text("❌ Failed to analyze stock. Please try again later.")
