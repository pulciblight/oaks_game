import telebot
from clava import key_chooser
from telebot import types

# Токен вашего бота
TOKEN = '7842674848:AAHaZqKSI2gplCBCPo89O52YJXauRz3DuNU'

# Создаём экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Состояния игры
game_states = {
    'start': {
        'text': 'Это просто супер мега игра про Дубки. '
                'Вы готовы начать приключение? Или хотите узнать больше?',
        'options': ['Начать игру', 'Узнать легенду']
    },
    'Начать игру': {
        'text': 'Пожалуйста, сообщите, женский или мужской у вас персонаж',
        'options': ['Женский', 'Мужской']
    },
    'Узнать легенду': {
        'text': 'Вы - студент-первокурсник. Будьте добры, выживите))',
        'options': ['Начать игру']
    },
    'Искать выход': {
        'text': 'Вы нашли выход из леса!',
        'options': ['Вернуться в начало']
    },
    'Осмотреться': {
        'text': 'Вы осмотрелись, но ничего интересного не нашли.',
        'options': ['Вернуться в начало']
    },
    'Спуститься': {
        'text': 'Вы спустились с горы и вернулись в начало.',
        'options': ['Вернуться в начало']
    },
}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_game(message):
    user_id = message.from_user.id
    # Устанавливаем начальное состояние
    bot.send_message(user_id, game_states['start']['text'], reply_markup=key_chooser(game_states['start']['options']))

# Создание клавиатуры с кнопками


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text

    if text in game_states:
        # Обновляем состояние и отправляем новое сообщение
        bot.send_message(user_id, game_states[text]['text'], reply_markup=key_chooser(game_states[text]['options']))
    else:
        bot.send_message(user_id, 'Неизвестная команда. Попробуйте ещё раз.')

# Запуск бота
bot.polling()