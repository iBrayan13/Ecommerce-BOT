from telegram import (
    Update,
    Bot
)
from telegram.ext import CallbackContext
from decouple import config

async def admin(update: Update, context: CallbackContext):
    args = context.args
    bot = await update.get_bot()
    await bot.delete_message(chat_id= update.message.chat_id, message_id= update.message.message_id)

    if not len(args) == 1:
        await update.message.reply_text("Incorrect values.")
        raise ValueError
    
    password_msg = args[0]
    if not password_msg == config("ADMIN_PASSWD"):
        await update.message.reply_text("Incorrect password.")
        raise ValueError

    await update.message.reply_text("Hello Admin.")