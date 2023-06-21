# -*- coding: utf-8 -*-
import sqlite3

import telebot
from telebot import types

import formators as form

users_cache = {}

db_sql = sqlite3.connect('users.db')
cursor_sql = db_sql.cursor()

command_sql = """
CREATE TABLE IF NOT EXISTS users (
    id biginteger primary key,
    username text,
    first_name text,
    last_name text
);

CREATE TABLE IF NOT EXISTS transactions (
    id integer primary key,
    user_id biginteger,
    cost real,
    date text,
    category text
);

CREATE TABLE IF NOT EXISTS dreams (
    id integer primary key,
    user_id biginteger,
    dream text,
    date text,
    cost integer,
    priority integer
);
"""
cursor_sql.executescript(command_sql)
db_sql.commit()
cursor_sql.close()
root = {
    'pages': {
        'start': {
            'name': 'Добро пожаловать!',
            'content': '😜 Привет, я твой финансовый помощник! 💪 Я помогу тебе разобраться в основах финансовой грамотности и быть в курсе статистики своих доходов и расходов! 😄',
            'buttons': ['start'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        },
        'not_found': {
            'name': 'Ой...',
            'content': '😟 Мы тебя не поняли. Используй клавиатуру готовых ответов, чтобы такого не случалось.',
            'buttons': ['ok_sorry'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        },
        'main': {
            'name': 'Финансовый помощник',
            'content': '🤨 Что тебя сюда привело?',
            'buttons': ['learn', 'count'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        },
        'learn': {
            'name': 'Уроки по финансовой грамотности',
            'content': '😉 Из выпадающего списка, выбери материал для изучения',
            'buttons': ['learn_finance', 'learn_save_money', 'main_back'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        },
        'lesson_finance': {
            'name': 'Что такое финансовая грамотность?',
            'content': 'Финансовая грамотность - это умение хранить и распределять свои денежные сбережения, а также сохранять своё благосостояние и качество жизни.\n\nФинансово грамотным человеком является тот, кто умеет обращаться со своим имуществом и деньгами, а также знает как тратить и экономить деньги.\n\nНадеюсь вам понравилась статья 😉',
            'buttons': ['learn_back'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        },
        'lesson_save_money': {
            'name': 'Как начать копить деньги?',
            'content': 'Хочешь купить велосипед? Тогда начни копить деньги. Чтобы начать копить деньги нужно просто откладывать небольшую сумму, полученную тобой, в копилку. Через некоторое время в ней наберётся достаточно денег.\n\nК примеру, ты хочешь купить велоспед, он стоит 5000 рублей. Родители каждую неделю дают тебе 1500 рублей в карманные деньги, а после школы ты ходишь на подработку, где тебе платят 500 рублей за один день работы. То есть за неделю ты получаешь 500 × 7 = 3500 рублей. Складываем с карманными деньгами: получается 3500 + 1500 = 5000 рублей. Откладываем 500 рублей в копилку. И получается, что если мы поделим цену велосипеда на 500 рублей, то мы получим количество недель, через которые деньги на велосипед будут накоплены. 5000 ÷ 500 = 10 недель. Значит, откладывая по 10% в месяц, мы сможем купить велосипед уже через 10 недель (2 с чем-то месяца).\n\nТеперь ты знаешь как копить деньги!\n\nНадеюсь вам понравилась статья 😉',
            'buttons': ['learn_back'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        },
        'earnings': {
            'name': 'Доходы и расходы',
            'content': form.earnings_formator,
            'buttons': ['pay-in', 'pay-out', 'main_back'],
            'inline_buttons': ['analyse', 'dreams'],
            'inline_name': 'Услуги по финансам',
            'inline_content': '🤗 Также мы можем предложить тебе некоторые услуги по твоим доходам и расходам'
        },
        'transaction': {
            'name': 'Введи значение',
            'content': form.transaction_formator,
            'buttons': ['transaction_back'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        },
        'transaction_category': {
            'name': 'Категория',
            'content': '🤝 Выбери категорию транзакции из выпадающего списка',
            'buttons': form.transaction_category_formator,
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        },
        'analyse': {
            'name': 'Анализируем ваши доходы и расходы...',
            'content': form.analyse_formator,
            'buttons': ['analyse_back'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        },
        'dreams': {
            'name': 'Список желаний',
            'content': form.dreams_formator,
            'buttons': ['wish', 'dreams_back'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        },
        'wish': {
            'name': 'Добавление в список желаний',
            'content': '🤝 Что ты собираешься добавить в список желаний? Напиши словами. Не пиши длиннее 32 символов.',
            'buttons': ['wish_back'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        },
        'wish_cost': {
            'name': 'Добавление в список желаний',
            'content': '🤝 Напиши стоимость желаемого в рублях. Мы поможем тебе накопить эту сумму денег, исходя из ваших расходов и доходов во вкладке "Анализировать расходы".',
            'buttons': ['wish_back'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        }
    },
    'buttons': {
        'start': {
            'name': '🤩 Ого',
            'redirect': 'main'
        },
        'ok_sorry': {
            'name': '😏 Окей',
            'redirect': 'main'
        },
        'learn': {
            'name': '🤑 Я бы хотел побольше узнать о финансовой грамотности',
            'redirect': 'learn'
        },
        'count': {
            'name': '🤓 Я бы хотел подсчитать свои доходы и расходы',
            'redirect': 'earnings'
        },
        'learn_finance': {
            'name': '💵 Что такое финансовая грамотность?',
            'redirect': 'lesson_finance'
        },
        'learn_save_money': {
            'name': '💵 Как начать копить деньги?',
            'redirect': 'lesson_save_money'
        },
        'learn_back': {
            'name': '👍 Спасибо за информацию',
            'redirect': 'learn'
        },
        'main_back': {
            'name': '↩️ Назад',
            'redirect': 'main'
        },
        'pay-in': {
            'name': '📈 Внести доход',
            'redirect': 'transaction'
        },
        'pay-out': {
            'name': '📉 Внести расход',
            'redirect': 'transaction'
        },
        'transaction_back': {
            'name': '❌ Отмена',
            'redirect': 'earnings'
        },
        'transaction_category_entertainment': {
            'name': '🎉 Развлечения',
            'redirect': 'earnings'
        },
        'transaction_category_food': {
            'name': '🍔 Еда',
            'redirect': 'earnings'
        },
        'transaction_category_knowledges': {
            'name': '🎓 Учёба',
            'redirect': 'earnings'
        },
        'transaction_category_item': {
            'name': '🚲 Вещь',
            'redirect': 'earnings'
        },
        'transaction_category_job': {
            'name': '💼 Работа',
            'redirect': 'earnings'
        },
        'transaction_category_gift': {
            'name': '🎁 Подарок',
            'redirect': 'earnings'
        },
        'transaction_category_pocket_money': {
            'name': '📔 Карманные деньги',
            'redirect': 'earnings'
        },
        'transaction_category_win': {
            'name': '💸 Выигрыш / Призовой фонд',
            'redirect': 'earnings'
        },
        'analyse_back': {
            'name': '😅 Хорошо',
            'redirect': 'earnings'
        },
        'dreams_back': {
            'name': '↩️ Выйти из списка желаний',
            'redirect': 'earnings'
        },
        'wish': {
            'name': '🤩 Добавить в список желаний',
            'redirect': 'wish'
        },
        'wish_back': {
            'name': '🚫 Отмена',
            'redirect': 'dreams'
        }
    },
    'inline_buttons': {
        'analyse': {
            'name': '〽️ Анализировать расходы',
            'redirect': 'analyse'
        },
        'dreams': {
            'name': '✴️ Список желаний',
            'redirect': 'wish'
        }
    }
}
db_sql.close()

bot = telebot.TeleBot('5742123865:AAEZU3tnVMjVR3pL4x4scKb1RF2qKHcU5MY')


def render_page(message, markup, inline_markup, page):
    if root['pages'][page]['inline_name'] is not None:
        inline_answer = f"*• {root['pages'][page]['inline_name']}*\n\n{root['pages'][page]['inline_content']}"
    else:
        inline_answer = None

    answer = f"*• {root['pages'][page]['name']}*\n\n"
    if isinstance(root['pages'][page]['content'], str):
        answer = answer + root['pages'][page]['content']
    else:
        answer = answer + root['pages'][page]['content'](message, users_cache[message.from_user.id])

    if isinstance(root['pages'][page]['buttons'], list):
        for button in root['pages'][page]['buttons']:
            markup.add(types.KeyboardButton(root['buttons'][button]['name']))
    else:
        for button in root['pages'][page]['buttons'](message, users_cache[message.from_user.id]):
            markup.add(types.KeyboardButton(root['buttons'][button]['name']))

    for button in root['pages'][page]['inline_buttons']:
        inline_markup.add(types.InlineKeyboardButton(text=root['inline_buttons'][button]['name'], callback_data=button))

    return {
        'answer': answer,
        'inline_answer': inline_answer
    }


@bot.message_handler(commands=['start'])
def start_message(message):
    print(message)
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    command = """
    INSERT OR IGNORE INTO users (id, username, first_name, last_name) VALUES (?, ?, ?, ?);
    """
    cursor.execute(command, [message.from_user.id,
                             message.from_user.username,
                             message.from_user.first_name,
                             message.from_user.last_name])
    db.commit()
    cursor.close()
    db.close()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    inline_markup = types.InlineKeyboardMarkup()
    render = render_page(message, markup, inline_markup, 'start')
    bot.send_message(message.chat.id, render['answer'], reply_markup=markup, parse_mode="Markdown")


@bot.message_handler(content_types=['text'])
def new_message(message):
    try:
        users_cache[message.from_user.id]
    except KeyError:
        users_cache[message.from_user.id] = {'page': None}

    page = None
    render = None
    for button in root['buttons']:
        if message.text == root['buttons'][button]['name']:
            page = root['buttons'][button]['redirect']
            break

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    inline_markup = types.InlineKeyboardMarkup()

    if page is not None:
        if users_cache[message.from_user.id]['page'] == 'transaction_category':
            if button != 'transaction_back' and button != 'ok_sorry':
                users_cache[message.from_user.id]['category'] = button
        render = render_page(message, markup, inline_markup, page)
        users_cache[message.from_user.id]['page'] = page
    elif users_cache[message.from_user.id]['page'] == 'transaction':
        try:
            float(message.text)
        except ValueError:
            bot.send_message(message.chat.id, '❌ Ты вписал не число!')
        else:
            if round(float(message.text), 2) > 250000:
                bot.send_message(message.chat.id, '❌ Так много!? Не верим!')
            else:
                if round(float(message.text), 2) < 1:
                    bot.send_message(message.chat.id, '❌ Слишком маленькое значение!')
                else:
                    users_cache[message.from_user.id]['cost'] = round(float(message.text), 2)
                    render = render_page(message, markup, inline_markup, 'transaction_category')
                    users_cache[message.from_user.id]['page'] = 'transaction_category'
    elif users_cache[message.from_user.id]['page'] == 'wish':
        if 32 >= len(message.text) > 1:
            users_cache[message.from_user.id]['wish_name'] = message.text
            render = render_page(message, markup, inline_markup, 'wish_cost')
            users_cache[message.from_user.id]['page'] = 'wish_cost'
        else:
            bot.send_message(message.chat.id, '❌ Название желания должно быть от 2 до 32 символов!')
    else:
        render = render_page(message, markup, inline_markup, 'not_found')

    if render is not None:
        bot.send_message(message.chat.id, render['answer'], reply_markup=markup, parse_mode="Markdown")
        if len(inline_markup.keyboard) > 0:
            bot.send_message(message.chat.id, render['inline_answer'], reply_markup=inline_markup,
                             parse_mode="Markdown")


@bot.callback_query_handler(func=lambda c: True)
def button_pressed(query):
    bot.edit_message_reply_markup(query.message.chat.id, query.message.id, reply_markup=None)
    try:
        users_cache[query.from_user.id]
    except KeyError:
        users_cache[query.from_user.id] = {'page': None}

    render = None
    page = root['inline_buttons'][query.data]['redirect']

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    inline_markup = types.InlineKeyboardMarkup()

    if page is not None:
        render = render_page(query, markup, inline_markup, page)
    else:
        render = render_page(query, markup, inline_markup, 'not_found')

    if render is not None:
        bot.send_message(query.message.chat.id, render['answer'], reply_markup=markup, parse_mode="Markdown")
        if len(inline_markup.keyboard) > 0:
            bot.send_message(query.message.chat.id, render['inline_answer'], reply_markup=inline_markup, parse_mode="Markdown")


bot.infinity_polling()
