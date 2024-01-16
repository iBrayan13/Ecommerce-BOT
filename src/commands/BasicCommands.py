from telegram import (
    Update,
    InlineKeyboardMarkup,
    WebAppInfo,
    KeyboardButton,
    InlineKeyboardButton,
)
from telegram.ext import ContextTypes
import json
from decouple import config

async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = json.loads(update.effective_message.web_app_data.data)
    userdata = update.message.chat.to_dict()

    # Verifying order
    for product in data['order']:
        if not product['amount'] <= product['stock']:
            await update.message.reply_text(
                f"Sorry, {userdata['first_name']}. You try to order {product['amount']} {product['name']}, but our stock is {product['stock']} units."
            )
            raise ValueError
        
        elif not product['amount'] > 0:
            await update.message.reply_text(
                f"Sorry, {userdata['first_name']}. You try to order and invalid amount of {product['name']}. Try again with other value."
            )
            raise ValueError

    # Getting order
    msg = f"Hey {userdata['first_name']}! You have been ordered:\n"
    total = 0
    for product in data['order']:
        by_product = product['price'] * product['amount']
        total += by_product
        msg += f"\nProduct: {product['name']}\nPrice: ${product['price']}\nUnits: {product['amount']}\nTotal by this product: ${by_product}\n"
    msg += f"\nTotal: ${total}"
    
    reply_btn = [InlineKeyboardButton('✅ CONFIRM ✅', callback_data='accepted')]
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup([reply_btn]))

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
    if query.data == "accepted":
        await query.message.reply_text("ORDER SENT ✅")