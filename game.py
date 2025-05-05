import telebot
from requests import options

from clava import basic, key_chooser, start_keyboard, sex_choose
from scenario import scene

API_TOKEN = '7842674848:AAHaZqKSI2gplCBCPo89O52YJXauRz3DuNU'
bot = telebot.TeleBot(API_TOKEN)
@bot.message_handler(commands=['start'])
def handle_start(message):
  bot.reply_to(message, 'Привет! Я бот.', reply_markup=start_keyboard)

@bot.message_handler(func=lambda message: message.text in ['Начать игру', 'Узнать легенду'])
def handle_message(message):
  if message.text == 'Начать игру':
      bot.send_message(message.chat.id, 'пжшки скажите какого вы пола' , reply_markup=sex_choose)
  elif message.text == 'Узнать легенду':
      bot.send_message(message.chat.id, 'Вы - студент-первокурсник. Будьте добры, выживите))')

bot.polling()