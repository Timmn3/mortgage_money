from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_cancel.add(KeyboardButton('Отмена'))
