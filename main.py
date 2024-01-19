from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from decouple import config

from src.commands.BasicCommands import start, menu_actions, web_app_data
from src.commands.AdminCommands import (
    admin,
    admin_inventory,
    admin_get_product,
    admin_reset_inventory,
    admin_add_product,
    admin_product_change_stock,
    admin_product_change_price,
    admin_product_change_name,
    admin_delete_product
)

def main():
    bot = Application.builder().token(config("API_KEY")).build()

    bot.add_handler(CommandHandler('start', start))
    bot.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    bot.add_handler(CallbackQueryHandler(menu_actions))

    bot.add_handler(CommandHandler('admin', admin))
    bot.add_handler(CommandHandler('admin_inventory', admin_inventory))
    bot.add_handler(CommandHandler('admin_get_product', admin_get_product))
    bot.add_handler(CommandHandler('admin_reset_inventory', admin_reset_inventory))
    bot.add_handler(CommandHandler('admin_add_product', admin_add_product))
    bot.add_handler(CommandHandler('admin_product_change_stock', admin_product_change_stock))
    bot.add_handler(CommandHandler('admin_product_change_price', admin_product_change_price))
    bot.add_handler(CommandHandler('admin_product_change_name', admin_product_change_name))
    bot.add_handler(CommandHandler('admin_delete_product', admin_delete_product))

    bot.run_polling()

if __name__ == "__main__":
    main()