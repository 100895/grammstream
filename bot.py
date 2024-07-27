import os
from pyrogram import Client, filters
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Inicializar el cliente de Pyrogram
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.document)
async def handle_file(client, message):
    # Manejar el archivo recibido y enviar un enlace de descarga
    file_id = message.document.file_id
    file_info = await client.get_media(file_id)
    download_url = f"https://github.com/your-repo/your-file-{file_id}.pdf"  # Reemplaza con tu URL
    await message.reply_text(f"Archivo recibido. Puedes descargarlo desde: {download_url}")

@app.on_message(filters.text)
async def handle_text(client, message):
    await message.reply_text("Mensaje recibido!")

# Ejecutar el bot
app.run()  # Mantener el bot ejecutándose
