import time
import sqlite3


categories = {
    'transaction_category_job': '💼 Работа',
    'transaction_category_gift': '🎁 Подарок',
    'transaction_category_pocket_money': '📔 Карманные деньги',
    'transaction_category_win': '💸 Выигрыш / Призовой фонд',
    'transaction_category_entertainment': '🎉 Развлечения',
    'transaction_category_food': '🍔 Еда',
    'transaction_category_knowledges': '🎓 Учёба',
    'transaction_category_item': '🚲 Вещь'
}

def earnings_formator(message, user_cache):
    try:
        if 'category' in user_cache.keys():
            with sqlite3.connect('users.db') as db:
                cursor = db.cursor()
                command = """
                INSERT INTO transactions (user_id, cost, date, category) VALUES (?, ?, ?, ?)
                """
                cursor.execute(command, [message.from_user.id,
                                         user_cache['cost'] * user_cache['multy'],
                                         time.strftime('%m.%Y'),
                                         user_cache['category']])
                cursor.close()
                db.commit()
    finally:
        try:
            del user_cache['multy']
            del user_cache['cost']
            del user_cache['category']
        finally:
            with sqlite3.connect('users.db') as db:
                cursor = db.cursor()
                transactions = list(cursor.execute('SELECT * FROM transactions WHERE user_id = ? AND date = ?', [message.from_user.id, time.strftime('%m.%Y')]))
                cursor.close()

            if len(transactions) > 0:
                text = '🧐 Все ваши доходы и расходы за этот месяц находятся тут:\n\n'
                money = 0
                index = 0
                for transaction in transactions:
                    money += transaction[2]
                    if transaction[2] > 0:
                        text = text + f'*{index + 1}.* 📈 Доход на сумму в *{str(transaction[2])}* руб.'
                    else:
                        text = text + f'*{index + 1}.* 📉 Расход на сумму в *{str(- transaction[2])}* руб.'
                    text = text + f' ({categories[transaction[4]]})\n'
                    index += 1
                text = text + f'\n\n😉 Итого: _у вас осталось_ *{str(money)}* _рублей_'
            else:
                text = 'История доходов и расходов пуста 😥'

            return text


def transaction_formator(message, user_cache):
    text = '🤝 Напиши в чат число, которое будет означать количество денег, входящих в транзакцию.'

    if message.text == '📉 Внести расход':
        user_cache['multy'] = -1
    else:
        user_cache['multy'] = 1

    return text


def transaction_category_formator(message, user_cache):
    if user_cache['multy'] == 1:
        buttons = ['transaction_category_job',
                   'transaction_category_gift',
                   'transaction_category_pocket_money',
                   'transaction_category_win']
    else:
        buttons = ['transaction_category_entertainment',
                   'transaction_category_food',
                   'transaction_category_knowledges',
                   'transaction_category_item']

    buttons.append('transaction_back')

    return buttons


def analyse_formator(message, user_cache):
    with sqlite3.connect('users.db') as db:
        cursor = db.cursor()
        command = """
        SELECT * FROM transactions WHERE user_id = ? AND date = ?
        """
        transactions = list(cursor.execute(command, [message.from_user.id, time.strftime('%m.%Y')]))
        cursor.close()

    if len(transactions) > 5:
        balance = 0
        all_money = 0
        for transaction in transactions:
            balance += transaction[2]
            all_money += abs(transaction[2])

        if balance / all_money > 0.1:
            text = '😄 Всё нормально!'
        else:
            text = '😕 Вы слишком много тратите! Чтобы копить деньги оставляйте хотя-бы по 10% от своего дохода.'

    else:
        text = '😴 Недостаточно данных для анализирования финансов'

    return text


def dreams_formator(message, user_cache):
    with sqlite3.connect('users.db') as db:
        cursor = db.cursor()
        command = """
        SELECT * FROM dreams WHERE user_id = ?
        """
        transactions = list(cursor.execute(command, [message.from_user.id]))
        cursor.close()
    if len(transactions) > 0:
        print('')
        # тут что-то должно быть
    else:
        text = '😯 Список желаний пуст!'

    return text
