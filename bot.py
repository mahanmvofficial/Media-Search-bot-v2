import logging
import threading
from flask import Flask
from pyrogram import Client
import os

# Logging setup
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

# Flask server for health checks
app = Flask(name)

@app.route('/')
def health_check():
    return "Healthy", 200

def run_flask():
    app.run(host="0.0.0.0", port=8000)

# Pyrogram bot
class Bot(Client):
    def init(self, session_name, api_id, api_hash, bot_token):
        super().init(
            session_name,
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token,
            workers=4,
            plugins=dict(root="plugins"),
            sleep_threshold=10
        )

    async def start(self):
        await super().start()
        print("Bot started")
        logging.info("Bot started successfully.")
        # Add any other startup tasks here

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped")
        logging.info("Bot stopped.")

# Bot initialization and run
if name == "main":
    # Flask runs in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Load API credentials from environment variables
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")
    bot_token = os.getenv("BOT_TOKEN")

    if not api_id or not api_hash or not bot_token:
        raise ValueError("API_ID, API_HASH, and BOT_TOKEN environment variables must be set!")

    bot = Bot("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

    try:
        bot.run()
    except Exception as e:
        logging.error(f"Error running bot: {e}")
        bot.stop()
