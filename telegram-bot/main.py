import os
import logging
import requests
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define your token
TOKEN = os.getenv("TELEGRAM_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")
BRANCH_NAME = "gh-pages"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Send me a file and I will process it.')

def handle_file(update: Update, context: CallbackContext) -> None:
    file = update.message.document
    if file:
        file_path = file.get_file().download()
        file_name = os.path.basename(file_path)
        upload_to_github(file_name, file_path)
        download_url = f"https://{REPO_NAME.split('/')[0]}.github.io/{REPO_NAME.split('/')[1]}/{file_name}"
        update.message.reply_text(f'File received and uploaded. You can download it from {download_url}')

def upload_to_github(file_name, file_path):
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{file_name}"
    with open(file_path, "rb") as file:
        content = file.read()
    content_encoded = content.encode("base64")
    data = {
        "message": f"Add {file_name}",
        "content": content_encoded,
        "branch": BRANCH_NAME,
    }
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.put(url, json=data, headers=headers)
    response.raise_for_status()

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.document, handle_file))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
