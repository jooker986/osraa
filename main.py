import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
        ApplicationBuilder,
        ContextTypes,
        CommandHandler,
        CallbackQueryHandler
    )

from keep_alive import keep_alive  # تأكد من وجود هذا الملف في نفس مجلد المشروع

    # إعداد اللوجات
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
logger = logging.getLogger(__name__)

TOKEN = "8410165519:AAFBaIoEFPgnfGr3H2R9nRD8dm-qIfMgrfk"
ADMIN_ID = 701816050  # غيره للـ ID بتاعك

    # الروابط
FESTIVAL_FORM = "https://drive.google.com/file/d/1rPS99XjB2hWB4-AXFswXQFv9y9GWynJs/view"
SPIRITUAL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSfUOx4iyVip5GbUw2B-cMjiBp3koRnZP1uJxRgZimyr2TF3uQ/viewform"
WHATSAPP_LINK = "https://wa.me/qr/YI3HRQTQQCU2I1"

    # تخزين المستخدمين
users = set()

    # القائمة الرئيسية
def get_main_keyboard():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("📍مهرجان افتقدنا بخلاصك 2025", callback_data='festival')],
            [InlineKeyboardButton("✝️ التسجيل في النشاط الروحي", callback_data='spiritual')],
            [InlineKeyboardButton("⚽ النشاط الرياضي (قريباً)", callback_data='sports')],
            [InlineKeyboardButton("🎭 النشاط الفني (قريباً)", callback_data='art')],
            [InlineKeyboardButton("📞 للتواصل والاستفسار", url=WHATSAPP_LINK)]
        ])

    # دالة /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        users.add(user.id)
        username = user.username or user.full_name or str(user.id)

        logger.info(f"User {username} started the bot.")

        # إرسال إشعار للإدمن
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🚨 مستخدم جديد دخل البوت:\nUsername: @{username}\nID: {user.id}"
        )

        await update.message.reply_text(
            "مرحباً بك في بوت اسرة البابا كيرلس و الانبا توماس\nاختر الخيار المناسب من القائمة:",
            reply_markup=get_main_keyboard()
        )

    # دالة الأزرار
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        if query.data == 'festival':
            await query.edit_message_text(
                f"رابط متابعة المهرجان:\n{FESTIVAL_FORM}",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data='back')]])
            )
        elif query.data == 'spiritual':
            await query.edit_message_text(
                f"رابط التسجيل في النشاط الروحي:\n{SPIRITUAL_FORM}",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data='back')]])
            )
        elif query.data in ['sports', 'art']:
            await query.edit_message_text(
                "هذا النشاط سيتم إطلاقه قريباً\nتابعنا للمزيد من التفاصيل",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data='back')]])
            )
        elif query.data == 'back':
            await query.edit_message_text(
                "مرحباً بك مرة أخرى 👋\nاختر من القائمة:",
                reply_markup=get_main_keyboard()
            )

    # التشغيل
def main():
        keep_alive()  # تشغيل السيرفر الخلفي
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button))

        print("✅ Bot is running...")
        app.run_polling()

if __name__ == '__main__':
        main()