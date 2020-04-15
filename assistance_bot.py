import os
import telebot
import apiai
import json
from telebot import apihelper
from telebot import types
from pyowm import OWM


knownUsers = []  # содержит известных пользователей
userStep = {}

# Расшифровка команды HELP
commands = {
	'geo'	: 'Покажу прогноз погоды, если ты разрешишь мне передать свои координаты'
}

def get_user_step(uid):
	if uid in userStep:
		return userStep[uid]
	else:
		knownUsers.append(uid)
		userStep[uid] = 0
		return 0


TelegramTOKEN = os.environ['Telegram_TOKEN']
API_key_OWM = os.environ['OWM_TOKEN']
DialogTOKEN = os.environ['Dialogflow_TOKEN']

# Токен API Telegram
bot = telebot.TeleBot(TelegramTOKEN)
# Токен API OWM к Telegram
owm = OWM(API_key_OWM)

# Команда start
@bot.message_handler(commands=['start'])
def command_start(message):
	cid = message.chat.id
	first_name_id = message.chat.first_name
	username_id = message.chat.username
	feedback = 'К нам присоеденился @' + str(username_id) + '\n' + 'по имени ' + str(first_name_id) + '\n' + 'его id ' + str(cid)
	welcome_first = 'Привет @' + str(username_id) + '! \n' + 'Ты только что меня включил и я готов к работе!'
	welcome_second = 'Я уже включен и работаю! Попробуй написать /help чтобы узнать команды'

	# Если пользователь первы раз нажимает /start
	if cid not in knownUsers:
		knownUsers.append(cid)
		userStep[cid] = 0
		bot.send_message(cid, welcome_first)
		bot.send_message(142371402, feedback)
		command_help(message)
	# Последующие нажатия /start
	else:
		bot.send_message(cid, welcome_second)
		bot.send_message(142371402, feedback)


# Команда help
@bot.message_handler(commands=['help'])
def command_help(message):
	cid = message.chat.id
	help_text = "Вот что я умею: \n"

	# Вывод текста help_text
	for key in commands:
		help_text += "/" + key + ": "
		help_text += commands[key] + "\n"
	bot.send_message(cid, help_text)


# Команда geo
@bot.message_handler(commands=["geo"])
def geo(message):
	keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
	keyboard.add(button_geo)
	bot.send_message(message.chat.id, "Если ты поделишься своими координатами, то я смогу показать тебе текущую погоду", reply_markup=keyboard)


# Получение координат пользователя и их обработка
@bot.message_handler(content_types=["location"])
def location(message):
	if message.location is not None:
		# получаем координаты пользователя
		obs = owm.weather_at_coords(message.location.latitude, message.location.longitude)
		w = obs.get_weather()
		l = obs.get_location()
		location = str(l.get_name())
		temp = str(w.get_temperature(unit='celsius'))

		# преобразуем корректный вывод температуры
		correct_temp = temp[8:15]
		weather_message = 'Вот что я получил: ' + '\n' + 'Широта: ' + str(message.location.latitude) + '\n' + "Долгота " + str(message.location.longitude) + '\n' + 'Давай я посмотрю что у нас по погоде на openweathermap.org'+ '\n' + "Ты сейчас находишься в месте под названием - " + str(location) + '\n' + "И сейчас " + str(correct_temp) + " Градусов по Цельсию "
		bot.send_message(message.chat.id, weather_message)

		# собираем feedback
		w_feedback = '@' + str(message.chat.username) + '\n' + 'поделился своими координатами ' + '\n' + 'Широта ' + str(message.location.latitude)+ '\n' + 'Долгота ' + str(message.location.longitude) + '\n' + 'Он сейчас находишься в месте под названием - ' + str(location) + '\n' + 'И сейчас там' + str(correct_temp) + ' Градусов по Цельсию'
		bot.send_message(142371402, w_feedback)


# Используем возможности dialogflow
@bot.message_handler(content_types=['text'])
def send_text(message):
	request = apiai.ApiAI(DialogTOKEN).text_request()
	request.lang = 'ru'
	request.session_id = 'BatlabAIBot'
	request.query = message.text
	responseJson = json.loads(request.getresponse().read().decode('utf-8'))
	response = responseJson['result']['fulfillment']['speech']
	if response:
		bot.send_message(message.chat.id, text=response)
	else:
		bot.send_message(message.chat.id, text='Я вас не совсем понял...')


bot.polling(none_stop=True)
