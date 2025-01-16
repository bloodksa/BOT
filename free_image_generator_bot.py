import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from diffusers import StableDiffusionPipeline
import torch

TOKEN = os.environ.get("FREE_IMAGE_GENERATOR_BOT_TOKEN")

# تهيئة نموذج توليد الصور
model_id = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('مرحبا! أنا بوت توليد الصور المجاني. أرسل لي وصفًا للصورة التي تريد إنشاءها.')

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = update.message.text
    image = pipe(prompt).images[0]
    
    image.save("generated_image.png")
    await update.message.reply_photo(photo=open("generated_image.png", "rb"))
    os.remove("generated_image.png")

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))
    application.run_polling()

if __name__ == '__main__':
    main()

