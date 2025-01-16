import os
import importlib
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes
from server_utils import deploy_bot_to_server, deploy_free_trial_bot

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

MAIN_MENU, CHOOSE_TEMPLATE, ADD_TOKEN, VIEW_BOTS, CONFIRM_DELETE, SEARCH_GITHUB, SELECT_GITHUB_REPO, FREE_TRIAL = range(8)

templates = {
    "video_downloader": "بوت تحميل الفيديو من منصات التواصل",
    "text_to_speech": "بوت تحويل النص لصوت",
    "free_ai": "بوت ذكاء اصطناعي مجاني",
    "tiktok_trend": "بوت الترند على تيك توك",
    "bot_assistant": "بوت مبرمج بوتات مساعد",
    "free_image_generator": "بوت توليد الصور المجاني",
    "file_converter": "بوت تحويل الملفات",
    "tiktok_live_followers": "بوت رفع متابعين اللايف بالتيك توك",
    "tiktok_addons": "بوت إضافات تيك توك",
    "youtube_summary": "بوت استخراج الخلاصة من مقاطع فيديو اليوتيوب",
    "image_to_cartoon": "بوت تحويل الصور لكرتون"
}

user_data = {}

disclaimer_message = "تنبيه هام: أنا أبري ذمتي من أي شخص يستخدم هذا البوت أو أي بوت تم إنشاؤه بواسطته بشكل خاطئ أو غير قانوني. المستخدم وحده يتحمل المسؤولية الكاملة عن استخدام هذه الخدمة."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(disclaimer_message)
    
    keyboard = [
        [InlineKeyboardButton("إضافة بوت جديد", callback_data="add_bot")],
        [InlineKeyboardButton("البحث عن بوت في GitHub", callback_data="search_github")],
        [InlineKeyboardButton("عرض البوتات الخاصة بي", callback_data="view_bots")],
        [InlineKeyboardButton("تجربة مجانية", callback_data="free_trial")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "مرحبا! أنا بوت إدارة البوتات المتقدم. ماذا تريد أن تفعل؟",
        reply_markup=reply_markup
    )
    return MAIN_MENU

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    choice = query.data
    
    if choice == "add_bot":
        keyboard = [[InlineKeyboardButton(name, callback_data=template)] for template, name in templates.items()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "اختر قالبًا لإنشاء بوت جديد:",
            reply_markup=reply_markup
        )
        return CHOOSE_TEMPLATE
    elif choice == "search_github":
        await query.edit_message_text("أدخل كلمة البحث للعثور على بوتات في GitHub:")
        return SEARCH_GITHUB
    elif choice == "view_bots":
        return await view_bots(update, context)
    elif choice == "free_trial":
        return await setup_free_trial(update, context)

async def choose_template(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    template = query.data
    context.user_data['template'] = template
    await query.edit_message_text(
        f"لقد اخترت {templates[template]}. الآن، أرسل لي توكن البوت الخاص بك."
    )
    return ADD_TOKEN

async def add_token(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_token = update.message.text
    user_id = update.effective_user.id
    template = context.user_data['template']
    
    if user_id not in user_data:
        user_data[user_id] = {}
    
    # إنشاء نسخة جديدة من البوت
    bot_module = importlib.import_module(f"{template}_bot")
    new_bot = bot_module.main  # نفترض أن الدالة الرئيسية للبوت اسمها 'main'
    
    # رفع البوت على السيرفر
    success = await deploy_bot_to_server(template, user_token)
    
    if success:
        user_data[user_id][template] = {
            'type': 'template',
            'token': user_token
        }
        
        keyboard = [
            [InlineKeyboardButton("إضافة بوت آخر", callback_data="add_bot")],
            [InlineKeyboardButton("عرض البوتات الخاصة بي", callback_data="view_bots")],
            [InlineKeyboardButton("العودة للقائمة الرئيسية", callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(disclaimer_message)
        await update.message.reply_text(
            f"تم إنشاء ورفع {templates[template]} على السيرفر بنجاح! ماذا تريد أن تفعل الآن؟",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text("حدث خطأ أثناء رفع البوت على السيرفر. يرجى المحاولة مرة أخرى.")
    
    return MAIN_MENU

async def view_bots(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if query:
        await query.answer()
    
    user_id = update.effective_user.id
    if user_id in user_data and user_data[user_id]:
        message = "البوتات الخاصة بك:\n\n"
        keyboard = []
        for template, bot_info in user_data[user_id].items():
            if template == 'free_trial':
                message += f"النسخة التجريبية المجانية: {bot_info['token'][:10]}...\n"
            else:
                message += f"{templates[template]}: {bot_info['token'][:10]}...\n"
            keyboard.append([InlineKeyboardButton(f"حذف {templates.get(template, 'النسخة التجريبية المجانية')}", callback_data=f"delete_{template}")])
        
        keyboard.append([InlineKeyboardButton("العودة للقائمة الرئيسية", callback_data="main_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if query:
            await query.edit_message_text(message, reply_markup=reply_markup)
        else:
            await update.message.reply_text(message, reply_markup=reply_markup)
    else:
        keyboard = [[InlineKeyboardButton("العودة للقائمة الرئيسية", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = "ليس لديك أي بوتات مضافة بعد."
        if query:
            await query.edit_message_text(message, reply_markup=reply_markup)
        else:
            await update.message.reply_text(message, reply_markup=reply_markup)
    
    return MAIN_MENU

async def confirm_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    template = query.data.split('_')[1]
    context.user_data['to_delete'] = template
    
    keyboard = [
        [InlineKeyboardButton("نعم، احذف البوت", callback_data="confirm_delete")],
        [InlineKeyboardButton("لا، احتفظ بالبوت", callback_data="cancel_delete")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f"هل أنت متأكد أنك تريد حذف {templates.get(template, 'النسخة التجريبية المجانية')}؟",
        reply_markup=reply_markup
    )
    return CONFIRM_DELETE

async def delete_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    choice = query.data
    
    if choice == "confirm_delete":
        template = context.user_data['to_delete']
        user_id = update.effective_user.id
        if user_id in user_data and template in user_data[user_id]:
            del user_data[user_id][template]
            message = f"تم حذف {templates.get(template, 'النسخة التجريبية المجانية')} بنجاح."
        else:
            message = "حدث خطأ أثناء محاولة حذف البوت."
    else:
        message = "تم إلغاء عملية الحذف."
    
    keyboard = [[InlineKeyboardButton("العودة للقائمة الرئيسية", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(message, reply_markup=reply_markup)
    return MAIN_MENU

async def setup_free_trial(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    trial_token = await deploy_free_trial_bot()
    user_id = update.effective_user.id
    
    if user_id not in user_data:
        user_data[user_id] = {}
    
    user_data[user_id]['free_trial'] = {
        'type': 'trial',
        'token': trial_token
    }
    
    keyboard = [
        [InlineKeyboardButton("العودة للقائمة الرئيسية", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(disclaimer_message)
    await query.edit_message_text(
        f"تم إنشاء نسخة تجريبية مجانية لك! التوكن الخاص بك هو: {trial_token}\n"
        "يمكنك استخدام هذا التوكن للوصول إلى النسخة التجريبية المجانية.",
        reply_markup=reply_markup
    )
    return MAIN_MENU

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(main_menu, pattern="^(add_bot|search_github|view_bots|main_menu|free_trial)$"),
            ],
            CHOOSE_TEMPLATE: [
                CallbackQueryHandler(choose_template, pattern=f"^({'|'.join(templates.keys())})$"),
            ],
            ADD_TOKEN: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add_token),
            ],
            VIEW_BOTS: [
                CallbackQueryHandler(confirm_delete, pattern="^delete_"),
            ],
            CONFIRM_DELETE: [
                CallbackQueryHandler(delete_bot, pattern="^(confirm_delete|cancel_delete)$"),
            ],
            FREE_TRIAL: [
                CallbackQueryHandler(setup_free_trial),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()

