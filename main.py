import telebot
import wikipedia
from weather import get_weather
from openpyxl import load_workbook
from config import telegram_token as TOKEN

# Изменяем язык википеди на русский
wikipedia.set_lang("ru")

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)
# Создаеам словарь для перевода описания погоды на русский язык
descriptions = {}
sheet = load_workbook('description.xlsx')['Лист1']
for row in sheet.rows:
    descriptions[str(row[0].value)] = (str(row[1].value))


def translate_description(word):
    """
    функция, для перевода описания погоды
    передать нужно описание погоды на английском
    """
    try:
        return descriptions[word]
    except:
        return word


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id, 'Привет я погода-бот!')


# Функция, обрабатывающая команду /help
@bot.message_handler(commands=["help"])
def hlp(m):
    bot.send_message(m.chat.id, 'Пришли мне название своего города)))'
                                'если возникли какие-то проблемы пиши 👉 @pachkasigaretnikogda')


# Функция, обрабатывающая команду /stop
@bot.message_handler(commands=["stop"])
def stop():
    bot.stop_bot()


# Функция, обрабатывающая команду /wiki
@bot.message_handler(commands=["wiki"])
def wiki(m):
    try:
        bot.send_message(m.chat.id, wikipedia.summary('Новосибирск'))
    except:
        bot.send_message(m.chat.id, 'ERROR')


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        data = get_weather(message.text)
        photo = open(f"pic/{data['icon']}.png", 'rb')
        bot.send_message(message.chat.id, f"Погода в вашем городе 🌡 {data['temperature']}℃"
                                          f"\n {translate_description(data['description'])}")

        bot.send_photo(message.chat.id, photo)
    except Exception as ex:
        print(ex)
        bot.send_message(message.chat.id, f"Кажется, такого города не существует🤨")


# Запускаем бота
bot.polling(none_stop=True, interval=0)
