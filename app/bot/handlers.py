from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    InlineQueryHandler
)
from app.bot.commands import start, show_main_menu

def setup_handlers(application):
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    # ... other handlers
