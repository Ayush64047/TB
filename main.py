import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

# Handles the "/start" command
def start(update: Update, context: CallbackContext) -> None:
    # Sends a welcome message to the user
    update.message.reply_text("Welcome to the Terabox Link Download Bot! Please send me a Terabox link to get started.")

# Handles messages containing Terabox links
def terabox_link(update: Update, context: CallbackContext) -> None:
    # Extracts the Terabox link from the message text
    link = update.message.text
    # Sends a message to the user with the download quality options
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("480p", callback_data="480p"), InlineKeyboardButton("720p", callback_data="720p"), InlineKeyboardButton("1080p", callback_data="1080p")],
        [InlineKeyboardButton("Original File", callback_data="original")]
    ])
    update.message.reply_text("Please select the download quality:", reply_markup=reply_markup)
    # Stores the Terabox link in the user's context for later use
    context.user_data['link'] = link

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
    query.bot.send_document(chat_id=query.message.chat_id, document=response.content, filename=file_name)
    # Clears the user's context
    context.user_data.clear()

# Define the Telegram bot token
TOKEN = "5647123835:AAHN6PUFsVpCFkxYuSdHlX4iW_Wc8Nuo7IU"

# Creates the bot and adds the necessary handlers
updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'https?://[^\s]+'), terabox_link))
updater.dispatcher.add_handler(CallbackQueryHandler(download_quality))

# Starts the bot
updater.start_polling()
updater.idle()
