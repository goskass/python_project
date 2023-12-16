import telebot
from config import keys, TOKEN
from extensions import ConversionExceptions, CashConverter
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start",])
def help(message:telebot.types.Message):
    text = ("Привет, я умею переводить валюту из одной в другую.\n"
            "Узнать как мной пользоваться:\n"
            "Введи команду /help.\n"
            "Список валют /value.")
    bot.reply_to(message,text)

@bot.message_handler(commands=['help'])
def help(message:telebot.types.Message):
    text = ("Чтобы начать работу - введите сообщение в следующем формате:\n "
            "<имя валюты> <в какую валюту > <количество валюты>\n"
            "Названия валюты вводиться через пробел русскими буквами:\n"
            "доллар рубль 100 - корректно введенные данные\n"
            "Список всех валют: /value ")
    bot.reply_to(message,text)

@bot.message_handler(commands=["value",])
def value(message:telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = '\n'.join((text,key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert (message:telebot.types.Message):
    try:
        values = message.text.upper().split(" ")

        if len(values) != 3:
            raise ConversionExceptions("Неправильное количество параметров - смотри /help")
        quote, base, amount = values

        total_base = CashConverter.convert(quote, base, amount)
        total_base *= float(amount)
    except ConversionExceptions as e:
        bot.reply_to(message,f"Ошибка ввода данных. Пробуйте ввести снова\n{e}")
    except Exception as e:
        bot.reply_to(message,f"Не удалось обработать команду \n{e}")
    else:
        text = f"цена  {amount} {quote} в {base} равна: {total_base}"
        bot.send_message(message.chat.id, text)




bot.polling()
