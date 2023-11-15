from keyboards.inline import ikb_personal_data
from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from utils.db_api.proposal_commands import update_fio_by_user_id, update_photo_passport_1_by_user_id, \
    update_photo_passport_2_by_user_id, update_photo_snils_by_user_id, \
    update_photo_from_1_credit_history_site_by_user_id, update_photo_from_2_credit_history_site_by_user_id
from utils.db_api.users_commands import update_user_fio, update_user_city, update_user_telephone


class EditPersonalData(StatesGroup):
    edit_fio = State()  # изменить фамилия, имя, отчество
    edit_city = State()  # изменить город
    edit_phone = State()  # изменить телефон
    edit_photo_passport_1 = State()  # изменить фото 1 страницы паспорта
    edit_photo_passport_2 = State()  # изменить фото 2 страницы паспорта
    edit_photo_snils = State()  # изменить фото СНИЛС или фото водительских прав
    edit_photo_from_1_credit_history_site = State()  # изменить фото с сайта кредитных историй
    edit_photo_from_2_credit_history_site = State()  # изменить фото с другого сайта кредитных историй


# Обработчик для обработки "Редактировать заявку" callback
@dp.callback_query_handler(lambda c: c.data == 'Редактировать заявку', state='*')
async def edit_application(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Выберите, что бы вы хотели поменять и выберите опцию:', reply_markup=ikb_personal_data)


# Обработчик обратного запроса для обработки параметров редактирования персональных данных
@dp.callback_query_handler(lambda c: c.data in {'personal_info', 'city', 'phone', 'passport_page1', 'passport_page2',
                                                'snils_or_license', 'credit_history_site1', 'credit_history_site2'},
                           state='*')
async def handle_personal_data_edit_option(call: types.CallbackQuery, state: FSMContext):
    option = call.data
    option_labels = {
        'personal_info': 'Фамилия, Имя, Отчество',
        'city': 'Город',
        'phone': 'Телефон',
        'passport_page1': 'Фото 1 страницы паспорта',
        'passport_page2': 'Фото 2 страницы паспорта',
        'snils_or_license': 'Фото СНИЛС или фото водительских прав',
        'credit_history_site1': 'Фото с сайта кредитных историй',
        'credit_history_site2': 'Фото с другого сайта кредитных историй',
    }

    if option == 'personal_info':
        await EditPersonalData.edit_fio.set()
    elif option == 'city':
        await EditPersonalData.edit_city.set()
    elif option == 'phone':
        await EditPersonalData.edit_phone.set()
    elif option == 'passport_page1':
        await EditPersonalData.edit_photo_passport_1.set()
    elif option == 'passport_page2':
        await EditPersonalData.edit_photo_passport_2.set()
    elif option == 'snils_or_license':
        await EditPersonalData.edit_photo_snils.set()
    elif option == 'credit_history_site1':
        await EditPersonalData.edit_photo_from_1_credit_history_site.set()
    elif option == 'credit_history_site2':
        await EditPersonalData.edit_photo_from_2_credit_history_site.set()
    else:
        await call.message.answer(f'Неизвестная опция: {option}')

        # Теперь вы можете предложить пользователю ввести новое значение на основе выбранного параметра.
    if option in option_labels:
        await call.message.answer(f'Вы выбрали редактирование {option_labels[option]}. Теперь введите новое значение:')


# Обработчик для получения новых значения фамилии, имени и отчества
@dp.message_handler(state=EditPersonalData.edit_fio)
async def process_personal_info(message: types.Message, state: FSMContext):
    new_values = message.text
    await update_user_fio(message.from_user.id, new_values)
    await update_fio_by_user_id(message.from_user.id, new_values)
    await state.finish()
    await message.answer(f'Вы успешно обновили персональные данные')


# Обработчик для получения новых значений Город
@dp.message_handler(state=EditPersonalData.edit_city)
async def process_edit_city(message: types.Message, state: FSMContext):
    new_values = message.text
    await update_user_city(message.from_user.id, new_values)
    await state.finish()
    await message.answer(f'Вы успешно обновили персональные данные')


# Обработчик для получения новых значения phone
@dp.message_handler(state=EditPersonalData.edit_phone)
async def process_edit_phone(message: types.Message, state: FSMContext):
    new_values = message.text
    await update_user_telephone(message.from_user.id, new_values)
    await state.finish()
    await message.answer(f'Вы успешно обновили персональные данные')


# Обработчик для получения новых значения edit_photo_passport_1
@dp.message_handler(content_types=['photo'], state=EditPersonalData.edit_photo_passport_1)
async def process_edit_photo_passport_1(message: types.Message, state: FSMContext):
    photo = message.photo[-1]  # Берем последнюю фотографию из списка
    file_id = photo.file_id
    await update_photo_passport_1_by_user_id(message.from_user.id, file_id)
    await state.finish()
    await message.answer(f'Вы успешно обновили персональные данные')


# Обработчик для получения новых значения edit_photo_passport_2
@dp.message_handler(content_types=['photo'], state=EditPersonalData.edit_photo_passport_2)
async def process_edit_photo_passport_2(message: types.Message, state: FSMContext):
    photo = message.photo[-1]  # Берем последнюю фотографию из списка
    file_id = photo.file_id
    await update_photo_passport_2_by_user_id(message.from_user.id, file_id)
    await state.finish()
    await message.answer(f'Вы успешно обновили персональные данные')


# Обработчик для получения новых значения СНИЛС
@dp.message_handler(content_types=['photo'], state=EditPersonalData.edit_photo_snils)
async def process_edit_photo_snils(message: types.Message, state: FSMContext):
    photo = message.photo[-1]  # Берем последнюю фотографию из списка
    file_id = photo.file_id
    await update_photo_snils_by_user_id(message.from_user.id, file_id)
    await state.finish()
    await message.answer(f'Вы успешно обновили персональные данные')


all_photos_1 = []


# Обработчик для получения новых значения credit_history_site1
@dp.message_handler(state=EditPersonalData.edit_photo_from_1_credit_history_site)
async def process_edit_photo_from_1_credit_history_site(message: types.Message, state: FSMContext):
    await message.answer(f'Загружайте фотографии, когда все загрузите, напишите слово "загружено"')
    if message.text == 'загружено':
        await state.finish()
        await message.answer(f'Вы успешно обновили персональные данные')
        photo_from_1 = ','.join(map(str, all_photos_1))
        await update_photo_from_1_credit_history_site_by_user_id(message.from_user.id, photo_from_1)
    if message.content_type == "photo":
        photo = message.photo[-1]  # Берем последнюю фотографию из списка
        file_id = photo.file_id
        all_photos_1.append(file_id)
        await message.answer(f'жду еще...')


all_photos_2 = []


# Обработчик для получения новых значения credit_history_site2
@dp.message_handler(state=EditPersonalData.edit_photo_from_2_credit_history_site)
async def process_edit_photo_from_2_credit_history_site(message: types.Message, state: FSMContext):
    await message.answer(f'Загружайте фотографии, когда все загрузите, напишите слово "загружено"')
    if message.text == 'загружено':
        await state.finish()
        await message.answer(f'Вы успешно обновили персональные данные')
        photo_from_2 = ','.join(map(str, all_photos_2))
        await update_photo_from_2_credit_history_site_by_user_id(message.from_user.id, photo_from_2)
    if message.content_type == "photo":
        photo = message.photo[-1]  # Берем последнюю фотографию из списка
        file_id = photo.file_id
        all_photos_2.append(file_id)
        await message.answer(f'жду еще...')



