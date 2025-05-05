import telebot
from clava import keyboard1, key_chooser
import repliki
API_TOKEN = '7842674848:AAHaZqKSI2gplCBCPo89O52YJXauRz3DuNU'
bot = telebot.TeleBot(API_TOKEN)
@bot.message_handler(commands=['start'])
def handle_start(message):
  bot.reply_to(message, 'Привет! Я бот.', reply_markup=keyboard1)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
  if message.text == 'Начать игру':
      bot.send_message(message.chat.id, repliki.intro , reply_markup=key_chooser(repliki.intro))
  elif message.text == 'Узнать легенду':
      bot.send_message(message.chat.id, 'Вы - студент-первокурсник. Будьте добры, выживите))')
  elif message.text == 'Далее':
      bot.send_message(message.chat.id, repliki.first , reply_markup=key_chooser(repliki.first))
  elif message.text == 'Ресурсы':
      bot.send_message(message.chat.id, repliki.resource, reply_markup=key_chooser(repliki.resource))

bot.polling()