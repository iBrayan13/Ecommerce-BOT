from telegram import (
    Update,
    InlineKeyboardMarkup,
    WebAppInfo,
    KeyboardButton
)
from telegram.ext import ContextTypes
import json
from decouple import config

async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = json.loads(update.effective_message.web_app_data.data)
    print(data)

async def start(update: Update, context: ContextTypes):
    userdata = update.message.chat.to_dict()
    menu_main = [
        [KeyboardButton(
            'Shop',
            web_app=WebAppInfo(
                url=f"{config('NGROK_HOST')}/shop?chat_id={userdata['id']}&username={userdata['username']}"
            )
        )]
    ]

    msg = f"Hello {userdata['first_name']}, Welcome to the bot ecommerce!.\n\nUse the following commands to get started."
    reply_markup = InlineKeyboardMarkup(menu_main)

    await update.message.reply_text(msg, reply_markup= reply_markup)
    
async def menu_actions(update: Update, context: ContextTypes):
    query = update.callback_query
    if query.data == "shop":
        await query.message.reply_text("This is the shop")