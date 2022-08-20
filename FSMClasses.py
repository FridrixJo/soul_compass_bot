from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMUser(StatesGroup):
    choose_rate = State()
    choose_rate_installment_payment = State()
    choose_payment = State()
    payment_type = State()
    apply_payment = State()
    photo = State()


class FSMAdmin(StatesGroup):
    admin_opps = State()
    change_statement = State()
    get_rate = State()
    edit_rate = State()
    classify_users = State()
    admin_back = State()
    sharing = State()
    add_admin = State()


class FSMReply(StatesGroup):
    message = State()
    request_id = State()
    reply_message = State()
    payment_id = State()
    choice = State()
    classify = State()
    success_payment = State()
