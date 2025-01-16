import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from gtts import gTTS

TOKEN = os.environ.get("TEXT_TO_SPEECH_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('مرحبا! أرسل لي نصًا وسأقوم بتحويله إلى ملف صوتي.')

async def text_to_speech(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    tts = gTTS(text=text, lang='ar')
    tts.save("speech.mp3")
    
    await update.message.reply_voice(voice=open("speech.mp3", 'rb'))
    os.remove("speech.mp3")

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_to_speech))
    application.run_polling()

if __name__ == '__main__':
    main()

