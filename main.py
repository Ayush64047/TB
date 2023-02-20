import os
import requests
import mimetypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

# Handles the download quality button presses
def download_quality(update: Update, context: CallbackContext) -> None:
    # Extracts the callback data (i.e. the download quality) from the button press
    query = update.callback_query
    quality = query.data
    # Retrieves the Terabox link from the user's context
    link = context.user_data['link']
    # Downloads the file from Terabox in the selected quality
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"}
    if quality == "original":
        response = requests.get(link, headers=headers)
        file_name = os.path.basename(link)
    else:
        response = requests.get(f"{link}?q={quality}", headers=headers)
        file_name = f"{quality}p_{os.path.basename(link)}"
    # Sends the file to the user
    query.edit_message_text("Downloading file...")
    # Set the appropriate content type based on the file type
    content_type, encoding = mimetypes.guess_type(file_name)
    if content_type and "video" in content_type:
        query.bot.send_video(chat_id=query.message.chat_id, video=response.content, filename=file_name)
    elif content_type and "image" in content_type:
        query.bot.send_photo(chat_id=query.message.chat_id, photo=response.content, filename=file_name)
    elif content_type and "application" in content_type:
        query.bot.send_document(chat_id=query.message.chat_id, document=response.content, filename=file_name)
    else:
        query.bot.send_document(chat_id=query.message.chat_id, document=response.content, filename=file_name)
    # Clears the user's context
    context.user_data.clear()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the Terabox downloader bot! Send me a link and I will download it for you.')

def handle_link(update: Update, context: CallbackContext) -> None:
    # Save the link in the user's context for later use
    context.user_data['link'] = update.message.text
    # Create the download quality button options
    buttons = [
        [InlineKeyboardButton("Original", callback_data="original")],
        [InlineKeyboardButton("480p", callback_data="480"), InlineKeyboardButton("720p", callback_data="720"), InlineKeyboardButton("1080p", callback_data="1080")],
    ]
    # Sends the download quality options to the user
    update.message.reply_text("Choose a download quality:", reply_markup=InlineKeyboardMarkup(buttons))

def main() -> None:
    # Create the Updater and pass it the bot's token
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Add message handler for handling links
    dispatcher.add_handler(MessageHandler(Filters.regex(r'^https?://'), handle_link))

    # Add callback query handler for handling download quality button presses
    dispatcher.add_handler(CallbackQueryHandler(download_quality))

    # Start the bot
    updater.start_polling()
    updater.idle()

