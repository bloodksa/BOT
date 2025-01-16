import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

TOKEN = os.environ.get("YOUTUBE_SUMMARY_BOT_TOKEN")

# تهيئة نموذج تلخيص النصوص
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('مرحبا! أنا بوت تلخيص فيديوهات يوتيوب. أرسل لي رابط الفيديو وسأقوم بتلخيصه لك.')

async def summarize_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    video_url = update.message.text
    video_id = video_url.split("v=")[1]
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([i['text'] for i in transcript])
        
        summary = summarizer(transcript_text, max_length=150, min_length=30, do_sample=False)
        
        await update.message.reply_text(f"ملخص الفيديو:\n\n{summary[0]['summary_text']}")
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ أثناء تلخيص الفيديو: {str(e)}")

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, summarize_video))
    application.run_polling()

if __name__ == '__main__':
    main()

