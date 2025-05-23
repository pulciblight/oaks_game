import telebot
import copy
import random
from telebot import types
from states import start_states
from m_states import states_m
from f_states import states_f
from clava import key_chooser, alternate_scenario
from resources import resource, day_ends, tips

API_TOKEN = '7842674848:AAHaZqKSI2gplCBCPo89O52YJXauRz3DuNU'
bot = telebot.TeleBot(API_TOKEN)
users_data = dict()
basic_resources = resource
original_scene = copy.deepcopy(start_states)
original_scene_f = copy.deepcopy(states_f)
original_scene_m = copy.deepcopy(states_m)
scenario = copy.deepcopy(start_states)
command_list = [
    types.BotCommand('start', 'Начать новую игру'),
    types.BotCommand('status', 'Посмотреть текущее состояние персонажа'),
    types.BotCommand('help', 'Узнать правила игры')
]
bot.set_my_commands(command_list)
bot.set_chat_menu_button(menu_button=types.MenuButtonCommands())
@bot.message_handler(commands=['start', 'status', 'help'])
def handle_commands(message):
    global scenario
    user_id = message.chat.id
    if message.text == '/start':
        users_data[user_id] = copy.deepcopy(basic_resources)
        users_data[user_id]['scene'] = copy.deepcopy(original_scene)
        scenario = copy.deepcopy(original_scene)
        bot.send_message(user_id, scenario['start']['text'],
                        reply_markup=key_chooser(scenario['start']['options']))
    elif message.text == '/status':
        if user_id not in users_data or 'Начало' not in users_data[user_id]['Выборы']:
            bot.send_message(user_id, 'Сначала начните игру!')
        else:
            current_status = []
            for key in users_data[user_id]['Ресурсы']:
                current_status.append(f'{key}: {users_data[user_id]['Ресурсы'][key]}')
            current_status = '\n'.join(current_status)
            bot.send_message(user_id, current_status, parse_mode="HTML")
    elif message.text == '/help':
        bot.send_message(user_id, scenario['help']['text'])

@bot.message_handler(func=lambda message: message.text in scenario.keys())
def finally_game(message):
    user_id = message.chat.id
    text = message.text
    global scenario
    if users_data[user_id]['Ресурсы']['Жизни'] < 1:
        bot.send_photo(user_id, scenario['Смерть']['picture'],
                       caption=scenario['Смерть']['text'],
                       reply_markup=key_chooser(scenario['Смерть']['options']), parse_mode="HTML")
        if users_data[user_id]['Пол'] == 'ж':
            users_data[user_id] = copy.deepcopy(basic_resources)
            scenario.update(copy.deepcopy(original_scene_f))
            users_data[user_id]['scene'].update(copy.deepcopy(original_scene_f))
            users_data[user_id]['Пол'] = 'ж'
        else:
            users_data[user_id] = copy.deepcopy(basic_resources)
            scenario.update(copy.deepcopy(original_scene_m))
            users_data[user_id]['scene'].update(copy.deepcopy(original_scene_m))
            users_data[user_id]['Пол'] = 'м'
        users_data[user_id]['Выборы'].append('Начало')
        return
    if users_data[user_id]['Ресурсы']['Дисциплинарки'] == 3:
        bot.send_photo(user_id, scenario['Дисциплине конец']['picture'],
                       caption=scenario['Дисциплине конец']['text'],
                       reply_markup=key_chooser(scenario['Дисциплине конец']['options']), parse_mode="HTML")
        if users_data[user_id]['Пол'] == 'ж':
            users_data[user_id] = copy.deepcopy(basic_resources)
            scenario.update(copy.deepcopy(original_scene_f))
            users_data[user_id]['scene'].update(copy.deepcopy(original_scene_f))
            users_data[user_id]['Пол'] = 'ж'
        else:
            users_data[user_id] = copy.deepcopy(basic_resources)
            scenario.update(copy.deepcopy(original_scene_m))
            users_data[user_id]['scene'].update(copy.deepcopy(original_scene_m))
            users_data[user_id]['Пол'] = 'м'
        users_data[user_id]['Выборы'].append('Начало')
        return
    if text in day_ends:
        current_status = []
        for key in users_data[user_id]['Ресурсы']:
            current_status.append(f'{key}: {users_data[user_id]['Ресурсы'][key]}')
        current_status = '\n'.join(current_status)
        if not bool(users_data[user_id]['Советы']):
            users_data[user_id]['Советы'] = tips.copy()
        index, tip = random.choice(list(users_data[user_id]['Советы'].items()))
        users_data[user_id]['scene'][text]['addtext'] = f'\n\n{current_status}\n\n<b>Совет:</b>\n{tip['text']}'
        users_data[user_id]['scene'][text]['picture'] = tip['picture']
        del users_data[user_id]['Советы'][index]
    alternate_scenario(users_data[user_id]['scene'][text], text, users_data[user_id]['Выборы'],
                       users_data[user_id]['Пол'], users_data[user_id]['Ресурсы']['Жизни'],
                       users_data[user_id]['Ресурсы']['Репутация'],
                       users_data[user_id]['Ресурсы']['Дисциплинарки'],
                       users_data[user_id]['Ресурсы']['Деньги'])
    if 'conseq' in users_data[user_id]['scene'][text].keys():
        for key in users_data[user_id]['scene'][text]['conseq']:
            users_data[user_id]['Ресурсы'][key] += users_data[user_id]['scene'][text]['conseq'][key]
    if 'picture' not in users_data[user_id]['scene'][text].keys():
        if 'options' not in users_data[user_id]['scene'][text].keys():
            bot.send_message(user_id, users_data[user_id]['scene'][text]['text'], parse_mode="HTML")
        elif 'addtext' in users_data[user_id]['scene'][text].keys():
            bot.send_message(user_id, users_data[user_id]['scene'][text]['text'] + users_data[user_id]['scene'][text]['addtext'],
                             reply_markup=key_chooser(users_data[user_id]['scene'][text]['options']), parse_mode="HTML")
        else:
            bot.send_message(user_id, users_data[user_id]['scene'][text]['text'],
                             reply_markup=key_chooser(users_data[user_id]['scene'][text]['options']), parse_mode="HTML")
    elif 'addtext' in users_data[user_id]['scene'][text].keys():
        bot.send_photo(user_id, users_data[user_id]['scene'][text]['picture'],
                       caption=users_data[user_id]['scene'][text]['text']+users_data[user_id]['scene'][text]['addtext'],
                       reply_markup=key_chooser(users_data[user_id]['scene'][text]['options']), parse_mode="HTML")
    else:
        if users_data[user_id]['scene'][text]['picture'] == ('https://github.com/pulciblight/stuff/blob/main'
                                                             '/pics/shokschedule.jpg?raw=true'):
            bot.send_photo(user_id, users_data[user_id]['scene'][text]['picture'],
                           caption=users_data[user_id]['scene'][text]['text'], has_spoiler=True,
                           reply_markup=key_chooser(users_data[user_id]['scene'][text]['options']), parse_mode="HTML")
        else:
            bot.send_photo(user_id, users_data[user_id]['scene'][text]['picture'],
                           caption=users_data[user_id]['scene'][text]['text'],
                           reply_markup=key_chooser(users_data[user_id]['scene'][text]['options']), parse_mode="HTML")
    if 'happened' in users_data[user_id]['scene'][text].keys():
        users_data[user_id]['Выборы'].append(users_data[user_id]['scene'][text]['happened'])
    if text == 'Начать заново':
        if users_data[user_id]['Пол'] == 'ж':
            users_data[user_id] = copy.deepcopy(basic_resources)
            scenario.update(copy.deepcopy(original_scene_f))
            users_data[user_id]['scene'].update(copy.deepcopy(original_scene_f))
            users_data[user_id]['Пол'] = 'ж'
        else:
            users_data[user_id] = copy.deepcopy(basic_resources)
            scenario.update(copy.deepcopy(original_scene_m))
            users_data[user_id]['scene'].update(copy.deepcopy(original_scene_m))
            users_data[user_id]['Пол'] = 'м'
        users_data[user_id]['Выборы'].append('Начало')

@bot.message_handler(func=lambda message: message.text in ['Женский', 'Мужской'])
def sex_assignment(message):
    user_id = message.chat.id
    text = message.text
    global scenario
    if text == 'Женский':
        users_data[user_id]['Пол'] = 'ж'
        scenario.update(copy.deepcopy(original_scene_f))
        users_data[user_id]['scene'].update(copy.deepcopy(original_scene_f))
    else:
        users_data[user_id]['Пол'] = 'м'
        scenario.update(copy.deepcopy(original_scene_m))
        users_data[user_id]['scene'].update(copy.deepcopy(original_scene_m))
    bot.send_message(user_id, scenario['Начало']['text'],
                     reply_markup=key_chooser(scenario['Начало']['options']),
                     parse_mode="HTML")
bot.polling()