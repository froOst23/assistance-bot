import telebot
import datetime
from telebot import apihelper
from telebot import types
from pyowm import OWM

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # Расшифровка команды HELP
	'geo'	: 'Покажу прогноз погоды, если ты разрешишь мне передать свои координаты'
}

now = 	datetime.datetime.now()

def get_user_step(uid):
	if uid in userStep:
		return userStep[uid]
	else:
		knownUsers.append(uid)
		userStep[uid] = 0
		return 0

API_key_OWM = '0fdbf8fa3686cb494aa67a2f04c9ab9e'
owm = OWM(API_key_OWM)

TOKEN = '980391350:AAHlF91WcX12-1dHfzaXoObQh7DrboGqjzs'
#PROXY = 'https://91.236.239.149:3128'
apihelper.proxy = {'https': PROXY}
bot = telebot.TeleBot(TOKEN)

# команда START
@bot.message_handler(commands=['start'])
def command_start(m):

	cid = m.chat.id
	first_name_id = m.chat.first_name
	username_id = m.chat.username

	feedback = 'К нам присоеденился @' + str(username_id) + '\n' + 'по имени ' + str(first_name_id) + '\n' + 'его id ' + str(cid)
	welcome_first = 'Привет @' + str(username_id) + '! \n' + 'Ты только что меня включил и я готов к работе!' + '\n' + 'На данный момент я умею определять температуру воздуха по двум координатам'
	welcome_second = 'Я уже включен и работаю! Попробуй написать /help чтобы узнать команды'

	if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
		knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
		userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
		bot.send_message(cid, welcome_first)
		bot.send_message(142371402, feedback)
		command_help(m)  # show the new user the help page
	else:
		bot.send_message(cid, welcome_second)
		bot.send_message(142371402, feedback)

# команда HELP
@bot.message_handler(commands=['help'])
def command_help(m):
	cid = m.chat.id
	help_text = "Вот что я умею: \n"
	for key in commands:  # generate help text out of the commands dictionary defined at the top
		help_text += "/" + key + ": "
		help_text += commands[key] + "\n"
	bot.send_message(cid, help_text)  # send the generated help page

@bot.message_handler(commands=["geo"])
def geo(message):
	keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
	keyboard.add(button_geo)
	bot.send_message(message.chat.id, "Если ты поделишься своими координатами, то я смогу показать тебе текущую погоду", reply_markup=keyboard)

@bot.message_handler(content_types=["location"])
def location(message):
	if message.location is not None:
		#print(message.location)
		#print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))
		obs = owm.weather_at_coords(message.location.latitude, message.location.longitude)
		w = obs.get_weather()
		l = obs.get_location()
		location = str(l.get_name())
		temp = str(w.get_temperature(unit='celsius'))
		correct_temp = temp[8:15]
		weather_message = 'Вот что я получил: ' + '\n' + 'Широта: ' + str(message.location.latitude) + '\n' + "Долгота " + str(message.location.longitude) + '\n' + 'Давай я посмотрю что у нас по погоде на openweathermap.org'+ '\n' + "Ты сейчас находишься в месте под названием - " + str(location) + '\n' + "И сейчас " + str(correct_temp) + " Градусов по Цельсию "
		bot.send_message(message.chat.id, weather_message)

		# собираем feedback
		w_feedback = '@' + str(message.chat.username) + '\n' + 'поделился своими координатами ' + '\n' + 'Широта ' + str(message.location.latitude)+ '\n' + 'Долгота ' + str(message.location.longitude) + '\n' + 'Он сейчас находишься в месте под названием - ' + str(location) + '\n' + 'И сейчас там' + str(correct_temp) + ' Градусов по Цельсию'
		bot.send_message(142371402, w_feedback)

bot.polling(none_stop=True)