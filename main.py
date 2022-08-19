import asyncio
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

from aiogram import types
import random
import string
from config import *
from key_boards import *
from FSMClasses import *

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from data_base.db_users import UsersDB
from data_base.db_statement import StatementsDB
from data_base.db_requests import RequestDB

storage = MemoryStorage()

bot = Bot(token=TOKEN)

dispatcher = Dispatcher(bot=bot, storage=storage)

ADMIN_IDS = [int(admin_id)]


users_db = UsersDB('data_base/compass.db')
statement_db = StatementsDB('data_base/compass.db')
requests_db = RequestDB('data_base/compass.db')


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

    await send_menu(message)


@dispatcher.callback_query_handler()
async def get_callback(call: types.CallbackQuery):
    if call.data == 'payment':
        text = 'Выберите тариф'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_rates())
        await FSMUser.choose_rate.set()
    elif call.data == 'installment':
        pass
    elif call.data == 'questions':
        await get_questions(call.message)
    elif call.data == 'support':
        if not requests_db.user_exists(call.message.chat.id):
            await bot.send_message(call.message.chat.id, 'Введите сообщение, которое хотите отправить менеджеру', reply_markup=reply_markup_call_off('Отмена'))
            await FSMReply.message.set()
        else:
            text = 'Вы уже отправили сообщение менеджеру. Ожидайте ответа, в скорем времени с вами свяжутся'
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_back('На главное меню'))
    elif call.data == 'book_place':
        pass
    elif call.data == 'back':
        await edit_to_menu(call.message)
    elif call.data == 'reply_message':
        await bot.send_message(call.message.chat.id, 'Скопируйте и отправьте ID сообщения для того, чтобы ответить данному пользователю', reply_markup=reply_markup_call_off('Назад'))
        await FSMReply.request_id.set()


@dispatcher.callback_query_handler(state=FSMUser.choose_rate)
async def get_rate(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
        await edit_to_menu(call.message)


@dispatcher.message_handler(commands=['moderator'], state=['*'])
async def start_moderator(message: types.Message, state: FSMContext):
    await clear_state(state)
    for i in ADMIN_IDS:
        if message.chat.id == i:
            await send_moderator_menu(message)
            await FSMAdmin.admin_opps.set()


@dispatcher.message_handler(Text(equals='отмена', ignore_case=True), state=[FSMAdmin.change_statement])
async def cancel_handler(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, '<i>Действие отменено</i> ↩', reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
    await clear_state(state)
    await send_moderator_menu(message)
    await FSMAdmin.admin_opps.set()


@dispatcher.message_handler(Text(equals='назад', ignore_case=True), state=[FSMReply.reply_message, FSMReply.request_id])
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
        pass


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


try:
    asyncio.run(executor.start_polling(dispatcher=dispatcher, skip_updates=False))
except Exception as error:
    print(error)


