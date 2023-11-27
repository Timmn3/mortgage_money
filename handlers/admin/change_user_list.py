""" Изменить список пользователей """
from filters import AdminsMessage
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from utils.db_api.users_commands import update_database_from_excel
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup,
                           InlineKeyboardButton)

class Change(StatesGroup):
    list = State()


keyboard_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_cancel.add(KeyboardButton('Отмена'))


# команда /message отправить сообщения всем пользователям
@dp.message_handler(AdminsMessage(), Command('change_user_list'))
async def input_file(message: types.Message):
    await message.answer('Отправьте excel файл:', reply_markup=keyboard_cancel)
    await Change.list.set()  # устанавливаем состояние


# Отлавливаем состояние введенного сообщения
@dp.message_handler(state=Change.list, content_types=[types.ContentType.DOCUMENT, types.ContentType.TEXT])
async def change_file(message: types.Message, state: FSMContext):
    text = message.text
    if text.lower() == 'отмена':
        await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
        await state.finish()  # обязательно завершаем состояние
    else:
        # Получаем информацию о файле
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)

        # Скачиваем файл
        file_path = file_info.file_path
        downloaded_file = await bot.download_file(file_path)

        # Сохраняем файл на сервере
        save_path = f"temp/пользователи.xlsx"
        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file.read())

        # Выполняем вашу логику обновления базы данных с использованием сохраненного файла
        await update_database_from_excel(message.from_user.id, save_path)
        await state.finish()