import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from yt_dlp import YoutubeDL

TOKEN = os.environ.get("VIDEO_DOWNLOADER_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('مرحبا! أرسل لي رابط الفيديو وسأقوم بتحميله لك.')

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    ydl_opts = {'outtmpl': 'video.%(ext)s'}
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)
        
        await update.message.reply_video(video=open(video_path, 'rb'))
        os.remove(video_path)
    except Exception as e:
        await update.message.reply_text(f'حدث خطأ أثناء تحميل الفيديو: {str(e)}')

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    application.run_polling()

if __name__ == '__main__':
    main()

