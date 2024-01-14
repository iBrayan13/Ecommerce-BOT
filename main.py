from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from decouple import config

from src.commands.BasicCommands import start, menu_actions, web_app_data

bot = Application.builder().token(config("API_KEY")).build()
def main():
    bot.add_handler(CommandHandler('start', start))
    bot.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    bot.add_handler(CallbackQueryHandler(menu_actions))

    bot.run_polling()

if __name__ == "__main__":
    main()