from filters import AdminsMessage
from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from utils.db_api import users_commands as commands
from asyncio import sleep
from aiogram.dispatcher.filters.state import StatesGroup, State
from loguru import logger

from utils.db_api.admin_commands import get_newsletter_text, replace_newsletter_period, get_set_bonus_1, \
    get_set_bonus_2, set_set_bonus_1, set_set_bonus_2, get_tariff, set_tariff, get_variants_proposal, \
    set_variants_proposal
from utils.db_api.users_commands import change_user_role


class SendMessage(StatesGroup):
    send_mess = State()
    time = State()
    mess = State()
    user_id = State()
    role = State()
    bonus_selection = State()
    amount = State()
    tariff = State()
    options = State()


@dp.message_handler(text="/test")
async def command_help(message: types.Message):
    await message.answer(f'Тест ')
    ref_link = await get_newsletter_text()
    print(ref_link)


@dp.message_handler(AdminsMessage(), Command('admin'))
async def req(message: types.Message):
    await message.answer(f'/message - отправить сообщения всем пользователям\n'
                         f'/auto_mailing - создать рассылку сообщений по времени\n'
                         f'/set_user_status - задать статус пользователю (роль)\n'
                         f'/edit_bonuses - редактировать процент бонусов\n'
                         f'/edit_tariff - редактировать тариф \n'
                         f'/edit_application_options - редактировать варианты заявок \n'
                         f'/edit_application_rejections - редактировать варианты причин отклонения заявки \n'
                         f'/list_users - список пользователей в формате\n'
                         f'/registered_applications - зарегистрированные заявки \n'
                         f'/approved_applications - одобренные заявки \n')


# команда /message отправить сообщения всем пользователям
@dp.message_handler(AdminsMessage(), Command('message'))
async def send_message(message: types.Message):
    await message.answer('Какое сообщение отправить:')
    await SendMessage.send_mess.set()  # устанавливаем состояние


# Отлавливаем состояние введенного сообщения
@dp.message_handler(state=SendMessage.send_mess)
async def send_message(message: types.Message, state: FSMContext):
    await send_mess(message.text)
    await message.answer('отправлено')
    await state.finish()


# команда /auto_mailing отправить сообщения всем пользователям по времени
@dp.message_handler(AdminsMessage(), Command('auto_mailing'))
async def send_auto_mailing(message: types.Message):
    await message.answer('Установите частоту отправки (введите количество дней, например "3" - '
                         'отправка будет 1 раз в 3 дня):')
    await SendMessage.time.set()  # устанавливаем состояние


# Отлавливаем состояние введенного day
@dp.message_handler(state=SendMessage.time)
async def input_day(message: types.Message, state: FSMContext):
    await state.update_data(day=message.text)
    await message.answer('Какое сообщение отправлять:')
    await SendMessage.mess.set()  # устанавливаем состояние


# Отлавливаем состояние введенного сообщения
@dp.message_handler(state=SendMessage.mess)
async def send_mailing(message: types.Message, state: FSMContext):
    data = await state.get_data()
    day = data['day']
    await replace_newsletter_period(day)
    await message.answer(f'Каждые {day} дня, отправлять сообщение {message.text}')
    await state.finish()


async def send_mess(message: types.Message):
    # все пользователи из БД
    users = await commands.select_all_users()
    for user in users:
        try:
            await dp.bot.send_message(chat_id=user.user_id, text=message)
            await sleep(0.25)  # 4 сообщения в секунду
        except Exception as e:
            logger.error(e)


# команда /set_user_status задать статус пользователю (роль)
@dp.message_handler(AdminsMessage(), Command('set_user_status'))
async def set_user_status(message: types.Message):
    await message.answer('Введите user_id пользователя:')
    await SendMessage.user_id.set()  # устанавливаем состояние


# Отлавливаем состояние введенного user_id
@dp.message_handler(state=SendMessage.user_id)
async def input_data(message: types.Message, state: FSMContext):
    await state.update_data(user_id=message.text)

    # Создаем клавиатуру с кнопками ролей
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    roles = ['admin', 'handler', 'manager', 'copywriter', 'client']
    keyboard.add(*roles)

    await message.answer('Выберите роль пользователя:', reply_markup=keyboard)
    await SendMessage.role.set()  # устанавливаем состояние


@dp.message_handler(state=SendMessage.role)
async def input_role(message: types.Message, state: FSMContext):
    role = message.text
    data = await state.get_data()
    user_id = int(data['user_id'])
    # функция записи данных в БД
    await state.finish()
    # убрать кнопки
    keyboard = types.ReplyKeyboardRemove()

    if await change_user_role(user_id=user_id, new_role=role):
        await message.answer(f'Пользователю {user_id} установлен статус: {role}', reply_markup=keyboard)
    else:
        await message.answer(f'Пользователя с {user_id} нет!', reply_markup=keyboard)


# edit_bonuses - редактировать процент бонусов
@dp.message_handler(AdminsMessage(), Command('edit_bonuses'))
async def input_selection(message: types.Message):
    # Создаем клавиатуру с кнопками ролей
    keyboard_bonuses = types.ReplyKeyboardMarkup(resize_keyboard=True)
    roles = ['ожидаемый', 'фактический']
    keyboard_bonuses.add(*roles)
    await message.answer('Выберите бонусную программу:', reply_markup=keyboard_bonuses)
    await SendMessage.bonus_selection.set()  # устанавливаем состояние


# Отлавливаем состояние бонусную программ
@dp.message_handler(state=SendMessage.bonus_selection)
async def input_bonuses(message: types.Message, state: FSMContext):
    bonus_selection = message.text
    await state.update_data(bonus_selection=bonus_selection)
    get_bonus = ""
    if bonus_selection == "ожидаемый":
        get_bonus = await get_set_bonus_1()
    elif bonus_selection == "фактический":
        get_bonus = await get_set_bonus_2()
    else:
        await message.answer(f'Введено неверное значение"')
    await message.answer(f'{bonus_selection} бонус равен {get_bonus}\n'
                         f'Введите новое значение:')
    await SendMessage.amount.set()  # устанавливаем состояние


# Отлавливаем состояние введенного сообщения
@dp.message_handler(state=SendMessage.amount)
async def input_amount(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите число:")
        return
    data = await state.get_data()
    bonus_selection = data['bonus_selection']
    if bonus_selection == "ожидаемый":
        await set_set_bonus_1(amount)
    elif bonus_selection == "фактический":
        await set_set_bonus_2(amount)
    await message.answer("Установлено!")
    await state.finish()


# /edit_rate - редактировать тариф
@dp.message_handler(AdminsMessage(), Command('edit_tariff'))
async def edit_rate(message: types.Message):
    tariff = await get_tariff()
    await message.answer(f'Тариф равен {tariff}, установите новое значение:')
    await SendMessage.tariff.set()  # устанавливаем состояние


# Отлавливаем состояние введенного сообщения
@dp.message_handler(state=SendMessage.tariff)
async def input_tariff(message: types.Message, state: FSMContext):
    try:
        tariff = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите число:")
        return
    await set_tariff(tariff)
    await message.answer('Установлено!')
    await state.finish()


# /edit_application_options - редактировать варианты заявок
@dp.message_handler(AdminsMessage(), Command('edit_application_options'))
async def edit_application_options(message: types.Message):
    options = await get_variants_proposal()
    await message.answer(f'Варианты заявок: {options}, введите новые значения через запятую:')
    await SendMessage.options.set()  # устанавливаем состояние


# Отлавливаем состояние введенного сообщения
@dp.message_handler(state=SendMessage.options)
async def input_options(message: types.Message, state: FSMContext):
    options = message.text
    output_list = options.split(', ')
    await set_variants_proposal(output_list)
    await message.answer('Установлено!')
    await state.finish()