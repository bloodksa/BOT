import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, ContextTypes

TOKEN = os.environ.get("TIKTOK_ADDONS_BOT_TOKEN")

CHOOSING = range(1)

addons = {
    "followers": "زيادة المتابعين",
    "likes": "زيادة الإعجابات",
    "views": "زيادة المشاهدات",
    "comments": "زيادة التعليقات"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[InlineKeyboardButton(name, callback_data=addon)] for addon, name in addons.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "مرحبا! أنا بوت إضافات تيك توك. اختر الإضافة التي تريدها:",
        reply_markup
    )
    return CHOOSING

async def choose_addon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    addon = query.data
    await query.edit_message_text(f"لقد اخترت {addons[addon]}. سيتم تنفيذ هذه الإضافة قريبًا.")
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [CallbackQueryHandler(choose_addon)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()

