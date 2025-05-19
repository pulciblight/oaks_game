import telebot
import copy
from telebot import types
from states import start_states
from m_states import states_m
from f_states import states_f
from clava import key_chooser
from resources import resource, important_events

API_TOKEN = '7842674848:AAHaZqKSI2gplCBCPo89O52YJXauRz3DuNU'
bot = telebot.TeleBot(API_TOKEN)
users_data = dict()
basic_resources = resource
scenario = start_states.copy()
command_list = [
    types.BotCommand('start', 'Начать новую игру'),
    types.BotCommand('status', 'Посмотреть текущее состояние персонажа'),
    types.BotCommand('help', 'Узнать легенду и создателей')
]
bot.set_my_commands(command_list)
bot.set_chat_menu_button(menu_button=types.MenuButtonCommands())
@bot.message_handler(commands=['start', 'status', 'help'])
def handle_commands(message):
    user_id = message.chat.id
    if message.text == '/start':
        users_data[user_id] = copy.deepcopy(basic_resources)
        bot.send_message(user_id, scenario['start']['text'],
                        reply_markup=key_chooser(start_states['start']['options']))
    elif message.text == '/status':
        if 'Начать игру' in users_data[user_id]['Выборы']:
            current_status = []
            for key in users_data[user_id]['Ресурсы']:
                current_status.append(f'{key}: {users_data[user_id]['Ресурсы'][key]}')
            current_status = '\n'.join(current_status)
            bot.send_message(user_id, current_status)
        else:
            bot.send_message(user_id, 'Сначала начните игру!')
    elif message.text == '/help':
        bot.send_message(user_id, scenario['Узнать легенду']['text'])

@bot.message_handler(func=lambda message: message.text in scenario.keys())
def finally_game(message):
    user_id = message.chat.id
    text = message.text
    if 'conseq' in scenario[text].keys():
        for key in scenario[text]['conseq']:
            users_data[user_id]['Ресурсы'][key] += scenario[text]['conseq'][key]
    if 'picture' not in scenario[text].keys():
        bot.send_message(user_id, scenario[text]['text'],
                         reply_markup=key_chooser(scenario[text]['options']))
    else:
        bot.send_photo(user_id, scenario[text]['picture'],
                       caption=scenario[text]['text'],
                       reply_markup=key_chooser(scenario[text]['options']))
    if text in important_events:
        users_data[user_id]['Выборы'].append(text)

@bot.message_handler(func=lambda message: message.text in ['Женский', 'Мужской'])
def sex_assignment(message):
    global scenario
    user_id = message.chat.id
    text = message.text
    if text == 'Женский':
        users_data[user_id]['Пол'] = 'ж'
    elif text == 'Мужской':
        users_data[user_id]['Пол'] = 'м'
    if users_data[user_id]['Пол'] == 'ж':
        scenario.update(states_f)
    elif users_data[user_id]['Пол'] == 'м':
        scenario.update(states_m)
    bot.send_message(user_id, scenario['Начало']['text'],
                     reply_markup=key_chooser(scenario['Начало']['options']))
bot.polling()
