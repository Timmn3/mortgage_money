from aiogram import types


from loader import dp
from utils.db_api.admin_commands import get_greeting_foto_id, get_greeting_video_id
from loguru import logger


@dp.message_handler(text="/instruction")
async def command_instruction(message: types.Message):
    await greeting(message)
    from handlers.users.bot_start import out_text
    await message.answer(out_text)


async def greeting(message: types.Message):
    try:
        photo = await get_greeting_foto_id()
        if photo:
            await message.answer_photo(photo)

        # text = await get_greeting_text()
        # await message.answer(text)
        # await message.answer("https://t.me/TeamCapital_bot/oferta")

        video = await get_greeting_video_id()
        if video:
            await message.answer_video(video=video)

    except Exception as e:
        logger.error(e)


