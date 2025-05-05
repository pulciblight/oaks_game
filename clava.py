from telebot import types
from repliki import scenario
keyboard1 = types.ReplyKeyboardMarkup(row_width=2)
button1 = types.KeyboardButton('Начать игру')
button2 = types.KeyboardButton('Узнать легенду')
keyboard1.add(button1, button2)
def key_chooser(text):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    if scenario[text] == 1:
        continued = types.KeyboardButton('Далее')
        keyboard.add(continued)
    elif scenario[text] == 2:
        button1 = types.KeyboardButton('Написать в чат, что у тебя не работает микрофон: Отлично! Преподаватель поверил тебе и спросил твоего одногруппника.')
        button2 = types.KeyboardButton('Ответить на вопрос своими словами и попытаться заболтать преподавателя')
        keyboard.add(button1, button2)
    legend = types.KeyboardButton('Ресурсы')
    keyboard.add(legend)
    return keyboard