""" Изменить список пользователей """
from filters import AdminsMessage
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from utils.db_api.users_commands import update_database_from_excel


class Change(StatesGroup):
    list = State()


# команда /message отправить сообщения всем пользователям
@dp.message_handler(AdminsMessage(), Command('change_user_list'))
async def input_file(message: types.Message):
    await message.answer('Отправьте excel файл:')
    await Change.list.set()  # устанавливаем состояние


# Отлавливаем состояние введенного сообщения
@dp.message_handler(state=Change.list, content_types=types.ContentType.DOCUMENT)
async def change_file(message: types.Message, state: FSMContext):
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