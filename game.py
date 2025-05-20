import telebot
import copy
import random
from telebot import types
from states import start_states
from m_states import states_m
from f_states import states_f
from clava import key_chooser
from resources import resource, day_ends

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
        if 'Начало' in users_data[user_id]['Выборы']:
            current_status = []
            for key in users_data[user_id]['Ресурсы']:
                current_status.append(f'{key}: {users_data[user_id]['Ресурсы'][key]}')
            current_status = '\n'.join(current_status)
            bot.send_message(user_id, current_status, parse_mode="HTML")
        else:
            bot.send_message(user_id, 'Сначала начните игру!')
    elif message.text == '/help':
        bot.send_message(user_id, scenario['Узнать легенду']['text'])

@bot.message_handler(func=lambda message: message.text in scenario.keys())
def finally_game(message):
    user_id = message.chat.id
    text = message.text
    if users_data[user_id]['Ресурсы']['Жизни'] < 1:
        bot.send_photo(user_id, scenario['Смерть']['picture'],
                       caption=scenario['Смерть']['text'],
                       reply_markup=key_chooser(scenario['Смерть']['options']), parse_mode="HTML")
        if users_data[user_id]['Пол'] == 'ж':
            users_data[user_id] = copy.deepcopy(basic_resources)
            users_data[user_id]['Пол'] = 'ж'
        else:
            users_data[user_id] = copy.deepcopy(basic_resources)
            users_data[user_id]['Пол'] = 'м'
        users_data[user_id]['Выборы'].append('Начало')
        return
    if users_data[user_id]['Ресурсы']['Дисциплинарки'] == 3:
        bot.send_photo(user_id, scenario['Дисциплине конец']['picture'],
                       caption=scenario['Дисциплине конец']['text'],
                       reply_markup=key_chooser(scenario['Дисциплине конец']['options']), parse_mode="HTML")
        if users_data[user_id]['Пол'] == 'ж':
            users_data[user_id] = copy.deepcopy(basic_resources)
            users_data[user_id]['Пол'] = 'ж'
        else:
            users_data[user_id] = copy.deepcopy(basic_resources)
            users_data[user_id]['Пол'] = 'м'
        users_data[user_id]['Выборы'].append('Начало')
        return
    if text in day_ends:
        current_status = []
        for key in users_data[user_id]['Ресурсы']:
            current_status.append(f'{key}: {users_data[user_id]['Ресурсы'][key]}')
        current_status = '\n'.join(current_status)
        index, tip = random.choice(list(users_data[user_id]['Советы'].items()))
        scenario[text]['addtext'] = f'\n\n{current_status}\n\n<b>Совет:</b>\n{tip['text']}'
        scenario[text]['picture'] = tip['picture']
        del users_data[user_id]['Советы'][index]
    if text == 'Начать второй день' and 'Экзамен' in users_data[user_id]['Выборы']:
        scenario[text]['text'] = ('Доброе утро! Надо привести себя в приличный вид и подключать прокторинг для экзамена. '
                                'Ты умываешься, достаешь из стиралки сырую, но чистую футболку и садишься за ноутбук. '
                                'Экзамен начался. Удачи!')
        scenario[text]['picture'] = 'https://raw.githubusercontent.com/pulciblight/stuff/refs/heads/main/pics/proctor.jpg'
        scenario[text]['options'] = ['1 вопрос']
    if text == 'Далее' and 'Дисциплинарка на экзе' in users_data[user_id]['Выборы']:
        scenario[text]['text'] = ('Спустя какое-то время после начала экзамена '
                                  'дверь в твою комнату резко открывается. Упс, твой сосед понял, '
                                  'кто вчера с утра съел его бутерброд. Он начинает очень громко на тебя кричать. '
                                  'Твой проктор посчитал это нарушением порядка проведения экзамена.'
                                  '\n\nТы получил <b>1</b> дисциплинарку и потерял <b>1 балл</b> репутации')
        scenario[text]['conseq'] = {'Дисциплинарки': 1, 'Репутация': -1}
        scenario[text]['options'] = ['Надо заняться делами']
    if text == 'Конечно хочу!' and 'Не ответил на вопрос' in users_data[user_id]['Выборы']:
        scenario[text]['text'] = 'Ты соглашаешься. Вечер будет весёлый!'
        scenario[text]['happened'] = 'Приехал любимый зять будем пить пииво'
        scenario[text]['options'] = ['Закончить пару']
        del scenario[text]['conseq']
    if text == 'Продолжить развлечения' and users_data[user_id]['Ресурсы']['Репутация'] > -3:
        scenario[text]['text'] = ('Тебе пришло сообщение от соседа: '
                                  '«Можно потише, вас очень хорошо слышно в соседних комнатах! '
                                  'У меня уже голова болит от вашего ора». Пришлось стать тише.')
        scenario[text]['options'] = ['Надо придумать, чем заняться вечером.']
    if text == 'Пойти на стадион' and users_data[user_id]['Ресурсы']['Жизни'] < 3:
        scenario[text]['text'] = ('Ты зашёл на стадион. Ты не знал, что перед бегом нужно размяться, '
                                  'и побежал сразу. На середине круга у тебя что-то защемило в ноге '
                                  'и ты упал прямо перед группой подростков. Раздался неприятный смех. '
                                  'Кажется, тебя засмеяли местные дети, но тем не менее ты размялся!'
                                  '\n\nТы заработал <b>1</b> жизнь')
        scenario[text]['options'] = ['Вернуться домой']
        scenario[text]['conseq'] = {'Жизни': +1}
    if 'conseq' in scenario[text].keys():
        for key in scenario[text]['conseq']:
            users_data[user_id]['Ресурсы'][key] += scenario[text]['conseq'][key]
    if 'picture' not in scenario[text].keys():
        bot.send_message(user_id, scenario[text]['text'],
                         reply_markup=key_chooser(scenario[text]['options']), parse_mode="HTML")
    elif 'addtext' in scenario[text].keys():
        bot.send_photo(user_id, scenario[text]['picture'],
                       caption=scenario[text]['text']+scenario[text]['addtext'],
                       reply_markup=key_chooser(scenario[text]['options']), parse_mode="HTML")
    else:
        bot.send_photo(user_id, scenario[text]['picture'],
                       caption=scenario[text]['text'],
                       reply_markup=key_chooser(scenario[text]['options']), parse_mode="HTML")
    if 'happened' in scenario[text].keys():
        users_data[user_id]['Выборы'].append(scenario[text]['happened'])
    if text == 'Начать заново':
        if users_data[user_id]['Пол'] == 'ж':
            users_data[user_id] = copy.deepcopy(basic_resources)
            users_data[user_id]['Пол'] = 'ж'
        else:
            users_data[user_id] = copy.deepcopy(basic_resources)
            users_data[user_id]['Пол'] = 'м'
        users_data[user_id]['Выборы'].append('Начало')

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