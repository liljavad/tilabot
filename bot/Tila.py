import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Configure basic logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Handler for /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user is not None:
        user_id = user.id
        await update.message.reply_text(f"آیدی کاربری شما: {user_id}")
    else:
        await update.message.reply_text("نمی‌توان آیدی کاربری شما را تشخیص داد.")

def main():
    # Replace with your actual bot token
    token = "YOUR_BOT_TOKEN"

    app = ApplicationBuilder().token(token).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()