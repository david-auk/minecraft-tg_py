from app.telegram.bot import bot
import app.telegram.handlers  # Import handlers to register them
from app.telegram.logger import logger

if __name__ == "__main__":
#    try:
        logger.info("Bot is starting...")
        bot.polling(none_stop=True)
#    except Exception as e:
#        logger.error(f"Bot crashed due to error: {e}")