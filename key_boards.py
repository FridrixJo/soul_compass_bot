from aiogram import types
from data_base.db_statement import StatementsDB


def inline_markup_menu():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Оплата', callback_data='payment')
    btn2 = types.InlineKeyboardButton('Рассрочка', callback_data='installment')
    btn3 = types.InlineKeyboardButton('FAQ', callback_data='questions')
    btn4 = types.InlineKeyboardButton('Связаться с менеджером', callback_data='support')
    btn5 = types.InlineKeyboardButton('Забронировать место', callback_data='book_place')

    kb.add(btn1, btn2, btn3, btn4, btn5)

    return kb


def inline_markup_rates(db: StatementsDB):
    kb = types.InlineKeyboardMarkup(row_width=1)
    f_rate = db.get_first_rate_name()
    s_rate = db.get_second_rate_name()
    th_rate = db.get_third_rate_name()
    if f_rate is None:
        f_rate = 'Тариф 1'
    if s_rate is None:
        s_rate = 'Тариф 2'
    if th_rate is None:
        th_rate = 'Тариф 3'
    btn1 = types.InlineKeyboardButton(text=f_rate, callback_data='first_rate')
    btn2 = types.InlineKeyboardButton(text=s_rate, callback_data='second_rate')
    btn3 = types.InlineKeyboardButton(text=th_rate, callback_data='third_rate')
    btn4 = types.InlineKeyboardButton('Назад ↩', callback_data='back')

    kb.add(btn1, btn2, btn3, btn4)

    return kb


def inline_markup_rate_opps():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Редактировать название', callback_data='edit_name')
    btn2 = types.InlineKeyboardButton('Редактировать описание', callback_data='edit_descr')
    btn3 = types.InlineKeyboardButton('Редактировать цену', callback_data='edit_price')
    btn4 = types.InlineKeyboardButton('Редактировать условия рассрочки', callback_data='edit_conditions')
    btn5 = types.InlineKeyboardButton('Назад ↩', callback_data='back')

    kb.add(btn1, btn2, btn3, btn4, btn5)

    return kb


def inline_markup_rate_opps_client():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Реквизиты', callback_data='get_requisites')
    btn2 = types.InlineKeyboardButton('Рассрочка', callback_data='get_installment_payment')
    btn3 = types.InlineKeyboardButton('Назад ↩', callback_data='back')

    kb.add(btn1, btn2, btn3)

    return kb


def inline_markup_rate_installment_opps_client():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Реквизиты', callback_data='get_requisites')
    btn2 = types.InlineKeyboardButton('Назад ↩', callback_data='back')

    kb.add(btn1, btn2)

    return kb


def inline_markup_payment():
    kb = types.InlineKeyboardMarkup(row_width=2)

    btn1 = types.InlineKeyboardButton('Главное меню', callback_data='main_menu')
    btn2 = types.InlineKeyboardButton('Я оплатил(а)', callback_data='done')

    kb.add(btn1, btn2)

    return kb


def inline_markup_admin_menu():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Тарифы', callback_data='admin_rates')
    btn2 = types.InlineKeyboardButton('Вопросы', callback_data='admin_questions')
    btn3 = types.InlineKeyboardButton('Реквизиты', callback_data='admin_requisites')
    btn4 = types.InlineKeyboardButton('Списки пользователей', callback_data='users_list')
    btn5 = types.InlineKeyboardButton('Рассылка пользователям', callback_data='sharing')
    btn6 = types.InlineKeyboardButton('Добавить админа', callback_data='add_admin')
    btn7 = types.InlineKeyboardButton('Главное меню', callback_data='main_menu')

    kb.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)

    return kb


def reply_markup_call_off(text):
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton(text=text)

    kb.add(btn1)

    return kb


def inline_markup_back(text):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text + ' ↩️', callback_data='back')

    kb.add(btn1)

    return kb


def inline_markup_check_request():
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('ОТВЕТИТЬ НА СООБЩЕНИЕ', callback_data='reply_message')

    kb.add(btn1)

    return kb


def inline_markup_check_payment():
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('ОБРАБОТАТЬ ПЛАТЕЖ', callback_data='check_payment')

    kb.add(btn1)

    return kb


def inline_markup_request_opps():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Одобрить платеж ✅', callback_data='approve')
    btn2 = types.InlineKeyboardButton('Отклонить платеж ❌', callback_data='reject')

    kb.add(btn1, btn2)

    return kb


def inline_markup_classify_client():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('1 тариф', callback_data='1_rate')
    btn2 = types.InlineKeyboardButton('2 тариф', callback_data='2_rate')
    btn3 = types.InlineKeyboardButton('3 тариф', callback_data='3_rate')
    btn4 = types.InlineKeyboardButton('1 тариф рассрочка', callback_data='1i_rate')
    btn5 = types.InlineKeyboardButton('2 тариф рассрочка', callback_data='2i_rate')
    btn6 = types.InlineKeyboardButton('3 тариф рассрочка', callback_data='3i_rate')
    btn7 = types.InlineKeyboardButton('Бронь', callback_data='book_rate')
    btn8 = types.InlineKeyboardButton('Назад ↩', callback_data='back')

    kb.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)

    return kb


def inline_markup_classify_client_users_list():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('1 тариф', callback_data='1_rate')
    btn2 = types.InlineKeyboardButton('2 тариф', callback_data='2_rate')
    btn3 = types.InlineKeyboardButton('3 тариф', callback_data='3_rate')
    btn4 = types.InlineKeyboardButton('1 тариф рассрочка', callback_data='1i_rate')
    btn5 = types.InlineKeyboardButton('2 тариф рассрочка', callback_data='2i_rate')
    btn6 = types.InlineKeyboardButton('3 тариф рассрочка', callback_data='3i_rate')
    btn7 = types.InlineKeyboardButton('Бронь', callback_data='book_rate')
    btn8 = types.InlineKeyboardButton('Обычные пользователи', callback_data='simple')
    btn9 = types.InlineKeyboardButton('Все пользователи', callback_data='all_users')
    btn10 = types.InlineKeyboardButton('Назад ↩', callback_data='back')

    kb.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10)

    return kb
