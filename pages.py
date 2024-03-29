import formators as form

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
            'buttons': ['learn_finance', 'learn_save_money', 'learn_shop_traps', 'learn_inflation', 'main_back'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        },
        'lesson_finance': {
            'name': 'Что такое финансовая грамотность?',
            'content': 'Финансовая грамотность - это умение хранить и распределять свои денежные сбережения, '
                       'а также сохранять своё благосостояние и качество жизни.\n\nФинансово грамотным человеком '
                       'является тот, кто умеет обращаться со своим имуществом и деньгами, а также знает как тратить '
                       'и экономить деньги.\n\nНадеюсь, вам понравилась статья 😉',
            'buttons': ['learn_back'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        },
        'lesson_save_money': {
            'name': 'Как начать копить деньги?',
            'content': 'Хочешь купить велосипед? Тогда начни копить деньги. Чтобы начать копить деньги нужно просто '
                       'откладывать небольшую сумму, полученную тобой, в копилку. Через некоторое время в ней '
                       'наберётся достаточно денег.\n\nК примеру, ты хочешь купить велоспед, он стоит 5000 рублей. '
                       'Родители каждую неделю дают тебе 1500 рублей в карманные деньги, а после школы ты ходишь на '
                       'подработку, где тебе платят 500 рублей за один день работы. То есть за неделю ты получаешь '
                       '500 × 7 = 3500 рублей. Складываем с карманными деньгами: получается 3500 + 1500 = 5000 рублей. '
                       'Откладываем 500 рублей в копилку. И получается, что если мы поделим цену велосипеда на 500 '
                       'рублей, то мы получим количество недель, через которые деньги на велосипед будут накоплены. '
                       '5000 ÷ 500 = 10 недель. Значит, откладывая по 10% в месяц, мы сможем купить велосипед уже '
                       'через 10 недель (2 с чем-то месяца).\n\nТеперь ты знаешь как '
                       'копить деньги!\n\nНадеюсь, вам понравилась статья 😉',
            'buttons': ['learn_back'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        },
        'lesson_shop_traps': {
            'name': 'Что такое магазинные ловушки и как в них не попасться?',
            'content': 'В магазине ты можешь заметить множество разных наклеек с надписями на ценниках. Ими могут быть '
                       'акции "три по цене двух" или "при покупке от двух товаров скидка 20%". Также '
                       'в магазинах бывают распродажи. Всё это - магазинные ловушки. Их цель - привлечь покупателя, '
                       'чтобы тот купил товар, думая, что акция может закончиться в любой момент, а товар может ещё '
                       'пригодиться. В итоге, человек покупает слишком много ненужных вещей. Чтобы не попадаться на '
                       'такие ловушки нужно быть внимательным к своим покупкам.\n\nНадеюсь, вам понравилась статья 😉',
            'buttons': ['learn_back'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        },
        'lesson_inflation': {
            'name': 'Что такое инфляция?',
            'content': 'Инфляция - это рост цен на товары и услуги. Происходит это когда деньги обесцениваются. '
                       'Другими словами, если в 2008 году товар стоил 2500 рублей, то на 2023 год этот товар будет '
                       'стоить больше из-за инфляции. Также есть другое понятие - дефляция. Это обратный процесс '
                       'инфляции, то есть, когда цены на товары и услуги снижаются, а значимость денег '
                       'растёт.\n\nНадеюсь, вам понравилась статья 😉',
            'buttons': ['learn_back'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        },
        'earnings': {
            'name': 'Доходы и расходы',
            'content': form.earnings_formator,
            'buttons': ['pay-in', 'pay-out', 'pay_clear', 'main_back'],
            'inline_buttons': ['analyse', 'dreams'],
            'inline_name': 'Услуги по финансам',
            'inline_content': '🤗 Также мы можем предложить тебе некоторые услуги по твоим доходам и расходам'
        },
        'transaction_clear': {
            'name': 'Очистка дохода или расхода',
            'content': '⚠️ Если ты нажал на кнопку случайно, то отмени очистку с помощью кнопки на клавиатуре быстрых ответов.\n\n🤝 Если же ты нажал на кнопку не случайно, то введи в чат номер транзакции или текст "всё", чтобы удалить конкретную транзакцию или все сразу соответственно.',
            'buttons': ['transaction_back'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
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
            'buttons': ['wish', 'wish_priority', 'wish_remove', 'dreams_back'],
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
        },
        'wish_priority': {
            'name': 'Измененение приоритета желания',
            'content': '🤝 Напиши номер желания. Он указан перед каждым твоим желанием в виде: "Номер. Желание".',
            'buttons': ['wish_back'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        },
        'wish_priority_place': {
            'name': 'Измененение приоритета желания',
            'content': '🤝 Напиши значение приоритета желания. Оно должно быть от 1 (наивысший приоритет) до 100 (самый низкий).',
            'buttons': ['wish_back'],
            'inline_buttons': [],
            'inline_name': None,
            'inline_content': None
        },
        'wish_remove': {
            'name': 'Удаление желания',
            'content': '⚠️ Если ты уже получил желаемое или у тебя пропал к нему интерес, то ты можешь смело удалять его. Если нет, то вы можете отменить удаление, нажав на кнопку на клавиатуре быстрых ответов.\n\n🤝 Если же ты действительно решил удалить желание из списка желаний, то впиши его номер в чат. Номер желания расположен перед названием желания в формате "Номер. Желание".',
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
        'learn_shop_traps': {
            'name': '💵 Что такое магазинные ловушки и как в них не попасться?',
            'redirect': 'lesson_shop_traps'
        },
        'learn_inflation': {
            'name': '💵 Что такое инфляция?',
            'redirect': 'lesson_inflation'
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
        'pay_clear': {
            'name': '🗑️ Очистить доход или расход',
            'redirect': 'transaction_clear'
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
        'transaction_category_transport': {
            'name': '🚕 Траспорт',
            'redirect': 'earnings'
        },
        'transaction_category_products': {
            'name': '🍎 Продукты',
            'redirect': 'earnings'
        },
        'transaction_category_clothes': {
            'name': '👕 Одежда',
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
        },
        'wish_priority': {
            'name': '🔥 Изменить приоритет желания',
            'redirect': 'wish_priority'
        },
        'wish_remove': {
            'name': '💥 Удалить желание из списка желаний',
            'redirect': 'wish_remove'
        }
    },
    'inline_buttons': {
        'analyse': {
            'name': '〽️ Анализировать расходы',
            'redirect': 'analyse'
        },
        'dreams': {
            'name': '✴️ Список желаний',
            'redirect': 'dreams'
        }
    }
}