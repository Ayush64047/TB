import os
import requests
import mimetypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

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
    

# Initializes the Telegram bot with the provided API token
updater = Updater("YOUR_API_TOKEN_HERE", use_context=True)

# Defines the start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me a Terabox download link and I'll download it for you!")

# Defines the message handler for downloading the Terabox file
def download_file(update: Update, context: CallbackContext) -> None:
    # Saves the Terabox download link to the user's context
    context.user_data['link'] = update.message.text
    # Creates a keyboard for selecting the download quality
    keyboard = [
        [InlineKeyboardButton("Original", callback_data="original")],
        [InlineKeyboardButton("720p", callback_data="720p"), InlineKeyboardButton("480p", callback_data="480p")],
        [InlineKeyboardButton("360p", callback_data="360p"), InlineKeyboardButton("240p", callback_data="240p")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Sends the keyboard to the user and waits for their input
    update.message.reply_text("Select a download quality:", reply_markup=reply_markup)

# Defines the callback query handler for the download quality buttons
updater.dispatcher.add_handler(CallbackQueryHandler(download_quality))

# Defines the start and message handlers
updater.dispatcher.add_handler(CommandHandler("start", start))
updater
