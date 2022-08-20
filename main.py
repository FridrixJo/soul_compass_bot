import asyncio
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

from aiogram import types
import random
import string
#from config import *
from key_boards import *
from FSMClasses import *

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from data_base.db_users import UsersDB
from data_base.db_statement import StatementsDB
from data_base.db_requests import RequestDB
from data_base.db_photos import PhotosDB

storage = MemoryStorage()

bot = Bot(token='5344363786:AAE4qn8hr5NgAQYexfWYHVikLXm8G6dsTn4')

dispatcher = Dispatcher(bot=bot, storage=storage)

ADMIN_IDS = [899951880]


users_db = UsersDB('data_base/compass.db')
statement_db = StatementsDB('data_base/compass.db')
requests_db = RequestDB('data_base/compass.db')
photos_db = PhotosDB('data_base/compass.db')


async def send_menu(message: types.Message):
    text = 'Главное меню'
    await bot.send_message(message.chat.id, text=text, reply_markup=inline_markup_menu())


async def edit_to_menu(message: types.Message):
    text = 'Главное меню'
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=inline_markup_menu())


async def send_moderator_menu(message: types.Message):
    text = 'Модераторское меню'
    await bot.send_message(message.chat.id, text=text, reply_markup=inline_markup_admin_menu())


async def edit_to_moderator_menu(message: types.Message):
    text = 'Модераторское меню'
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=inline_markup_admin_menu())


async def clear_state(state: FSMContext):
    try:
        current_state = state.get_state()
        if current_state is not None:
            await state.finish()
    except Exception as error:
        print(error)


def get_name(message: types.Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    name = ''
    if first_name is not None:
        name += first_name
        name += ' '
    if last_name is not None:
        name += last_name
        name += ' '
    if username is not None:
        name += '@'
        name += username

    return name


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    if not users_db.user_exists(message.chat.id):
        users_db.add_user(message.chat.id, get_name(message))
        text = 'Здравствуй, дорогой путник! Рады приветствовать тебя …. Что-то тут будет в тематике средиземья'
        await bot.send_message(message.chat.id, text)

        text = f'Пользователь {str(users_db.get_name(message.chat.id))} перешел в бота'
        for i in ADMIN_IDS:
            await bot.send_message(chat_id=i, text=text)

    await send_menu(message)


@dispatcher.callback_query_handler()
async def get_callback(call: types.CallbackQuery):
    if call.data == 'payment':
        text = 'Выберите тариф'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_rates(statement_db))
        await FSMUser.choose_rate.set()
    elif call.data == 'installment':
        text = 'Будь внимателен, условия рассрочки и бонусов для всех тарифов отличаются. Какой тариф тебя интересует?'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_rates(statement_db))
        await FSMUser.choose_rate_installment_payment.set()
    elif call.data == 'questions':
        await get_questions(call.message)
    elif call.data == 'support':
        if not requests_db.user_exists(call.message.chat.id):
            await bot.send_message(call.message.chat.id, 'Введите сообщение, которое хотите отправить менеджеру', reply_markup=reply_markup_call_off('Назад'))
            await FSMReply.message.set()
        else:
            text = 'Вы уже отправили сообщение менеджеру. Ожидайте ответа, в скорем времени с вами свяжутся'
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_back('На главное меню'))
    elif call.data == 'book_place':
        pass
    elif call.data == 'back':
        print(1)
        await edit_to_menu(call.message)
    elif call.data == 'reply_message':
        await bot.send_message(call.message.chat.id, 'Скопируйте и отправьте ID сообщения для того, чтобы ответить данному пользователю', reply_markup=reply_markup_call_off('Назад'))
        await FSMReply.request_id.set()
    elif call.data == 'check_payment':
        await bot.send_message(call.message.chat.id, 'Скопируйте и отправьте ID платежа для того, чтобы его обработать', reply_markup=reply_markup_call_off('Назад'))
        await FSMReply.payment_id.set()


@dispatcher.callback_query_handler(state=FSMUser.choose_rate)
async def get_rate(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
        await edit_to_menu(call.message)
    elif call.data == 'first_rate':
        async with state.proxy() as file:
            file['rate'] = 'first'
        text = statement_db.get_first_rate_descr()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_rate_opps_client())
        await FSMUser.payment_type.set()
    elif call.data == 'second_rate':
        async with state.proxy() as file:
            file['rate'] = 'second'
        text = statement_db.get_second_rate_descr()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_rate_opps_client())
        await FSMUser.payment_type.set()
    elif call.data == 'third_rate':
        async with state.proxy() as file:
            file['rate'] = 'third'
        text = statement_db.get_third_rate_descr()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_rate_opps_client())
        await FSMUser.payment_type.set()


@dispatcher.callback_query_handler(state=FSMUser.choose_rate_installment_payment)
async def get_rate(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
        await edit_to_menu(call.message)
    elif call.data == 'first_rate':
        async with state.proxy() as file:
            file['rate'] = 'i_first'
        text = f'Условия рассрочки для тарифа <b>{statement_db.get_first_rate_name()}</b>' + '\n\n'
        text += statement_db.get_first_rate_conditions() + '\n\n'
        text += f'<i>Полная цена тарифа:</i> <b>{statement_db.get_first_rate_price()}₽</b>' + '\n'
        text += f'<i>Цена первого взноса с расрочкой для этого тарифа</i>: <b>{int(int(statement_db.get_first_rate_price()) * 0.5)}₽</b>'

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_rate_installment_opps_client(), parse_mode='HTML')
        await FSMUser.payment_type.set()
    elif call.data == 'second_rate':
        async with state.proxy() as file:
            file['rate'] = 'i_second'
        text = f'Условия рассрочки для тарифа <b>{statement_db.get_second_rate_name()}</b>' + '\n\n'
        text += statement_db.get_second_rate_conditions() + '\n\n'
        text += f'<i>Полная цена тарифа:</i> <b>{statement_db.get_second_rate_price()}₽</b>' + '\n'
        text += f'<i>Цена первого взноса с расрочкой для этого тарифа</i>: <b>{int(int(statement_db.get_second_rate_price()) * 0.4)}₽</b>'

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_rate_installment_opps_client(), parse_mode='HTML')
        await FSMUser.payment_type.set()
    elif call.data == 'third_rate':
        async with state.proxy() as file:
            file['rate'] = 'i_third'
        text = f'Условия рассрочки для тарифа <b>{statement_db.get_third_rate_name()}</b>' + '\n\n'
        text += statement_db.get_third_rate_conditions() + '\n\n'
        text += f'<i>Полная цена тарифа:</i> <b>{statement_db.get_third_rate_price()}₽</b>' + '\n'
        text += f'<i>Цена первого взноса с расрочкой для этого тарифа</i>: <b>{int(int(statement_db.get_third_rate_price()) * 0.4)}₽</b>'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_rate_installment_opps_client(), parse_mode='HTML')
        await FSMUser.payment_type.set()


@dispatcher.callback_query_handler(state=FSMUser.payment_type)
async def get_payment_type(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
        await edit_to_menu(message=call.message)
    elif call.data == 'get_requisites':
        if not photos_db.user_exists(call.message.chat.id):
            async with state.proxy() as file:
                rate = file['rate']
            if rate == 'first':
                async with state.proxy() as file:
                    file['price'] = statement_db.get_first_rate_price()
                text = f'Оплатите <code>{statement_db.get_first_rate_price()}</code>₽ по следующим реквизитам:' + '\n\n'
                text += f'<code>{statement_db.get_requisites()}</code>' + '\n\n'
                text += '<b>Только после оплаты</b> нажмите на кнопку "Я оплатил(а)"'
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_payment(), parse_mode='HTML')
                await FSMUser.apply_payment.set()
            elif rate == 'second':
                async with state.proxy() as file:
                    file['price'] = statement_db.get_second_rate_price()
                text = f'Оплатите <code>{statement_db.get_first_rate_price()}</code>₽ по следующим реквизитам:' + '\n\n'
                text += f'<code>{statement_db.get_requisites()}</code>' + '\n\n'
                text += '<b>Только после оплаты</b> нажмите на кнопку "Я оплатил(а)"'
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_payment(), parse_mode='HTML')
                await FSMUser.apply_payment.set()
            elif rate == 'third':
                async with state.proxy() as file:
                    file['price'] = statement_db.get_third_rate_price()
                text = f'Оплатите <code>{statement_db.get_first_rate_price()}</code>₽ по следующим реквизитам:' + '\n\n'
                text += f'<code>{statement_db.get_requisites()}</code>' + '\n\n'
                text += '<b>Только после оплаты</b> нажмите на кнопку "Я оплатил(а)"'
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_payment(), parse_mode='HTML')
                await FSMUser.apply_payment.set()
            elif rate == 'i_first':
                price = int(int(statement_db.get_first_rate_price()) * 0.5)
                async with state.proxy() as file:
                    file['price'] = price
                text = f'Оплатите <code>{price}</code>₽ по следующим реквизитам:' + '\n\n'
                text += f'<code>{statement_db.get_requisites()}</code>' + '\n\n'
                text += '<b>Только после оплаты</b> нажмите на кнопку "Я оплатил(а)"'
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_payment(), parse_mode='HTML')
                await FSMUser.apply_payment.set()
            elif rate == 'i_second':
                price = int(int(statement_db.get_second_rate_price()) * 0.4)
                async with state.proxy() as file:
                    file['price'] = price
                text = f'Оплатите <code>{price}</code>₽ по следующим реквизитам:' + '\n\n'
                text += f'<code>{statement_db.get_requisites()}</code>' + '\n\n'
                text += '<b>Только после оплаты</b> нажмите на кнопку "Я оплатил(а)"'
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_payment(), parse_mode='HTML')
                await FSMUser.apply_payment.set()
            elif rate == 'i_third':
                price = int(int(statement_db.get_third_rate_price()) * 0.4)
                async with state.proxy() as file:
                    file['price'] = price
                text = f'Оплатите <code>{price}</code>₽ по следующим реквизитам:' + '\n\n'
                text += f'<code>{statement_db.get_requisites()}</code>' + '\n\n'
                text += '<b>Только после оплаты</b> нажмите на кнопку "Я оплатил(а)"'
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_payment(), parse_mode='HTML')
                await FSMUser.apply_payment.set()
        else:
            await clear_state(state)
            text = 'У вас уже есть один необработанный платеж. Ожидайте ответа менеджера, в скорем времени с вами свяжутся'
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_back('На главное меню'))
    elif call.data == 'get_installment_payment':
        await clear_state(state)
        text = 'Будь внимателен, условия рассрочки и бонусов для всех тарифов отличаются. Какой тариф тебя интересует?'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_rates(statement_db))
        await FSMUser.choose_rate_installment_payment.set()


@dispatcher.callback_query_handler(state=FSMUser.apply_payment)
async def apply_payment(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'main_menu':
        await clear_state(state)
        await edit_to_menu(call.message)
    elif call.data == 'done':
        text = '🧾 Прикрепите изображение, подтверждающее оплату 📎⬇'
        await bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Вернуться на главное меню'))
        await FSMUser.photo.set()


@dispatcher.message_handler(content_types=['photo', 'text'], state=FSMUser.photo)
async def get_photo(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        if message.text == 'Вернуться на главное меню':
            await clear_state(state)
            await send_menu(message)
    elif message.content_type == 'photo':
        numb = ''.join(random.choice(string.digits) for _ in range(random.randrange(8, 16)))

        async with state.proxy() as file:
            rate = file['rate']
            price = file['price']

        name = get_name(message)

        photos_db.add_request(numb)
        photos_db.set_user_id(numb, message.chat.id)
        photos_db.set_name(numb, name)
        photos_db.set_type(numb, rate)

        rate_name = 'Название тарифа'
        if rate == 'first':
            rate_name = f'<b>{statement_db.get_first_rate_name()}</b>'
        elif rate == 'second':
            rate_name = f'<b>{statement_db.get_second_rate_name()}</b>'
        elif rate == 'third':
            rate_name = f'<b>{statement_db.get_third_rate_name()}</b>'
        elif rate == 'i_first':
            rate_name = f'Рассрочка для тарифа "{statement_db.get_first_rate_name()}"'
        elif rate == 'i_second':
            rate_name = f'Рассрочка для тарифа "{statement_db.get_second_rate_name()}"'
        elif rate == 'i_third':
            rate_name = f'Рассрочка для тарифа "{statement_db.get_third_rate_name()}"'

        for i in ADMIN_IDS:
            text = f'Номер платежа: <code>{numb}</code>' + '\n\n'
            text += f'Клиент выбрал тариф: <b>{rate_name}</b>' + '\n'
            text += f'Вам клиент отправил <b>{price}₽</b>' + '\n'

            text += f'Имя клиента: {str(name)}'

            try:
                await bot.send_photo(i, photo=message.photo[-1].file_id, caption=text, reply_markup=inline_markup_check_payment(), parse_mode='HTML')
            except Exception as e:
                print(e)

        text = f'Ваш платеж #<code>{numb}</code> сейчас находится на расмотрении 🔎' + '\n'
        text += '<i>Ожидайте, с вами скоро свяжется менеджер...</i>'
        await bot.send_message(message.chat.id, text, reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
        await clear_state(state)
        await send_menu(message)


@dispatcher.message_handler(commands=['moderator'], state=['*'])
async def start_moderator(message: types.Message, state: FSMContext):
    await clear_state(state)
    for i in ADMIN_IDS:
        if message.chat.id == i:
            await send_moderator_menu(message)
            await FSMAdmin.admin_opps.set()


@dispatcher.message_handler(Text(equals='отмена', ignore_case=True), state=[FSMAdmin.change_statement, FSMAdmin.add_admin, FSMAdmin.sharing])
async def cancel_handler(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, '<i>Действие отменено</i> ↩', reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
    await clear_state(state)
    await send_moderator_menu(message)
    await FSMAdmin.admin_opps.set()


@dispatcher.message_handler(Text(equals='назад', ignore_case=True), state=[FSMReply.reply_message, FSMReply.request_id, FSMReply.payment_id, FSMReply.message])
async def cancel_handler(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, '<i>Действие отменено</i> ↩', reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
    await clear_state(state)
    await send_menu(message)


@dispatcher.callback_query_handler(state=FSMAdmin.admin_opps)
async def get_callback(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'main_menu':
        await clear_state(state)
        await edit_to_menu(call.message)
    elif call.data == 'admin_rates':
        text = 'Выберите тариф для его редактирования'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_rates(statement_db))
        await FSMAdmin.get_rate.set()
    elif call.data == 'admin_installment_rates':
        pass
    elif call.data == 'admin_requisites':
        async with state.proxy() as file:
            file['status'] = 'requisites'

        text = 'Ваши текущие реквизиты:' + '\n\n'
        requisites = statement_db.get_requisites()
        if requisites is None:
            requisites = 'У вас их нет, установите новые пожалуйста'
        text += f'{requisites}' + '\n\n'
        text += 'Отправьте новые реквизиты либо нажмите "Отмена"'

        await bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
        await FSMAdmin.change_statement.set()
    elif call.data == 'admin_questions':
        async with state.proxy() as file:
            file['status'] = 'questions'

        await get_questions_admin(call.message)
        await FSMAdmin.change_statement.set()
    elif call.data == 'sharing':
        async with state.proxy() as file:
            file['status'] = 'sharing'
        text = 'Выберите критерий, по которому будут отбираться списки пользователей для рассылки'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_classify_client_users_list())
        await FSMAdmin.classify_users.set()
    elif call.data == 'users_list':
        async with state.proxy() as file:
            file['status'] = 'users_list'
        text = 'Выберите критерий, по которому будут отбираться списки пользователей'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_classify_client_users_list())
        await FSMAdmin.classify_users.set()
    elif call.data == 'add_admin':
        text = 'Введите ChatID пользователя'
        await bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
        await FSMAdmin.add_admin.set()


@dispatcher.message_handler(state=FSMAdmin.add_admin)
async def add_admin(message: types.Message, state: FSMContext):
    if users_db.user_exists(message.text):
        ADMIN_IDS.append(int(message.text))
        text = 'Выполнено ✅'
        await bot.send_message(message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove())
        await send_moderator_menu(message)
        await FSMAdmin.admin_opps.set()


async def get_users_list_by_param(message: types.Message, param: str):
    text = users_db.get_users_by_type(param)
    users = f'Количество: <b>{len(text)}</b>' + '\n\n'
    for i in text:
        users += users_db.get_name(int(i[0])) + f'  code>{int(i[0])}</code>' + '\n'

    if len(users) > 4096:
        for x in range(0, len(users), 4096):
            await bot.send_message(message.chat.id, users[x:x+4096], parse_mode='HTML')
    else:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=users, parse_mode='HTML')


async def get_all_users_list(message: types.Message):
    text = users_db.get_users()
    users = f'Количество: <b>{len(text)}</b>' + '\n\n'
    for i in text:
        users += users_db.get_name(int(i[0])) + f'  <code>{int(i[0])}</code>' + '\n'

    if len(users) > 4096:
        for x in range(0, len(users), 4096):
            await bot.send_message(message.chat.id, users[x:x+4096], parse_mode='HTML')
    else:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=users, parse_mode='HTML')


@dispatcher.callback_query_handler(state=FSMAdmin.classify_users)
async def classify_users(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
        await edit_to_moderator_menu(call.message)
        await FSMAdmin.admin_opps.set()
    else:
        async with state.proxy() as file:
            status = file['status']
        if status == 'sharing':
            async with state.proxy() as file:
                file['param'] = call.data
            text = 'Введите сообщение для рассылки данной группе пользователей'
            await bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
            await FSMAdmin.sharing.set()
        else:
            if call.data == '1_rate':
                await get_users_list_by_param(call.message, call.data)
                text = f'Все пользователи, которые приобрели тариф "{statement_db.get_first_rate_name()}"'
                await bot.send_message(call.message.chat.id, text=text, reply_markup=inline_markup_back('Назад'))
                await FSMAdmin.admin_back.set()
            elif call.data == '2_rate':
                await get_users_list_by_param(call.message, call.data)
                text = f'Все пользователи, которые приобрели тариф "{statement_db.get_second_rate_name()}"'
                await bot.send_message(call.message.chat.id, text=text, reply_markup=inline_markup_back('Назад'))
                await FSMAdmin.admin_back.set()
            elif call.data == '3_rate':
                await get_users_list_by_param(call.message, call.data)
                text = f'Все пользователи, которые приобрели тариф "{statement_db.get_second_rate_name()}"'
                await bot.send_message(call.message.chat.id, text=text, reply_markup=inline_markup_back('Назад'))
                await FSMAdmin.admin_back.set()
            elif call.data == '1i_rate':
                await get_users_list_by_param(call.message, call.data)
                text = f'Все пользователи, которые внесли первый платеж для рассрочки тарифа "{statement_db.get_first_rate_name()}"'
                await bot.send_message(call.message.chat.id, text=text, reply_markup=inline_markup_back('Назад'))
                await FSMAdmin.admin_back.set()
            elif call.data == '2i_rate':
                await get_users_list_by_param(call.message, call.data)
                text = f'Все пользователи, которые внесли первый платеж для рассрочки тарифа "{statement_db.get_second_rate_name()}"'
                await bot.send_message(call.message.chat.id, text=text, reply_markup=inline_markup_back('Назад'))
                await FSMAdmin.admin_back.set()
            elif call.data == '3i_rate':
                await get_users_list_by_param(call.message, call.data)
                text = f'Все пользователи, которые внесли первый платеж для рассрочки тарифа "{statement_db.get_second_rate_name()}"'
                await bot.send_message(call.message.chat.id, text=text, reply_markup=inline_markup_back('Назад'))
                await FSMAdmin.admin_back.set()
            elif call.data == 'book_rate':
                await get_users_list_by_param(call.message, call.data)
                text = f'Все пользователи, которые забронировали место "{statement_db.get_second_rate_name()}"'
                await bot.send_message(call.message.chat.id, text=text, reply_markup=inline_markup_back('Назад'))
                await FSMAdmin.admin_back.set()
            elif call.data == 'simple':
                await get_users_list_by_param(call.message, call.data)
                text = f'Все пользователи, которые ничего не приобрели'
                await bot.send_message(call.message.chat.id, text=text, reply_markup=inline_markup_back('Назад'))
                await FSMAdmin.admin_back.set()
            elif call.data == 'all_users':
                await get_all_users_list(call.message)
                text = f'Все пользователи бота'
                await bot.send_message(call.message.chat.id, text=text, reply_markup=inline_markup_back('Назад'))
                await FSMAdmin.admin_back.set()


@dispatcher.callback_query_handler(state=FSMAdmin.admin_back)
async def back_to_moderator_menu(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        text = 'Выберите критерий, по которому будут отбираться списки пользователей'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_classify_client_users_list())
        await FSMAdmin.classify_users.set()


@dispatcher.message_handler(state=FSMAdmin.sharing)
async def sharing_by_param(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        param = file['param']
    count = 0
    if param == 'all_users':
        for i in users_db.get_users():
            try:
                await bot.send_message(int(i[0]), text=message.text)
                count += 1
            except Exception as e:
                print(e)
    else:
        for i in users_db.get_users_by_type(param):
            try:
                await bot.send_message(int(i[0]), text=message.text)
                count += 1
            except Exception as e:
                print(e)

    text = 'Рассылка прошла успешно ✅' + '\n'
    text += f'Количество отправленных сообщений: <b>{count}</b>'
    await bot.send_message(message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
    await send_moderator_menu(message)
    await FSMAdmin.admin_opps.set()


async def get_questions_admin(message: types.Message):
    text = 'Ваши текущие вопросы:' + '\n\n'
    questions = statement_db.get_questions()
    if questions is None:
        questions = 'У вас их нет, установите новые пожалуйста'
    text += f'{questions}' + '\n\n'

    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            await bot.send_message(message.chat.id, text[x:x+4096])
    else:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, parse_mode='HTML')
    await bot.send_message(message.chat.id, 'Отправьте новые вопросы либо нажмите "Отмена"', reply_markup=reply_markup_call_off('Отмена'), parse_mode='HTML')


async def get_questions(message: types.Message):
    text = statement_db.get_questions()
    if text is None:
        text = 'Информация о вопросах обновляется'

    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            await bot.send_message(message.chat.id, text[x:x+4096])
    else:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, parse_mode='HTML')
    await bot.send_message(message.chat.id, 'Список самых популярных вопросов 🌐', reply_markup=inline_markup_back('Назад'), parse_mode='HTML')


@dispatcher.message_handler(state=FSMAdmin.change_statement)
async def change_statement(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        status = file['status']

    text = 'Успешно выполнено ✅'

    if status == 'questions':
        statement_db.set_questions(message.text)
    elif status == 'requisites':
        statement_db.set_requisites(message.text)
    elif status == 'rate_name':
        async with state.proxy() as file:
            rate = file['rate']
        if rate == 'first':
            statement_db.set_first_rate_name(message.text)
        elif rate == 'second':
            statement_db.set_second_rate_name(message.text)
        elif rate == 'third':
            statement_db.set_third_rate_name(message.text)
    elif status == 'rate_descr':
        async with state.proxy() as file:
            rate = file['rate']
        if rate == 'first':
            statement_db.set_first_rate_descr(message.text)
        elif rate == 'second':
            statement_db.set_second_rate_descr(message.text)
        elif rate == 'third':
            statement_db.set_third_rate_descr(message.text)
    elif status == 'rate_price':
        async with state.proxy() as file:
            rate = file['rate']
        if rate == 'first':
            statement_db.set_first_rate_price(message.text)
        elif rate == 'second':
            statement_db.set_second_rate_price(message.text)
        elif rate == 'third':
            statement_db.set_third_rate_price(message.text)
    elif status == 'rate_conditions':
        async with state.proxy() as file:
            rate = file['rate']
        if rate == 'first':
            statement_db.set_first_rate_conditions(message.text)
        elif rate == 'second':
            statement_db.set_second_rate_conditions(message.text)
        elif rate == 'third':
            statement_db.set_third_rate_conditions(message.text)

    await bot.send_message(message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove())
    await send_moderator_menu(message)
    await FSMAdmin.admin_opps.set()


@dispatcher.message_handler(content_types=['text'], state=FSMReply.message)
async def get_request_message(message: types.Message, state: FSMContext):
    numb = ''.join(random.choice(string.digits) for _ in range(random.randrange(8, 16)))

    requests_db.add_request(numb)
    requests_db.set_user_id(numb, message.chat.id)
    requests_db.set_name(numb, users_db.get_name(message.chat.id))

    for i in ADMIN_IDS:
        try:
            text = f'Вам поступило сообещние от пользователя {users_db.get_name(message.chat.id)} с ChatID <code>{message.chat.id}</code>' + '\n\n'
            text += f'Текст сообещние: {message.text}' + '\n\n'
            text += f'ID сообщения: <code>{numb}</code>'
            await bot.send_message(i, text, reply_markup=inline_markup_check_request(), parse_mode='HTML')
        except Exception as e:
            print(e)

    text = 'Ваше сообщение было успешно отправлено менеджеру. В скором времени с вами свяжутся'
    await bot.send_message(message.chat.id, text, reply_markup=types.ReplyKeyboardRemove())
    await clear_state(state)
    await send_menu(message)


@dispatcher.message_handler(state=FSMReply.request_id)
async def get_request_id(message: types.Message, state: FSMContext):
    if requests_db.request_exists(message.text):
        async with state.proxy() as file:
            file['request_id'] = message.text

        text = f'Отправьте сообщение пользователю {requests_db.get_name(int(message.text))}'
        await bot.send_message(message.chat.id, text, reply_markup=reply_markup_call_off('Назад'))
        await FSMReply.reply_message.set()
    else:
        await bot.send_message(message.chat.id, 'Сообщения с таким ID не найдено. Попробуйте еще раз', reply_markup=reply_markup_call_off('Назад'))
        await FSMReply.request_id.set()


@dispatcher.message_handler(content_types=['text'], state=FSMReply.reply_message)
async def get_request_message(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        request_id = file['request_id']

    text = 'Ответ менеджера:' + '\n\n'
    text += message.text
    await bot.send_message(chat_id=requests_db.get_user_id(int(request_id)), text=text)

    text = f'Ваше сообщение было успешно отправлено пользователю {requests_db.get_name(int(request_id))}'
    await bot.send_message(message.chat.id, text, reply_markup=types.ReplyKeyboardRemove())
    requests_db.delete_request(request_id)

    await clear_state(state)
    await send_menu(message)


@dispatcher.message_handler(state=FSMReply.payment_id)
async def get_request_id(message: types.Message, state: FSMContext):
    if photos_db.request_exists(message.text):
        async with state.proxy() as file:
            file['request_id'] = message.text

        text = f'#<code>{message.text}</code>\n\nЧто делаем с данным платежом?'
        await bot.send_message(message.chat.id, text, reply_markup=inline_markup_request_opps(), parse_mode='HTML')
        await FSMReply.choice.set()
    else:
        await bot.send_message(message.chat.id, 'Платеж с таким ID не найден. Попробуйте еще раз', reply_markup=reply_markup_call_off('Назад'))
        await FSMReply.payment_id.set()


@dispatcher.callback_query_handler(state=FSMReply.choice)
async def check_request_id(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'approve':
        text = 'К какой категории относится ваш клиент'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_classify_client())
        await FSMReply.classify.set()
    elif call.data == 'reject':
        async with state.proxy() as file:
            request_id = file['request_id']

        client_id = requests_db.get_user_id(request_id)
        text = f'<b>Платеж</b> #<code>{request_id}</code> отклонен ❌' + '\n'
        requests_db.delete_request(request_id)
        await bot.send_message(int(client_id), text, parse_mode='HTML')
        await bot.send_message(call.message.chat.id, 'Принято ✅', reply_markup=types.ReplyKeyboardRemove())
        await clear_state(state)
        await send_menu(call.message)


@dispatcher.callback_query_handler(state=FSMReply.classify)
async def classify_client(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        async with state.proxy() as file:
            request_id = file['request_id']

        text = f'#<code>{request_id}</code>\n\nЧто делаем с данным платежом?'
        await bot.send_message(call.message.chat.id, text, reply_markup=inline_markup_request_opps(), parse_mode='HTML')
        await FSMReply.choice.set()
    else:
        async with state.proxy() as file:
            request_id = file['request_id']
        user_id = photos_db.get_user_id(request_id)
        users_db.set_type(int(user_id), call.data)
        text = 'Отправьте сообщение данному клиенту об успешном приобретерии тарифа'
        await bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
        await FSMReply.success_payment.set()


@dispatcher.message_handler(state=FSMReply.success_payment)
async def get_success_message(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        request_id = file['request_id']
    user_id = photos_db.get_user_id(request_id)
    photos_db.delete_request(request_id)
    text = 'Ответ от менеджера:' + '\n\n'
    text += message.text
    await bot.send_message(int(user_id), text=text)
    await bot.send_message(message.chat.id, text='Сообщение успешно отправлено ✅', reply_markup=types.ReplyKeyboardRemove())
    await clear_state(state)
    await send_menu(message)


async def get_rate_text(call: types.CallbackQuery, name: str, descr: str, price: str, conditions: str):
    text = 'Название тарифа:' + '\n'
    if name is None:
        name = 'У вашего тарифа нет названия'
    text += name + '\n\n'
    text += 'Описание тарифа:' + '\n'
    if descr is None:
        descr = 'У вашего тарифа нет описания'
    text += descr + '\n\n'
    text += 'Цена тарифа:' + '\n'
    if price is None:
        price = 'У вашего тарифа нет цены'
    text += price + ' ₽' + '\n\n'
    text += 'Условия рассрочки для тарифа:' + '\n'
    if conditions is None:
        conditions = 'У вашего тарифа нет условия для рассрочки'
    text += conditions + '\n\n'
    text += 'Выберите, что хотите отредактировать либо вернитесь назад'

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_rate_opps())


@dispatcher.callback_query_handler(state=FSMAdmin.get_rate)
async def get_rate(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'first_rate':
        async with state.proxy() as file:
            file['rate'] = 'first'
        await get_rate_text(call, name=statement_db.get_first_rate_name(), descr=statement_db.get_first_rate_descr(), price=statement_db.get_first_rate_price(), conditions=statement_db.get_first_rate_conditions())
        await FSMAdmin.edit_rate.set()
    elif call.data == 'second_rate':
        async with state.proxy() as file:
            file['rate'] = 'second'
        await get_rate_text(call, name=statement_db.get_second_rate_name(), descr=statement_db.get_second_rate_descr(), price=statement_db.get_second_rate_price(), conditions=statement_db.get_second_rate_conditions())
        await FSMAdmin.edit_rate.set()
    elif call.data == 'third_rate':
        async with state.proxy() as file:
            file['rate'] = 'third'
        await get_rate_text(call, name=statement_db.get_third_rate_name(), descr=statement_db.get_third_rate_descr(), price=statement_db.get_third_rate_price(), conditions=statement_db.get_third_rate_conditions())
        await FSMAdmin.edit_rate.set()
    elif call.data == 'back':
        await clear_state(state)
        await edit_to_moderator_menu(call.message)
        await FSMAdmin.admin_opps.set()


@dispatcher.callback_query_handler(state=FSMAdmin.edit_rate)
async def edit_rate(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        text = 'Выберите тариф для его редактирования'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_rates(statement_db))
        await FSMAdmin.get_rate.set()
    else:
        if call.data == 'edit_name':
            async with state.proxy() as file:
                file['status'] = 'rate_name'
            text = 'Введите новое название тарифа'
            await bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
            await FSMAdmin.change_statement.set()
        elif call.data == 'edit_descr':
            async with state.proxy() as file:
                file['status'] = 'rate_descr'
            text = 'Введите новое описание тарифа'
            await bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
            await FSMAdmin.change_statement.set()
        elif call.data == 'edit_price':
            async with state.proxy() as file:
                file['status'] = 'rate_price'
            text = 'Введите новую цену тарифа'
            await bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
            await FSMAdmin.change_statement.set()
        elif call.data == 'edit_conditions':
            async with state.proxy() as file:
                file['status'] = 'rate_conditions'
            text = 'Введите новые условия рассрочки тарифа'
            await bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
            await FSMAdmin.change_statement.set()


try:
    asyncio.run(executor.start_polling(dispatcher=dispatcher, skip_updates=False))
except Exception as error:
    print(error)


