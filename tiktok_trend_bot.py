import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

TOKEN = os.environ.get("TIKTOK_TREND_BOT_TOKEN")
RAPID_API_KEY = os.environ.get("RAPID_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('مرحبا! أنا بوت الترند على تيك توك. أرسل لي "trend" لأعرض لك أحدث الترندات.')

async def get_tiktok_trends(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = "https://tiktok-trends.p.rapidapi.com/trends"
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "tiktok-trends.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    trends = response.json()

    trend_text = "أحدث الترندات على تيك توك:\n\n"
    for trend in trends[:5]:
        trend_text += f"- {trend['title']}\n"

    await update.message.reply_text(trend_text)

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex('^trend$'), get_tiktok_trends))
    application.run_polling()

if __name__ == '__main__':
    main()

