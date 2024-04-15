from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import qrcode
import io

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome to the QR Bot! Send me text, a link, or a photo and I'll generate a QR code for you."
    )

def generate_qr_code(update: Update, context: CallbackContext) -> None:
    message = update.message
    if message.text:
        generate_text_qr_code(message)
    elif message.photo:
        generate_photo_qr_code(message)
    elif message.entities:
        for entity in message.entities:
            if entity.type == 'url':
                generate_link_qr_code(message, entity)

def generate_text_qr_code(message: Update) -> None:
    text = message.text
    qr_code = qrcode.make(text)
    send_qr_code(message, qr_code)

def generate_photo_qr_code(message: Update) -> None:
    photo_file = message.photo[-1].get_file()
    qr_code = qrcode.make(photo_file.download_as_bytearray())
    send_qr_code(message, qr_code)

def generate_link_qr_code(message: Update, entity) -> None:
    link = message.text[entity.offset: entity.offset + entity.length]
    qr_code = qrcode.make(link)
    send_qr_code(message, qr_code)

def send_qr_code(message: Update, qr_code) -> None:
    bio = io.BytesIO()
    bio.name = 'qrcode.png'
    qr_code.save(bio)
    bio.seek(0)
    message.reply_photo(photo=bio)

def main() -> None:
    # Initialize the Telegram Bot
    updater = Updater("7089899954:AAGNOPz_iQCUrxw_PTgm7XJ2HNELWqK-LxA")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))

    # Register message handlers
    dispatcher.add_handler(MessageHandler(Filters.text | Filters.photo, generate_qr_code))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
