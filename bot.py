import os
import logging
import base64
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Configurar el logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtener tokens de entorno
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
    else:
        update.message.reply_text('Please send a file.')

def upload_to_github(file_name, file_path):
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{file_name}"
    with open(file_path, "rb") as file:
        content = file.read()
    content_encoded = base64.b64encode(content).decode()
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
    # Crear el Updater y pasar el token del bot
    updater = Updater(TOKEN)

    # Obtener el dispatcher para registrar los handlers
    dispatcher = updater.dispatcher

    # Añadir handlers para diferentes comandos y mensajes
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_file))

    # Iniciar el bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
