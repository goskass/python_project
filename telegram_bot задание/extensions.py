import json                                          # импортируем библиотеку
import requests                                      # иипортируем библиотеку
from config import keys                              # импортируем из файла config значение ключей
class ConversionExceptions(Exception):
    pass

class CashConverter:                                 # класс отвечающий за исключения

    @staticmethod                                    #
    def convert(quote:str, base:str, amount:str):    # все данные приходят в виде строки
        if quote == base:                            # обрабатываем исключени если в туже валюту переводим
            raise ConversionExceptions(f"Нельзя перевести одинаковые валюты {base} ")

        try:
            quote_ticker = keys[quote]               #обрабатываем исключение если не корректно ввели данные валюты какую переводим
        except KeyError:
            raise ConversionExceptions(f"Не удалось обработать валюту {quote}")

        try:
            base_ticker = keys[base]                  # обрабатываем исключение если не корректно ввели данные валюты в какую переводим
        except KeyError:
            raise ConversionExceptions(f"Не удалось обработать валюту {base}")

        try:
            amount = float(amount)                    # обрабатываем исключение по корректности введных данных
        except ValueError:
            raise ConversionExceptions(f"Не удалось обработать количество {amount}")
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = json.loads(r.content)[keys[base]] #обрабатываем базовую валюту по ключу
        return total_base                              #вохвращеаем значение если не было исключения
