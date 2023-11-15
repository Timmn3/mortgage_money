from aiogram import types
from loader import dp
from utils.db_api.admin_commands import get_greeting_text, get_greeting_foto_id, get_greeting_video_id
from loguru import logger


@dp.message_handler(text="/instruction")
async def command_instruction(message: types.Message):
    await get_greeting_text(message)


async def greeting(message: types.Message):
    try:
        photo = await get_greeting_foto_id()
        if photo:
            await message.answer_photo(photo)

        text = await get_greeting_text()
        await message.answer(text)
        await message.answer("https://telegra.ph/Bot-zayavki-TZ-11-07")


        video = await get_greeting_video_id()
        if video:
            await message.answer_video(video=video)

    except Exception as e:
        logger.error(e)


