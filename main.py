# -*- coding: utf-8 -*-
import sqlite3

import time

import telebot
from telebot import types

import formators as form

import math

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
    day integer,
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
from pages import root
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
            if math.isnan(float(message.text)):
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
    elif users_cache[message.from_user.id]['page'] == 'transaction_clear':
        if message.text.lower() in ['всё', 'all', 'все']:
            users_cache[message.from_user.id]['transaction_clear'] = '*'
            render = render_page(message, markup, inline_markup, 'earnings')
            users_cache[message.from_user.id]['page'] = 'earnings'
        else:
            try:
                int(message.text)
            except ValueError:
                bot.send_message(message.chat.id, '❌ Ты вписал не число!')
            else:
                if math.isnan(int(message.text)):
                    bot.send_message(message.chat.id, '❌ Ты вписал не число!')
                else:
                    with sqlite3.connect('users.db') as db:
                        cursor = db.cursor()
                        command = """
                               SELECT * FROM transactions WHERE user_id = ? AND date = ?
                               """
                        transactions = list(cursor.execute(command, [message.from_user.id, time.strftime('%m.%Y')]))
                        cursor.close()

                    if len(transactions) >= int(message.text) >= 1:
                        users_cache[message.from_user.id]['transaction_clear'] = int(message.text)
                        render = render_page(message, markup, inline_markup, 'earnings')
                        users_cache[message.from_user.id]['page'] = 'earnings'
                    else:
                        bot.send_message(message.chat.id, '❌ Твоё число вне диапазона транзакций!')

    elif users_cache[message.from_user.id]['page'] == 'wish':
        if 32 >= len(message.text) > 1:
            users_cache[message.from_user.id]['wish_name'] = message.text
            render = render_page(message, markup, inline_markup, 'wish_cost')
            users_cache[message.from_user.id]['page'] = 'wish_cost'
        else:
            bot.send_message(message.chat.id, '❌ Название желания должно быть от 2 до 32 символов!')
    elif users_cache[message.from_user.id]['page'] == 'wish_cost':
        try:
            float(message.text)
        except ValueError:
            bot.send_message(message.chat.id, '❌ Ты вписал не число!')
        else:
            if math.isnan(float(message.text)):
                bot.send_message(message.chat.id, '❌ Ты вписал не число!')
            else:
                if round(float(message.text), 2) > 1500000:
                    bot.send_message(message.chat.id, '❌ Так много!? Не верим!')
                else:
                    if round(float(message.text), 2) < 10:
                        bot.send_message(message.chat.id, '❌ Слишком маленькое значение!')
                    else:
                        users_cache[message.from_user.id]['wish_cost'] = round(float(message.text), 2)
                        render = render_page(message, markup, inline_markup, 'dreams')
                        users_cache[message.from_user.id]['page'] = 'dreams'
    elif users_cache[message.from_user.id]['page'] == 'wish_priority':
        try:
            int(message.text)
        except ValueError:
            bot.send_message(message.chat.id, '❌ Ты вписал не число!')
        else:
            if math.isnan(int(message.text)):
                bot.send_message(message.chat.id, '❌ Ты вписал не число!')
            else:
                with sqlite3.connect('users.db') as db:
                    cursor = db.cursor()
                    command = """
                           SELECT * FROM dreams WHERE user_id = ? ORDER BY priority ASC
                           """
                    dreams = list(cursor.execute(command, [message.from_user.id]))
                    cursor.close()
                if int(message.text) > len(dreams) or int(message.text) < 1:
                    bot.send_message(message.chat.id, '❌ Идентификатор вне диапазона твоих желаний!')
                else:
                    users_cache[message.from_user.id]['wish_id'] = int(message.text)
                    render = render_page(message, markup, inline_markup, 'wish_priority_place')
                    users_cache[message.from_user.id]['page'] = 'wish_priority_place'
    elif users_cache[message.from_user.id]['page'] == 'wish_priority_place':
        try:
            int(message.text)
        except ValueError:
            bot.send_message(message.chat.id, '❌ Ты вписал не число!')
        else:
            if math.isnan(int(message.text)):
                bot.send_message(message.chat.id, '❌ Ты вписал не число!')
            else:
                if 100 >= int(message.text) >= 1:
                    users_cache[message.from_user.id]['wish_priority'] = int(message.text)
                    render = render_page(message, markup, inline_markup, 'dreams')
                    users_cache[message.from_user.id]['page'] = 'dreams'
                else:
                    bot.send_message(message.chat.id, '❌ Твоё число не соответствует диапазону от 1 до 100!')
    elif users_cache[message.from_user.id]['page'] == 'wish_remove':
        try:
            int(message.text)
        except ValueError:
            bot.send_message(message.chat.id, '❌ Ты вписал не число!')
        else:
            if math.isnan(int(message.text)):
                bot.send_message(message.chat.id, '❌ Ты вписал не число!')
            else:
                with sqlite3.connect('users.db') as db:
                    cursor = db.cursor()
                    command = """
                           SELECT * FROM dreams WHERE user_id = ? ORDER BY priority ASC
                           """
                    dreams = list(cursor.execute(command, [message.from_user.id]))
                    cursor.close()
                if int(message.text) > len(dreams) or int(message.text) < 1:
                    bot.send_message(message.chat.id, '❌ Идентификатор вне диапазона твоих желаний!')
                else:
                    users_cache[message.from_user.id]['wish_remove_id'] = int(message.text)
                    render = render_page(message, markup, inline_markup, 'dreams')
                    users_cache[message.from_user.id]['page'] = 'dreams'
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
            bot.send_message(query.message.chat.id, render['inline_answer'], reply_markup=inline_markup,
                             parse_mode="Markdown")


bot.infinity_polling()
