from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup,
                           InlineKeyboardButton)
from loguru import logger
from misc.save_excel import create_excel_file
from utils.db_api.admin_commands import get_variants_proposal
from utils.db_api.proposal_commands import add_proposal, get_proposal_data
from utils.db_api.users_commands import update_user_data, get_user_city_and_telephone


class ApplyNow(StatesGroup):
    variant_proposal = State()  # вариант заявки
    fio = State()  # фамилия, имя, отчество
    city = State()  # город
    phone = State()  # телефон
    photo_passport_1 = State()  # фото 1 страницы паспорта
    photo_passport_2 = State()  # фото 2 страницы паспорта
    photo_snils = State()  # фото СНИЛС или фото водительских прав
    photo_from_1_credit_history_site = State()  # фото с сайта кредитных историй
    photo_from_2_credit_history_site = State()  # фото с другого сайта кредитных историй


@dp.callback_query_handler(text='Подать заявку')
async def accept_reg(call: types.CallbackQuery):
    # получаем список заявок
    variants_proposals = await get_variants_proposal()
    # Создаем кнопки на основе полученных вариантов заявок
    keyboard_proposal = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_proposal.add(*[KeyboardButton(text=variant) for variant in variants_proposals])
    await call.message.answer('Выберите вариант заявки:', reply_markup=keyboard_proposal)
    await ApplyNow.variant_proposal.set()


@dp.message_handler(state=ApplyNow.variant_proposal)
async def process_variant_proposal(message: types.Message, state: FSMContext):
    selected_variant = message.text
    await state.update_data(variant_proposal=selected_variant)
    # await message.delete()
    await message.answer('Заполните заявку, ответив на вопросы, представленные ниже, если Вы хотите '
                         'прекратить заполнение, напишите слово "отмена"')
    await message.answer(f'Введите Фамилию, Имя и Отчество:')

    await ApplyNow.fio.set()


@dp.message_handler(state=ApplyNow.fio)
async def process_fio(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await message.answer('Отменено')
        await state.finish()  # обязательно завершаем состояние
    else:
        # сохраняем фамилию, имя, отчество в состояние
        await state.update_data(fio=message.text)
        await message.answer('Введите город:')
        await ApplyNow.city.set()


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Поделиться номером телефона', request_contact=True)
        ]
    ], resize_keyboard=True)


@dp.message_handler(state=ApplyNow.city)
async def process_city(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await message.answer('Отменено')
        await state.finish()  # обязательно завершаем состояние
    else:
        # сохраняем город в состояние
        await state.update_data(city=message.text)
        await message.answer('Отправьте свой номер телефона', reply_markup=keyboard)
        await ApplyNow.phone.set()


@dp.message_handler(state=ApplyNow.phone, content_types=[types.ContentType.CONTACT, types.ContentType.TEXT])
async def process_phone_text(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await message.answer('Отменено')
        await state.finish()  # обязательно завершаем состояние
    else:
        try:
            contact = message.contact.phone_number
            await state.update_data(phone=contact)
            await message.answer('Пришлите фото 1 страницы паспорта:', reply_markup=ReplyKeyboardRemove())
            await ApplyNow.photo_passport_1.set()
        except Exception as e:
            await message.answer('Отправьте свой номер телефона')
            logger.error(e)


@dp.message_handler(state=ApplyNow.photo_passport_1, content_types=[types.ContentType.PHOTO, types.ContentType.TEXT])
async def process_photo_passport_1(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await message.answer('Отменено')
        await state.finish()  # обязательно завершаем состояние
    else:
        if message.content_type == "photo":
            # сохраняем фото 1 страницы паспорта в состояние
            photo_passport_1 = message.photo[-1].file_id
            await state.update_data(photo_passport_1=photo_passport_1)
            await message.answer('Пришлите фото 2 страницы паспорта:')
            await ApplyNow.photo_passport_2.set()
        else:
            await message.answer('Ошибка ввода! Пришлите фотографию:')


@dp.message_handler(state=ApplyNow.photo_passport_2, content_types=[types.ContentType.PHOTO, types.ContentType.TEXT])
async def process_photo_passport_2(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await message.answer('Отменено')
        await state.finish()  # обязательно завершаем состояние
    else:
        if message.content_type != "photo":
            await message.answer('Ошибка ввода! Пришлите фотографию:')
        else:
            # сохраняем фото 2 страницы паспорта в состояние
            photo_passport_2 = message.photo[-1].file_id
            await state.update_data(photo_passport_2=photo_passport_2)
            await message.answer('Пришлите фото СНИЛС или фото водительских прав:')
            await ApplyNow.photo_snils.set()


@dp.message_handler(state=ApplyNow.photo_snils, content_types=[types.ContentType.PHOTO, types.ContentType.TEXT])
async def process_photo_snils(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await message.answer('Отменено')
        await state.finish()  # обязательно завершаем состояние
    else:
        if message.content_type != "photo":
            await message.answer('Ошибка ввода! Пришлите фотографию:')
        else:
            # сохраняем фото СНИЛС или фото водительских прав в состояние
            photo_snils = message.photo[-1].file_id
            await state.update_data(photo_snils=photo_snils)
            await message.answer('Пришлите несколько фотографий (по одной) с сайта кредитных историй:')
            await ApplyNow.photo_from_1_credit_history_site.set()


all_photos_1 = []


@dp.message_handler(state=ApplyNow.photo_from_1_credit_history_site,
                    content_types=[types.ContentType.PHOTO, types.ContentType.TEXT])
async def process_photo_credit_history_1(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await message.answer('Отменено')
        await state.finish()  # обязательно завершаем состояние
    else:
        if message.content_type != "photo":
            await message.answer('Ошибка ввода! Пришлите фотографию:')
        else:
            try:
                photo_credit_history_1 = message.photo[-1].file_id

                # Добавляем фото в список
                all_photos_1.append(photo_credit_history_1)

                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text='Продолжить заполнять заявку',
                                                        callback_data='continue_application_1'))

                # Отправляем сообщение с кнопками
                await message.answer(
                    'Загрузите еще фото или нажмите "Продолжить заполнение заявки"!',
                    reply_markup=keyboard
                )
            except Exception as e:
                logger.error(e)


@dp.callback_query_handler(lambda c: c.data == 'continue_application_1', state='*')
async def continue_application(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()  # удаляем сообщение
    try:
        await state.update_data(photo_from_1_credit_history_site=all_photos_1)
        await call.message.answer('Теперь пришлите еще фотографии (по одной) с другого сайта кредитных историй:')
        await ApplyNow.photo_from_2_credit_history_site.set()
    except Exception as e:
        logger.error(e)


all_photos_2 = []


@dp.message_handler(state=ApplyNow.photo_from_2_credit_history_site,
                    content_types=[types.ContentType.PHOTO, types.ContentType.TEXT])
async def process_photo_credit_history_2(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await message.answer('Отменено')
        await state.finish()  # обязательно завершаем состояние
    else:
        if message.content_type != "photo":
            await message.answer('Ошибка ввода! Пришлите фотографию:')
        else:
            try:
                # сохраняем фото с другого сайта кредитных историй в состояние
                photo_credit_history_2 = message.photo[-1].file_id
                # Добавляем фото в список
                all_photos_2.append(photo_credit_history_2)

                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text='Продолжить заполнять заявку',
                                                        callback_data='continue_application_2'))

                # Отправляем сообщение с кнопками
                await message.answer(
                    'Загрузите еще фото или нажмите "Продолжить заполнение заявки"!',
                    reply_markup=keyboard
                )
            except Exception as e:
                logger.error(e)


# добавить обработку кнопок "оправить заявку" и "редактировать заявку"
keyboard_send = InlineKeyboardMarkup(row_width=1)
keyboard_send.add(InlineKeyboardButton(text='Оправить заявку', callback_data='Оправить заявку'))
keyboard_send.add(InlineKeyboardButton(text='Редактировать заявку', callback_data='Редактировать заявку'))


@dp.callback_query_handler(lambda c: c.data == 'continue_application_2', state='*')
async def continue_application(call: types.CallbackQuery, state: FSMContext):
    try:
        await state.update_data(photo_from_2_credit_history_site=all_photos_2)
        await call.message.delete()  # удаляем сообщение
        # извлекаем фактические данные из объекта Update
        data = await state.get_data()
        # обновляем данные в базе данных user
        await update_user_data(call.from_user.id, data)

        photo_list_1 = data['photo_from_1_credit_history_site']
        photo_from_1_credit_history_site_str = ','.join(map(str, photo_list_1))

        photo_list_2 = data['photo_from_2_credit_history_site']
        photo_from_2_credit_history_site_str = ','.join(map(str, photo_list_2))

        # создаем заявку в БД proposal
        await add_proposal(user_id=call.from_user.id, fio=data['fio'], variant_proposal=data['variant_proposal'],
                           status_proposal='', approved_amount=0, loan_amount=0,
                           photo_passport_1=data['photo_passport_1'], photo_passport_2=data['photo_passport_2'],
                           photo_snils=data['photo_snils'],
                           photo_from_1_credit_history_site=photo_from_1_credit_history_site_str,
                           photo_from_2_credit_history_site=photo_from_2_credit_history_site_str)

        await call.message.answer('Выберите действие:', reply_markup=keyboard_send)

    except Exception as e:
        logger.error(e)


async def merge_proposals(proposal, proposal_2):
    data = {
        'variant_proposal': proposal['variant_proposal'],
        'fio': proposal['fio'],
        'city': proposal_2['city'],
        'phone': f"+{proposal_2['telephone']}",
        'photo_passport_1': proposal['photo_passport_1'],
        'photo_passport_2': proposal['photo_passport_2'],
        'photo_snils': proposal['photo_snils'],
        'photo_from_1_credit_history_site': [proposal['photo_from_1_credit_history_site']],
        'photo_from_2_credit_history_site': [proposal['photo_from_2_credit_history_site']],
    }
    return data


@dp.callback_query_handler(lambda c: c.data == 'Оправить заявку', state='*')
async def submit_application(call: types.CallbackQuery, state: FSMContext):
    # делаем excel файл заявки
    proposal = await get_proposal_data(call.from_user.id)
    proposal_2 = await get_user_city_and_telephone(call.from_user.id)
    data = await merge_proposals(proposal, proposal_2)
    await create_excel_file(call.from_user.id, data)
    await call.message.answer('Спасибо за предоставленные данные. Ваша заявка принята!')
    await state.finish()
