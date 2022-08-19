from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMUser(StatesGroup):
    choose_rate = State()


class FSMAdmin(StatesGroup):
    admin_opps = State()
    change_statement = State()


class FSMReply(StatesGroup):
    message = State()
    request_id = State()
    reply_message = State()
