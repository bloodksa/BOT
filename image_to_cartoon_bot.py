import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import cv2
import numpy as np

TOKEN = os.environ.get("IMAGE_TO_CARTOON_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('مرحبا! أنا بوت تحويل الصور إلى كرتون. أرسل لي صورة وسأقوم بتحويلها إلى رسم كرتوني.')

async def cartoonize_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file = await context.bot.get_file(update.message.document.file_id)
    await file.download_to_drive("image.jpg")
    
    img = cv2.imread("image.jpg")
    
    # تحويل الصورة إلى رمادي
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    
    # تطبيق فلتر ثنائي
    color = cv2.bilateralFilter(img, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    
    cv2.imwrite("cartoon.jpg", cartoon)
    
    await update.message.reply_photo(photo=open("cartoon.jpg", "rb"))
    os.remove("image.jpg")
    os.remove("cartoon.jpg")

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.IMAGE, cartoonize_image))
    application.run_polling()

if __name__ == '__main__':
    main()

