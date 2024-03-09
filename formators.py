import time
import datetime
import sqlite3
import math

categories = {
    'transaction_category_job': '💼 Работа',
    'transaction_category_gift': '🎁 Подарок',
    'transaction_category_pocket_money': '📔 Карманные деньги',
    'transaction_category_win': '💸 Выигрыш / Призовой фонд',
    'transaction_category_entertainment': '🎉 Развлечения',
    'transaction_category_food': '🍔 Еда',
    'transaction_category_knowledges': '🎓 Учёба',
    'transaction_category_item': '🚲 Вещь',
    'transaction_category_transport': '🚕 Транспорт',
    'transaction_category_products': '🍎 Продукты',
    'transaction_category_clothes': '👕 Одежда'
}


def earnings_formator(message, user_cache):
    try:
        if 'transaction_clear' in user_cache.keys():
            with sqlite3.connect('users.db') as db:
                cursor = db.cursor()
                if user_cache['transaction_clear'] == '*':
                    command = """
                    DELETE FROM transactions WHERE user_id = ?
                    """
                    cursor.execute(command, [message.from_user.id])
                else:
                    command = """
                    SELECT * FROM transactions WHERE user_id = ? AND date = ?
                    """
                    transactions = list(cursor.execute(command, [message.from_user.id, time.strftime('%m.%Y')]))
                    transaction_id = transactions[user_cache['transaction_clear'] - 1][0]
                    command = """
                    DELETE FROM transactions WHERE id = ?
                    """
                    cursor.execute(command, [transaction_id])
                cursor.close()
                db.commit()
        if 'category' in user_cache.keys() and 'cost' in user_cache.keys() and 'multy' in user_cache.keys():
            with sqlite3.connect('users.db') as db:
                cursor = db.cursor()
                command = """
                INSERT INTO transactions (user_id, cost, date, day, category) VALUES (?, ?, ?, ?, ?)
                """
                cursor.execute(command, [message.from_user.id,
                                         user_cache['cost'] * user_cache['multy'],
                                         time.strftime('%m.%Y'),
                                         (datetime.date.today() - datetime.date(2023, 1, 1)).days,
                                         user_cache['category']])
                cursor.close()
                db.commit()
    finally:
        try:
            del user_cache['transaction_clear']
        except KeyError:
            pass

        try:
            del user_cache['multy']
            del user_cache['cost']
            del user_cache['category']
        except KeyError:
            pass

        with sqlite3.connect('users.db') as db:
            cursor = db.cursor()
            transactions = list(cursor.execute('SELECT * FROM transactions WHERE user_id = ? AND date = ?',
                                               [message.from_user.id, time.strftime('%m.%Y')]))
            cursor.close()

        if len(transactions) > 0:
            text = '🧐 Все твои доходы и расходы за этот месяц находятся тут:\n\n'
            money = 0
            index = 0
            last_date = None
            for transaction in transactions:
                day = transaction[4]
                date = datetime.date(2023, 1, 1) + datetime.timedelta(days=day)
                money += transaction[2]
                if last_date != date:
                    last_date = date
                    text = text + f'• Дата: *{date.strftime("%d.%m.%Y")}*\n'
                if transaction[2] > 0:
                    text = text + f'*{index + 1}.* 📈 Доход на сумму в *{str(transaction[2])}* руб.'
                else:
                    text = text + f'*{index + 1}.* 📉 Расход на сумму в *{str(- transaction[2])}* руб.'
                text = text + f' ({categories[transaction[5]]})\n'
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
                   'transaction_category_item',
                   'transaction_category_transport',
                   'transaction_category_products',
                   'transaction_category_clothes']

    buttons.append('transaction_back')

    return buttons


def analyse_formator(message, user_cache):
    with sqlite3.connect('users.db') as db:
        cursor = db.cursor()
        command = """
        SELECT * FROM transactions WHERE user_id = ? ORDER BY id DESC LIMIT 50
        """
        transactions = list(cursor.execute(command, [message.from_user.id]))
        dreams = list(cursor.execute('SELECT * FROM dreams WHERE user_id = ? ORDER BY priority ASC LIMIT 1',
                                     [message.from_user.id]))
        dream = None
        if len(dreams) > 0:
            dream = dreams[0]
        cursor.close()

        start_index = None
        if len(transactions) > 8:
            index = 8
            for transaction in transactions[8:]:
                if transaction[2] > 0:
                    while index + 1 < len(transactions) and transactions[index + 1][2] > 0:
                        index += 1
                    start_index = index
                    day = transactions[index][4]
                    analyse_transactions = transactions[:index + 1]

                    break
                index += 1

    transactions.reverse()

    if start_index is not None:
        payouts = {}
        index = 0
        for transaction in transactions:
            if transaction[2] < 0:
                if transaction[5] not in payouts.keys():
                    payouts[transaction[5]] = 0
                payouts[transaction[5]] -= transaction[2]

            index += 1

        balance = 0
        money_triggered = 0
        for transaction in analyse_transactions:
            balance += transaction[2]
            money_triggered += abs(transaction[2])

        money_percent = balance / money_triggered

        text = '*Анализ доходов и расходов показал:*\n'

        # Анализ доходов и расходов
        if money_percent < 0:
            text = text + f'💡 Твои расходы начали превышать доходы (на {abs(balance)} рублей)! Старайся больше экономить и меньше тратить!\n'
            if dream is not None:
                text = text + '💡 Ты не можешь накопить денег на желание с текущими доходами и расходами!\n'
        elif money_percent < 0.1:
            text = text + '💡 Твои расходы не превышают доходов, однако твои копления почти не растут! Старайся оставлять хотя-бы 10% от своих доходов, чтобы копить быстрее!\n'
            if dream is not None:
                text = text + f'💡 При сохранении текущих доходов и расходов, до накопления средств на *{dream[2]}* останется *{math.ceil(float(dream[4]) / balance * float(((datetime.date.today() - datetime.date(2023, 1, 1)).days) - day + 1))}* дней\n'
        elif money_percent > 0.9:
            text = text + '💡 Твои доходы почти не тратятся, это хорошо, однако не бойся их тратить, главное - оставлять хотя-бы по 10% от своих доходов и тогда всё будет хорошо!\n'
            if dream is not None:
                text = text + f'💡 При сохранении текущих доходов и расходов, до накопления средств на *{dream[2]}* останется *{math.ceil(float(dream[4]) / balance * float(((datetime.date.today() - datetime.date(2023, 1, 1)).days) - day + 1))}* дней\n'
        else:
            text = text + '✅ Отлично, у тебя нет проблем с коплением денег!\n'
            if dream is not None:
                days_until_dream = math.ceil(float(dream[4]) / balance * float(((datetime.date.today() - datetime.date(2023, 1, 1)).days) - day + 1))
                if days_until_dream < 30:
                    text = text + f'💡 При сохранении текущих доходов и расходов, до накопления средств на *{dream[2]}* останется *{days_until_dream}* дней\n'
                else:
                    text = text + f'💡 При сохранении текущих доходов и расходов, до накопления средств на *{dream[2]}* останется *{days_until_dream}* дней. Если хочешь получить желаемое быстрее, попробуй откладывать больше денег от твоих заработков, чтобы твои деньги копились быстрее\n'

        # Вычисление процентов затрат
        max_value = sum(payouts.values())
        for payout in payouts:
            payouts[payout] = payouts[payout] / max_value * 100

        payouts = list(map(lambda c: {c: round(payouts[c], 1)}, payouts))

        text = text + '\n\n*Вы тратите:*\n'
        for payout in payouts:
            text = text + f'{categories[list(payout.keys())[0]]}: *{list(payout.values())[0]}%*\n'
    else:
        text = '😴 Недостаточно данных для анализирования финансов'

    return text


def dreams_formator(message, user_cache):
    try:
        if 'wish_remove_id' in user_cache.keys():
            with sqlite3.connect('users.db') as db:
                cursor = db.cursor()
                command = """
                SELECT * FROM dreams WHERE user_id = ? ORDER BY priority ASC
                """
                dreams = list(cursor.execute(command, [message.from_user.id]))
                dream_id = dreams[user_cache['wish_remove_id'] - 1][0]
                command = """
                DELETE FROM dreams WHERE id = ?
                """
                cursor.execute(command, [dream_id])
                cursor.close()
                db.commit()
        if 'wish_id' in user_cache.keys() and 'wish_priority' in user_cache.keys():
            with sqlite3.connect('users.db') as db:
                cursor = db.cursor()
                command = """
                SELECT * FROM dreams WHERE user_id = ? ORDER BY priority ASC
                """
                dreams = list(cursor.execute(command, [message.from_user.id]))
                dream_id = dreams[user_cache['wish_id'] - 1][0]
                command = """
                UPDATE dreams SET priority = ? WHERE id = ?
                """
                cursor.execute(command, [user_cache['wish_priority'] - 1, dream_id])
                cursor.close()
                db.commit()
        if 'wish_cost' in user_cache.keys() and 'wish_name' in user_cache.keys():
            with sqlite3.connect('users.db') as db:
                cursor = db.cursor()
                command = """
                INSERT INTO dreams (user_id, dream, date, cost, priority) VALUES (?, ?, ?, ?, 0)
                """
                cursor.execute(command, [message.from_user.id,
                                         user_cache['wish_name'],
                                         time.strftime('%m.%Y'),
                                         user_cache['wish_cost']])
                cursor.close()
                db.commit()
    finally:
        try:
            del user_cache['wish_remove_id']
        except KeyError:
            pass

        try:
            del user_cache['wish_id']
            del user_cache['wish_priority']
        except KeyError:
            pass

        try:
            del user_cache['wish_name']
            del user_cache['wish_cost']
        except KeyError:
            pass
        text = '🤔 Эта вкладка показывает список твоих желаний. Исходя из него, вкладка "Анализировать расходы" поможет тебе правильно составить план расходов, чтобы твоё желание поскорее осуществилось. Желанием может быть от обычной жевачки до нового смартфона или велосипеда.\n\nПриоритет желания - то, насколько скоро тебе понадобится эта вещь относительно других желаний. Чем выше место (меньше число), тем приоритетней оно будет.\n\n'
        with sqlite3.connect('users.db') as db:
            cursor = db.cursor()
            command = """
            SELECT * FROM dreams WHERE user_id = ? ORDER BY priority ASC
            """
            dreams = list(cursor.execute(command, [message.from_user.id]))
            cursor.close()
        if len(dreams) > 0:
            index = 0
            for dream in dreams:
                text = text + f'*{index + 1}. {dream[2]}*\n'
                text = text + f'- Стоимость: *{dream[4]}* рублей\n'
                text = text + f'- Приоритет: *{dream[5] + 1}* место\n'
                text = text + '\n'
                index += 1
        else:
            text = text + '😯 Список желаний пуст!'

    return text
