import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

TOKEN = os.environ.get("TIKTOK_LIVE_FOLLOWERS_BOT_TOKEN")
RAPID_API_KEY = os.environ.get("RAPID_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('مرحبا! أنا بوت متابعي البث المباشر على تيك توك. أرسل لي اسم المستخدم للحصول على عدد المتابعين.')

async def get_live_followers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.message.text
    url = "https://tiktok-live-stats.p.rapidapi.com/live-stats"
    querystring = {"username": username}
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "tiktok-live-stats.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    if 'error' in data:
        await update.message.reply_text(f"حدث خطأ: {data['error']}")
    else:
        followers = data['stats']['followerCount']
        await update.message.reply_text(f"عدد متابعي {username} حاليًا: {followers}")

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_live_followers))
    application.run_polling()

if __name__ == '__main__':
    main()

