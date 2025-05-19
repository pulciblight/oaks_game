from telebot import types

def key_chooser(options):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for option in options:
        keyboard.add(types.KeyboardButton(option))
    return keyboard
