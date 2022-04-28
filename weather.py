import requests
from config import openweather_token as TOKEN
from Translit import translit


def get_weather(city):
    """
    Функция, делающая запрос через api openweathermap
    передать нужно название города на русском языке
    возвращает словарь  {'temperature': температура в градусах по цельсию),
                    'icon': номер картинки,
                    'description': описание}
    """
    try:
        res = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={translit(city)}&appid={TOKEN}").json()
        return res

        # return {'temperature': round(res['main']['temp'] - 273),
                #'icon': res['weather'][0]['icon'][:2],
                #'description': res['weather'][0]['description']}
    except Exception as ex:
        return ex

print(get_weather('Новосибирск'))