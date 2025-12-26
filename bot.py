import logging
import random
import string
import threading
from flask import Flask
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ChatAction

TOKEN = "8439992263:AAFvOBpxzYy9eqk_P6Q63qASxiDFB30lIFc"

files_db = {}
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def generate_key(length=6):
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))

def start(update, context):
    update.message.reply_text(
        "Send me a file → मैं key दूँगा\n"
        "Key लिखो → वही file मिल जाएगी\n\n"
        "Example: ABC123"
    )

def handle_file(update, context):
    doc = update.message.document
    photo = update.message.photo

    if doc:
        file_id = doc.file_id
    elif photo:
        file_id = photo[-1].file_id
    else:
        update.message.reply_text("Please send a document or image.")
        return

    key = generate_key()
    files_db[key] = file_id

    update.message.reply_text(
        f"✔ File Saved\n🔑 Your Key: `{key}`",
        parse_mode="Markdown"
    )

def handle_text(update, context):
    key = update.message.text.strip()

    if key in files_db:
        update.message.chat.send_action(ChatAction.UPLOAD_DOCUMENT)
        update.message.reply_document(files_db[key])
    else:
        update.message.reply_text("❌ Invalid key — file not found")

def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document | Filters.photo, handle_file))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    updater.start_polling()
    updater.idle()

@app.route("/")
def home():
    return "Bot is running on Render Web Service!"

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
