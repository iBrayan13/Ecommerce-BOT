from telegram import (
    Update,
    InlineKeyboardMarkup,
    WebAppInfo,
    KeyboardButton,
    ReplyKeyboardRemove
)
from telegram.ext import ContextTypes
import json

async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = json.loads(update.effective_message.web_app_data.data)
    await update.message.reply_html( text= f"{data}", reply_markup= ReplyKeyboardRemove())

async def start(update: Update, context: ContextTypes):
    username = update.message.chat.to_dict()["first_name"]
    menu_main = [
        [KeyboardButton('Shop', web_app=WebAppInfo(url="https://e8ed-186-14-22-30.ngrok-free.app"))]
    ]

    msg = f"Hello {username}, Welcome to the bot ecommerce!.\n\nUse the following commands to get started."
    reply_markup = InlineKeyboardMarkup(menu_main)

    await update.message.reply_text(msg, reply_markup= reply_markup)
    
async def menu_actions(update: Update, context: ContextTypes):
    query = update.callback_query
    if query.data == "shop":
        await query.message.reply_text("This is the shop")