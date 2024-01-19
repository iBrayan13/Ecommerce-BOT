from telegram import (
    Update,
    InlineKeyboardMarkup,
    WebAppInfo,
    KeyboardButton,
    InlineKeyboardButton,
)
from telegram.ext import ContextTypes
import json
from src.models.order import Order
from src.models.product import ProductOrdered
from src.services.ProductServices import ProductService
from requests import api
from decouple import config

product_service = ProductService()

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
    global order
    order = Order(username= userdata['username'], products= [])

    ids = []
    for product in data['order']:
        # Verifying order product list
        if not int(product['id']) in ids:

            # Setting message
            by_product = product['price'] * product['amount']
            total += by_product
            msg += f"\nProduct: {product['name']}\nPrice: ${product['price']}\nUnits: {product['amount']}\nTotal by this product: ${by_product}\n"

            # Setting product object
            order.products.append(ProductOrdered(
                id= product['id'],
                name= product['name'],
                img= product['img'],
                price= product['price'],
                stock= product['stock'],
                amount= product['amount']
            ))
            ids.append(int(product['id']))

    date = order.date
    msg += f"\nTotal: ${total}"
    msg += f"\nDate: {date.year}/{date.month}/{date.day} at {date.hour}:{date.minute} UTC"
    
    reply_btn = [InlineKeyboardButton('✅ CONFIRM ✅', callback_data= 'accepted'), InlineKeyboardButton('❌ CANCEL ❌', callback_data= 'canceled')]
    bot_message = await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup([reply_btn]))
    context.user_data['message_to_delete'] = bot_message.message_id

async def start(update: Update, context: ContextTypes):
    userdata = update.message.chat.to_dict()
    print(userdata['id'])
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
    
async def menu_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == 'accepted':

        message_id = context.user_data.get('message_to_delete')
        if not message_id:
            raise TimeoutError
        
        bot = update.get_bot()
        await bot.delete_message(chat_id= query.message.chat_id, message_id= int(message_id))

        if order.canceled:
            await query.message.reply_text("You already sent that order.")
            raise TimeoutError

        msg = ""
        msg_admin = ""
        total = 0
        for product in order.products:
            by_product = product.price * product.amount
            total += by_product

            msg += f"\nProduct: {product.name}\nPrice: ${product.price}\nUnits: {product.amount}\nTotal by this product: ${by_product}\n"
            msg_admin += f"\nProduct ID: {product.id}\nProduct: {product.name}\nPrice: ${product.price}\nUnits: {product.amount}\nTotal by this product: ${by_product}\n"

            product_service.change_stock(product.id, int(product.stock - product.amount))

        msg += f"\nTotal: ${total}"
        msg_admin += f"\nTotal: ${total}"

        date = order.date
        msg += f"\nDate: {date.year}/{date.month}/{date.day} at {date.hour}:{date.minute} UTC"
        msg_admin += f"\nDate: {date.year}/{date.month}/{date.day} at {date.hour}:{date.minute} UTC"

        url = f'https://api.telegram.org/bot{config("API_KEY")}/sendMessage'
        params = {'chat_id': config('ADMIN_CHAT_ID'), 'text': f"Hello Admin!\n@{order.username} has ordered:\n{msg_admin}"}
        api.post(url, data=params)

        await query.message.reply_text(f"✅ ORDER SENT TO ADMIN\n{msg}")
        order.canceled = True
    
    if query.data == 'canceled':
        order.canceled = True

        message_id = context.user_data.get('message_to_delete')
        if not message_id:
            raise TimeoutError
        
        bot = update.get_bot()
        await bot.delete_message(chat_id= query.message.chat_id, message_id= int(message_id))