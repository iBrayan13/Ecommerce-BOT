from telegram.ext import Application
from decouple import config

def main():
    app = Application.builder().token(config("API_KEY")).build()

    app.run_polling()

if __name__ == "__main__":
    main()