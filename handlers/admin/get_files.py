from aiogram.types import ContentType, Message

from loader import dp
from utils.db_api.admin_commands import save_greeting_video_id, save_greeting_photo_id, save_greeting_document_id
from loguru import logger


@dp.message_handler(content_types=ContentType.PHOTO)
async def get_photo_id(message: Message):
    try:
        photo_id = message.photo[-1].file_id
        # await save_greeting_photo_id(photo_id)
    except Exception as e:
        logger.exception(f"Ошибка сохранения фотографии: {e}")


@dp.message_handler(content_types=ContentType.VIDEO)
async def get_video_id(message: Message):
    try:
        video_id = message.video.file_id
        # await save_greeting_video_id(video_id)
    except Exception as e:
        logger.exception(f"Ошибка сохранения video: {e}")


@dp.message_handler(content_types=ContentType.DOCUMENT)
async def get_document_id(message: Message):
    try:
        document_id = message.document.file_id
        # await save_greeting_document_id(document_id)
    except Exception as e:
        logger.exception(f"Ошибка сохранения документа: {e}")
