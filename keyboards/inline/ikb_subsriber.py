from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.admin_commands import get_channel_list


async def generate_subscription_keyboard():
    channels = await get_channel_list()

    # Создайте список списков, где каждый внутренний список содержит одну кнопку.
    keyboard_buttons = [
        [InlineKeyboardButton(text=f'Telegram Channel: {channel}', url=channel)]
        for channel in channels
    ]

    # Создайте InlineKeyboardMarkup с одной кнопкой в каждой строке.
    subscription_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    return subscription_keyboard

