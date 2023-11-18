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
    os.environ['HELGA_ID'], 
    os.environ['RASMUS_ID']
]
bot = Bot(token=bot_token)


def handle_all(update: Update, context):  
    userid = update.message.from_user.id
    if str(userid) not in admins: 
        bot.send_message(text="ERROR: Invalid user", chat_id=userid)
        return

    if update.message.audio:
        path=download_file(bot.get_file(update.message.audio.file_id))
        print(f"\npath: {path}")
        resp1=translation(path)
        print(f"\nresp1: {resp1}")
        resp2=transcription(path)
        print(f"\nresp2: {resp2}")

        bot.send_message(text=f"Translation 1:\n\n{resp1}", chat_id=userid, parse_mode="Markdown")
        
        bot.send_message(text=f"Translation 2:\n\n{resp2}", chat_id=userid, parse_mode="Markdown")
    
    elif update.message.voice.file_id:
        path=download_file(bot.get_file(update.message.voice.file_id))
        resp1=transcription(path)
        resp2=translation(path)

    else:
        bot.send_message(text="Please send audio", chat_id=userid)


# def handle_audio(update: Update, context):
#     userid = update.message.from_user.id
#     if str(userid) not in admins: 
#         return
    
#     file = bot.get_file(update.message.audio.file_id)
    
#     file_path = download_file(file)
#     text = transcribe(file_path)
#     resp = translate(text)
    
#     bot.send_message(text=resp, chat_id=userid, parse_mode="Markdown")


# def handle_voice(update: Update, context):
#     userid = update.message.from_user.id
#     if str(userid) not in admins: 
#         return

#     file = bot.get_file(update.message.voice.file_id)
    
#     file_path = download_file(file)
#     text = transcribe(file_path)
#     resp = translate(text)

#     bot.send_message(text=resp, chat_id=userid, parse_mode="Markdown")


def main():
    # Create an instance of the Updater class using the bot token
    updater = Updater(token=bot_token, use_context=True)
    dp = updater.dispatcher

    # # Create handler to capture audio messages
    # dp.add_handler(MessageHandler(Filters.audio, handle_audio))

    # # Create handler to capture audio messages
    # dp.add_handler(MessageHandler(Filters.voice, handle_voice))

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
