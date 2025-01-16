import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from transformers import pipeline

TOKEN = os.environ.get("FREE_AI_BOT_TOKEN")

# تهيئة نموذج الذكاء الاصطناعي
generator = pipeline('text-generation', model='gpt2')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('مرحبا! أنا بوت ذكاء اصطناعي مجاني. أرسل لي أي نص وسأقوم بإكماله.')

async def generate_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = update.message.text
    response = generator(prompt, max_length=100, num_return_sequences=1)
    generated_text = response[0]['generated_text']
    await update.message.reply_text(generated_text)

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_text))
    application.run_polling()

if __name__ == '__main__':
    main()

