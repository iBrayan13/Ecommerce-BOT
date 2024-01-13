from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes):
    username = update.message.chat.to_dict()["first_name"]
    menu_main = [
        [InlineKeyboardButton('Shop', callback_data='shop')]
    ]

    msg = f"Hello {username}, Welcome to the bot ecommerce!.\n\nUse the following commands to get started."
    reply_markup = InlineKeyboardMarkup(menu_main)

    await update.message.reply_text(msg, reply_markup= reply_markup)

async def menu_actions(update: Update, context: ContextTypes):
    query = update.callback_query
    if query.data == "shop":
        await query.message.reply_text("This is the shop")
