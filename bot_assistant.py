import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_ASSISTANT_TOKEN")

CHOOSING, TYPING_REPLY = range(2)

bot_templates = {
    "echo": "بوت الصدى",
    "weather": "بوت الطقس",
    "translator": "بوت الترجمة"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[InlineKeyboardButton(name, callback_data=template)] for template, name in bot_templates.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "مرحبا! أنا بوت مساعد لإنشاء البوتات. اختر نوع البوت الذي تريد إنشاءه:",
        reply_markup=reply_markup
    )
    return CHOOSING

async def choose_template(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    template = query.data
    context.user_data['template'] = template
    await query.edit_message_text(f"لقد اخترت {bot_templates[template]}. الآن، أرسل لي توكن البوت الخاص بك.")
    return TYPING_REPLY

async def received_token(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_token = update.message.text
    template = context.user_data['template']
    
    # هنا يمكنك إضافة الكود لإنشاء البوت الفعلي باستخدام القالب والتوكن
    
    await update.message.reply_text(f"تم إنشاء {bot_templates[template]} بنجاح! يمكنك الآن استخدام البوت الجديد.")
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [CallbackQueryHandler(choose_template)],
            TYPING_REPLY: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_token)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()

