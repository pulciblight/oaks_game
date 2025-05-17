import telebot
from telebot import types
from states import start_states
from m_states import states_m
from f_states import states_f
from clava import key_chooser
from resources import resource

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
def handle_start(message):
    global basic_resources
    user_id = message.from_user.id
    if message.text == '/start':
        users_data[user_id] = basic_resources
        bot.send_message(user_id, scenario['start']['text'],
                        reply_markup=key_chooser(start_states['start']['options']))
    elif message.text == '/status':
        current_status = []
        for key in users_data[user_id]['Ресурсы']:
            current_status.append(f'{key}: {users_data[user_id]['Ресурсы'][key]}')
        current_status = '\n'.join(current_status)
        bot.send_message(user_id, current_status)
    elif message.text == '/help':
        bot.send_message(user_id, scenario['Узнать легенду']['text'])

@bot.message_handler(func=lambda message: message.text in scenario.keys())
def handle_message(message):
    user_id = message.from_user.id
    text = message.text
    bot.send_message(user_id, start_states[text]['text'],
                     reply_markup=key_chooser(start_states[text]['options']))


@bot.message_handler(func=lambda message: message.text in ['Женский', 'Мужской'])
def sex_assignment(message):
    global scenario
    user_id = message.from_user.id
    text = message.text
    if text == 'Женский':
        scenario = states_f.copy()
    elif text == 'Мужской':
        scenario = states_m.copy()
    bot.send_message(user_id, scenario[text]['text'],
                     reply_markup=key_chooser(scenario[text]['options']))

@bot.message_handler(func=lambda message: message.text in scenario.keys())
def finally_game(message):
    global user_resource, res_not
    user_id = message.from_user.id
    text = message.text
    res_not = ''
    if 'conseq' in scenario[text].keys():
        add_phrase = []
        for key in scenario[text]['conseq']:
            user_resource[key] += scenario[text]['conseq'][key]
            add_phrase.append(f'\n{key}: {user_resource[key]}.')
        res_not = "".join(add_phrase)
    if 'picture' not in scenario[text].keys():
        bot.send_message(user_id, scenario[text]['text'] + res_not,
                         reply_markup=key_chooser(scenario[text]['options']))
    else:
        bot.send_photo(user_id, scenario[text]['picture'],
                       caption=scenario[text]['text'] + res_not,
                       reply_markup=key_chooser(scenario[text]['options']))
bot.polling()