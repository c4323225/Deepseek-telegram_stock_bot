import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram.ext import Application
from app.bot.handlers import setup_handlers
from app.utils.database import init_db

# Load environment variables
load_dotenv()

# Initialize database
init_db()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    try:
        # Create Telegram application
        application = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
        
        # Setup handlers
        setup_handlers(application)
        
        # Start polling
        logger.info("Starting bot polling...")
        await application.run_polling()
        
    except Exception as e:
        logger.error(f"Application failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
