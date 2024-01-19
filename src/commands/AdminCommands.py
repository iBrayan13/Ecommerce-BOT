from telegram import (
    Update
)
from telegram.ext import CallbackContext
from decouple import config
from src.services.ProductServices import ProductService
from src.models.product import Product

product_service = ProductService()

# ONLY USE IT WITHIN THE COMMANDS, IT'S NOT ONE
async def verify_password(update: Update, context: CallbackContext, args_expected: int) -> bool:
    userdata = update.message.chat.to_dict()
    args = context.args
    bot = update.get_bot()
    await bot.delete_message(chat_id= update.message.chat_id, message_id= update.message.message_id)

    if not int(userdata['id']) == int(config('ADMIN_CHAT_ID')):
        await update.message.reply_text("❌ You're not admin.")
        return False

    if not len(args) == args_expected:
        await update.message.reply_text("❌ Incorrect values.")
        return False
    
    password_msg = args[0]
    if not password_msg == config("ADMIN_PASSWD"):
        await update.message.reply_text("❌ Incorrect password.")
        return False

    return True

async def admin(update: Update, context: CallbackContext):
    if not await verify_password(update, context, 1):
        raise PermissionError

    msg = 'Hello Admin. These are all the commands available to you.\nRemember change the value "password" for yours and all the values too.\n\n'
    msg += '--- ADMIN COMMANDS ---\n\n'
    msg += '/admin_inventory password --> See all the products in database.\n\n'
    msg += '/admin_reset_inventory password --> Delete all the products in database.\n\n'
    msg += '/admin_add_product password product_name product_img_url product_price product_stock --> Add a product into database (Remember do not use spaces in produc_name, always use "-" to indicate space).\n\n'
    msg += '/admin_get_product password product_id --> See the product information by its ID.\n\n'
    msg += '/admin_product_change_stock password product_id new_product_stock --> Update product stock on database.\n\n'
    msg += '/admin_product_change_price password product_id new_product_price --> Update product price on database (If your input is decimal use "." not ",").\n\n'
    msg += '/admin_product_change_name password product_id new_product_name --> Update product name on database (Remember do not use spaces in produc_name, always use "-" to indicate space).\n\n'
    msg += '/admin_delete_product password product_id --> Delete a product from database.\n\n'
    msg += '--- ADMIN COMMANDS ---'

    await update.message.reply_text(msg)

async def admin_inventory(update: Update, context: CallbackContext):
    if not await verify_password(update, context, 1):
        raise PermissionError
    
    products = product_service.get_all_products()
    if not len(products) > 0:
        await update.message.reply_text("Database empty.")
        raise ValueError
    
    msg = "Products in database:\n\n"
    for product in products:
        msg += f"Product ID: {product.id}\nProduct: {product.name}\nImage URL: {product.img}\nPrice: ${product.price}\nStock: {product.stock}\n\n"

    await update.message.reply_text(msg)

async def admin_reset_inventory(update: Update, context: CallbackContext):
    if not await verify_password(update, context, 1):
        raise PermissionError
    
    if not product_service.reset_products():
        await update.message.reply_text("❌ Something was wrong during reset inventory. Please try again.")
        raise ValueError
    
    await update.message.reply_text("✅ Inventory reseted.")
    
async def admin_add_product(update: Update, context: CallbackContext):
    if not await verify_password(update, context, 5):
        raise PermissionError

    args = context.args
    name = args[1]
    img = args[2]
    price = args[3]
    stock = args[4]

    if not type(product_service.add_product(Product(name= name, img= img, price= price, stock= stock))) == Product:
        await update.message.reply_text("❌ Something was wrong during add. Please check your input and try again.")
        raise ValueError
    
    await update.message.reply_text("✅ Product added into database.")

async def admin_get_product(update: Update, context: CallbackContext):
    if not await verify_password(update, context, 2):
        raise PermissionError
    
    args = context.args
    product_id = int(args[1])

    product = product_service.get_a_product(product_id)
    if not type(product) == Product:
        await update.message.reply_text("❌ Something was wrong during delete. Please check your input and try again.")
        raise ValueError
    
    await update.message.reply_text(f"Product ID: {product.id}\nProduct: {product.name}\nImage URL: {product.img}\nPrice: ${product.price}\nStock: {product.stock}")


async def admin_product_change_stock(update: Update, context: CallbackContext):
    if not await verify_password(update, context, 3):
        raise PermissionError
    
    args = context.args
    product_id = int(args[1])
    new_stock = int(args[2])

    if not product_service.change_stock(product_id, new_stock):
        await update.message.reply_text("❌ Something was wrong updating stock. Please check your input and try again.")
        raise ValueError
    
    await update.message.reply_text("✅ Product Stock changed.")

async def admin_product_change_price(update: Update, context: CallbackContext):
    if not await verify_password(update, context, 3):
        raise PermissionError
    
    args = context.args
    product_id = int(args[1])
    new_price = float(args[2])

    if not product_service.change_price(product_id, new_price):
        await update.message.reply_text("❌ Something was wrong updating price. Please check your input and try again.")
        raise ValueError
    
    await update.message.reply_text("✅ Product Price changed.")

async def admin_product_change_name(update: Update, context: CallbackContext):
    if not await verify_password(update, context, 3):
        raise PermissionError
    
    args = context.args
    product_id = int(args[1])
    new_name = str(args[2])

    if not product_service.change_name(product_id, new_name):
        await update.message.reply_text("❌ Something was wrong updating name. Please check your input and try again.")
        raise ValueError
    
    await update.message.reply_text("✅ Product Name changed.")

async def admin_delete_product(update: Update, context: CallbackContext):
    if not await verify_password(update, context, 2):
        raise PermissionError
    
    args = context.args
    product_id = int(args[1])
    if not product_service.delete_product(product_id):
        await update.message.reply_text("❌ Something was wrong during delete. Please check your input and try again.")
        raise ValueError
    
    await update.message.reply_text("✅ Product deleted.")