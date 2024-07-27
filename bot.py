import os
import logging
import base64
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env
load_dotenv()

# Configurar el logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtener tokens de entorno
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")
BRANCH_NAME = "gh-pages"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.document)
async def handle_file(client: Client, message: Message):
    file = message.document
    if file:
        # Descargar el archivo
        file_path = await message.download()
        file_name = os.path.basename(file_path)
        
        # Subir el archivo a GitHub
        upload_to_github(file_name, file_path)
        
        # Construir el URL de descarga
        download_url = f"https://{REPO_NAME.split('/')[0]}.github.io/{REPO_NAME.split('/')[1]}/{file_name}"
        await message.reply_text(f'File received and uploaded. You can download it from {download_url}')

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

app.run()  # Mantener el bot ejecutándose
