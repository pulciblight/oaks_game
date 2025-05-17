import telebot
from states import start_states
from m_states import states_m
from f_states import states_f
from clava import key_chooser
from res import resource

API_TOKEN = '7842674848:AAHaZqKSI2gplCBCPo89O52YJXauRz3DuNU'
bot = telebot.TeleBot(API_TOKEN)
user_resource = resource.copy()

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, start_states['start']['text'],
                    reply_markup=key_chooser(start_states['start']['options']))


@bot.message_handler(func=lambda message: message.text in ['Начать игру', 'Узнать легенду'])
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