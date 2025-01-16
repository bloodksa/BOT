import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image

TOKEN = os.environ.get("FILE_CONVERTER_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('مرحبا! أنا بوت تحويل الملفات. أرسل لي صورة وسأقوم بتحويلها إلى PDF.')

async def convert_to_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file = await context.bot.get_file(update.message.document.file_id)
    await file.download_to_drive("image.jpg")
    
    image = Image.open("image.jpg")
    pdf_path = "converted.pdf"
    image.save(pdf_path, "PDF", resolution=100.0)
    
    await update.message.reply_document(document=open(pdf_path, "rb"))
    os.remove("image.jpg")
    os.remove(pdf_path)

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.IMAGE, convert_to_pdf))
    application.run_polling()

if __name__ == '__main__':
    main()

