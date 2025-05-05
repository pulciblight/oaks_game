from telebot import types

start_keyboard = types.ReplyKeyboardMarkup(row_width=2)
button1 = types.KeyboardButton('Начать игру')
button2 = types.KeyboardButton('Узнать легенду')
start_keyboard.add(button1, button2)

sex_choose = types.ReplyKeyboardMarkup(row_width=2)
man = types.KeyboardButton('Девушка')
woman = types.KeyboardButton('Парень')
sex_choose.add(man, woman)

basic = types.ReplyKeyboardMarkup(row_width=2)
basic.add(types.KeyboardButton('Далее'))


def key_chooser(num_of_choices):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(1, num_of_choices + 1):
        keyboard.add(types.KeyboardButton(str(i)))
    return keyboard