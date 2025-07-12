import logging
import asyncio
from dotenv import load_dotenv
from bot.handlers import setup_handlers
from telegram.ext import Application

load_dotenv()

async def main():
    app = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    await setup_handlers(app)
    await app.run_polling()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
