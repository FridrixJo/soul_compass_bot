from aiogram import types


def inline_markup_menu():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Оплата', callback_data='payment')
    btn2 = types.InlineKeyboardButton('Рассрочка', callback_data='installment')
    btn3 = types.InlineKeyboardButton('FAQ', callback_data='questions')
    btn4 = types.InlineKeyboardButton('Связаться с менеджером', callback_data='support')
    btn5 = types.InlineKeyboardButton('Забронировать место', callback_data='book_place')

    kb.add(btn1, btn2, btn3, btn4, btn5)

    return kb


def inline_markup_rates():
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('Тариф 1', callback_data='first_rate')
    btn2 = types.InlineKeyboardButton('Тариф 2', callback_data='second_rate')
    btn3 = types.InlineKeyboardButton('Тариф 3', callback_data='third_rate')
    btn4 = types.InlineKeyboardButton('Назад ↩', callback_data='back')

    kb.add(btn1, btn2, btn3, btn4)

    return kb


def inline_markup_admin_menu():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Тарифы', callback_data='admin_rates')
    btn2 = types.InlineKeyboardButton('Вопросы', callback_data='admin_questions')
    btn3 = types.InlineKeyboardButton('Реквизиты', callback_data='admin_requisites')
    btn4 = types.InlineKeyboardButton('Рассылка пользователям', callback_data='sharing')
    btn5 = types.InlineKeyboardButton('Главное меню', callback_data='main_menu')

    kb.add(btn1, btn2, btn3, btn4, btn5)

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

