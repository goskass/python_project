import telebot                                              # ипортируем бибилотеку телеграм бота
from config import keys, TOKEN                              # обращаемся к файлу config и ипортируем ключи и токен
from extensions import ConversionExceptions, CashConverter  # обращаемся к extension и импортируем классы
bot = telebot.TeleBot(TOKEN)                                # присваиваем бот ключ чтоб он работал

@bot.message_handler(commands=["start",])  # обрабатываем команду старт
def help(message:telebot.types.Message):
    text = ("Привет, я умею переводить валюту из одной в другую.\n"
            "Узнать как мной пользоваться:\n"
            "Введи команду /help.\n"
            "Список валют /value.")
    bot.reply_to(message,text)                              #отвечаем на команду start

@bot.message_handler(commands=['help'])                     # обрабатываем команду help
def help(message:telebot.types.Message):
    text = ("Чтобы начать работу - введите сообщение в следующем формате:\n "
            "<имя валюты> <в какую валюту > <количество валюты>\n"
            "Названия валюты вводиться через пробел русскими буквами:\n"
            "доллар рубль 100 - корректно введенные данные\n"
            "Список всех валют: /value ")
    bot.reply_to(message,text)                              #отвечаем на сообщение пользователю на команду help

@bot.message_handler(commands=["value",])                   # обрабатываем команду value вывод валюты
def value(message:telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():                                 # выводим доступные валюты столбиком
        text = '\n'.join((text,key))
    bot.reply_to(message, text)                             # отвечаем на сообщение пользователя

@bot.message_handler(content_types=['text'])                # обрабатываем текс сообщения от пользователя
def convert (message:telebot.types.Message):
    try:
        values = message.text.upper().split(" ")             # разбиваем сообщение  по пробелам и переводим в верхний регистр

        if len(values) != 3:                                 # проверям количество вводимых данных
            raise ConversionExceptions("Неправильное количество параметров - смотри /help")
        quote, base, amount = values
        total_base = CashConverter.convert(quote, base, amount) # присваеваем значение
        total_base *= float(amount)                             # общая сумма конвертируевой валюты
    except ConversionExceptions as e:                           # обработчик исключения
        bot.reply_to(message,f"Ошибка ввода данных. Пробуйте ввести снова\n{e}")
    except Exception as e:                                      # обработчик исключения
        bot.reply_to(message,f"Не удалось обработать команду \n{e}")
    else:
        text = f"цена  {amount} {quote} в {base} равна: {total_base}" # выводим сообщение в суммой
        bot.send_message(message.chat.id, text)

bot.polling()                                                         #запускаем бота
