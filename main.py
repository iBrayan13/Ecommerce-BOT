from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from decouple import config

from src.commands.BasicCommands import start, menu_actions

def main():
    app = Application.builder().token(config("API_KEY")).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(menu_actions))

    app.run_polling()

if __name__ == "__main__":
    main()