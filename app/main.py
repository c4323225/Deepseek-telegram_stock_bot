import logging
import asyncio
from dotenv import load_dotenv
from telegram.ext import Application
from app.bot.handlers import setup_handlers
import os

load_dotenv()

async def main():
    application = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    setup_handlers(application)
    await application.run_polling()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
