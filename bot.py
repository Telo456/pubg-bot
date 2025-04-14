from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ChatMemberHandler, ContextTypes
import os

TOKEN = os.getenv("7583533902:AAGZyy2a0grPRIig8VklAzDjGAvMlkyYLf4")  # ستحدد التوكن في Render لاحقاً

CHANNEL_USERNAME = "P_U_B_G_025"  # بدون @
GROUP_ID = -1002090285064  # تأكد أنه نفس آيدي مجموعتك

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! أنا بوت التحقق من الانضمام للقناة.")

async def check_joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != GROUP_ID:
        return

    user_id = update.effective_user.id
    member = await context.bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)

    if member.status not in ["member", "administrator", "creator"]:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME}")]])
        await update.message.reply_text("اشترك في القناة أولاً لتتمكن من الكتابة.", reply_markup=keyboard)
        await context.bot.restrict_chat_member(GROUP_ID, user_id, permissions={})
    else:
        await context.bot.restrict_chat_member(GROUP_ID, user_id, permissions={"can_send_messages": True})

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, check_joined))
    app.run_polling()
