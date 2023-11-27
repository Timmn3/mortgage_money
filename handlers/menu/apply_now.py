from aiogram.utils.deep_linking import get_start_link
import os
from filters import IsSubscriber
from filters.subscription import subscriber
from keyboards.inline.contract import ikb_contracts
from loader import dp, bot
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
import re


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


# @dp.callback_query_handler(text='Подать заявку')
# async def accept_reg(call: types.CallbackQuery):
#     # получаем список заявок
#     variants_proposals = await get_variants_proposal()
#     # Создаем кнопки на основе полученных вариантов заявок
#     keyboard_proposal = ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard_proposal.add(*[KeyboardButton(text=variant) for variant in variants_proposals])
#     await call.message.answer('Выберите вариант заявки:', reply_markup=keyboard_proposal)
#     await ApplyNow.variant_proposal.set()
#
#
# @dp.message_handler(state=ApplyNow.variant_proposal)
# async def process_variant_proposal(message: types.Message, state: FSMContext):
#     selected_variant = message.text
#     await state.update_data(variant_proposal=selected_variant)
#     # await message.delete()
#     await message.answer('Заполните заявку, ответив на вопросы, представленные ниже, если Вы хотите '
#                          'прекратить заполнение, напишите слово "отмена"')
#     await message.answer(f'Введите Фамилию, Имя и Отчество:')
#
#     await ApplyNow.fio.set()


keyboard_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_cancel.add(KeyboardButton('Отмена'))


@dp.callback_query_handler(text='Подать заявку')
async def accept_reg(call: types.CallbackQuery):
    if await subscriber(call.from_user.id):
        await call.message.edit_reply_markup()
        await call.message.answer('Заполните заявку, ответив на вопросы, представленные ниже, '
                                  'или нажмите "отмена"')
        await call.message.answer(f'Введите Фамилию, Имя и Отчество:', reply_markup=keyboard_cancel)

        await ApplyNow.fio.set()


@dp.message_handler(state=ApplyNow.fio)
async def process_fio(message: types.Message, state: FSMContext):
    selected_variant = ''
    await state.update_data(variant_proposal=selected_variant)
    text = str(message.text)
    if text.lower() == 'отмена':
        await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
        await state.finish()  # обязательно завершаем состояние
    else:
        # сохраняем фамилию, имя, отчество в состояние
        await state.update_data(fio=message.text)
        await message.answer('Введите город:', reply_markup=keyboard_cancel)
        await ApplyNow.city.set()


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Поделиться номером телефона', request_contact=True)
        ],
        [
            KeyboardButton(text='Отмена')
        ],
    ], resize_keyboard=True)


@dp.message_handler(state=ApplyNow.city)
async def process_city(message: types.Message, state: FSMContext):
    text = str(message.text)
    if text.lower() == 'отмена':
        await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
        await state.finish()  # обязательно завершаем состояние
    else:
        # сохраняем город в состояние
        await state.update_data(city=message.text)
        await message.answer('Отправьте свой номер телефона', reply_markup=keyboard)
        await ApplyNow.phone.set()


@dp.message_handler(state=ApplyNow.phone, content_types=[types.ContentType.CONTACT, types.ContentType.TEXT])
async def process_phone_text(message: types.Message, state: FSMContext):
    text = str(message.text)
    if text.lower() == 'отмена':
        await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
        await state.finish()  # обязательно завершаем состояние
    else:
        try:
            # Пытаемся получить номер телефона из контакта
            contact = message.contact.phone_number
            await state.update_data(phone=contact)
        except AttributeError:
            # Если не удалось получить номер из контакта, попробуем из текста
            phone_match = re.search(r'\b(?:8|\+7)?9[0-9]{9}\b', text)
            if phone_match:
                contact = phone_match.group(0)
                await state.update_data(phone=contact)
            else:
                # Если номер не найден, сообщаем пользователю и завершаем функцию
                await message.answer('Отправьте свой номер телефона в правильном формате (89*********)',
                                     reply_markup=keyboard_cancel)
                return

        await message.answer('Пришлите фото 1 страницы паспорта:', reply_markup=keyboard_cancel)
        await ApplyNow.photo_passport_1.set()


@dp.message_handler(state=ApplyNow.photo_passport_1, content_types=[types.ContentType.PHOTO, types.ContentType.TEXT])
async def process_photo_passport_1(message: types.Message, state: FSMContext):
    text = str(message.text)
    if text.lower() == 'отмена':
        await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
        await state.finish()  # обязательно завершаем состояние
    else:
        if message.content_type == "photo":
            # сохраняем фото 1 страницы паспорта в состояние
            photo_passport_1 = message.photo[-1].file_id
            await state.update_data(photo_passport_1=photo_passport_1)
            await message.answer('Пришлите фото 2 страницы паспорта:', reply_markup=keyboard_cancel)
            await ApplyNow.photo_passport_2.set()
        else:
            await message.answer('Ошибка ввода! Пришлите фотографию:', reply_markup=keyboard_cancel)


@dp.message_handler(state=ApplyNow.photo_passport_2, content_types=[types.ContentType.PHOTO, types.ContentType.TEXT])
async def process_photo_passport_2(message: types.Message, state: FSMContext):
    text = str(message.text)
    if text.lower() == 'отмена':
        await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
        await state.finish()  # обязательно завершаем состояние
    else:
        if message.content_type != "photo":
            await message.answer('Ошибка ввода! Пришлите заново:', reply_markup=keyboard_cancel)
        else:
            # сохраняем фото 2 страницы паспорта в состояние
            photo_passport_2 = message.photo[-1].file_id
            await state.update_data(photo_passport_2=photo_passport_2)
            await message.answer('Пришлите фото СНИЛС или фото водительских прав:', reply_markup=keyboard_cancel)
            await ApplyNow.photo_snils.set()


@dp.message_handler(state=ApplyNow.photo_snils, content_types=[types.ContentType.PHOTO, types.ContentType.TEXT])
async def process_photo_snils(message: types.Message, state: FSMContext):
    text = str(message.text)
    if text.lower() == 'отмена':
        await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
        await state.finish()  # обязательно завершаем состояние
    else:
        if message.content_type != "photo":
            await message.answer('Ошибка ввода! Пришлите фотографию:', reply_markup=keyboard_cancel)
        else:
            # сохраняем фото СНИЛС или фото водительских прав в состояние
            photo_snils = message.photo[-1].file_id
            await state.update_data(photo_snils=photo_snils)
            foto = "AgACAgIAAxkBAAIUhGVk5G4BTOEDJq5b6HOJcykm8k40AAJT1jEbnkwoSwzfTAnbu70bAQADAgADeAADMwQ"
            await message.answer_photo(foto, 'Отправьте отчет PDF, скаченный с раздела КРЕДИТНАЯ ИСТОРИЯ с сайта \n'
                                             'https://person.nbki.ru:'
                                       , reply_markup=keyboard_cancel)
            await ApplyNow.photo_from_1_credit_history_site.set()


all_photos_1 = []
foto_1 = "AgACAgIAAxkBAAIUhWVk5Hn48_2Zv0qIQLrKBRCTlveoAAJh1jEbnkwoSxrlUU31qHSxAQADAgADeQADMwQ"
foto_2 = "AgACAgIAAxkBAAIUhmVk5ISCkLZAqyh_zBlKahh6wEzMAAJk1jEbnkwoS8dK_IBd6rGbAQADAgADeQADMwQ"
foto_3 = "AgACAgIAAxkBAAIUh2Vk5IuCE-wlHdLDfTZXlw4rLLzvAAJm1jEbnkwoSybVdy8kF_kBAQADAgADeQADMwQ"


@dp.message_handler(state=ApplyNow.photo_from_1_credit_history_site,
                    content_types=[types.ContentType.PHOTO, types.ContentType.TEXT, types.ContentType.DOCUMENT])
async def process_photo_credit_history_1(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = str(message.text)
    if text.lower() == 'отмена':
        await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
        await state.finish()  # обязательно завершаем состояние
    else:
        if message.content_type == "photo":
            try:
                photo_credit_history_1 = message.photo[-1].file_id
                all_photos_1.append(photo_credit_history_1)

                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton(text='Продолжить заполнять заявку',
                                                        callback_data='continue_application_1'))

                await message.answer(
                    'Загрузите еще фото или нажмите "Продолжить заполнение заявки"!',
                    reply_markup=keyboard
                )
            except Exception as e:
                logger.error(e)
        elif message.content_type == "document":
            document_credit_history_1 = message.document.file_id
            await state.update_data(photo_from_1_credit_history_site=['temp'])

            # Получение информации о файле
            file_info = await bot.get_file(document_credit_history_1)

            # Скачивание файла
            file_path = file_info.file_path
            downloaded_file = await bot.download_file(file_path)

            # Сохранение файла в папку temp
            save_path = os.path.join("temp", f"{user_id}_document_1.pdf")
            with open(save_path, 'wb') as file:
                file.write(downloaded_file.read())

            await message.answer_photo(foto_1,
                                       'Внутри личного кабинета на сайте Кредистория https://credistory.ru '
                                       'нажимаете кнопку ПРОВЕРИТЬ КРЕДИТНУЮ ИСТОРИЮ')

            await message.answer_photo(foto_2, 'Выбираете последний загруженный отчет')

            await message.answer_photo(foto_3, 'Жмете СКАЧАТЬ PDF и отправляете его в эту заявку',
                                       reply_markup=keyboard_cancel)
            await ApplyNow.photo_from_2_credit_history_site.set()
        else:
            await message.answer('Ошибка ввода! Пришлите заново:', reply_markup=keyboard_cancel)


@dp.callback_query_handler(lambda c: c.data == 'continue_application_1', state='*')
async def continue_application(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()  # удаляем сообщение
    try:
        await state.update_data(photo_from_1_credit_history_site=all_photos_1)
        await call.message.answer_photo(foto_1,
                                   'Внутри личного кабинета на сайте Кредистория https://credistory.ru '
                                   'нажимаете кнопку ПРОВЕРИТЬ КРЕДИТНУЮ ИСТОРИЮ')

        await call.message.answer_photo(foto_2, 'Выбираете последний загруженный отчет')

        await call.message.answer_photo(foto_3, 'Жмете СКАЧАТЬ PDF и отправляете его в эту заявку',
                                   reply_markup=keyboard_cancel)
        await ApplyNow.photo_from_2_credit_history_site.set()
    except Exception as e:
        logger.error(e)


all_photos_2 = []


@dp.message_handler(state=ApplyNow.photo_from_2_credit_history_site,
                    content_types=[types.ContentType.PHOTO, types.ContentType.TEXT, types.ContentType.DOCUMENT])
async def process_photo_credit_history_2(message: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Продолжить заполнять заявку',
                                            callback_data='continue_application_2'))
    user_id = message.from_user.id
    text = str(message.text)
    if text.lower() == 'отмена':
        await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
        await state.finish()  # обязательно завершаем состояние
    else:
        if message.content_type == "photo":
            try:
                photo_credit_history_2 = message.photo[-1].file_id

                # Добавляем фото в список
                all_photos_2.append(photo_credit_history_2)
                await state.update_data(photo_from_2_credit_history_site='foto')
                # Отправляем сообщение с кнопками
                await message.answer(
                    'Загрузите еще фото или нажмите "Продолжить заполнение заявки"!',
                    reply_markup=keyboard
                )
            except Exception as e:
                logger.error(e)
        elif message.content_type == "document":
            document_credit_history_2 = message.document.file_id
            await state.update_data(photo_from_2_credit_history_site=['temp'])

            # Получение информации о файле
            file_info = await bot.get_file(document_credit_history_2)

            # Скачивание файла
            file_path = file_info.file_path
            downloaded_file = await bot.download_file(file_path)

            # Сохранение файла в папку temp
            save_path = os.path.join("temp", f"{user_id}_document_2.pdf")
            with open(save_path, 'wb') as file:
                file.write(downloaded_file.read())
            await message.answer(text='Нажмите продолжить:', reply_markup=keyboard)
        else:
            await message.answer('Ошибка ввода! Пришлите фотографию:', reply_markup=keyboard_cancel)


# добавить обработку кнопок "оправить заявку" и "редактировать заявку"
keyboard_send = InlineKeyboardMarkup(row_width=1)
keyboard_send.add(InlineKeyboardButton(text='Оправить заявку', callback_data='Оправить заявку'))
keyboard_send.add(InlineKeyboardButton(text='Редактировать заявку', callback_data='Редактировать заявку'))


@dp.callback_query_handler(lambda c: c.data == 'continue_application_2', state='*')
async def continue_application(call: types.CallbackQuery, state: FSMContext):
    # извлекаем фактические данные из объекта Update
    data = await state.get_data()
    if data['photo_from_2_credit_history_site'] != ['temp']:
        await state.update_data(photo_from_2_credit_history_site=all_photos_2)
    data = await state.get_data()

    await call.message.delete()  # удаляем сообщение

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

    await call.message.answer('Ура! Вы справились! Данные по вашей заявке успешно загружены! '
                              'Осталось оправить или отредактировать заявку.\n\n✅ Выберите действие:',
                              reply_markup=ReplyKeyboardRemove())
    await call.message.answer('Выберите действие:', reply_markup=keyboard_send)


async def merge_proposals(proposal, proposal_2):
    data = {
        'id': proposal['id'],
        'username': proposal_2['username'],
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
    await call.message.answer('Спасибо за предоставленные данные. Ваша заявка принята!\n\n'
                              'Для начала работы по вашей заявке необходимо заключить договор.\n'
                              'Это обеспечит Вам гарантии исполнения договора и обоснование для вашего '
                              'обслуживания.\n\n'
                              '1. Распечатать договор\n'
                              '2. Подписать\n'
                              '3. Отправить фото или скан в этого бота в разделе МОЙ ДОГОВОР \n'
                              '\n меню пользователя /menu ')
    ref_link = await get_start_link(payload=call.from_user.id)
    await call.message.answer(f'Примите участие в партнерской программе:\n'
                              f'Приглашайте пользователей по своей реферальной ссылке: {ref_link}'
                              f'и получите бонусы', reply_markup=ikb_contracts)
    await create_excel_file(call.from_user.id, data)
    await state.finish()
