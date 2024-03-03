import telebot
import requests

BOT_TOKEN = "6833081929:AAE1ippzFIThRODn9CpiEN8ex-gjUV_iSgw"
bot = telebot.TeleBot(BOT_TOKEN)

EXCHANGE_RATES_API_URL = "https://api.exchangerate-api.com/v4/latest/"

CURRENCIES = {
    "USD": "Доллар США",
    "EUR": "Евро",
    "RUB": "Российский рубль",
    "UAH": "Украинская гривна",
    "KZT": "Казахстанский тенге",
    "BYN": "Белорусский рубль",
    "KGS": "Кыргызский сом"
}

@bot.message_handler(commands=["start"])
def start_command(message):
    bot.reply_to(message, "Привет! Это бот для конвертации валют.\n\n"
                          "Введите команду /help, чтобы узнать больше.")

@bot.message_handler(commands=["help"])
def help_command(message):
    bot.reply_to(message, "Как пользоваться ботом:\n"
                          "1. Введите сумму, которую хотите конвертировать.\n"
                          "2. Введите код исходной валюты (например, USD, EUR, RUB).\n"
                          "3. Введите код целевой валюты (например, USD, EUR, RUB).\n\n"
                          "Пример:\n"
                          "100 USD EUR\n\n"
                          "Бот ответит:\n"
                          "100 USD = 95.43 EUR\n\n"
                          "Список доступных валют:\n"
                          "/currencies")

@bot.message_handler(commands=["currencies"])
def currencies_command(message):
    bot.reply_to(message, "\n".join([f"{code} - {name}" for code, name in CURRENCIES.items()]))

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    try:
        parts = message.text.split()

        if len(parts) != 3:
            raise ValueError("Неверный формат команды.")

        amount = float(parts[0])
        source_currency = parts[1].upper()
        target_currency = parts[2].upper()

        if source_currency not in CURRENCIES or target_currency not in CURRENCIES:
            raise ValueError("Неверный код валюты.")

        if source_currency == target_currency:
            converted_amount = amount
        else:
            url = f"{EXCHANGE_RATES_API_URL}{source_currency}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                rate = data["rates"][target_currency]
                converted_amount = amount * rate
            else:
                raise ValueError("Не удалось получить курс валюты.")

        bot.reply_to(message, f"{amount} {source_currency} = {converted_amount:.2f} {target_currency}")
    except ValueError as error:
        bot.reply_to(message, f"Ошибка: {error}")

bot.polling()