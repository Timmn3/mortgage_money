
from aiogram.utils.deep_linking import get_start_link
from aiogram.types import (ReplyKeyboardRemove, InlineKeyboardMarkup,
                           InlineKeyboardButton)
from filters.subscription import subscriber
from keyboards.cancel import keyboard_cancel
from keyboards.inline import ikb_contracts
from loader import dp
from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import os
from aiogram.types import InputFile
from loguru import logger

keyboard_contract = InlineKeyboardMarkup(row_width=1)
keyboard_contract.add(
    InlineKeyboardButton(text='Скачать договор оказания услуг', callback_data='Скачать договор оказания услуг'))
keyboard_contract.add(InlineKeyboardButton(text='Оправить заполненный договор',
                                           callback_data='Оправить заполненный договор'))


class Contract(StatesGroup):
    send = State()


@dp.callback_query_handler(text='Договор')
async def accept_reg(call: types.CallbackQuery):
    if await subscriber(call.from_user.id):
        await call.message.answer("Выберите действие:", reply_markup=keyboard_contract)


@dp.callback_query_handler(text='Скачать договор оказания услуг')
async def download_service_contract(call: types.CallbackQuery):
    if await subscriber(call.from_user.id):
        try:
            # Указываем путь к файлу
            file_path = "admin_documents/договор оказания услуг/Договор оказания услуг.pdf"

            # Проверяем, существует ли файл
            if os.path.exists(file_path):
                # Отправляем файл пользователю
                await call.message.answer_document(InputFile(file_path))
            else:
                # Если файл не найден, отправляем соответствующее сообщение
                await call.message.answer("Файл не найден.")
        except Exception as e:
            # Обрабатываем случай, если файл не может быть отправлен
            await call.message.answer(f"Не удалось отправить договор. Пожалуйста, попробуйте позже")
            logger.error(e)


@dp.callback_query_handler(text='Оправить заполненный договор')
async def accept_reg(call: types.CallbackQuery):
    if await subscriber(call.from_user.id):
        await call.message.answer("Отправьте мне подписанный договор:", reply_markup=keyboard_cancel)
        await Contract.send.set()


@dp.message_handler(state=Contract.send, content_types=[types.ContentType.DOCUMENT, types.ContentType.TEXT])
async def input_document(message: types.Message, state: FSMContext):
    text = str(message.text)
    if text.lower() == 'отмена':
        await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
        await state.finish()  # обязательно завершаем состояние\
    else:
        # Получаем имя файла
        file_extension = message.document.file_name.split('.')[-1]  # Извлечение расширения файла
        file_name = f"Договор_{message.from_user.id}.{file_extension}"

        # Сохраняем файл в папку "contracts" с уникальным именем
        file_path = os.path.join("admin_documents/contracts", file_name)
        await message.document.download(destination_file=file_path)

        # Добавьте здесь логику, которая вам нужна после сохранения файла
        # Например, отправка подтверждения или обработка файла

        # Очищаем состояние FSM
        await state.finish()
        ref_link = await get_start_link(payload=message.from_user.id)
        # Отправляем ответ пользователю
        await message.answer(f"Договор отправлен!")
        await message.answer(f'Примите участие в партнерской программе:\n'
                             f'Приглашайте пользователей по своей реферальной ссылке: {ref_link} '
                             f'и получите бонусы', reply_markup=ikb_contracts)


@dp.callback_query_handler(text='Скачать свой договор')
async def download_contract(call: types.CallbackQuery):
    if await subscriber(call.from_user.id):
        user_id = call.from_user.id
        file_name = f"Договор_{user_id}"

        # Формируем путь к файлу
        file_path = os.path.join("admin_documents/contracts", file_name)

        try:
            # Получаем список файлов в папке
            files_in_directory = os.listdir("admin_documents/contracts")

            # Ищем файл с нужным префиксом (без учета расширения)
            matching_files = [file for file in files_in_directory if file.startswith(file_name)]

            # Берем первый найденный файл
            if matching_files:
                full_file_name = matching_files[0]
                full_file_path = os.path.join("admin_documents/contracts", full_file_name)

                # Отправляем файл пользователю
                await call.message.answer_document(InputFile(full_file_path))
            else:
                # Если файл не найден, отправляем соответствующее сообщение
                await call.message.answer("Файл не найден.")
        except Exception as e:
            # Обрабатываем случай, если файл не может быть отправлен
            await call.message.answer(f"Не удалось отправить договор. Пожалуйста, попробуйте позже")
            logger.error(e)
