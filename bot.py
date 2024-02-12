import os
import threading
from telegram import Bot, Update # type: ignore
from telegram.ext import Filters, MessageHandler, Updater # type: ignore 
from keep_alive import keep_alive, keep_alive_ping
from utils import download_file, transcription, translation

keep_alive_ping()

# Define the Telegram bot token & user id from the environment variable
bot_token = os.environ['BOT_TOKEN']
admins = [
    os.environ['HELGA_ID']
]
bot = Bot(token=bot_token)


def handle_all(update: Update, context):  
    userid = update.message.from_user.id
    if str(userid) not in admins: 
        bot.send_message(text="ERROR: Invalid user", chat_id=userid)
        return

    if update.message.audio:
        path=download_file(bot.get_file(update.message.audio.file_id))
        resp1=transcription(path)
        resp2=translation(path)

        bot.send_message(text=f"Translation 1:\n\n{resp1}", chat_id=userid, parse_mode="Markdown")
    
        bot.send_message(text=f"Translation 2:\n\n{resp2}", chat_id=userid, parse_mode="Markdown")
    
    elif update.message.voice.file_id:
        path=download_file(bot.get_file(update.message.voice.file_id))
        resp1=transcription(path)
        resp2=translation(path)

        bot.send_message(text=f"Translation 1:\n\n{resp1}", chat_id=userid, parse_mode="Markdown")

        bot.send_message(text=f"Translation 2:\n\n{resp2}", chat_id=userid, parse_mode="Markdown")

    else:
        bot.send_message(text="Please send audio", chat_id=userid)


def main():
    # Create an instance of the Updater class using the bot token
    updater = Updater(token=bot_token, use_context=True)
    dp = updater.dispatcher
    
    # Create handler for text messages
    dp.add_handler(MessageHandler(Filters.all, handle_all))
        
    # Start the bot
    updater.start_polling()
    
    keep_alive_thread = threading.Thread(target=keep_alive)
    keep_alive_thread.daemon = True
    keep_alive_thread.start()

    updater.idle()
    updater.stop()

if __name__ == '__main__':
    main()
